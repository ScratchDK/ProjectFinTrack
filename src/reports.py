import logging
import os
from datetime import datetime, timedelta
from typing import Optional, Callable, Any

import pandas as pd
from dateutil.relativedelta import relativedelta

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

path_file_logs = os.path.join(base_dir, "logs", "reports.log")

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(path_file_logs, encoding="utf-8", mode="w")
file_formatter = logging.Formatter(
    "%(asctime)s - %(filename)s [%(funcName)s] - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def write_to_file(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Any]:
    """Функция 'обертка' для ведения логов входящих функций, если в параметрах указан файл,
    то статус выполнения функции сохраняется в него, если нет то выводится в консоль."""

    def my_decorator(func: Callable) -> Any:
        def wrapper(df: pd.DataFrame, *args: Any, **kwargs: Any) -> Any:

            result = func(df, *args, **kwargs)

            if filename is None:
                path_file_spending_by_category = os.path.join(base_dir, "data", "spending_by_category.xlsx")
                result.to_excel(path_file_spending_by_category, index=False)
            else:
                path_file_spending_by_category = os.path.join(base_dir, "data", filename)
                result.to_excel(path_file_spending_by_category, index=False)

            return result

        return wrapper

    return my_decorator


@write_to_file()
def spending_by_category(
    df: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:
    logger.info("Старт")
    if date is None:
        date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    end_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S") + timedelta(days=1)
    start_date = end_date + relativedelta(months=-3)

    df["Дата операции"] = pd.to_datetime(
        df["Дата операции"], format="%d.%m.%Y %H:%M:%S"
    )

    filtered_df = df[
        (df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)
    ]

    filtered_by_category = filtered_df[filtered_df["Категория"] == category]

    logger.info("Данные переданы")
    return filtered_by_category


full_path_file = os.path.join(base_dir, "data", "operations.xlsx")

df_ = pd.read_excel(full_path_file)

#print(spending_by_category(df_, 'Супермаркеты', "24.12.2021 19:00:00"))
