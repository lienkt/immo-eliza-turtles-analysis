#IMPORTS :
from src import dataframe_cleaner
import pandas as pd


def main():
    raw_df = pd.read_json("./data/raw/dataframe.json")
    #Cleaning process
    df = dataframe_cleaner(raw_df)


    #output_file


    #Graphs

    #we call the functions imported from different files, each function creates a graph starting from the df and saves it in the output_file


    #fct_graph1(df, output_file)
    #fct_graph2(df, output_file)
    #fct_graph3(df, output_file)
    #fct_graph4(df, output_file)
    #fct_graph5(df, output_file)
    #fct_graph6(df, output_file)
    #fct_graph7(df, output_file)
    #fct_graph8(df, output_file)


    pass


if __name__ == "__main__":
    main()