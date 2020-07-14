import requests
import json
import logging

from flask import Flask, Blueprint, current_app, jsonify, request

from gasprice.utils.validation import validate_input, ValidationError
from gasprice.utils.cache import (
    cached, should_cache_api_response, make_key_from_args
)
from gasprice.utils.header import allow_ratelimit_headers


logger = logging.getLogger(__name__)
gasfeed_bp = Blueprint('GasFeed', __name__)


@gasfeed_bp.route('/stations/brands')
def station_brands():
    """Return all gas stations brands
    """
    gas_client = GasFeedClient(current_app)
    result, status, headers = gas_client.station_brands()

    if result:
        return jsonify(result), 200, headers

    return {
        'error': {
            'code': status,
            'message': 'Could not get response from GasFeed'
        }
    }, status, headers


@gasfeed_bp.route('/stations/near/<string:lat>,<string:lon>')
def nearby_stations(lat: str, lon: str):
    """Return all station near by location
    """
    # Validate input
    try:
        lat = validate_input(
            lat, float, 'latitude', min_value=-90, max_value=90)
        lon = validate_input(
            lon, float, 'longitude', min_value=-180, max_value=180)
        distance = validate_input(
            request.args.get('distance', 2.0),
            float,
            'distance',
            min_value=0,
            max_value=50
        )
        fuel_type = validate_input(
            request.args.get('fuel_type', 'reg'),
            str,
            'fuel_type',
            message='Only reg, mid, pre or diesel allowed for fuel_type',
            choices=('reg', 'mid', 'pre', 'diesel')
        )
        sort_by = validate_input(
            request.args.get('sort_by', 'price'),
            str,
            'sort_by',
            message='Only price and distance allowed for sort_by',
            choices=('price', 'distance')
        )
    except ValidationError as ex:
        return {
            'error':  {
                'message': str(ex),
                'code': 422
            }
        }, 422

    gas_client = GasFeedClient(current_app)
    result, status, headers = gas_client.nearby_stations(
        lat, lon,
        distance=distance,
        sort_by=sort_by,
        fuel_type=fuel_type
    )

    if result:
        return jsonify(result), 200, headers

    return {
        'error': {
            'code': status,
            'message': 'Could not get response from GasFeed'
        }
    }, status, headers


class GasFeedClient:
    """
    Gas feed api wrapper
    """
    def __init__(self, app: Flask):
        self.api_url = app.config['GASFEED_API']
        self.api_key = app.config['GASFEED_API_KEY']

    def fetch(self, path: str) -> tuple:
        """Make get request to gasfeed api

        Gas feed is old and sometime return warning php code in response
        this may cause json to break. In this case this function will try to
        clean up warning and parse json again
        Example of failure: http://devapi.mygasfeed.com/stations/radius/47.9494949/120.23423432/distance/reg/rfej9napna.json

        Args:
            path: api path

        Returns:
            Response payload
        """
        url = f'{self.api_url}/{path}/{self.api_key}.json'
        response = requests.get(url)

        try:
            return (
                response.json(),
                response.status_code,
                allow_ratelimit_headers(response.headers)
            )
        except json.JSONDecodeError as ex:
            logger.warn(f'gas feed api break json encoder {ex}')

            # try to remove php warning and parse again
            last_pre = response.text.rfind('</pre>')
            if last_pre:
                clean_text = response.text[last_pre + 6:]
                try:
                    return (
                        json.loads(clean_text),
                        response.status_code,
                        allow_ratelimit_headers(response.headers)
                    )
                except json.JSONDecodeError:
                    pass

        return (
            None,
            response.status_code,
            allow_ratelimit_headers(response.headers)
        )

    @cached(
        static_key='static_key',
        should_cache=should_cache_api_response
    )
    def station_brands(self) -> tuple:
        """Get all gas stations brands
        """
        return self.fetch('/stations/brands')

    @cached(
        make_key=lambda _, *args, **kwargs: make_key_from_args(*args, **kwargs),
        should_cache=should_cache_api_response,
        expire=300
    )
    def nearby_stations(
        self,
        lat: float,
        lon: float,
        distance: float = 8,
        fuel_type: str = 'reg',
        sort_by: str = 'price'
    ) -> tuple:
        """Find all near by gas station for given parameters

        Args:
            lat: latitude
            lon: longitude
            distance: radius from center (in mile)
            fuel_type: one of these fuel types reg, mid, pre or diesel,
            sort_by: one of price or distance

        Returns:
            A dictionary has information about current location and near by
            gas station:

            {
                "status": {},
                "geoLocation": {},
                "stations": []
            }
        """
        return self.fetch(
            f'/stations/radius/{lat}/{lon}/{distance}/{fuel_type}/{sort_by}')
