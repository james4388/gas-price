from time import sleep

from tests import BaseTestCase
from gasprice import config
from gasprice.utils.cache import (
    keysify,
    should_cache_api_response,
    make_key_from_args,
    get_cache_client,
    cached
)


class CacheTestCase(BaseTestCase):
    def test_keysify(self):
        self.assertEqual(
            keysify(1, 2, 3, 4), 
            '1_2_3_4',
            msg="Should work with Int key")
        self.assertEqual(
            keysify('key1', None, '33'), 
            'key1_None_33', 
            msg="Should work with None in keys")
        self.assertEqual(
            keysify('hello', None, 'world', 123, sparator='+'),
            'hello+None+world+123', 
            msg="Should work with different sparator")


    def test_should_cache_api_response(self):
        self.assertTrue(
            should_cache_api_response((None, 200, None)), 'Should cache 200')
        self.assertFalse(
            should_cache_api_response((None, 400, None)),
            'Should not cache 400')
        self.assertFalse(
            should_cache_api_response((None, None, None)),
            'Should not cache anything')

    def test_make_key_from_args(self):
        self.assertEqual(
            make_key_from_args(1, True, None, 'str'),
            '(1,True,None,str,)',
            msg='Should work with arg only'
        )
        self.assertEqual(
            make_key_from_args(1, True, None, 'str', a='b', c='d'),
            '(1,True,None,str,a=b,c=d)',
            msg='Should work with arg and kwarg'
        )
        self.assertEqual(
            make_key_from_args(a='b', c='d'),
            '(,a=b,c=d)',
            msg='Should work with kwarg only'
        )

    def test_get_cache_client(self):
        if config.TESTING:
            import fakeredis
            self.assertIsInstance(
                get_cache_client(), 
                fakeredis.FakeStrictRedis,
                'Should return fake redis instance in test'
            )
    
    def test_cached(self):
        from random import randint
        
        @cached(make_key=make_key_from_args)
        def random_num(something):
            return randint(0, 100000)

        first = random_num(1)
        second = random_num(2)
        self.assertEqual(random_num(1), first, 'Should cache same arg')
        self.assertNotEqual(random_num(2), first, 'Should not cache different arg')
        self.assertNotEqual(random_num(3), first, 'Should not cache different arg')
        self.assertEqual(random_num(1), first, 'Should cache same arg')
        self.assertEqual(random_num(2), second, 'Should cache same arg')

    