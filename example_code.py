
import pandas as pd
from pathlib import Path
import os

def process_folder(folder_path, source_identifier):
    # Initialize an empty list to store DataFrames
    data_frames = []

    # Loop through all files in the folder
    for file_path in folder_path.glob('*.csv'):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Append the DataFrame to the list
        data_frames.append(df)

    # Concatenate all DataFrames into one
    combined_df = pd.concat(data_frames, ignore_index=True)

    # Remove duplicates based on the "transactionID" column
    combined_df = combined_df.drop_duplicates(subset='transactionID')

    # Add a new "source" column with the provided source identifier
    combined_df['source'] = source_identifier

    return combined_df

def create_folders_if_not_exist(folder_list):
    for folder in folder_list:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Folder '{folder}' created.")

# List of folders to create if they don't exist
folders_to_create = ['/path/to/folder1', '/path/to/folder2', '/path/to/folder3']

# Create the folders if they don't exist
create_folders_if_not_exist(folders_to_create)

# Example usage:
for folder_path in folders_to_create:
    source_id = 'YourSourceIdentifier'
    result_df = process_folder(Path(folder_path), source_id)

import pandas as pd

def compare_and_update_csv(file1_path, file2_path, key_column, output_file_path):
    """
    Compares two CSV files, adds missing rows from the first file to the second file,
    and saves the updated dataframe to a new CSV file.

    Parameters:
    file1_path (str): Path to the first CSV file.
    file2_path (str): Path to the second CSV file.
    key_column (str): The column name used as the key for comparison.
    output_file_path (str): Path where the updated CSV file will be saved.
    """

    # Read the CSV files
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)

    # Merge the two dataframes on the key column to find rows that are missing in df2
    merged_df = df1.merge(df2, on=key_column, how='left', indicator=True)

    # Filter out the rows that are only in df1 (not in df2)
    missing_rows = merged_df[merged_df['_merge'] == 'left_only']

    # Drop the merge indicator column and keep only the columns from df1
    missing_rows = missing_rows[df1.columns]

    # Append the missing rows to df2
    updated_df2 = df2.append(missing_rows, ignore_index=True)

    # Save the updated df2 to the output CSV file
    updated_df2.to_csv(output_file_path, index=False)

# Example usage
# compare_and_update_csv('file1.csv', 'file2.csv', 'id', 'updated_file2.csv')

