import pytest
import pandas as pd
from src.reports import spending_by_category


@pytest.mark.parametrize(
    "data, category, date, expected",
    [
        (
            {
                "Дата операции": [
                    "01.01.2022 10:00:00",
                    "02.02.2022 11:00:00",
                    "03.03.2022 12:00:00",
                ],
                "Сумма операции": [100, 200, 300],
                "Категория": ["Супермаркеты", "Каршеринг", "Дом и ремонт"],
            },
            "Супермаркеты",
            "29.03.2022 10:00:00",
            {
                "Дата операции": ["01.01.2022 10:00:00"],
                "Сумма операции": [100],
                "Категория": ["Супермаркеты"],
            },
        )
    ],
)
def test_spending_by_category(data, category, date, expected):
    df = pd.DataFrame(data)

    result = spending_by_category(df, category, date)

    expected_df = pd.DataFrame(expected)

    expected_df["Дата операции"] = pd.to_datetime(
        expected_df["Дата операции"], format="%d.%m.%Y %H:%M:%S"
    )

    assert result.equals(expected_df)
