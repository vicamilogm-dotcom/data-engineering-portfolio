from nbresult import ChallengeResultTestCase


class TestCustomerClv(ChallengeResultTestCase):
    def test_row_count(self):
        self.assertTrue(len(self.result.df_clv_pd) > 0)

    def test_clv_non_negative(self):
        self.assertTrue(all(self.result.df_clv_pd["CLV"] >= 0))

    def test_values(self):
        self.assertEqual(
            [13664.08, 7274.88, 6929.31, 6922.21, 6726.66],
            sorted(self.result.df_clv_pd["CLV"], reverse=True)[:5],
        )
