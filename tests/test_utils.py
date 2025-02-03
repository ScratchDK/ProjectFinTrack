from unittest.mock import patch

import pandas as pd

from src.utils import get_currencies_rates, get_info_card, get_share_price, get_top_transactions


def test_get_top_transactions(test_df: pd.DataFrame) -> None:
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = test_df
        assert get_top_transactions("09.02.2022 19:00:00") == [
            {
                'date': '2022-02-06 15:00:00',
                'amount': -1000,
                'category': 'Супермаркеты',
                'description': 'Колхоз'
            },
            {
                'date': '2022-02-04 13:00:00',
                'amount': -500,
                'category': 'Супермаркеты',
                'description': 'Магнит'
            },
            {
                'date': '2022-02-03 12:00:00',
                'amount': -300,
                'category': 'Мобильная связь',
                'description': 'beeline +7 903 438 91 72'
            },
            {
                'date': '2022-02-02 11:00:00',
                'amount': -200,
                'category': 'Мобильная связь',
                'description': 'Я МТС +7 921 11-22-33'
            },
            {
                'date': '2022-02-01 10:00:00',
                'amount': -100,
                'category': 'Каршеринг',
                'description': 'Rumyanyj Khleb'
            }
        ]


def test_get_info_card(test_df: pd.DataFrame) -> None:
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = test_df
        assert get_info_card("12.02.2022 19:00:00") == [
            {'last_digits': '4556', 'total_spent': 1000.0, 'cashback': 10.0},
            {'last_digits': '7197', 'total_spent': 900.0, 'cashback': 9.0}
        ]


def test_get_share_price() -> None:
    with patch("json.load") as mock_get:
        mock_get.return_value = {"user_stocks": ["AAPL", "GOOGL", "TSLA"]}
        assert get_share_price() == [
            {"stocks": "AAPL", "price": 184.73},
            {"stocks": "GOOGL", "price": 137.67},
            {"stocks": "TSLA", "price": 248.42},
        ]


def test_get_currencies_rates() -> None:
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {
            "success": True,
            "query": {"from": "USD", "to": "RUB", "amount": 1},
            "info": {"timestamp": 1733205976, "rate": 106.501573},
            "date": "2024-12-03",
            "result": 106.501573,
        }
        result = get_currencies_rates()
        assert result == [
            {"currency": "USD", "rate": 106.501573},
            {"currency": "EUR", "rate": 106.501573},
        ]
