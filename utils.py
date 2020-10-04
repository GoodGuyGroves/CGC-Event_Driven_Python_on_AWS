"""Utility functions for operating with CSV data"""
import pandas as pd
import numpy as np


def load_csv(url) -> pd.DataFrame:
    """Loads a CSV from a URL into a Pandas DataFrame"""
    df = pd.read_csv(url, index_col=None)
    return df


def convert_date(df: pd.DataFrame, date_column="date") -> pd.DataFrame:
    """Converts all date strings into datetime objects"""
    df[date_column] = pd.to_datetime(df[date_column], format="%Y-%m-%d")
    return df


def filter_criteria(df: pd.DataFrame, column_name, row_value) -> pd.DataFrame:
    """Filters out rows containing row_value"""
    return df.loc[df[column_name] == row_value]


def find_new(cur_data: pd.DataFrame, new_data: pd.DataFrame) -> pd.DataFrame:
    """Takes in two Pandas DataFrames, finds which rows exist only in the
    'right' dataframe and returns those rows only as a new DataFrame"""
    return new_data[np.equal(new_data.date.isin(cur_data.date), False)]


def merge_df(
    left_df: pd.DataFrame, right_df: pd.DataFrame, right_cols: list, left_on, right_on
) -> pd.DataFrame:
    """Merges two DataFrames"""
    merged_df = pd.merge(
        left_df, right_df[right_cols], left_on=left_on, right_on=right_on, how="left"
    )
    return merged_df


def remove_column(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """Removes a column from a DataFrame"""
    del df[col_name]
    return df


def lowercase_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Changes all column names to lowercase"""
    df.columns = map(str.lower, df.columns)
    return df
