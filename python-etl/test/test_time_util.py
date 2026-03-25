from unittest import TestCase
from util.time_util import ts10_to_date_str, ts13_to_date_str


class TestTimeUtil(TestCase):
    def setUp(self):
        pass
    
    def test_ts10_to_date_str(self):
        ts = 1774479707
        result = ts10_to_date_str(ts)
        self.assertEqual(result, '2026-03-26 00:01:47')
        
    def test_ts13_to_date_str(self):
        ts = 1774479707360
        result = ts13_to_date_str(ts)
        self.assertEqual(result, '2026-03-26 00:01:47')