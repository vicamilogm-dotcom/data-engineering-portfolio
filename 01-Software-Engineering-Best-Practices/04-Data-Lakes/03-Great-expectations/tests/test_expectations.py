import pandas as pd
from unittest.mock import patch
import unittest
from scraper.expectations import run_expectations
from copy import deepcopy


class TestScraperExpectations(unittest.TestCase):
    def setUp(self):
        valid_data = {
            "rank": list(range(1, 31)),
            "title": ["Title " + str(i) for i in range(1, 31)],
            "site": ["site{}.com".format(i) for i in range(1, 31)],
            "link": ["https://www.github.com/article" + str(i) for i in range(1, 31)],
            "score": list(range(1, 31)),
            "author": ["author" + str(i) for i in range(1, 31)],
            "comments_number": list(range(0, 30)),
        }

        self.valid_df = pd.DataFrame(valid_data)

        invalid_data = {
            "rank": list(range(1, 31)),
            "title": ["Title " + str(i) for i in range(1, 31)],
            "site": ["site{}.com".format(i) for i in range(1, 31)],
            "link": ["https://www.github.com/article" + str(i) for i in range(1, 31)],
            "score": list(range(1, 31)),
            "author": ["author" + str(i) for i in range(1, 31)],
            "comments_number": list(range(0, 30)),
        }

        invalid_data_rank = deepcopy(invalid_data)
        invalid_data_site = deepcopy(invalid_data)

        invalid_data_rank["rank"][0] = 2  # Introduce duplicate rank
        self.invalid_df_rank = pd.DataFrame(invalid_data_rank)

        invalid_data_site["site"][0] = "invalid_site"  # Invalid site format
        self.invalid_df_site = pd.DataFrame(invalid_data_site)

    @patch("scraper.expectations.send_message")
    def test_execution_of_expectations_all_passed(self, mock_send_message):
        run_expectations(self.valid_df)
        mock_send_message.assert_called_once_with("All expectations passed!")

    @patch("scraper.expectations.send_message")
    def test_execution_of_expectations_failed_rank(self, mock_send_message):
        run_expectations(self.invalid_df_rank)
        expected_call_site = "[call('Expectation failed!'), call('rank')]"
        self.assertEqual(str(mock_send_message.call_args_list[:2]), expected_call_site)

    @patch("scraper.expectations.send_message")
    def test_execution_of_expectations_failed_site(self, mock_send_message):
        run_expectations(self.invalid_df_site)
        expected_call_site = "[call('Expectation failed!'), call('site')]"
        self.assertEqual(str(mock_send_message.call_args_list[:2]), expected_call_site)
