from flask import url_for

from tests import BaseTestCase
from gasprice import config, create_app
from gasprice.services.geocoding import (
    GeocodingApi
)


class GeocodingTestCase(BaseTestCase):
    def test_great_circle_distance(self):
        geo = GeocodingApi(create_app())

        loc1 = (43.677, -79.630)
        loc2 = (-26.133, 28.242)
        self.assertAlmostEqual(
            geo.great_circle_distance(loc1, loc2), 
            geo.great_circle_distance(loc2, loc1),
            msg='Should be the same'
        )

        self.assertAlmostEqual(
            geo.great_circle_distance(loc1, loc2), 
            13368.752,
            delta=0.2,
            msg='Should be correct distance',
        )

        newport_ri = (41.49008, -71.312796)
        cleveland_oh = (41.499498, -81.695391)
        self.assertAlmostEqual(
            geo.great_circle_distance(newport_ri, cleveland_oh), 
            864.2144943393627,
            delta=0.2,
            msg='Should be correct distance',
        )

        hcm = (10.649745, 106.761979)
        hcm_antipodes = geo.antipodes(hcm)
        self.assertAlmostEqual(
            geo.great_circle_distance(hcm, hcm_antipodes),
            20015.086796,
            delta=0.3
        )

        self.assertAlmostEqual(
            geo.great_circle_distance(hcm, hcm),
            0,
            delta=0.0001
        )

    def test_distance_api(self):
        with self.app.app_context():
            resp = self.client.get(
                url_for(
                    'Geocoding.distance',
                    lata='43.677', 
                    lona='-79.630',
                    latb='-26.133',
                    lonb='28.242')
            )
            data = resp.json
            self.assertAlmostEqual(data['distance'], 13368.752440, delta=0.0001)

    def test_lookup_latlng(self):
        with self.app.app_context():
            resp = self.client.get(
                url_for(
                    'Geocoding.lookup_latlng',
                    address='1600 Amphitheatre Parkway, Mountain View, CA'
                )
            )
            
            data = resp.json
            self.assertIn('status', data)
            self.assertEqual(data['status'], 'OK')
            self.assertTrue(len(data['results']) > 0)


    def test_lookup_address(self):
        with self.app.app_context():
            resp = self.client.get(
                url_for(
                    'Geocoding.lookup_address',
                    lat='37.4131208',
                    lon='-122.0908522'
                )
            )
            
            data = resp.json
            self.assertIn('status', data)
            self.assertEqual(data['status'], 'OK')
            self.assertTrue(len(data['results']) > 0)