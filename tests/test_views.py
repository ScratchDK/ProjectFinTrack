from unittest.mock import patch

from src.views import main


def test_main(returned_data: str) -> None:
    with patch("json.dumps") as mock_json_dumps, \
            patch('src.views.get_currencies_rates') as mock_currencies_rates, \
            patch('src.views.get_share_price') as mock_share_price:
        mock_json_dumps.return_value = returned_data
        mock_currencies_rates.return_value = [
            {'currency': 'USD', 'rate': 102.454469}, {'currency': 'EUR', 'rate': 106.393185}
        ]
        mock_share_price.return_value = [
            {'stocks': 'AAPL', 'price': 184.73},
            {'stocks': 'AMZN', 'price': 149.93},
            {'stocks': 'GOOGL', 'price': 137.67},
            {'stocks': 'MSFT', 'price': 368.12},
            {'stocks': 'TSLA', 'price': 248.42}]
        assert main("28.12.2021 19:00:00") == returned_data
