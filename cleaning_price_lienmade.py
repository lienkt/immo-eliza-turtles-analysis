import pandas as pd


def check_and_fix_price(df):
    df = df.copy()

    # Make sure the price column is numeric before we compare values.
    df["price"] = pd.to_numeric(df["price"], errors="coerce").astype(float)

    # Mark rows where the price looks way too high.
    df["price_flag"] = df["price"] > 5_000_000

    # Divide only the flagged rows by 100.
    df.loc[df["price_flag"], "price"] = df.loc[df["price_flag"], "price"] / 100

    # Round the cleaned price and store it back as an integer column.
    df["price"] = df["price"].round(0).astype("Int64")

    # If garage or swimming pool is missing, the team decided it means 0.
    df.fillna(value={"garage": 0, "swimming_pool": 0}, inplace=True)

    return df


def save_fixed_price_file():
    df = pd.read_json("./data/cleaned/clean_dataframe.json")
    df = check_and_fix_price(df)

    df.to_json(
        "./data/cleaned/clean_dataframe_fixed.json",
        orient="records",
        indent=2,
        force_ascii=False,
    )

    print("Done: price cleaned + file saved!")


if __name__ == "__main__":
    save_fixed_price_file()
