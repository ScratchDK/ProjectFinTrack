import logging
import os

import pandas as pd

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

path_file_logs = os.path.join(base_dir, "logs", "services.log")

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(path_file_logs, encoding="utf-8", mode="w")
file_formatter = logging.Formatter(
    "%(asctime)s - %(filename)s [%(funcName)s] - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def search_by_phone_number() -> str:
    logger.info("Старт")
    full_path_file = os.path.join(base_dir, "data", "operations.xlsx")

    try:
        df = pd.read_excel(full_path_file)
    except Exception as e:
        logger.error(f"{type(e).__name__}, файл не найден!")
        return type(e).__name__

    df_phone_number = df[df["Описание"].str.contains(r"\+\d|7\d+")]

    data_json = df_phone_number.to_json(orient="records", force_ascii=False)

    logger.info("Данные переданы")
    return data_json
