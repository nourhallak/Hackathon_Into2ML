import matplotlib.pyplot as plt
import seaborn as sns
import os
from data_processing import load_and_process_data

def plot_grades_vs_feeling(data, feeling_col_name):
    """
    Plots the distribution of total grades against the feeling.

    Args:
        data (pd.DataFrame): The processed DataFrame with 'Total Grade' and feeling columns.
        feeling_col_name (str): The name of the column containing the feeling data.
    """
    if data.empty:
        print("Cannot plot because the data is empty.")
        return

    # Define the desired categories and their order
    plot_order = ['A', 'B', 'C', 'D', 'E', 'F']

    # Filter the data to include only the specified categories
    filtered_data = data[data[feeling_col_name].isin(plot_order)]
    print(f"Filtered data for plotting. Kept categories: {plot_order}. New shape: {filtered_data.shape}")

    # --- 3. Plot the Data ---
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(10, 6))

    # A boxplot is great for showing distribution of a numeric value (Total Grade)
    # across different categories (Feeling).
    sns.boxplot(x=feeling_col_name, y='Total Grade', data=filtered_data, order=plot_order)

    # Add titles and labels for clarity
    plt.title('Distribution of Total Grades by Feeling', fontsize=16)
    plt.xlabel(feeling_col_name, fontsize=12)
    plt.ylabel('Sum of Grades', fontsize=12)
    plt.xticks(rotation=45) # Rotate x-axis labels if they are long
    plt.tight_layout() # Adjust layout to make room for labels

    # Show the plot
    plt.show()


if __name__ == '__main__':
    # Get the directory where the script is located.
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the data file.
    # This assumes the 'rawdata' directory is in the same directory as the script.
    file_path = os.path.join(script_dir, 'OneDrive_2025-11-25/National Assessment Results/Results- Raw Data', 'Grade_4.xlsx')

    # Load and process the data using the dedicated function
    processed_data, feeling_column = load_and_process_data(file_path, sheet_name='En - written')

    # Plot the processed data
    if not processed_data.empty:
        plot_grades_vs_feeling(processed_data, feeling_column)
