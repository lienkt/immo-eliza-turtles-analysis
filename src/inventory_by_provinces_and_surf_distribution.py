import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns


def inventory_by_province(df, base_dir):
    """
    Function 1
    """
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
    plt.savefig(os.path.join(base_dir, "./images/nb_properties_by_province.png"), bbox_inches="tight", dpi=300)
    plt.close("all")


def surface_distribution(df, base_dir):
    """
    Function 2
    """
    plt.figure(figsize=(12, 6))
    surface_filtered = df[(df["livable_surface"] >= 0) & (df["livable_surface"] <= 800)]
    sns.histplot(
        data=surface_filtered, 
        x="livable_surface", 
        hue="property_type", 
        element="step", 
        kde=True, 
        palette=["darkblue", "red"], 
        bins=50)
    plt.grid(True, linestyle='--', alpha=0.6, zorder=0)
    plt.title("What is the Distribution of Properties by Livable Surface (m²)?")
    plt.xlabel("Livable Surface (m²)")
    plt.ylabel("Number of Properties")
    plt.savefig(os.path.join(base_dir, "./images/surface_distribution.png"), bbox_inches="tight", dpi=300)
    plt.close("all")
