from unittest.mock import patch

from src.views import main


def test_main() -> None:
    with patch("src.views.get_currencies_rates") as mock_currencies_rates, patch(
        "src.views.get_share_price"
    ) as mock_share_price:
        mock_currencies_rates.return_value = [
            {"currency": "USD", "rate": 102.454469},
            {"currency": "EUR", "rate": 106.393185},
        ]
        mock_share_price.return_value = [
            {"stocks": "AAPL", "price": 184.73},
            {"stocks": "AMZN", "price": 149.93},
            {"stocks": "GOOGL", "price": 137.67},
            {"stocks": "MSFT", "price": 368.12},
            {"stocks": "TSLA", "price": 248.42},
        ]

        result = main("28.12.2021 19:00:00")

        assert result == ('{"greeting": "Добрый вечер!", "cards": [{"last_digits": "4556", "total_spent": 952.9,'
                          ' "cashback": 9.53}, {"last_digits": "5091", "total_spent": 14502.26, "cashback": 145.02},'
                          ' {"last_digits": "7197", "total_spent": 23355.15, "cashback": 233.55}],'
                          ' "top_transactions": [{"date": "2021-12-22 23:30:44", "amount": -28001.94,'
                          ' "category": "Переводы", "description": "Перевод Кредитная карта. ТП 10.2 RUR"},'
                          ' {"date": "2021-12-16 16:40:47", "amount": -14216.42, "category": "ЖКХ", '
                          '"description": "ЖКУ Квартира"}, {"date": "2021-12-23 16:14:59", '
                          '"amount": -10000.0, "category": "Переводы", "description": "Светлана Т."}, '
                          '{"date": "2021-12-02 16:26:02", "amount": -5510.8, "category": "Каршеринг", '
                          '"description": "Ситидрайв"}, {"date": "2021-12-14 11:04:32", "amount": -5000.0, "category": '
                          '"Переводы", "description": "Светлана Т."}], "currency_rates": [{"currency": "USD", '
                          '"rate": 102.454469}, {"currency": "EUR", "rate": 106.393185}], '
                          '"stock_prices": [{"stocks": "AAPL", "price": 184.73}, '
                          '{"stocks": "AMZN", "price": 149.93}, '
                          '{"stocks": "GOOGL", "price": 137.67}, {"stocks": "MSFT", "price": 368.12}, '
                          '{"stocks": "TSLA", "price": 248.42}]}')
