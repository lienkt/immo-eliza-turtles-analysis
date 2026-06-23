import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
#exemple import
#from src.graph_price_surface_outliers import (
    #make_price_vs_surface_graph,
    #make_bedrooms_vs_price_graph,
    #make_outlier_graph,


PRICE_SURFACE_IMAGE = "../images/price_vs_livable_surface.png"
BEDROOM_IMAGE = "../images/bedrooms_vs_price.png"
OUTLIER_IMAGE = "../images/outlier_boxplots.png"


def make_price_vs_surface_graph(df):
    """Generate a scatter plot of price vs livable surface.

    Input:
        df: pandas DataFrame with livable_surface, price, and property_type columns.
    """
    def euro_tick(value, _):
        # Show full euro values on the axis so nobody has to read 1e6 math.
        return f"{int(value):,}"

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
    ax = plt.gca()
    ax.yaxis.set_major_formatter(FuncFormatter(euro_tick))
    ax.yaxis.offsetText.set_visible(False)
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(PRICE_SURFACE_IMAGE, dpi=180)
    plt.close()


def make_bedrooms_vs_price_graph(df):
    """Generate a line graph of median price by bedroom count.

    Input:
        df: pandas DataFrame with bedroom_count, price, and property_type columns.
    """
    def euro_tick(value, _):
        # Show full euro values on the axis so nobody has to read 1e6 math.
        return f"{int(value):,}"

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
    ax = plt.gca()
    ax.yaxis.set_major_formatter(FuncFormatter(euro_tick))
    ax.yaxis.offsetText.set_visible(False)
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(BEDROOM_IMAGE, dpi=180)
    plt.close()

def make_outlier_graph(df):
    """Generate a bar chart showing which numeric variables have the most outliers.

    Input:
        df: pandas DataFrame with price, livable_surface, total_surface, and bedroom_count columns.
    """
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
