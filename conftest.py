import pandas as pd
import pytest


@pytest.fixture
def test_df():
    df = pd.DataFrame({
                "Дата операции": [
                    "01.02.2022 10:00:00",
                    "02.02.2022 11:00:00",
                    "03.02.2022 12:00:00",
                    "04.02.2022 13:00:00",
                    "06.02.2022 15:00:00",
                    "08.02.2022 19:00:00"
                ],
                "Сумма платежа": [-100, -200, -300, -500, -1000, 2000],
                "Статус": ["OK", "FAILED", "OK", "OK", "OK", "FAILED"],
                "Номер карты": ["*7197", "*4556", "*7197", "*7197", "*4556", "*4556"],
                "Сумма операции": [-100, -200, -300, -500, -1000, 2000],
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
            })
    return df


@pytest.fixture
def returned_data():
    return ('{"greeting": "Добрый вечер!", "cards": [{"last_digits": "4556", '
            '"total_spent": 952.9, "cashback": 9.53}, {"last_digits": "5091", '
            '"total_spent": 14622.26, "cashback": 146.22}, {"last_digits": "7197", '
            '"total_spent": 23408.03, "cashback": 234.08}], "top_transactions": [{"date": '
            '"2021-12-22 23:30:44", "amount": -28001.94, "category": "Переводы", '
            '"description": "Перевод Кредитная карта. ТП 10.2 RUR"}, {"date": "2021-12-16 '
            '16:40:47", "amount": -14216.42, "category": "ЖКХ", "description": "ЖКУ '
            'Квартира"}, {"date": "2021-12-23 16:14:59", "amount": -10000.0, "category": '
            '"Переводы", "description": "Светлана Т."}, {"date": "2021-12-02 16:26:02", '
            '"amount": -5510.8, "category": "Каршеринг", "description": "Ситидрайв"}, '
            '{"date": "2021-12-14 11:04:32", "amount": -5000.0, "category": "Переводы", '
            '"description": "Светлана Т."}], "currency_rates": [{"currency": "USD", '
            '"rate": 102.454469}, {"currency": "EUR", "rate": 106.393185}], '
            '"stock_prices": [{"stocks": "AAPL", "price": 184.73}, {"stocks": "AMZN", '
            '"price": 149.93}, {"stocks": "GOOGL", "price": 137.67}, {"stocks": "MSFT", '
            '"price": 368.12}, {"stocks": "TSLA", "price": 248.42}]}')
