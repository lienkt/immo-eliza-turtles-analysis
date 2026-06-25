import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd
import os

PRICE_SURFACE_IMAGE = "./images/price_vs_livable_surface.png"
BEDROOM_IMAGE = "./images/bedrooms_vs_price.png"
OUTLIER_IMAGE = "./images/outlier_boxplots.png"
PROPERTY_STATE_M2_IMAGE = "./images/property_state_price_per_m2.png"
CONVENIENCE_SPACE_IMAGE = "./images/convenience_vs_space.png"
BUILD_YEAR_M2_IMAGE = "./images/build_year_price_per_m2.png"

# Change these at the top to align colours across the team's scripts.
COLOR_PRICE_BAR = "#2166ac" # bar colour shared by outlier + build‑year graphs
COLOR_ENERGY_LINE = "#d6604d"# energy‑consumption line in build‑year graph

#all the path & colors variable are here there is nothing else to change in the definition exept the graph themselves.


def make_price_vs_surface_graph(df, base_dir):
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
    plt.savefig(os.path.join(base_dir, PRICE_SURFACE_IMAGE), dpi=180)
    plt.close()


def make_bedrooms_vs_price_graph(df, base_dir):
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
    plt.savefig(os.path.join(base_dir, BEDROOM_IMAGE), dpi=180)
    plt.close()

def make_outlier_graph(df, base_dir):
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
    bars = plt.barh(outlier_df["variable"], outlier_df["outliers"], color=COLOR_PRICE_BAR)

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
    plt.savefig(os.path.join(base_dir, OUTLIER_IMAGE), dpi=180)
    plt.close()

#You can ignroe that one i was doing this while looking for creative idea.
def make_property_state_price_m2_graph_imad(df, base_dir):
    """Generate a bar chart of median price per M2 by property state.

    Input:
        df: pandas DataFrame with price_per_m2, property_state, and property_type columns.
    """
    def euro_tick(value, _):
        return f"{int(value):,}"

    # Keep rows where we have the values needed for this graph.
    graph_df = df[["price_per_m2", "property_state", "property_type"]].dropna().copy()

    # Keep only positive numbers so the price per M2 makes sense.
    graph_df = graph_df[graph_df["price_per_m2"] > 0]

    # Keep realistic values so one strange listing does not dominate the scale.
    graph_df = graph_df[(graph_df["price_per_m2"] > 300) & (graph_df["price_per_m2"] < 20000)]

    # Group by property state and property type.
    # Median is useful here because a few luxury listings will not dominate the result.
    grouped_df = (
        graph_df.groupby(["property_state", "property_type"])["price_per_m2"]
        .median()
        .reset_index()
    )

    # Put the states in a logical order from worst condition to best condition.
    order = [
        "To be renovated",
        "To renovate",
        "Normal",
        "Fully renovated",
        "Excellent",
        "New",
    ]
    grouped_df["property_state"] = pd.Categorical(
        grouped_df["property_state"],
        categories=order,
        ordered=True,
    )

    # Reshape the grouped data so houses and apartments become separate bars.
    grouped_df = grouped_df.dropna().sort_values("property_state")
    pivot_df = grouped_df.pivot(
        index="property_state",
        columns="property_type",
        values="price_per_m2",
    )

    ax = pivot_df.plot(kind="bar", figsize=(10, 6), color=["#ff7f0e", "#1f77b4"])
    ax.set_title("Median price per M2 by property state")
    ax.set_xlabel("Property state")
    ax.set_ylabel("Median price per M2 (EUR)")
    ax.yaxis.set_major_formatter(FuncFormatter(euro_tick))
    ax.yaxis.offsetText.set_visible(False)
    plt.xticks(rotation=35, ha="right")
    plt.grid(alpha=0.25, axis="y")
    plt.legend(title="Property type")
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, PROPERTY_STATE_M2_IMAGE), dpi=180)
    plt.close()


def make_convenience_vs_space_graph(df, base_dir):
    """Generate a graph comparing supermarket distance, price per M2, and surface.

    Input:
        df: pandas DataFrame with price_per_m2, livable_surface, and supermarket_distance_m columns.
    """
    def euro_tick(value, _):
        return f"{int(value):,}"

    # Keep rows where we have the values needed for this graph.
    graph_df = df[["price_per_m2", "livable_surface", "supermarket_distance_m"]].dropna().copy()

    # Keep only positive numbers so the price per M2 makes sense.
    graph_df = graph_df[(graph_df["price_per_m2"] > 0) & (graph_df["livable_surface"] > 0)]

    # Keep realistic values so one strange listing does not dominate the scale.
    graph_df = graph_df[(graph_df["price_per_m2"] > 300) & (graph_df["price_per_m2"] < 20000)]

    # Split the properties into 4 groups from closest to farthest from a supermarket.
    graph_df["distance_group"] = pd.qcut(
        graph_df["supermarket_distance_m"],
        4,
        labels=["Closest", "Close", "Far", "Farthest"],
    )

    # For each distance group, keep the median price per M2, surface, and distance.
    grouped_df = (
        graph_df.groupby("distance_group", observed=True)
        .agg(
            price_per_m2=("price_per_m2", "median"),
            livable_surface=("livable_surface", "median"),
            distance=("supermarket_distance_m", "median"),
        )
        .reset_index()
    )

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    # Bars show median price per M2.
    ax1.bar(
        grouped_df["distance_group"],
        grouped_df["price_per_m2"],
        color="#4c78a8",
        alpha=0.8,
        label="Median price per M2",
    )

    # The line shows median livable surface on a second axis.
    ax2.plot(
        grouped_df["distance_group"],
        grouped_df["livable_surface"],
        marker="o",
        color="#f58518",
        linewidth=2,
        label="Median livable surface",
    )

    # Show the median distance on top of each bar to make the quartiles easier to read.
    for i, row in grouped_df.iterrows():
        ax1.text(i, row["price_per_m2"], f"{row['distance']:.0f} m", ha="center", va="bottom")

    ax1.set_title("Convenience vs space")
    ax1.set_xlabel("Distance to nearest supermarket")
    ax1.set_ylabel("Median price per M2 (EUR)")
    ax2.set_ylabel("Median livable surface (m2)")
    ax1.yaxis.set_major_formatter(FuncFormatter(euro_tick))
    ax1.yaxis.offsetText.set_visible(False)
    ax1.grid(alpha=0.25, axis="y")
    fig.legend(loc="upper right", bbox_to_anchor=(0.9, 0.9))
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, CONVENIENCE_SPACE_IMAGE), dpi=180)
    plt.close()


def make_build_year_price_m2_graph(df, base_dir):
    """Generate a graph comparing build period, price per M2, and energy consumption.

    Input:
        df: pandas DataFrame with price_per_m2, build_year, and energy_consumption_kWh/m2/year columns.
    """
    def euro_tick(value, _):
        return f"{int(value):,}"

    # Keep rows where we have the values needed for this graph.
    graph_df = df[
        ["price_per_m2", "build_year", "energy_consumption_kWh/m2/year"]
    ].dropna().copy()

    # Keep only rows where price per M2 and build year make sense.
    graph_df = graph_df[
        (graph_df["price_per_m2"] > 0)
        & (graph_df["build_year"] >= 1800)
        & (graph_df["build_year"] <= 2026)
    ]

    # Keep realistic values so one strange listing does not dominate the scale.
    graph_df = graph_df[(graph_df["price_per_m2"] > 300) & (graph_df["price_per_m2"] < 20000)]

    # Group build years into broad periods so the trend is easier to read.
    graph_df["build_period"] = pd.cut(
        graph_df["build_year"],
        bins=[1799, 1918, 1945, 1970, 1990, 2010, 2026],
        labels=["<=1918", "1919-1945", "1946-1970", "1971-1990", "1991-2010", "2011+"],
    )

    # For each build period, keep the median price per M2 and median energy consumption.
    grouped_df = (
        graph_df.groupby("build_period", observed=True)
        .agg(
            price_per_m2=("price_per_m2", "median"),
            energy=("energy_consumption_kWh/m2/year", "median"),
        )
        .reset_index()
    )

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    # Bars show median price per M2.
    ax1.bar(
        grouped_df["build_period"],
        grouped_df["price_per_m2"],
        color=COLOR_PRICE_BAR,
        alpha=0.8,
        label="Median price per M2",
    )

    # The line shows median energy consumption on a second axis.
    ax2.plot(
        grouped_df["build_period"],
        grouped_df["energy"],
        marker="o",
        color=COLOR_ENERGY_LINE,
        linewidth=2,
        label="Median energy consumption",
    )

    ax1.set_title("Newer properties: higher price per M2, lower energy consumption")
    ax1.set_xlabel("Build period")
    ax1.set_ylabel("Median price per M2 (EUR)")
    ax2.set_ylabel("Median energy consumption (kWh/m2/year)")
    ax1.yaxis.set_major_formatter(FuncFormatter(euro_tick))
    ax1.yaxis.offsetText.set_visible(False)
    ax1.grid(alpha=0.25, axis="y")
    fig.legend(loc="upper right", bbox_to_anchor=(0.9, 0.9))
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, BUILD_YEAR_M2_IMAGE), dpi=180)
    plt.close()
