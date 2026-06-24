import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# from src import inventory_by_province, surface_distribution

def inventory_by_province(df):
    inventory = df.groupby(["province", "property_type"]).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(12, 6))
    inventory.plot(kind="bar", stacked=True, ax=ax, color=["red", "yellow"])
    for container in ax.containers:
    ax.bar_label(container, label_type='edge', padding=3, fontsize=12)
    ax.margins(y=0.1)     
    plt.xticks(rotation=45, ha="right")
    plt.title("What is the Number of Houses vs Apartments by Province?")
    plt.xlabel("Province")
    plt.ylabel("Count")
    plt.savefig(os.path.join(OUTPUT_DIR, "nb_properties_by_province.png"), bbox_inches="tight", dpi=300)
    plt.close("all")


def surface_distribution(df):
    plt.figure(figsize=(12, 6))
    surface_filtered = df[(df["livable_surface"] >= 0) & (df["livable_surface"] <= 800)]
    sns.histplot(
        data=surface_filtered, 
        x="Livable_surface", 
        hue="Property_type", 
        element="step", 
        kde=True, 
        palette=["darkblue", "red"], 
        bins=50)
    plt.grid(True, linestyle='--', alpha=0.6, zorder=0)
    plt.title("What is the Distribution of Properties by Livable Surface (m²)?")
    plt.xlabel("Livable Surface (m²)")
    plt.ylabel("Number of Properties")
    plt.savefig(os.path.join(OUTPUT_DIR, "surface_distribution.png"), bbox_inches="tight", dpi=300)
    plt.close("all")
