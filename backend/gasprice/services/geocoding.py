"""
Geocoding API wraper
"""
import json
import math
import logging
import requests

from typing import Tuple
from flask import Blueprint, Flask, current_app, jsonify

from gasprice.utils.validation import validate_input, ValidationError
from gasprice.utils.cache import (
    cached, should_cache_api_response, make_key_from_args
)
from gasprice.utils.header import allow_ratelimit_headers


logger = logging.getLogger(__name__)
geocoding_bp = Blueprint('Geocoding', __name__)


EARTH_RADIUS = 6371  # Km


@geocoding_bp.route('/latlng/<string:lat>,<string:lon>')
def lookup_address(lat: str, lon: str):
    """Look up address by lat lon
    """
    # Validate input
    try:
        lat = validate_input(
            lat, float, 'latitude', min_value=-90, max_value=90)
        lon = validate_input(
            lon, float, 'longitude', min_value=-180, max_value=180)
    except ValidationError as ex:
        return {
            'error':  {
                'message': str(ex),
                'code': 422
            }
        }, 422

    geocoding = GeocodingApi(current_app)
    result, status, headers = geocoding.lookup(latlng=f'{lat},{lon}')

    if result:
        return jsonify(result), 200, headers

    return {
        'error': {
            'code': status,
            'message': 'Could not get response from Google'
        }
    }, status


@geocoding_bp.route('/address/<string:address>')
def lookup_latlng(address: str):
    """Look up address by lat lon
    """
    geocoding = GeocodingApi(current_app)
    result, status, headers = geocoding.lookup(address=address)

    if result:
        return jsonify(result), 200, headers

    return {
        'error': {
            'code': status,
            'message': 'Could not get response from Google'
        }
    }, status


@geocoding_bp.route('/distance/<string:lata>,<string:lona>/<string:latb>,<string:lonb>')
def distance(lata: str, lona: str, latb: str, lonb: str):
    """Calculate distance between two point
    """
    # Validate input
    try:
        lata = validate_input(
            lata, float, 'latitude a', min_value=-90, max_value=90)
        lona = validate_input(
            lona, float, 'longitude a', min_value=-180, max_value=180)
        latb = validate_input(
            latb, float, 'latitude b', min_value=-90, max_value=90)
        lonb = validate_input(
            lonb, float, 'longitude b', min_value=-180, max_value=180)
    except ValidationError as ex:
        return {
            'error':  {
                'message': str(ex),
                'code': 422
            }
        }, 422

    geocoding = GeocodingApi(current_app)
    distance = geocoding.great_circle_distance((lata, lona), (latb, lonb))

    return {
        'unit': 'km',
        'distance': distance,
        'coord_a': {
            'lat': lata,
            'lng': lona
        },
        'coord_b': {
            'lat': latb,
            'lng': lonb
        }
    }


class GeocodingApi:
    def __init__(self, app: Flask):
        self.api_key = app.config['GOOGLE_GEOCODING_API_KEY']
        self.api_url = 'https://maps.googleapis.com/maps/api/geocode/json'

    @cached(
        make_key=lambda _, *args, **kwargs: make_key_from_args(*args, **kwargs),
        should_cache=should_cache_api_response,
        expire=300
    )
    def lookup(self, latlng: str = None, address: str = None) -> dict:
        """Look up address by latitude, longitude or reverse look up
        using address

        Pass through all rate limitter header to client so it can choose to
        retry with backoff

        Args:
            latlng: lat,lon
            address: Full address

        Returns:
            Address if provide latlng
            LatLng if provide address

        """
        params = {
            'key': self.api_key
        }

        if latlng:
            params['latlng'] = latlng
        elif address:
            params['address'] = address

        request = requests.get(self.api_url, params=params)
        return (
            request.json(),
            request.status_code,
            allow_ratelimit_headers(request.headers)
        )

    def antipodes(self, coord: Tuple[float, float]) -> Tuple[float, float]:
        """Return antipodes location (the point through earth center)
        """
        lat, lng = coord
        return -lat, lng - 180 if lng > 0 else 180 + lng

    @cached(
        make_key=lambda _, *args: make_key_from_args(*args),
    )
    def great_circle_distance(
        self,
        coord_a: Tuple[float, float],
        coord_b: Tuple[float, float]
    ) -> float:
        """Calculate great circle distance between two (lat, lng) coordinate

        See more at
        https://en.wikipedia.org/wiki/Great-circle_distance#Formulae

        Args:
            coor_a: (float, float) lat, lng coordinate of the first point
            coor_b: (float, float) lat, lng coordinate of the second point
        
        Return distance in km
        """
        if coord_a == coord_b:
            central_angle = 0
        elif self.antipodes(coord_a) == coord_b:
            central_angle = math.pi
        else:
            lata, lnga = map(math.radians, coord_a)
            latb, lngb = map(math.radians, coord_b)

            cos_delta_lng = math.cos(abs(lnga - lngb))
            sin_latab = math.sin(lata) * math.sin(latb)
            cos_latab_detalng = math.cos(lata) * math.cos(latb) * cos_delta_lng
            central_angle = math.acos(sin_latab + cos_latab_detalng)

        return EARTH_RADIUS * central_angle


