import unittest
import requests
from unittest.mock import patch, mock_open, MagicMock
from valentinas_p_mod1_atsiskaitymas.web_crawling import *

class TestCrawlingFunction(unittest.TestCase):

    @patch('valentinas_p_mod1_atsiskaitymas.web_crawling.fetchingCamelia')
    @patch('valentinas_p_mod1_atsiskaitymas.web_crawling.parseHTML')
    @patch('valentinas_p_mod1_atsiskaitymas.web_crawling.extractLrytas')
    @patch('valentinas_p_mod1_atsiskaitymas.web_crawling.saveToFile')
    def test_invalid_source(self, mock_saveToFile, mock_extractLrytas, mock_parseHTML, mock_fetchingCamelia):
        result = crawling(time_limit=60, source="lr.lt", return_format="list")

        mock_fetchingCamelia.assert_not_called()
        mock_parseHTML.assert_not_called()
        mock_extractLrytas.assert_not_called()
        mock_saveToFile.assert_not_called()

        self.assertIsNone(result)

    @patch('requests.get')
    def test_request_exception(self, mock_get):
        # Simulate a network error
        mock_get.side_effect = requests.exceptions.RequestException("Connection failed")
        with self.assertRaises(ValueError) as error:
            parseHTML("https://example.com")
        self.assertIn("Klaida analizuojant HTML", str(error.exception))

    @patch('requests.get')
    def test_invalid_format(self, mock_get):
        with self.assertRaises(ValueError) as error:
            saveToFile("camelia.lt", [], "s")
        self.assertEqual(str(error.exception), "Nepalaikomas formatas. Naudokite 'list', 'csv' arba 'json'.")

    @patch("builtins.print")
    @patch("builtins.open", new_callable=mock_open)
    def test_saving_file_to_json(self, mock_open_file, mock_print):
        dataList = [
            {
                "ID" : 1, "Pavadinimas" : "vaistas1",
                "ID": 2, "Pavadinimas": "vaistas2",
            }
        ]
        saveToFile("camelia.lt", dataList, "json")
        mock_open_file.assert_called_with(
            "./valentinas_p_mod1_atsiskaitymas/results/vaistaiList.json",
            "w", newline=''
        )
        mock_open_file().write.assert_called()
        mock_print.assert_called_with("Json failas sukurtas: vaistaiList.json")

    @patch("builtins.print")
    @patch("csv.writer")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_to_csv(self, mock_open_file, mock_csv_writer, mock_print):
        data_list = [
            [1, "Vaistas1", "https://example.com/image1"],
            [2, "Vaistas2", "https://example.com/image2"]
        ]
        mock_writer_instance = MagicMock()
        mock_csv_writer.return_value = mock_writer_instance
        saveToFile("camelia.lt", data_list, "csv")
        mock_open_file.assert_called_once_with(
            './valentinas_p_mod1_atsiskaitymas/results/vaistaiList.csv',
            'w', newline='', encoding='utf-8'
        )

        mock_csv_writer.assert_called_once_with(mock_open_file())

        mock_writer_instance.writerow.assert_any_call(['id', 'Pavadinimas', 'Nuotraukos URL'])

        for element in data_list:
            mock_writer_instance.writerow.assert_any_call(element)

        mock_print.assert_called_once_with("CSV failas sukurtas: vaistaiList.csv")

if __name__ == '__main__':
    unittest.main()
