import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

def read_data(file):
    current_directory = os.path.dirname(__file__)
    output_directory = os.path.join(current_directory, '../data/output')
    file = os.path.join(output_directory, file)
    return pd.read_csv(file)

def prepare_data(df):
    x = df.drop(columns=['Points', 'Name'])
    y = df['Points']

    numerical_features = ['Cost', 'Season Cost Change', 'Start Cost', 'Points Per Game', 'Minutes Played', 'Goals Scored', 'Goals Conceded', 'Assists', 'Clean Sheets', 'Saves', 'Penalties Saved', 'Yellow Cards', 'Red Cards']
    categorical_features = ['Season', 'Team', 'Position']
 
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(), categorical_features)
        ])
    return x, y, preprocessor

def build_and_evaluate_model(x, y, preprocessor):
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Create a pipeline
    model = Pipeline(steps=[('preprocessor', preprocessor),
                            ('regressor', LinearRegression())])

    # Train the model
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Squared Error: {mse}")
    print(f"R^2 Score: {r2}")

    return model
    

def export_model(model):
    current_directory = os.path.dirname(__file__)
    output_directory = os.path.join(current_directory, '../data/model_output')
    joblib.dump(model, os.path.join(output_directory, 'model.pkl'))

if __name__ == '__main__':
    data_set = read_data('combined.csv')
    x, y, preprocessor = prepare_data(data_set)
    model = build_and_evaluate_model(x, y, preprocessor)
    export_model(model)
    