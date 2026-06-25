    # Immo Eliza Data Analysis: Project Documentation

## Description

Following our data scraping phase, this project focuses on cleaning, exploring, and analyzing the Belgian real estate dataset for **Immo Eliza**. The ultimate goal is to uncover market insights and identify the key variables that influence property prices to help management make data-driven decisions.

## Project Objectives

* Clean the scraped dataset (handle duplicates, missing values, and data types).
* Analyze correlations, distributions, and outliers regarding property prices.
* Identify the most/least expensive municipalities in Belgium (by region).
* Deliver a non-technical, high-impact presentation with clear data visualizations.
* Keep the code understandable enough for the full team to review and maintain.

---

## Target Client Persona

Our analysis is tailored for **"Immovland"**, a new real estate agency launching in the Belgian market. 

As a newcomer facing established competitors, Immovland needs data-driven insights to build its business strategy. This analysis helps them answer:
* **Where to focus:** Which Belgian municipalities and regions offer the most lucrative or highly active markets?
* **What to target:** What property features (surface, location, bedrooms, etc.) have the strongest impact on a property's final selling price?
* **Competitive pricing:** How to accurately price new listings to attract clients quickly without losing profit margins.

---

## Team & Roles

* **Imad** – Project Lead (Agile Master)
* **Lien** – Git Commander (Repo Manager)
* **Max** – QA & Data Architect
* **Siegried** – Documentation Specialist

---

## Repository Structure

```text
immo-eliza-teamname-analysis/
├── .gitignore
├── README.md
├── main.py                 # Script to run the cleaning and generate all final images
├── analysis/               # Individual exploration and training folders
│   ├── imad_training/
│   ├── lien_training/
│   ├── max_training/
│   └── siegried_training/
├── data/
│   ├── cleaned/            
│   └── raw/                
├── images/                 
├── reports/               
└── src/                    # Source code for cleaning or processing functions

```

---

## Git Strategy

Working with Jupyter Notebooks (`.ipynb`) can make Git merges tricky because of background metadata changes. To maintain a clean repository, our team follows a strict branching workflow managed by our Git Commander:

1. **Feature Branches:** Every team member works on a separate branch named after their task (e.g., `feature/imad-exploration data`, `feature/max-cleaning`).
2. **The Dev Branch:** All individual branches are submitted via a Pull Request (PR) to the `dev` branch for testing, code review, and plot verification.
3. **The Main Branch:** On Thursday, once the pipeline in `main.py` is fully tested and stable, `dev` is merged into `main` for final delivery.

---

## Timeline & Workflow

* **Friday:** Solo exploration, individual notebook drafts, and role definition.
* **Monday:** Task repartition and data cleaning alignment (handling duplicates and blank spaces).
* **Tuesday:** Selecting the best insights/plots to display using the cleaned dataframe.
* **Wednesday:** Polishing selected plots and merging individual work into the `dev` branch.
* **Thursday:** Wrapping up, running `main.py` to export final visuals, finalizing slides, and presentation.

---

## Visualizations Checklist

All plots saved in the `images/` folder follow these strict presentation standards:

* Clear titles and understandable axis labels.
* Axis units included with comparable scales.
* No overlapping text and smart, intentional use of colors.
* A clear, single takeaway per visual.

---

## Installation & Usage

1. **Setup Environment:**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # On Mac use: source .venv/bin/activate
pip install -r requirements.txt

```

2. **Cleaning**
We also validate dataset quality by analyzing missing values per column and visualizing incomplete features.
```bash
def dataframe_cleaner(raw_df, clean_dataframe_filepath):
    """
    Function cleaning a raw dataframe and saving it in a json file
    :params: pandas.DataFrame
    Returns pandas.DataFrame
    """
    clean_df = raw_df.drop_duplicates(subset=['postcode', 'price', 'livable_surface', 'address'])

    clean_df['price_per_m2'] = clean_df['price'] / clean_df['livable_surface']

    rows_to_Int64 = ["postcode", "price", "build_year", "bedroom_count", "livable_surface", "total_surface", "garage", "terrace", "swimming_pool", "peb_category", "Preschool_distance", "Train_station_distance", "Supermarket_distance"]

    for row in rows_to_Int64:
        if clean_df[row].dtype == "float64":
            clean_df[row] = clean_df[row].astype("Int64")
    
    new_column_names = {"peb_category": "energy_consumption_kWh/m2/year",
                    "Preschool_distance": "preschool_distance_m",
                    "Train_station_distance": "train_station_distance_m",
                    "Supermarket_distance": "supermarket_distance_m",
                    "distance_nearest_city": "nearest_city_distance_km"}

    clean_df = clean_df.rename(columns=new_column_names)

    for col in ['city', 'province', 'address', 'nearest_city']:
        clean_df[col] = clean_df[col].apply(lambda x: html.unescape(x) if isinstance(x, str) else x)

    clean_df.fillna(value={'garage': 0, 'swimming_pool': 0}, inplace=True)

    clean_df["property_state"] = clean_df["property_state"].replace("To be renovated", "To renovate")

    clean_df.to_json(clean_dataframe_filepath, orient="records", force_ascii=False, indent=4)
```

3. **Run the Analysis Pipeline:**
To clean the raw data and export all final plots to the `images/` folder, run:
```bash
python main.py

```

---

## Project Pipeline Overview

The project follows a structured end-to-end data workflow:

1. Data Collection (Scraping phase – completed prior to this project)
2. Data Cleaning (handling missing values, duplicates, and formatting issues)
3. Exploratory Data Analysis (EDA)
4. Feature understanding and correlation analysis
5. Regional and market segmentation analysis
6. Visualization generation for business communication
7. Insight extraction for non-technical stakeholders (Immovland)

---

## Key Analytical Questions Addressed

The analysis is structured around a set of mandatory questions required by the project brief. Each question is explored through code and visualizations where relevant.

---

### Dataset structure and quality

* How many observations and features/columns do you have?
* What is the proportion of missing values per column?
* Which variables would you delete and why?

These questions help evaluate dataset completeness and determine whether certain features are too incomplete or unreliable for analysis.

---

### Data distribution and variable behavior

* What variables are most subject to outliers?
* How are the number of properties distributed according to their surface?

These analyses help identify skewed distributions, extreme values, and structural patterns in the dataset.

---

### Variable types and appropriate analysis methods

* How many qualitative and quantitative variables are there?
* What are appropriate visuals for quantitative vs qualitative data?
* What are appropriate measures for correlations when dealing with qualitative and quantitative variables?

This step ensures the correct statistical and visual approach is used depending on variable type.

---

### Correlation and relationships

* What is the correlation between variables and the price?
* Why do some variables correlate more strongly with price than others?
* How are variables themselves correlated to each other?
* Can you identify groups of strongly correlated variables?

This section focuses on understanding relationships between features and how they interact with each other and with price.

---

### Feature importance

* Which five variables do you consider the most important and why?

This question identifies the most impactful predictors of property price based on statistical relationships and business relevance.

---

### Regional and market analysis

* What are the least/most expensive municipalities in Belgium, Wallonia, and Flanders?

  * In terms of:

    * Average price
    * Median price
    * Price per m²

This section highlights geographic inequalities and helps identify investment opportunities or overpriced/underpriced areas.

---

## Summary

These questions form the backbone of the exploratory analysis. They ensure that the dataset is not only statistically understood, but also translated into actionable insights for **Immovland**, the business persona.

---


## Cleaned Data Dictionary

| Column | Type | Description |
| --- | --- | --- |
| `property_type` | string | Type of property (`house` or `apartment`) |
| `property_id` | string | Unique property reference code |
| `postcode` | integer | Postal code |
| `city` | string | City or municipality |
| `province` | string | Belgian province |
| `address` | string or `null` | Property address |
| `latitude` | float | Latitude coordinate |
| `longitude` | float | Longitude coordinate |
| `price` | integer | Sale price in euros |
| `property_state` | string or `null` | Property condition (e.g., good, to renovate) |
| `build_year` | integer or `null` | Construction year |
| `bedroom_count` | integer | Number of bedrooms |
| `livable_surface` | integer | Livable surface in square meters |
| `total_surface` | integer or `null` | Total land surface in square meters |
| `garage` | integer | `1` if a garage exists, `0` if not |
| `terrace` | integer | `1` if a terrace exists, `0` if not |
| `energy_consumption_kwh/m2/year` | integer or `null` | Energy consumption index |
| `swimming_pool` | integer | `1` if a swimming pool exists, `0` if not |
| `preschool_distance_m` | integer | Distance to the nearest preschool in meters |
| `train_station_distance_m` | integer | Distance to the nearest train station in meters |
| `supermarket_distance_m` | integer | Distance to the nearest supermarket in meters |
| `nearest_city` | string | Name of the nearest major city |
| `nearest_city_distance_km` | float | Distance to the nearest major city in kilometers |
| `price_per_m2` | integer | Price per square meter (€/m²) |

*Note: All columns are structured in lower_case. Missing or blank values are strictly set to `null` or `NaN` during the cleaning phase.*