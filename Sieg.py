import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DATA_PATH = r"D:\Users\Siegried\Desktop\Becode\immo-eliza-turtles-analysis\data\cleaned\clean_df.json"
OUTPUT_DIR = r"D:\Users\Siegried\Desktop\Becode\immo-eliza-turtles-analysis\images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def inventory_by_province(df):
    inventory = df.groupby(["Province", "Property_type"]).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(12, 6))
    inventory.plot(kind="bar", stacked=True, ax=ax, color=["red", "yellow"])
    for container in ax.containers:
        # label_type='edge' puts it on top, no rotation needed
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
    surface_filtered = df[(df["Livable_surface"] >= 0) & (df["Livable_surface"] <= 800)]
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


if __name__ == "__main__":
    df_raw = pd.read_json(DATA_PATH)
    df_raw.columns = df_raw.columns.str.capitalize()
    df_raw["Province"] = df_raw["Province"].str.capitalize()
    clean_df = df_raw 
    surface_distribution(clean_df)
    inventory_by_province(clean_df)
    os.startfile(OUTPUT_DIR)