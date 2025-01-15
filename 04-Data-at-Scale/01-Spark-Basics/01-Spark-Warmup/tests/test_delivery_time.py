from nbresult import ChallengeResultTestCase


class TestDeliveryTime(ChallengeResultTestCase):
    def test_catergories(self):
        self.assertEqual(
            list(self.result.df_delivery_time_pd["product_category_name"])[:2],
            ["artes_e_artesanato", "moveis_colchao_e_estofado"],
        )

    def test_values(self):
        self.assertEqual(
            list(self.result.df_delivery_time_pd["Avg_Extended_Delivery"])[:2],
            [-146.2061226851852, -155.48177927927927],
        )
