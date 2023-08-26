from django.test import TestCase
from ..logger import configure_logger

class TestExample(TestCase):
    def setUp(self):
        logger = configure_logger()
        logger.info(f"Example logger")

    def test_logging(self):
        with self.assertLogs() as captured:
            self.setUp()
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(captured.records[0].getMessage(),"Example logger")
