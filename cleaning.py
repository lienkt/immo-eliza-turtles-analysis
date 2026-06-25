import pandas as pd

raw_df = pd.read_json("./data/raw/dataframe.json")

print("Before:")
print(raw_df.dtypes)

columns_to_Int64 = [
    "postcode",
    "price",
    "build_year",
    "bedroom_count",
    "livable_surface",
    "total_surface",
    "garage",
    "terrace",
    "swimming_pool",
    "peb_category",
    "Preschool_distance",
    "Train_station_distance",
    "Supermarket_distance",
]

for col in columns_to_Int64:
    if col in raw_df.columns and pd.api.types.is_float_dtype(raw_df[col]):
        raw_df[col] = raw_df[col].astype("Int64")

new_column_names = {
    "peb_category": "energy_consumption_kwh_per_m2_per_year",
    "Preschool_distance": "preschool_distance_m",
    "Train_station_distance": "train_station_distance_m",
    "Supermarket_distance": "supermarket_distance_m",
    "distance_nearest_city": "nearest_city_distance_km",
}

clean_df = raw_df.rename(columns=new_column_names)

clean_df.to_json(
    "./data/cleaned/clean_dataframe.json",
    orient="records",
    force_ascii=False,
    indent=4,
)
print("\nAfter:")
print(clean_df.dtypes)