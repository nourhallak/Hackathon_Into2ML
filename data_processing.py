import pandas as pd

def load_and_process_data(file_path, sheet_name):
    """
    Loads and processes grade data from a specific sheet in an Excel file.

    Processing steps:
    1. Skips the first 2 rows and uses the 3rd as the header.
    2. Removes the first 6 columns.
    3. Renames the last column to 'My Feeling'.
    4. Converts grade columns to numeric types.
    5. Drops rows with invalid grade entries.
    6. Calculates 'Total Grade' by summing the grade columns.

    Args:
        file_path (str): The path to the Excel file.
        sheet_name (str): The name of the sheet to load.

    Returns:
        tuple: A tuple containing:
            - pd.DataFrame: The processed DataFrame.
            - str: The name of the feeling column ('My Feeling').
    """
    try:
        # --- 1. Load the Data ---
        # We skip the first 2 rows and use the 3rd row (index 2) as the header.
        data = pd.read_excel(file_path, sheet_name=sheet_name, header=2)

        # --- 2. Pre-process the DataFrame ---
        # Remove the first 6 columns
        if data.shape[1] > 6:
            data = data.iloc[:, 6:]
            print(f"Removed first 6 columns. New data shape: {data.shape}")
        else:
            print("Warning: Data has 6 or fewer columns, so no columns were removed.")

        if data.empty:
            print("The data is empty after initial processing.")
            return pd.DataFrame(), None

        # Identify the last column as 'feeling' and give it a consistent name.
        feeling_col_original_name = data.columns[-1]
        feeling_col_new_name = 'My Feeling'
        data.rename(columns={feeling_col_original_name: feeling_col_new_name}, inplace=True)
        print(f"Identified '{feeling_col_original_name}' as the feeling column, renamed to '{feeling_col_new_name}'.")

        # --- 3. Clean 'My Feeling' column ---
        # Ensure the column is of string type to use string operations
        data[feeling_col_new_name] = data[feeling_col_new_name].astype(str)

        # Replace 'nan' strings and hyphens with '0' before other processing
        data[feeling_col_new_name].replace({'nan': 'F', '-': 'F', '0':'F'}, inplace=True)
        print("Replaced 'nan' and '-' with 'F' in 'My Feeling' column.")


        # Define a mapping for Arabic character to English character transliteration
        arabic_to_english_char_map = {
            'أ': 'A', 'ا': 'A', 'ب': 'B', 'ج': 'C', 'د': 'D',
            'ه': 'E', 'و': 'F' # Replace spaces with underscores for cleaner labels
        }

        # Apply the character-by-character replacement
        for arabic_char, eng_char in arabic_to_english_char_map.items():
            data[feeling_col_new_name] = data[feeling_col_new_name].str.replace(arabic_char, eng_char)

        # Replace all lowercase 'a' with uppercase 'A'
        data[feeling_col_new_name] = data[feeling_col_new_name].str.replace('a', 'A')
        data[feeling_col_new_name] = data[feeling_col_new_name].str.replace('b', 'B')
        data[feeling_col_new_name] = data[feeling_col_new_name].str.replace('c', 'C')
        data[feeling_col_new_name] = data[feeling_col_new_name].str.replace('d', 'D')
        data[feeling_col_new_name] = data[feeling_col_new_name].str.replace('e', 'E')
        data[feeling_col_new_name] = data[feeling_col_new_name].str.replace('f', 'F')


        print("Cleaned 'My Feeling' column: Transliterated Arabic characters and replaced 'a' with 'A'.")

        grade_cols = data.columns[:-1]
        for col in grade_cols:
            data[col] = pd.to_numeric(data[col], errors='coerce')

        # Instead of dropping rows with non-numeric grades, fill them with 0.
        # This prevents the entire DataFrame from being deleted if there are bad entries.
        data[grade_cols] = data[grade_cols].fillna(0)
        print(f"Filled non-numeric grade values with 0. Data shape is now: {data.shape}")
        data['Total Grade'] = data[grade_cols].sum(axis=1)

        return data, feeling_col_new_name

    except FileNotFoundError:
        print(f"Error: The file was not found at {file_path}")
        return None, None
    except Exception as e:
        print(f"An error occurred during data processing: {e}")
        return None, None