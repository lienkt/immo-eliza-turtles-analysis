from src import export_most_least_expensive_municipalities_regions_report, dataframe_cleaner, correlations_matrix, price_vs_property_states, inventory_by_province, surface_distribution, make_outlier_graph, make_build_year_price_m2_graph
import pandas as pd
import os

def main():
    """

    """

    # ---------------------------------------
    # Load configuration file
    # ---------------------------------------
    # Get project base directory
    base_dir = os.path.dirname(__file__)
    clean_dataframe_filepath = os.path.join(base_dir, "./data/cleaned/clean_dataframe.json")
    raw_dataframe_filepath = os.path.join(base_dir, "./data/raw/dataframe.json")

    # ---------------------------------------
    # Cleaning process
    # ---------------------------------------
    raw_df = pd.read_json(raw_dataframe_filepath)
    df = dataframe_cleaner(raw_df, clean_dataframe_filepath)

    # ---------------------------------------
    # Colour palette we'll reuse 
    # ---------------------------------------
    BLUE   = '#2166ac'
    ORANGE = '#d6604d'
    GREEN  = '#4dac26'
    GREY   = '#878787'
    PALETTE = [BLUE, ORANGE, GREEN, '#9970ab', '#bf812d']

    # ---------------------------------------
    # Choose URL source mode
    # ---------------------------------------
    print("\n=== Choose report ===")
    print("'1' : Most common outlier")
    print("'2' : Build year vs price")
    print("'3' : Correlation matrix")
    print("'4' : Price/m2 vs property states")
    print("'5' : Nb of Houses vs Apartments by Regions")
    print("'6' : Distribution of properties vs surface")
    print("'7' : Most & least expensive municipalities/regions")
    print("'8' : To exit")


    while True:
        option = input("Choose an option: ")

        if option == "1":
            print("Report is generating")
            make_outlier_graph(df, base_dir)

        elif option == "2":
            print("Report is generating")
            make_build_year_price_m2_graph(df, base_dir)

        elif option == "3":
            print("Report is generating")
            correlations_matrix(df, base_dir)

        elif option == "4":
            print("Report is generating")
            price_vs_property_states(df, base_dir, PALETTE)

        elif option == "5":
            print("Report is generating")
            inventory_by_province(df, base_dir)

        elif option == "6":
            print("Report is generating")
            surface_distribution(df, base_dir)

        elif option == "7":
            print("Report is generating")
            export_most_least_expensive_municipalities_regions_report(clean_dataframe_filepath, base_dir)
        
        elif option == "8":
            break
        else:
            print("Options are 1 to 8. Please choose again.")
         


# ---------------------------------------
# Program entry point
# ---------------------------------------
if __name__ == "__main__":
    main()
