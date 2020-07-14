from flask import url_for

from tests import BaseTestCase
from gasprice import config, create_app
from gasprice.services.clearbit import (
    _normalize_name
)


class ClearBitTestCase(BaseTestCase):
    def test_normalize_name(self):
        self.assertEqual(
            _normalize_name('  ...aA  sd fs-sd FS_Dfsdfs#@%#$$^'),
            'aasdfssdfsdfsdfs',
            'Should remove all non alpha num char and lowercase'
        )

    def test_find_logo(self):
        with self.app.app_context():
            resp = self.client.get(
                url_for(
                    'ClearBit.find_company_logo',
                    company='Facebook'
                )
            )

            self.assertEqual(resp.status_code, 301)
            self.assertEqual(resp.location, 'https://logo.clearbit.com/facebook.com')

            resp = self.client.get(
                url_for(
                    'ClearBit.find_company_logo',
                    company='Google'
                )
            )

            self.assertEqual(resp.status_code, 301)
            self.assertEqual(resp.location, 'https://logo.clearbit.com/google.com')

            resp = self.client.get(
                url_for(
                    'ClearBit.find_company_logo',
                    company='Not existed company that I made 134324234'
                )
            )

            self.assertEqual(resp.status_code, 404)
