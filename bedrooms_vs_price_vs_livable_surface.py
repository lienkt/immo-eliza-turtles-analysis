import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from cleaning_price_lienmade import check_and_fix_price


DATA_PATH = "./data/cleaned/clean_dataframe.json"
FIXED_DATA_PATH = "./data/cleaned/clean_dataframe_fixed.json"
PRICE_SURFACE_IMAGE = "./images/price_vs_livable_surface.png"
BEDROOM_IMAGE = "./images/bedrooms_vs_price.png"
OUTLIER_IMAGE = "./images/outlier_boxplots.png"


def euro_tick(value, _):
    # Show full euro values on the axis so nobody has to read 1e6 math.
    return f"{int(value):,}"


def set_plain_euro_axis():
    ax = plt.gca()
    ax.yaxis.set_major_formatter(FuncFormatter(euro_tick))
    ax.yaxis.offsetText.set_visible(False)


def load_and_fix_data():
    # Grab the cleaned data file.
    df = pd.read_json(DATA_PATH)

    # Use Lien's price fix on the dataframe.
    df = check_and_fix_price(df)

    # Save the fixed file so the team can reuse it later.
    df.to_json(
        FIXED_DATA_PATH,
        orient="records",
        indent=2,
        force_ascii=False,
    )

    return df


def make_price_vs_surface_graph(df):
    # Keep rows where we have the 3 values we need for this graph.
    graph_df = df[["livable_surface", "price", "property_type"]].dropna().copy()

    # Keep only positive numbers so the scatter plot makes sense.
    graph_df = graph_df[(graph_df["livable_surface"] > 0) & (graph_df["price"] > 0)]

    # Split the data in 2 groups so houses and apartments get different colors.
    house_df = graph_df[graph_df["property_type"] == "house"]
    apartment_df = graph_df[graph_df["property_type"] == "apartment"]

    # Keep the full data, but zoom the graph on the part where most points are.
    x_limit = graph_df["livable_surface"].quantile(0.95)
    y_limit = graph_df["price"].quantile(0.95)

    plt.figure(figsize=(10, 6))
    plt.scatter(
        house_df["livable_surface"],
        house_df["price"],
        s=12,
        alpha=0.35,
        label="House",
        color="#1f77b4",
    )
    plt.scatter(
        apartment_df["livable_surface"],
        apartment_df["price"],
        s=12,
        alpha=0.35,
        label="Apartment",
        color="#ff7f0e",
    )

    plt.title("Price vs livable surface")
    plt.xlabel("Livable surface (m2)")
    plt.ylabel("Price (EUR)")
    plt.xlim(0, x_limit)
    plt.ylim(0, y_limit)
    set_plain_euro_axis()
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(PRICE_SURFACE_IMAGE, dpi=180)
    plt.close()


def make_bedrooms_vs_price_graph(df):
    # Keep rows where bedrooms, price, and property type are present.
    graph_df = df[["bedroom_count", "price", "property_type"]].dropna().copy()

    # Keep common bedroom counts so the graph stays readable.
    graph_df = graph_df[(graph_df["bedroom_count"] >= 0) & (graph_df["bedroom_count"] <= 8)]

    # Group by bedroom count and property type.
    # Median is useful here because a few very high prices will not dominate the result.
    grouped_df = (
        graph_df.groupby(["bedroom_count", "property_type"])["price"]
        .median()
        .reset_index()
    )

    house_df = grouped_df[grouped_df["property_type"] == "house"]
    apartment_df = grouped_df[grouped_df["property_type"] == "apartment"]

    plt.figure(figsize=(10, 6))
    plt.plot(
        house_df["bedroom_count"],
        house_df["price"],
        marker="o",
        label="House",
        color="#1f77b4",
    )
    plt.plot(
        apartment_df["bedroom_count"],
        apartment_df["price"],
        marker="o",
        label="Apartment",
        color="#ff7f0e",
    )

    plt.title("Median price by bedroom count")
    plt.xlabel("Bedroom count")
    plt.ylabel("Median price (EUR)")
    plt.xticks(range(0, 9))
    set_plain_euro_axis()
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(BEDROOM_IMAGE, dpi=180)
    plt.close()

def make_outlier_graph(df):
    # Numeric columns that make sense for the outlier question.
    columns = {
        "price": "Price",
        "livable_surface": "Livable surface",
        "total_surface": "Total surface",
        "bedroom_count": "Bedroom count",
    }

    outlier_counts = []
    for col in columns:
        series = df[col].dropna()
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        # IQR rule: values outside this range are unusually far from the middle 50%.
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        n_outliers = int(((series < lower) | (series > upper)).sum())
        outlier_counts.append(
            {
                "variable": columns[col],
                "outliers": n_outliers,
                "percentage": n_outliers / len(series) * 100,
            }
        )

    outlier_df = pd.DataFrame(outlier_counts).sort_values("outliers")

    plt.figure(figsize=(10, 5))
    bars = plt.barh(outlier_df["variable"], outlier_df["outliers"], color="#4c78a8")

    for bar, percentage in zip(bars, outlier_df["percentage"]):
        plt.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f"  {int(bar.get_width())} ({percentage:.1f}%)",
            va="center",
        )

    plt.title("Which variables have the most outliers?")
    plt.xlabel("Number of outliers")
    plt.ylabel("Variable")
    plt.grid(alpha=0.25, axis="x")
    plt.tight_layout()
    plt.savefig(OUTLIER_IMAGE, dpi=180)
    plt.close()


def main():
    df = load_and_fix_data()
    make_price_vs_surface_graph(df)
    make_bedrooms_vs_price_graph(df)
    make_outlier_graph(df)

    print("Done: fixed price file and 3 graphs saved!")


if __name__ == "__main__":
    main()
