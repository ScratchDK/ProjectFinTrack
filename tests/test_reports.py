import pandas as pd
import pytest

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
        ),
    ],
)
def test_spending_by_category(data: dict, category: str, date: str, expected: dict) -> None:
    df = pd.DataFrame(data)

    result = spending_by_category(df, category, date)

    expected_df = pd.DataFrame(expected)

    expected_df["Дата операции"] = pd.to_datetime(
        expected_df["Дата операции"], format="%d.%m.%Y %H:%M:%S"
    )

    assert result.equals(expected_df)


@pytest.mark.parametrize(
    "data, category, expected",
    [
        (
            {
                "Дата операции": [
                    "21.10.2024 10:00:00",
                    "22.11.2024 11:00:00",
                    "23.12.2024 12:00:00",
                ],
                "Сумма операции": [100, 200, 300],
                "Категория": ["Супермаркеты", "Каршеринг", "Дом и ремонт"],
            },
            "Супермаркеты",
            {
                "Дата операции": ["21.10.2024 10:00:00"],
                "Сумма операции": [100],
                "Категория": ["Супермаркеты"],
            },
        ),
    ],
)
def test_spending_by_category_no_date(data: dict, category: str, expected: dict) -> None:
    df = pd.DataFrame(data)

    result = spending_by_category(df, category)

    expected_df = pd.DataFrame(expected)

    expected_df["Дата операции"] = pd.to_datetime(
        expected_df["Дата операции"], format="%d.%m.%Y %H:%M:%S"
    )

    assert result.equals(expected_df)
