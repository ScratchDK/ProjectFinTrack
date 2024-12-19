from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta


def spending_by_category(
    df: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:

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

    return filtered_by_category
