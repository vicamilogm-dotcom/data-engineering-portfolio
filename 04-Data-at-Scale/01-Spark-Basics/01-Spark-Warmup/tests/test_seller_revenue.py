from nbresult import ChallengeResultTestCase


class TestSellerRevenue(ChallengeResultTestCase):
    def test_row_count(self):
        self.assertTrue(len(self.result.df_seller_revenue_pd) > 0)

    def test_revenue_non_negative(self):
        self.assertTrue(all(self.result.df_seller_revenue_pd["Total_Revenue"] >= 0))

    def test_revenue_total(self):
        self.assertEqual(
            13591643.7,
            round(self.result.df_seller_revenue_pd["Total_Revenue"].sum(), 2),
        )
