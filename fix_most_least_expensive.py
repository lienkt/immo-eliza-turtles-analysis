import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

BLUE = '#2166ac'
ORANGE = '#d6604d'

GEO_DATA = {
    "Bruxelles": {"name": "Bruxelles-Capitale", "provinces": ["brussels"]},
    "Flandre": {"name": "Flandre", "provinces": ["antwerp", "limburg", "east-flanders", "vlaams-brabant", "west-flanders"]},
    "Wallonie": {"name": "Wallonie", "provinces": ["hainaut", "liege", "luxembourg", "namur", "brabant-wallon"]}
}

def clean_data(df):
    df = df.copy()
    df["price"] = pd.to_numeric(df["price"], errors="coerce") / 1000
    df["livable_surface"] = pd.to_numeric(df["livable_surface"], errors="coerce")
    df = df[(df["price"] > 50) & (df["price"] < 3000)]
    df = df[(df["livable_surface"] > 30) & (df["livable_surface"] < 1000)]
    df = df.dropna(subset=["price", "livable_surface", "province"])
    df["price_per_m2"] = (df["price"] * 1000) / df["livable_surface"]
    df["province"] = df["province"].str.lower()
    df["city"] = df["city"].str.strip().str.capitalize()
    return df

def province_to_region(df):
    mapping = {p.lower(): r for r, info in GEO_DATA.items() for p in info["provinces"]}
    df["region"] = df["province"].map(mapping)
    return df

def export_real_estate_pdf(summary, graph_filename, filename):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    elements = [Paragraph("REAL ESTATE MARKET REPORT - BELGIUM", styles["Title"]), Spacer(1, 15)]
    if os.path.exists(graph_filename):
        elements.append(Image(graph_filename, width=450, height=550))
    doc.build(elements)

def draw_dashboard(df, output_picture_filepath, output_report_filepath):
    city_stats = df.groupby(["region", "city"]).agg(
        mean_price=("price", "mean"), median_price=("price", "median"),
        total_price=("price", "sum"), total_surface=("livable_surface", "sum")
    ).reset_index()
    city_stats["weighted_m2"] = np.where(city_stats["total_surface"] > 0, (city_stats["total_price"] * 1000) / city_stats["total_surface"], 0)

    summary = df.groupby("region", as_index=False).agg(mean_price=("price", "mean"), median_price=("price", "median"), mean_m2=("price_per_m2", "mean"))
    
    for metric, col, name in [("weighted_m2", "m2", "weighted_m2"), ("mean_price", "price", "mean_price"), ("median_price", "median", "median_price")]:
        min_df = city_stats.loc[city_stats.groupby("region")[metric].idxmin()][["region", "city", metric]].rename(columns={"city": f"min_city_{col}", metric: f"{col}_min"})
        max_df = city_stats.loc[city_stats.groupby("region")[metric].idxmax()][["region", "city", metric]].rename(columns={"city": f"max_city_{col}", metric: f"{col}_max"})
        summary = summary.merge(min_df, on="region").merge(max_df, on="region")

    fig, axes = plt.subplots(3, 1, figsize=(12, 18))
    metrics = [("m2", "m2", "€/m²", "What is the most and least expensive price per m²?"), 
               ("price", "price", "k€", "What is the most and least expensive average price?"), 
               ("median", "median", "k€", "What is the most and least expensive median price?")]
    
    x, w = np.arange(len(summary)), 0.35
    
    for i, (m_key, m_name, unit, title) in enumerate(metrics):
        mean_col = f"mean_{m_key}" if m_key != "median" else "median_price"
        axes[i].bar(x - w/2, summary[f"{m_name}_min"], w, color=ORANGE, label="Min City")
        axes[i].bar(x + w/2, summary[f"{m_name}_max"], w, color=BLUE, label="Max City")
        axes[i].plot(x, summary[mean_col], marker="o", color="red", label="Mean/Median", linewidth=2)
        
        for j in range(len(summary)):
            axes[i].text(x[j]+w/2, summary[f"{m_name}_max"][j], summary[f"max_city_{m_name}"][j], ha="center", fontsize=9, fontweight='bold')
            axes[i].text(x[j]-w/2, summary[f"{m_name}_min"][j], summary[f"min_city_{m_name}"][j], ha="center", fontsize=9, fontweight='bold')
            val = summary[mean_col][j]
            axes[i].text(x[j], val * 1.05, f"{val:,.0f}", ha="center", va="bottom", fontsize=9, color="red", fontweight='bold')
        
        axes[i].set_title(title, fontsize=20, fontweight='bold', pad=20)
        axes[i].set_ylabel(f"Price ({unit})", fontsize=12, fontweight='bold')
        axes[i].set_xticks(x)
        axes[i].set_xticklabels(summary["region"], fontsize=12, fontweight='bold')
        axes[i].legend(fontsize=12)

    plt.tight_layout(pad=3.0)
    plt.savefig(output_picture_filepath, dpi=200)
    plt.close()
    export_real_estate_pdf(summary, output_picture_filepath, output_report_filepath)