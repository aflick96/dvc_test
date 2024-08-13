import os
import joblib
import pandas as pd

def load_model():
    # Define the path to the saved model
    current_directory = os.path.dirname(__file__)
    model_path = os.path.join(current_directory, '../data/model_output/model.pkl')
    
    # Load the model
    model = joblib.load(model_path)
    return model

def prepare_input_data(data):
    # This function should prepare the input data in the same way the training data was prepared
    # For demonstration, let's assume we are given a dictionary that needs conversion to a DataFrame
    df = pd.DataFrame([data])
    
    # Make sure the data is consistent with what the model expects (e.g., correct columns, one-hot encoding if needed)
    return df

def predict(data):
    # Load the model
    model = load_model()
    
    # Prepare the data
    df = prepare_input_data(data)
    
    # Predict using the model
    prediction = model.predict(df)
    return prediction

if __name__ == '__main__':
    # Example input data
    new_data = {
        'Season': '2023-2024',
        'Team': 'ARS',
        'Position': 'FWD',
        'Cost': 7,
        'Season Cost Change': -0.1,
        'Start Cost': 6.9,
        'Points Per Game': 0.5,
        'Minutes Played': 300,
        'Goals Scored': 10,
        'Goals Conceded': 0,
        'Assists': 13,
        'Clean Sheets': 1,
        'Saves': 0,
        'Penalties Saved': 0,
        'Yellow Cards': 0,
        'Red Cards': 0
    }

    # Make prediction
    prediction = predict(new_data)
    print(f"Predicted Points: {prediction[0]}")
