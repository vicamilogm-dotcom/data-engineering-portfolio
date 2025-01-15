from nbresult import ChallengeResultTestCase


class TestOrderStatusCount(ChallengeResultTestCase):
    def test_row_count(self):
        self.assertTrue(len(self.result.order_status_count_df) > 0)

    def test_distinct_status(self):
        self.assertEqual(
            len(self.result.order_status_count_df),
            len(self.result.order_status_count_df["order_status"].unique()),
        )

    def test_non_negative_counts(self):
        self.assertTrue(all(self.result.order_status_count_df["count"] >= 0))

    def test_values(self):
        self.assertEqual(
            [2, 5, 301, 314, 609, 625, 1107, 96478],
            sorted(self.result.order_status_count_df["count"]),
        )
