import os
import glob
from data_processing import load_and_process_data

def main():
    """
    Finds all grade Excel files, applies the standard cleaning process,
    and saves the cleaned data as CSV files in a new directory.
    """
    # --- 1. Define Paths ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Directory containing the raw Excel files
    raw_data_dir = os.path.join(script_dir, 'OneDrive_2025-11-25/National Assessment Results/Results- Raw Data')
    
    # Directory where cleaned CSV files will be saved
    processed_data_dir = os.path.join(script_dir, 'processed_data')
    
    # Create the output directory if it doesn't exist
    os.makedirs(processed_data_dir, exist_ok=True)
    print(f"Cleaned files will be saved in: {processed_data_dir}")

    # --- 2. Find all Excel files to process ---
    # This looks for any file ending with .xlsx in the raw_data_dir
    files_to_process = glob.glob(os.path.join(raw_data_dir, '*.xlsx'))

    if not files_to_process:
        print(f"No Excel files found in {raw_data_dir}. Please check the path.")
        return

    print(f"Found {len(files_to_process)} files to process.")

    # --- 3. Loop through and process each file ---
    for file_path in files_to_process:
        filename = os.path.basename(file_path)
        print(f"\n--- Processing: {filename} ---")

        # We assume the sheet name is 'En - written' for all files.
        # This can be changed if needed.
        sheet_name = 'En - written'
        
        processed_data, _ = load_and_process_data(file_path, sheet_name=sheet_name)

        # If processing was successful, save the cleaned data
        if processed_data is not None and not processed_data.empty:
            # Create a new filename for the output CSV
            output_filename = os.path.splitext(filename)[0] + '_cleaned.csv'
            output_path = os.path.join(processed_data_dir, output_filename)
            
            # Save the DataFrame to a CSV file, without the pandas index
            processed_data.to_csv(output_path, index=False)
            print(f"Successfully cleaned and saved data to {output_path}")
        else:
            print(f"Skipping save for {filename} due to processing error or empty data.")

if __name__ == '__main__':
    main()