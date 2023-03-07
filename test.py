import unittest
from main import prepare_data


class PrepDataTest(unittest.TestCase):
    def setUp(self):
        self.enh_data_sample = """<a class="article__title link link--show-visited" href="https://www.seznamzpravy.cz/clanek/domaci-politika-lekari-vysvetluji-proc-by-mel-pavel-brat-dva-leky-227255#dop_ab_variant=0&amp;dop_source_zone_name=zpravy.sznhp.box&amp;dop_id=227255&amp;source=hp&amp;seq_no=1&amp;utm_campaign=&amp;utm_medium=z-boxiku&amp;utm_source=www.seznam.cz" rel="noopener" target="_blank">Lékaři vysvětlují, proč by měl Pavel brát dva léky</a>"""
        self.fin_data_sample = {'Lékaři vysvětlují, proč by měl Pavel brát dva\xa0léky': 'https://www.seznamzpravy.cz/clanek/domaci-politika-lekari-vysvetluji-proc-by-mel-pavel-brat-dva-leky-227255#dop_ab_variant=0&dop_source_zone_name=zpravy.sznhp.box&dop_id=227255&source=hp&seq_no=1&utm_campaign=&utm_medium=z-boxiku&utm_source=www.seznam.cz'}

    def test_pdata_correct(self):
        self.assertEqual(prepare_data(self.enh_data_sample), self.fin_data_sample)

    def test_pdata_empty_string(self):
        enh_data_sample = ""
        self.assertEqual(prepare_data(enh_data_sample), {})

    def test_pdata_no_tag(self):
        self.assertEqual(prepare_data(self.enh_data_sample[20:]), {})


if __name__ == '__main__':
    unittest.main()





