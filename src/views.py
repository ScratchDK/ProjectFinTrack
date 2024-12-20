import os
import json
import logging
from datetime import datetime

from src.utils import (
    get_share_price,
    get_currencies_rates,
    get_info_card,
    get_top_transactions,
)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

path_file_logs = full_path_file_logs = os.path.join(base_dir, "logs", "views.log")

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(path_file_logs, encoding="utf-8", mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s [%(funcName)s] - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def main(date):
    logger.info("Старт")
    try:
        date_obj = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    except Exception as e:
        logger.error(f"{type(e).__name__}, неверный формат даты!")
        return "Неверный формат даты!"
    else:
        hour = date_obj.hour

    if 6 <= hour < 12:
        greeting = "Доброе утро!"
    elif 12 <= hour < 17:
        greeting = "Добрый день!"
    elif 17 <= hour < 23:
        greeting = "Добрый вечер!"
    else:
        greeting = "Доброй ночи!"

    cards = get_info_card(date)
    top_transactions = get_top_transactions(date)
    currency_rates = get_currencies_rates()
    stock_prices = get_share_price()

    data_list = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    json_data = json.dumps(data_list, ensure_ascii=False)

    logger.info("Данные переданы")
    return json_data
