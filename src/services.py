import os
import logging
import pandas as pd

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

path_file_logs = full_path_file_logs = os.path.join(base_dir, "logs", "services.log")

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(path_file_logs, encoding="utf-8", mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s [%(funcName)s] - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def search_by_phone_number():
    logger.info("Старт")
    full_path_file = os.path.join(base_dir, "data", "operations.xlsx")
    df = pd.read_excel(full_path_file)

    df_phone_number = df[df["Описание"].str.contains(r"\+\d+")]

    data_json = df_phone_number.to_json(orient="records", force_ascii=False)

    logger.info("Данные переданы")
    return data_json
