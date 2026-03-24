from unittest import TestCase
from util.logging_util import init_logger
from logging import RootLogger
class TestLoggingUtil(TestCase):
    def setUp(self) -> None:
        pass
    
    def test_init_logger(self):
        logger = init_logger()
        result = isinstance(logger, RootLogger)
        self.assertTrue(result)
        
    def tearDown(self):
        pass