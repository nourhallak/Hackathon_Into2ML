import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def main():
    """
    Loads cleaned grade data, trains a model to predict 'My Feeling' based on grades,
    and evaluates the model's performance.
    """
    # --- 1. Load Cleaned Data ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the cleaned data file (we'll use Grade 4 as an example)
    cleaned_data_path = os.path.join(script_dir, 'processed_data', 'Grade_4_cleaned.csv')

    try:
        data = pd.read_csv(cleaned_data_path)
        print(f"Successfully loaded cleaned data from: {cleaned_data_path}")
    except FileNotFoundError:
        print(f"Error: Cleaned data file not found at {cleaned_data_path}")
        print("Please run 'batch_process_grades.py' first to generate the cleaned data.")
        return

    # --- 2. Prepare Data for Modeling ---
    # Define the target categories we want to predict
    target_categories = ['A', 'B', 'C', 'D', 'E', 'F']
    data = data[data['My Feeling'].isin(target_categories)]

    if data.empty:
        print("The dataset is empty after filtering for categories A-F. Cannot proceed.")
        return

    # Define features (X) and target (y)
    # Features are all columns except 'My Feeling'
    X = data.drop('My Feeling', axis=1)
    y = data['My Feeling']

    print(f"Features (X) shape: {X.shape}")
    print(f"Target (y) shape: {y.shape}")

    # --- 3. Split Data into Training and Testing Sets ---
    # We'll use 80% of the data for training and 20% for testing.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training set size: {len(X_train)}, Test set size: {len(X_test)}")

    # --- 4. Train a Classification Model ---
    print("\nTraining a RandomForestClassifier...")
    # n_estimators is the number of trees in the forest.
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print("Model training complete.")

    # --- 5. Evaluate the Model ---
    print("\n--- Model Evaluation ---")
    # Make predictions on the test data
    y_pred = model.predict(X_test)

    # Calculate and print accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2%}")

    # Print a detailed classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, labels=target_categories))

    # Display a confusion matrix to see where the model gets confused
    print("Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred, labels=target_categories)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=target_categories, yticklabels=target_categories)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title('Confusion Matrix')
    plt.show()

if __name__ == '__main__':
    main()