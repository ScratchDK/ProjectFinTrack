import json
from datetime import datetime

from src.utils import get_share_price, get_currencies_rates, get_info_card, get_top_transactions


def main(date):
    try:
        date_obj = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    except Exception as e:
        print(type(e).__name__)
        return "Неверный формат даты!"
    else:
        hour = date_obj.hour

    if 6 <= hour < 12:
        greeting = "Доброе утро!"
    elif 12 <= hour < 17:
        greeting = "Доброе день!"
    elif 17 <= hour < 23:
        greeting = "Доброе вечер!"
    else:
        greeting = "Доброй ночи!"

    cards = get_info_card(date)
    top_transactions = get_top_transactions(date)
    #currency_rates = get_currencies_rates()
    stock_prices = get_share_price()

    data_list = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        #"currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    json_data = json.dumps(data_list, ensure_ascii=False)

    return json_data
