from nbresult import ChallengeResultTestCase


class TestHighCancelCategories(ChallengeResultTestCase):
    def test_catergories(self):
        self.assertEqual(
            list(self.result.df_high_cancel_categories_pd["product_category_name"])[:2],
            ["esporte_lazer", "utilidades_domesticas"],
        )

    def test_values(self):
        self.assertEqual(
            list(
                self.result.df_high_cancel_categories_pd["Total_Canceled_Unavailable"]
            ),
            [51, 49, 46, 36, 36, 34, 31, 22, 21, 19],
        )
