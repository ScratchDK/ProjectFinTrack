import pytest
import pandas as pd
from unittest.mock import patch
from src.services import search_by_phone_number


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            {
                "Дата операции": [
                    "01.01.2022 10:00:00",
                    "02.02.2022 11:00:00",
                    "03.03.2022 12:00:00",
                    "04.03.2022 13:00:00"
                ],
                "Сумма операции": [100, 200, 300, 500],
                "Описание": ["Rumyanyj Khleb", "Я МТС +7 921 11-22-33", "beeline +7 903 438 91 72", "Магнит"],
            },
            '[{"Дата операции":"02.02.2022 11:00:00","Сумма операции":200,"Описание":"Я МТС +7 921 11-22-33"},'
            '{"Дата операции":"03.03.2022 12:00:00","Сумма операции":300,"Описание":"beeline +7 903 438 91 72"}]'
        )
    ],
)
def test_search_by_phone_number(data, expected):
    df = pd.DataFrame(data)
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = df
        assert search_by_phone_number() == expected
