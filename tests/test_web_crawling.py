from valentinas_p_mod1_atsiskaitymas.web_crawling import WebCrawling

import unittest
from unittest.mock import patch, mock_open, Mock


crawling = WebCrawling()

class TestWebCrawling(unittest.TestCase):
    def test_invalid_website(self):
        with self.assertRaises(ValueError):
            crawling.read_from_website("eurovaistine.lt")