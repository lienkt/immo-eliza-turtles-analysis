from src import export_most_least_expensive_municipalities_regions_report, dataframe_cleaner
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
  raw_df = pd.read_json(raw_dataframe_filepath)
  #Cleaning process
  df = dataframe_cleaner(raw_df)
  

# ---------------------------------------
# Choose URL source mode
# ---------------------------------------
  print("\n=== Choose report ===")
  print("1. Report name...")
  print("2. Report name...")
  print("3. Report name...")
  print("4. Report name...")
  print("5. Most & least expensive municipalities/regions")


  while True:
    option = input("Choose an option: ")

    if option == "1":
        print("Report is generating")
        break

    elif option == "2":
        print("Report is generating")
        break
    
    elif option == "3":
        print("Report is generating")
        break
    
    elif option == "4":
        print("Report is generating")
        break
    
    elif option == "5":
        print("Report is generating")

        output_picture_filepath = os.path.join(base_dir, "./images/most_least_expensive_municipalities_regions.png")
        output_report_filepath = os.path.join(base_dir, "./reports/most_least_expensive_municipalities_regions.pdf")
        export_most_least_expensive_municipalities_regions_report(clean_dataframe_filepath, output_picture_filepath, output_report_filepath)
        break

    else:
        print("Options are 1 to 5. Please choose again.")
         


# ---------------------------------------
# Program entry point
# ---------------------------------------
if __name__ == "__main__":
    main()