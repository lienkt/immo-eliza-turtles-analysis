import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak
from reportlab.platypus import Image
import os
import seaborn as sns

# ── Colour palette we'll reuse ────────────────────────────────────────────────
BLUE   = '#2166ac'
ORANGE = '#d6604d'

GEO_DATA = {
    "bruxelles": {
        "name": "Bruxelles-Capitale", 
        "provinces": ["brussels"]},
    "flandre": {
        "name": "Flandre", 
        "provinces": [
            "antwerp", 
            "limburg", 
            "east-flanders", 
            "vlaams-brabant", 
            "west-flanders"]},
    "wallonie": {
        "name": "Wallonie", 
        "provinces": [
            "hainaut", 
            "liege", 
            "luxembourg", 
            "namur", 
            "brabant-wallon"]}
}

def export_real_estate_pdf(
    summary: pd.DataFrame,
    output_picture_top_cities_filepath: str,
    graph_filename: str,
    filename: str
) -> None:
    """
    Generates a full PDF real estate report using summary statistics and images.
    """

    try:
        if os.path.exists(filename):
            os.remove(filename)
    except PermissionError:
        print(f"{filename} is open. Close it first.")
        return

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    elements = []

    # =====================================================
    # TITLE
    # =====================================================
    title = Paragraph(
        "REAL ESTATE MARKET REPORT - BELGIUM",
        styles["Title"]
    )
    elements.append(title)
    elements.append(Spacer(1, 15))

    intro = Paragraph(
        "This report summarizes the most and least expensive municipalities in Belgium, "
        "based on price per m², average price, and median price.",
        styles["BodyText"]
    )
    elements.append(intro)
    elements.append(Spacer(1, 20))


    # =========================
    # DASHBOARD IMAGE
    # =========================
    elements.append(Paragraph("<b>Visual Dashboard</b>", styles["Heading2"]))
    elements.append(Spacer(1, 6))

    if not os.path.exists(graph_filename):
        elements.append(Paragraph("Dashboard image missing", styles["Normal"]))
    else:
        try:
            img = Image(graph_filename)

            max_width = 400

            scale = max_width / img.imageWidth
            img.drawWidth = img.imageWidth * scale
            img.drawHeight = img.imageHeight * scale

            elements.append(img)
        except Exception as e:
            print(e)
            elements.append(Paragraph("Dashboard image not found.", styles["Normal"]))


    elements.append(PageBreak())
    elements.append(Paragraph("<b>Top 10 Expensive Municipalities</b>", styles["Heading2"]))
    elements.append(Spacer(1, 6))
    if not os.path.exists(output_picture_top_cities_filepath):
        elements.append(Paragraph("Top cities image missing", styles["Normal"]))
    else:
        try:
            img = Image(output_picture_top_cities_filepath)

            max_width = 400

            scale = max_width / img.imageWidth
            img.drawWidth = img.imageWidth * scale
            img.drawHeight = img.imageHeight * scale

            elements.append(img)
        except Exception as e:
            print(e)
            elements.append(Paragraph("Top cities image not found.", styles["Normal"]))

    # =====================================================
    # REGION TABLES
    # =====================================================
    for _, row in summary.iterrows():

        region = row["region"].upper()

        elements.append(Paragraph(f"<b>{region}</b>", styles["Heading2"]))
        elements.append(Spacer(1, 10))

        table_data = [
            ["Metric", "Lowest", "Value", "Highest", "Value"],

            ["Price per m²",
             row["min_city_m2"],
             f"€{row['m2_min']:,.0f}/m²",
             row["max_city_m2"],
             f"€{row['m2_max']:,.0f}/m²"],

            ["Average Price",
             row["min_city_price"],
             f"€{row['price_min']:,.0f}",
             row["max_city_price"],
             f"€{row['price_max']:,.0f}"],

            ["Median Price",
             row["min_city_median"],
             f"€{row['median_min']:,.0f}",
             row["max_city_median"],
             f"€{row['median_max']:,.0f}"],
        ]
        table = Table(
            table_data,
            colWidths=[80, 100, 80, 100, 80]
        )

        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.grey),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("GRID", (0,0), (-1,-1), 0.5, colors.black),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 15))

        # =================================================
        # INSIGHT TEXT (AUTO)
        # =================================================
        insight = f"""
        <b>Key Insight:</b><br /><br />
        In {region}, the highest price per m² is in
        <b>{row['max_city_m2']}</b>, while the lowest is
        <b>{row['min_city_m2']}</b>.<br /><br />

        The most expensive municipality overall is
        <b>{row['max_city_price']}</b>, while the cheapest is
        <b>{row['min_city_price']}</b>.<br /><br />

        This shows strong price inequality across municipalities in {region}.
        """

        elements.append(Paragraph(insight, styles["BodyText"]))
        elements.append(Spacer(1, 25))

    # =====================================================
    # FINAL BELGIUM SUMMARY
    # =====================================================
    belgium = summary[summary["region"].str.lower() == "belgium"].iloc[0]

    elements.append(Paragraph("<b>FINAL CONCLUSION</b>", styles["Heading1"]))
    elements.append(Spacer(1, 10))

    final_text = f"""
    • Most expensive municipality in Belgium:
    <b>{belgium['max_city_price']}</b> (€{belgium['price_max']:,.0f})<br/><br/>

    • Cheapest municipality in Belgium:
    <b>{belgium['min_city_price']}</b> (€{belgium['price_min']:,.0f})<br/><br/>

    • Highest price per m²:
    <b>{belgium['max_city_m2']}</b> (€{belgium['m2_max']:,.0f}/m²)<br/><br/>

    • Lowest price per m²:
    <b>{belgium['min_city_m2']}</b> (€{belgium['m2_min']:,.0f}/m²)<br/><br/>

    Belgium shows strong regional disparity between luxury and affordable municipalities.
    """

    elements.append(Paragraph(final_text, styles["BodyText"]))

    # =====================================================
    # BUILD PDF
    # =====================================================
    doc.build(elements)


def get_belgium_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes Belgium-wide summary statistics from city-level real estate data.
    """

    city_stats = (
        df.groupby("city")
        .agg(
            mean_price=("price", "mean"),
            median_price=("price", "median"),
            total_price=("price", "sum"),
            total_surface=("livable_surface", "sum")
        )
        .reset_index()
    )

    city_stats["weighted_m2"] = np.where(
        city_stats["total_surface"] == 0,
        np.nan,
        city_stats["total_price"] / city_stats["total_surface"]
    )

    return pd.DataFrame([{
        "region": "Belgium",

        # -------------------------
        # GLOBAL STATS
        # -------------------------
        "mean_price": round(df["price"].mean()),
        "median_price": round(df["price"].median()),
        "mean_m2": round(df["price_per_m2"].mean()),

        # -------------------------
        # €/m²
        # -------------------------
        "min_city_m2": city_stats.loc[city_stats["weighted_m2"].idxmin(), "city"],
        "m2_min": round(city_stats["weighted_m2"].min()),

        "max_city_m2": city_stats.loc[city_stats["weighted_m2"].idxmax(), "city"],
        "m2_max": round(city_stats["weighted_m2"].max()),

        # -------------------------
        # PRICE (mean)
        # -------------------------
        "min_city_price": city_stats.loc[city_stats["mean_price"].idxmin(), "city"],
        "price_min": round(city_stats["mean_price"].min()),

        "max_city_price": city_stats.loc[city_stats["mean_price"].idxmax(), "city"],
        "price_max": round(city_stats["mean_price"].max()),

        # -------------------------
        # MEDIAN
        # -------------------------
        "min_city_median": city_stats.loc[city_stats["median_price"].idxmin(), "city"],
        "median_min": round(city_stats["median_price"].min()),

        "max_city_median": city_stats.loc[city_stats["median_price"].idxmax(), "city"],
        "median_max": round(city_stats["median_price"].max()),
    }])

def plot_violin_top10_expensive_cities(
    df: pd.DataFrame,
    output_path: str | None = None
) -> None:
    """
    Creates a violin plot for top 10 most expensive cities.
    """

    # =====================================================
    # 1. GET TOP 10 CITIES BY MEAN PRICE
    # =====================================================

    city_rank = (
        df.groupby("city")["price"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    top_cities = city_rank.index.tolist()

    df_top = df[df["city"].isin(top_cities)].copy()

    # sort for better visualization
    city_order = top_cities

    # =====================================================
    # 2. PLOT
    # =====================================================
    fig, ax = plt.subplots(figsize=(14, 6))

    sns.violinplot(
        data=df_top,
        x="city",
        y="price",
        order=city_order,
        inner=None,
        alpha=0.6,
        ax=ax,
        log_scale=True
    )

    sns.stripplot(
        data=df_top,
        x="city",
        y="price",
        order=city_order,
        alpha=0.25,
        size=3,
        jitter=True,
        ax=ax,
        log_scale=True
    )

    # =====================================================
    # 3. MEAN + MEDIAN LINES
    # =====================================================
    for i, city in enumerate(city_order):

        city_data = df_top[df_top["city"] == city]["price"]

        mean_val = city_data.mean()
        median_val = city_data.median()

        # mean line
        ax.hlines(
            mean_val,
            i - 0.3,
            i + 0.3,
            color="white",
            lw=2.5
        )
        ax.hlines(
            mean_val,
            i - 0.3,
            i + 0.3,
            color=BLUE,
            lw=2,
            ls="--"
        )
        ax.text(
            i + 0.35,
            mean_val,
            f"{mean_val:,.0f}",
            va="center",
            fontsize=8
        )

        # median line
        ax.hlines(
            median_val,
            i - 0.3,
            i + 0.3,
            color=ORANGE,
            lw=2,
            ls="--"
        )
        ax.text(
            i + 0.35,
            median_val,
            f"{median_val:,.0f}",
            va="center",
            fontsize=8
        )

    # =====================================================
    # 4. STYLE
    # =====================================================
    ax.set_title("Top 10 Most Expensive Cities - Price Distribution (Violin Plot)")
    ax.set_xlabel("")
    ax.set_ylabel("Price (€)")
    ax.set_xticks(range(len(city_order)))
    ax.set_xticklabels(city_order, rotation=30, ha="right")

    plt.tight_layout()

    # =====================================================
    # 5. SAVE (optional)
    # =====================================================
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")

    plt.close(fig)

def draw_dashboard(
    df: pd.DataFrame,
    output_picture_top_cities_filepath: str,
    output_picture_filepath: str,
    output_report_filepath: str
) -> None:
    """
    Generates dashboard charts + violin plot + final PDF report.
    """
    # -------------------------
    # REGION LEVEL
    # -------------------------
    summary = df.groupby("region", as_index=False).agg(
        mean_price=("price", "mean"),
        median_price=("price", "median"),
        mean_m2=("price_per_m2", "mean")
    )

    # -------------------------
    # CITY LEVEL
    # -------------------------
    city_stats = df.groupby(["region", "city"]).agg(
        mean_price=("price", "mean"),
        median_price=("price", "median"),
        total_price=("price", "sum"),
        total_surface=("livable_surface", "sum")
    ).reset_index()

    city_stats["weighted_m2"] = np.where(
        city_stats["total_surface"] == 0,
        np.nan,
        city_stats["total_price"] / city_stats["total_surface"]
    )

    # =========================================================
    # MIN / MAX METRICS
    # =========================================================
    w_min = city_stats.loc[city_stats.groupby("region")["weighted_m2"].idxmin()][["region", "city", "weighted_m2"]]
    w_max = city_stats.loc[city_stats.groupby("region")["weighted_m2"].idxmax()][["region", "city", "weighted_m2"]]

    w_min = w_min.rename(columns={"city": "min_city_m2", "weighted_m2": "m2_min"})
    w_max = w_max.rename(columns={"city": "max_city_m2", "weighted_m2": "m2_max"})

    p_min = city_stats.loc[city_stats.groupby("region")["mean_price"].idxmin()][["region", "city", "mean_price"]]
    p_max = city_stats.loc[city_stats.groupby("region")["mean_price"].idxmax()][["region", "city", "mean_price"]]

    p_min = p_min.rename(columns={"city": "min_city_price", "mean_price": "price_min"})
    p_max = p_max.rename(columns={"city": "max_city_price", "mean_price": "price_max"})

    m_min = city_stats.loc[city_stats.groupby("region")["median_price"].idxmin()][["region", "city", "median_price"]]
    m_max = city_stats.loc[city_stats.groupby("region")["median_price"].idxmax()][["region", "city", "median_price"]]

    m_min = m_min.rename(columns={"city": "min_city_median", "median_price": "median_min"})
    m_max = m_max.rename(columns={"city": "max_city_median", "median_price": "median_max"})

    # =========================================================
    # MERGE
    # =========================================================
    summary = summary.merge(w_min, on="region").merge(w_max, on="region")
    summary = summary.merge(p_min, on="region").merge(p_max, on="region")
    summary = summary.merge(m_min, on="region").merge(m_max, on="region")

    # -------------------------
    # ADD BELGIUM SAFE
    # -------------------------
    belgium = get_belgium_summary(df)

    for col in summary.columns:
        if col not in belgium.columns:
            belgium[col] = np.nan

    belgium = belgium[summary.columns]

    summary = pd.concat([summary, belgium], ignore_index=True)

    summary = summary.sort_values("region").reset_index(drop=True)

    summary["region"] = summary["region"].str.strip().str.title()

    # =========================================================
    # PLOT
    # =========================================================
    x = np.arange(len(summary))
    width = 0.35
    fig, axes = plt.subplots(3, 1, figsize=(14, 14), constrained_layout=True)

    # -------------------------
    # 1 €/m²
    # -------------------------
    axes[0].bar(x - width/2, summary["m2_min"], width, label="Weighted €/m² - Min City", color=ORANGE)
    axes[0].bar(x + width/2, summary["m2_max"], width, label="Weighted €/m² - Max City", color=BLUE)
    axes[0].plot(x, summary["mean_m2"], marker="o", label="Weighted €/m² (Mean)", color="red")

    axes[0].set_title("Weighted Average Price €/m² distribution with Min/Max Cities")
    axes[0].set_ylabel("€/m²")
    
    for i in range(len(summary)):
            
        # label min city
        axes[0].text(
            x[i]-width/2,
            summary["m2_min"][i],
            summary["min_city_m2"][i],
            ha="center",
            fontsize=8
        )

        # label max city
        axes[0].text(
            x[i]+width/2,
            summary["m2_max"][i],
            summary["max_city_m2"][i],
            ha="center",
            fontsize=8
        )

        # label line chart (MEAN)
        axes[0].text(
            x[i],
            summary["mean_m2"][i],
            f"{summary['mean_m2'][i]:,.0f}",
            ha="center",
            va="bottom",
            fontsize=8,
            color="black"
        )

    # -------------------------
    # 2 Mean price
    # -------------------------
    axes[1].bar(x - width/2, summary["price_min"], width, label="Mean € - Min City", color=ORANGE)
    axes[1].bar(x + width/2, summary["price_max"], width, label="Mean € - Max City", color=BLUE)
    axes[1].plot(x, summary["mean_price"], marker="o", label="Mean €", color="red")

    axes[1].set_title("Mean Price € distribution with Min/Max Cities")
    axes[1].set_ylabel("€")

    for i in range(len(summary)):
        # label min city
        axes[1].text(
            x[i]-width/2,
            summary["price_min"][i],
            summary["min_city_price"][i],
            ha="center",
            fontsize=8
        )

        # label max city
        axes[1].text(
            x[i]+width/2,
            summary["price_max"][i],
            summary["max_city_price"][i],
            ha="center",
            fontsize=8
        )

        # label line chart (MEAN PRICE)
        axes[1].text(
            x[i],
            summary["mean_price"][i],
            f"{summary['mean_price'][i]:,.0f}",
            ha="center",
            va="bottom",
            fontsize=8,
            color="black"
        )

    # -------------------------
    # 3 Median price
    # -------------------------
    axes[2].bar(x - width/2, summary["median_min"], width, label="Median € - Min City", color=ORANGE)
    axes[2].bar(x + width/2, summary["median_max"], width, label="Median € - Max City", color=BLUE)
    axes[2].plot(x, summary["median_price"], marker="o", label="Median €", color="red")

    axes[2].set_title("Median Price € distribution with Min/Max Cities")
    axes[2].set_ylabel("€")

    for i in range(len(summary)):
        # label min city
        axes[2].text(
            x[i]-width/2,
            summary["median_min"][i],
            summary["min_city_median"][i],
            ha="center",
            fontsize=8
        )

        # label max city
        axes[2].text(
            x[i]+width/2,
            summary["median_max"][i],
            summary["max_city_median"][i],
            ha="center",
            fontsize=8
        )

        # label line chart (MEDIAN PRICE)
        axes[2].text(
            x[i],
            summary["median_price"][i],
            f"{summary['median_price'][i]:,.0f}",
            ha="center",
            va="bottom",
            fontsize=8,
            color="black"
        )

    # =========================================================
    # FIX X-AXIS (REGION LABELS)
    # =========================================================
    for ax in axes:
        ax.set_xticks(x)
        ax.set_xticklabels(summary["region"], rotation=0)
        # ax.set_xlabel("Region")
        
        ax.margins(y=0.2)
        ax.legend(
            loc="upper left",
            bbox_to_anchor=(1, 1),
            frameon=True
        )

    if os.path.exists(output_picture_filepath):
        os.remove(output_picture_filepath)

    plt.savefig(output_picture_filepath, dpi=300)
    plt.close(fig)

    plot_violin_top10_expensive_cities(df, output_picture_top_cities_filepath)

    export_real_estate_pdf(summary, output_picture_top_cities_filepath, output_picture_filepath, output_report_filepath)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw real estate dataset and computes price_per_m2.
    """

    df = df.copy()

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["livable_surface"] = pd.to_numeric(df["livable_surface"], errors="coerce")

    # FILTER CITIES WITH > 50 ROWS
    city_counts = df["city"].value_counts()
    valid_cities = city_counts[city_counts > 50].index

    df = df[df["city"].isin(valid_cities)].copy()

    # 2. remove missing
    df = df.dropna(subset=["price", "livable_surface", "province"])

    # 4. compute feature
    df["price_per_m2"] = df["price"] / df["livable_surface"]

    # 6. normalize text
    df["province"] = df["province"].str.lower()

    return df
def province_to_region(df: pd.DataFrame) -> pd.DataFrame:
    """
    Maps provinces to Belgian regions (Brussels, Flanders, Wallonia).
    """

    province_to_region = {
        province.lower(): region
        for region, info in GEO_DATA.items()
        for province in info["provinces"]
    }
    df["region"] = df["province"].map(province_to_region)
    return df

def export_most_least_expensive_municipalities_regions_report(
    clean_dataframe_filepath: str,
    base_dir: str
) -> None:
    """
    Full pipeline:
    load data → clean → map regions → generate dashboard → export report.
    """
    df = pd.read_json(clean_dataframe_filepath)
    df_clean = clean_data(df)
    df_clean = province_to_region(df_clean)
      
    output_picture_top_cities_filepath = os.path.join(base_dir, "./images/most_expensive_municipalities.png")
    output_most_least_expensive_picture_filepath = os.path.join(base_dir, "./images/most_least_expensive_municipalities_regions.png")
    output_report_filepath = os.path.join(base_dir, "./reports/most_least_expensive_municipalities_regions.pdf") 

    draw_dashboard(df_clean, output_picture_top_cities_filepath, output_most_least_expensive_picture_filepath, output_report_filepath)
    