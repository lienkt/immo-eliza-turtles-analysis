import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DATA_PATH = r"D:\Users\Siegried\Desktop\Becode\immo-eliza-turtles-analysis\data\cleaned\clean_dataframe.json"
OUTPUT_DIR = r"D:\Users\Siegried\Desktop\Becode\immo-eliza-turtles-analysis\images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# def get_clean_data(df):
#     df = df.copy()
#     df["Price"] = pd.to_numeric(df["Price"], errors='coerce')
#     df["Livable_surface"] = pd.to_numeric(df["Livable_surface"], errors='coerce')
#     df["Price_per_m2"] = (df["Price"] / 100) / df["Livable_surface"]
#     if "Province" in df.columns:
#         df["Province"] = df["Province"].astype(str).str.capitalize()
        
#     df = df[(df["Price_per_m2"] >= 0) & (df["Price_per_m2"] <= 10000)]
#    return df

def inventory_by_province(df):
    inventory = df.groupby(["Province", "Property_type"]).size().unstack(fill_value=0)
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

import matplotlib.ticker as ticker

def price_per_m2_by_provinces(df):
    plt.figure(figsize=(14, 8))
    avg_mean = df["Price_per_m2"].mean()
    ax = sns.boxplot(
        x="Province", 
        y="Price_per_m2", 
        data=df, 
        hue="Province", 
        palette="magma", 
        legend=False, 
        showfliers=False
    )
    plt.axhline(y=avg_mean, color="black", linestyle="--", linewidth=2, label=f"Average: {avg_mean:,.0f} €/m²")
    plt.legend(loc="upper right")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'.replace(',', ' ') + ' €/m²'))
    plt.title("What is the Price per m² by Province?", fontsize=18)
    plt.xlabel("Province")
    plt.ylabel("Price per m²")
    plt.xticks(rotation=45, ha="right")
    plt.savefig(os.path.join(OUTPUT_DIR, "price_per_m2.png"), bbox_inches="tight", dpi=300)
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

import matplotlib.ticker as ticker

def price_distribution_by_province(df):
    plt.figure(figsize=(14, 8))
    
    # Création du boxplot sans les valeurs extrêmes géantes
    ax = sns.boxplot(
        data=df, 
        x="Province", 
        y="Price", 
        hue="Property_type", 
        palette=["darkblue", "red"],
        showfliers=False
    )
    
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'.replace(',', ' ') + ' €'))
    plt.title("Price Distribution by Province and Property Type")
    plt.xlabel("Province")
    plt.ylabel("Price")
    plt.xticks(rotation=45, ha="right") # Incline le nom des provinces pour éviter la superposition
    plt.savefig(os.path.join(OUTPUT_DIR, "Price_distrib_Prov_Property_Type.png"), bbox_inches="tight", dpi=300)
    plt.close("all")

if __name__ == "__main__":
    if os.path.exists(DATA_PATH):
        df_raw = pd.read_json(DATA_PATH)
        df_raw.columns = df_raw.columns.str.capitalize()
        df_raw["Province"] = df_raw["Province"].str.capitalize()
        cols_to_Int64 = [
            "Postcode", "Price", "Build_year", "Bedroom_count", "Livable_surface", 
            "Total_surface", "Garage", "Terrace", "Swimming_pool", 
            "Energy_consumption_kwh/m2/year", "Preschool_distance_m", 
            "Train_station_distance_m", "Supermarket_distance_m", "Price_per_m2"
        ]

        for col in cols_to_Int64:
            if col in df_raw.columns and df_raw[col].dtype == "float64":
                df_raw[col] = df_raw[col].astype("Int64")
        clean_dataframe = df_raw 
        
        surface_distribution(clean_dataframe)
        inventory_by_province(clean_dataframe)
        price_per_m2_by_provinces(clean_dataframe)
        price_distribution_by_province(clean_dataframe) 
        os.startfile(OUTPUT_DIR)
    else:
        print(f"Error: File not found at {DATA_PATH}")