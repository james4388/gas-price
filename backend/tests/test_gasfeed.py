from flask import url_for

from tests import BaseTestCase
from gasprice import config, create_app


class GasFeedTestCase(BaseTestCase):
    def test_brands(self):
        with self.app.app_context():
            resp = self.client.get(
                url_for(
                    'GasFeed.station_brands'
                )
            )
            
            data = resp.json
            self.assertIsInstance(
                data['stations'], list, 'Should stations is a list')

    def test_nearby_stations(self):
        with self.app.app_context():
            resp = self.client.get(
                url_for(
                    'GasFeed.nearby_stations',
                    lat='iajsd',
                    lon='sddsf'
                )
            )
            data = resp.json
            self.assertEqual(resp.status_code, 422, 'Validation should work')

            resp = self.client.get(
                url_for(
                    'GasFeed.nearby_stations',
                    lat='37.4131208',
                    lon='-122.0908522'
                )
            )
            data = resp.json
            self.assertIsInstance(
                data['stations'], list, 'Should stations is a list')