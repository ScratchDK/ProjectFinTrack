import json
import logging
import os
from datetime import datetime, timedelta

import pandas as pd
import requests
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

path_file_logs = full_path_file_logs = os.path.join(base_dir, "logs", "utils.log")

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(path_file_logs, encoding="utf-8", mode="w")
file_formatter = logging.Formatter(
    "%(asctime)s - %(filename)s [%(funcName)s] - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_share_price() -> list:
    logger.info("Старт")
    full_path_file_data = os.path.join(base_dir, "data", "user_settings.json")

    with open(full_path_file_data, encoding="utf-8") as file_json:
        data = json.load(file_json)

    # Получаем список акций
    stocks = data["user_stocks"]

    # Создаем пустой словарь для хранения стоимости акций
    stock_prices = {}

    # Получаем стоимость каждой акции и добавляем в словарь
    for stock in stocks:
        stock_data = yf.Ticker(stock)
        stock_price = stock_data.history(period="ytd")["Close"].iloc[0]
        stock_prices[stock] = stock_price

    list_stocks = []

    for stock, price in stock_prices.items():
        stocks = {"stocks": stock, "price": round(float(abs(price)), 2)}
        list_stocks.append(stocks)

    logger.info("Данные переданы")
    return list_stocks


def get_currencies_rates() -> list:
    logger.info("Старт")
    full_path_file_data = os.path.join(base_dir, "data", "user_settings.json")

    with open(full_path_file_data, encoding="utf-8") as file_json:
        data = json.load(file_json)

    list_currencies = data["user_currencies"]

    exchange_rates_data_api = os.getenv("API_Key")

    list_currencies_rates = []

    for el in list_currencies:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={el}&amount=1"

        headers = {"apikey": exchange_rates_data_api}

        response = requests.get(url, headers=headers)

        result = response.json()
        dict_currencies = {"currency": el, "rate": result["result"]}
        list_currencies_rates.append(dict_currencies)

    logger.info("Данные переданы")
    return list_currencies_rates


def get_info_card(date: str) -> list:
    logger.info("Старт")
    full_path_file = os.path.join(base_dir, "data", "operations.xlsx")
    df = pd.read_excel(full_path_file)

    start_month = datetime.strptime(date, "%d.%m.%Y %H:%M:%S").replace(day=1)
    end_month = datetime.strptime(date, "%d.%m.%Y %H:%M:%S") + timedelta(days=1)

    df["Дата операции"] = pd.to_datetime(
        df["Дата операции"], format="%d.%m.%Y %H:%M:%S"
    )

    # Получаем операций за нужный промежуток времени
    filtered_df = df[
        (df["Дата операции"] >= start_month) & (df["Дата операции"] <= end_month)
    ]

    # Получаем только операций со знаком "-" и те чей статус "ОК"
    df_expenses = filtered_df[
        (filtered_df["Сумма операции"] < 0) & (filtered_df["Статус"] == "OK")
    ]

    # Группируем df по номерам карт и получаем общю сумму трат на каждую карту
    total_expenses = df_expenses.groupby("Номер карты")["Сумма операции"].sum()

    list_cards = []

    for card, total in total_expenses.items():
        card_str = str(card)
        cards = {
            "last_digits": card_str[-4:],
            "total_spent": round(float(abs(total)), 2),
            "cashback": round(float(abs(total / 100)), 2),
        }
        list_cards.append(cards)

    logger.info("Данные переданы")
    return list_cards


def get_top_transactions(date: str) -> list:
    logger.info("Старт")
    full_path_file = os.path.join(base_dir, "data", "operations.xlsx")

    df = pd.read_excel(full_path_file)

    start_month = datetime.strptime(date, "%d.%m.%Y %H:%M:%S").replace(day=1)
    end_month = datetime.strptime(date, "%d.%m.%Y %H:%M:%S") + timedelta(days=1)

    df["Дата операции"] = pd.to_datetime(
        df["Дата операции"], format="%d.%m.%Y %H:%M:%S"
    )

    # Получаем операций за нужный промежуток времени
    filtered_df = df[
        (df["Дата операции"] >= start_month) & (df["Дата операции"] <= end_month)
    ]

    df_negative = filtered_df[filtered_df["Сумма платежа"] < 0]

    df_top_five = df_negative.nsmallest(5, "Сумма платежа")

    list_top_five = []

    for i, row in df_top_five.iterrows():
        dict_top_five = {
            "date": str(row["Дата операции"]),
            "amount": row["Сумма платежа"],
            "category": row["Категория"],
            "description": row["Описание"],
        }
        list_top_five.append(dict_top_five)

    logger.info("Данные переданы")
    return list_top_five
