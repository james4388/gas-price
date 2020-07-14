"""Get company logo using clearbit api


"""
import re
import json
import logging
import requests

from flask import Flask, Blueprint, current_app, redirect

from gasprice.utils.cache import (
    cached, should_cache_api_response
)


logger = logging.getLogger(__name__)
clearbit_bp = Blueprint('ClearBit', __name__)


@clearbit_bp.route('/logo/<string:company>')
def find_company_logo(company: str):
    """Get company logo

    Redirect to company logo image (301 Moved Permanently) if found
    Otherwise return 404 not found

    """
    clearbit = ClearbitClient(current_app)
    logo = clearbit.find_logo(company)
    if logo:
        return redirect(logo, code=301)
    return {
        'error': {
            'message': 'Not found',
            'code': 404
        }
    }, 404


def _normalize_name(name: str) -> str:
    """Normalize string for name compare

    Args:
        name: string

    Returns:
        Remove all space, and special chars then lower the string.
    """
    return re.sub('[^A-Za-z0-9]+', '', name.lower())


class ClearbitClient:
    """Clearbit api wrapper
    """

    def __init__(self, app: Flask):
        self.autocomplete_api = app.config['CLEARBIT_NAME_API']

    @cached(
        make_key=lambda _, company: _normalize_name(company),
        should_cache=should_cache_api_response
    )
    def find_logo(self, company: str) -> str:
        """Get company logo url using company name

        Clear bit does not have "free" api to search company logo by name,
        Try to use their autocomplete api to get logo. If not possible to find
        a correct logo, return None. The result is cache in redis

        Args:
            company: Company name

        Returns:
            A url to clearbit logo for example:

            input 7 Eleven
            https://logo.clearbit.com/7-eleven.com

            If company name cannot be found, return None

        """
        company = _normalize_name(company)
        logo = None

        try:
            response = requests.get(f'{self.autocomplete_api}?query={company}')
            matches = response.json()

            for match in matches:
                name = _normalize_name(match['name'])
                domain = _normalize_name(match['domain'])
                if company == name or domain.startswith(company):
                    logo = match['logo']
                    break
        except requests.exceptions.RequestException as ex:
            logger.error(f'could not make find logo request: {ex}')
        except (json.JSONDecodeError, ValueError) as ex:
            logger.error(f'could not decode json response {ex}')
        except KeyError as ex:
            logger.error(f'clearbit api changed? {ex}')

        return logo
