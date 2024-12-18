import os
import yfinance as yf
import requests
import pandas as pd
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_share_price():
    # Получаем список акций
    stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']

    # Создаем пустой словарь для хранения стоимости акций
    stock_prices = {}

    # Получаем стоимость каждой акции и добавляем в словарь
    for stock in stocks:
        stock_data = yf.Ticker(stock)
        stock_price = stock_data.history(period='1d')['Close'].iloc[0]
        stock_prices[stock] = stock_price

    # Выводим список акций и их стоимость
    # for stock, price in stock_prices.items():
    #     print(f'{stock} - {price}')

    list_stocks = []

    for stock, price in stock_prices.items():
        stocks = {"stocks": stock, "price": round(float(abs(price)), 2)}
        list_stocks.append(stocks)

    return list_stocks


def get_currencies_rates():
    list_currencies = ["USD", "EUR"]

    exchange_rates_data_api = os.getenv("API_Key")

    list_currencies_rates = []

    for el in list_currencies:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={el}&amount=1"

        headers = {
            "apikey": exchange_rates_data_api
        }

        response = requests.request("GET", url, headers=headers)

        result = response.json()
        dict_currencies = {"currency": el, "rate": result["result"]}
        list_currencies_rates.append(dict_currencies)

    return list_currencies_rates


def get_info_card(date):
    full_path_file = os.path.join(base_dir, "data", "operations.xlsx")
    df = pd.read_excel(full_path_file)

    start_month = datetime.strptime(date, "%d.%m.%Y %H:%M:%S").replace(day=1)
    end_month = datetime.strptime(date, "%d.%m.%Y %H:%M:%S") + timedelta(days=1)

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    # Получаем операций за нужный промежуток времени
    filtered_df = df[(df["Дата операции"] >= start_month) & (df["Дата операции"] <= end_month)]

    # Получаем только операций со знаком "-" и те чей статус "ОК"
    df_expenses = filtered_df[(filtered_df["Сумма операции"] < 0) & (filtered_df["Статус"] == 'OK')]

    # Группируем df по номерам карт и получаем общю сумму трат на каждую карту
    total_expenses = df_expenses.groupby("Номер карты")["Сумма операции"].sum()

    list_cards = []

    for card, total in total_expenses.items():
        cards = {
            "last_digits": card[-4:],
            "total_spent": round(float(abs(total)), 2),
            "cashback": round(float(abs(total / 100)), 2)
        }
        list_cards.append(cards)

    return list_cards


def get_top_transactions(date):
    full_path_file = os.path.join(base_dir, "data", "operations.xlsx")
    df = pd.read_excel(full_path_file)

    start_month = datetime.strptime(date, "%d.%m.%Y %H:%M:%S").replace(day=1)
    end_month = datetime.strptime(date, "%d.%m.%Y %H:%M:%S") + timedelta(days=1)

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    # Получаем операций за нужный промежуток времени
    filtered_df = df[(df["Дата операции"] >= start_month) & (df["Дата операции"] <= end_month)]

    df_top_five = filtered_df.nsmallest(5, "Сумма платежа")

    list_top_five = []

    for i, row in df_top_five.iterrows():
        dict_top_five = {
            "date": str(row["Дата операции"]),
            "amount": row["Сумма платежа"],
            "category": row["Категория"],
            "description": row["Описание"]
        }
        list_top_five.append(dict_top_five)

    return list_top_five
