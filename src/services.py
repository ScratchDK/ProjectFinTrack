import os
import pandas as pd

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def search_by_phone_number():
    full_path_file = os.path.join(base_dir, "data", "operations.xlsx")
    df = pd.read_excel(full_path_file)

    df_phone_number = df[df["Описание"].str.contains(r"\+\d+")]

    data_json = df_phone_number.to_json(orient="records", force_ascii=False)

    return data_json
