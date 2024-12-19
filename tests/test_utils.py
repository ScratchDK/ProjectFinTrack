from unittest.mock import patch
from src.utils import get_top_transactions, get_info_card, get_share_price


def test_get_top_transactions(test_df):
    with (patch("pandas.read_excel") as mock_read_excel):
        mock_read_excel.return_value = test_df
        assert get_top_transactions("09.02.2022 19:00:00") == [
            {'date': '2022-02-06 15:00:00', 'amount': -1000, 'category': 'Супермаркеты', 'description': 'Колхоз'},
            {'date': '2022-02-04 13:00:00', 'amount': -500, 'category': 'Супермаркеты', 'description': 'Магнит'},
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
            }
        ]


def test_get_info_card(test_df):
    with (patch("pandas.read_excel") as mock_read_excel):
        mock_read_excel.return_value = test_df
        assert get_info_card("12.02.2022 19:00:00") == [
            {'last_digits': '4556', 'total_spent': 1000.0, 'cashback': 10.0},
            {'last_digits': '7197', 'total_spent': 800.0, 'cashback': 8.0}
        ]


def test_get_share_price():
    with patch("json.load") as mock_get:
        mock_get.return_value = {"user_stocks": ["AAPL", "GOOGL", "TSLA"]}
        assert get_share_price() == [
            {'stocks': 'AAPL', 'price': 195.98},
            {'stocks': 'GOOGL', 'price': 136.16},
            {'stocks': 'TSLA', 'price': 257.22}
        ]
