import pytest
import pandas as pd
from unittest.mock import patch
from src.utils import get_top_transactions


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            {
                "Дата операции": [
                    "01.02.2022 10:00:00",
                    "02.02.2022 11:00:00",
                    "03.02.2022 12:00:00",
                    "04.02.2022 13:00:00",
                    "06.02.2022 15:00:00",
                    "08.02.2022 19:00:00"
                ],
                "Сумма платежа": [-100, -200, -300, -500, -1000, 2000],
                "Категория": [
                    "Каршеринг", "Мобильная связь", "Мобильная связь", "Супермаркеты", "Супермаркеты", "Каршеринг"
                ],
                "Описание": [
                    "Rumyanyj Khleb",
                    "Я МТС +7 921 11-22-33",
                    "beeline +7 903 438 91 72",
                    "Магнит",
                    "Колхоз",
                    "Ситидрайв"
                ],
            },
            [
                {'date': '2022-02-06 15:00:00', 'amount': -1000, 'category': 'Супермаркеты', 'description': 'Колхоз'},
                {'date': '2022-02-04 13:00:00', 'amount': -500, 'category': 'Супермаркеты', 'description': 'Магнит'},
                {
                    'date': '2022-02-03 12:00:00',
                    'amount': -300, 'category': 'Мобильная связь',
                    'description': 'beeline +7 903 438 91 72'
                },
                {
                    'date': '2022-02-02 11:00:00',
                    'amount': -200, 'category': 'Мобильная связь',
                    'description': 'Я МТС +7 921 11-22-33'
                 }
            ]
        )
    ],
)
def test_search_by_phone_number(data, expected):
    df = pd.DataFrame(data)
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = df
    assert get_top_transactions("09.02.2022 19:00:00") == expected
