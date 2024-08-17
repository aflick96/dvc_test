import pandas as pd
import os
import argparse
import json
import sqlite3

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

def read_data():
    current_directory = os.path.dirname(__file__)
    output_directory = os.path.join(current_directory, '../data/database/fantasy.db')

    conn = sqlite3.connect(output_directory)

    # Read data from the database
    try:
        df = pd.read_sql_query('SELECT * FROM fantasy_data', conn)
    finally:
        conn.close()

    return df

def prepare_data(df):
    x = df.drop(columns=['Points', 'Name'])
    y = df['Points']

    numerical_features = ['Cost', 'Season_Cost_Change', 'Start_Cost', 'Points_Per_Game', 'Minutes_Played', 'Goals_Scored', 'Goals_Conceded', 'Assists', 'Clean_Sheets', 'Saves', 'Penalties_Saved', 'Yellow_Cards', 'Red_Cards']
    categorical_features = ['Season', 'Team', 'Position']
 
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(), categorical_features)
        ])
    return x, y, preprocessor

def build_and_tune_model(x_train, y_train, preprocessor, model, parameter_grid):
    model_pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', model)])
    grid_search = GridSearchCV(model_pipeline, parameter_grid, cv=5, scoring='neg_mean_squared_error')
    grid_search.fit(x_train, y_train)
    best_model = grid_search.best_estimator_
    return best_model, grid_search.best_params_

def compare_models(x, y, preprocessor, model_configs):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model_results = {}

    for name, (model, parameter_grid) in model_configs.items():
        best_model, best_params = build_and_tune_model(x_train, y_train, preprocessor, model, parameter_grid)
        y_pred = best_model.predict(x_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        model_results[name] = {'best_model': best_model, 'best_params': best_params, 'mse': mse, 'r2': r2}
    
    return model_results

def export_model(model, model_name):
    current_directory = os.path.dirname(__file__)
    output_directory = os.path.join(current_directory, '../data/model_output')
    joblib.dump(model, os.path.join(output_directory, f'{model_name}.pkl'))

def parse_model_configs(args):
    model_configs = {}

    if args.linear:
        model_configs['Linear'] = (LinearRegression(), {})

    if args.ridge:
        model_configs['Ridge'] = (Ridge(), {'regressor__alpha': args.ridge_alpha, 'regressor__solver': args.ridge_solver})

    if args.lasso:
        model_configs['Lasso'] = (Lasso(), {'regressor__alpha': args.lasso_alpha})

    if args.random_forest:
        model_configs['RandomForest'] = (RandomForestRegressor(), {'regressor__n_estimators': args.rf_estimators, 'regressor__max_depth': args.rf_max_depth})

    return model_configs

def save_model_parameters(parameters, output_name):
    current_directory = os.path.dirname(__file__)
    output_directory = os.path.join(current_directory, '../data/model_output')
    with open(os.path.join(output_directory, f'{output_name}.json'), 'w') as f:
        json.dump(parameters, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--linear', action='store_true')
    parser.add_argument('--ridge', action='store_true')
    parser.add_argument('--lasso', action='store_true')
    parser.add_argument('--random-forest', action='store_true')

    parser.add_argument('--ridge-alpha', nargs='+', type=float, default=[0.1, 1.0, 10.0, 100.0])
    parser.add_argument('--ridge-solver', nargs='+', default=['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga'])

    parser.add_argument('--lasso-alpha', nargs='+', type=float, default=[0.1, 1.0, 10.0])

    parser.add_argument('--rf-estimators', nargs='+', type=int, default=[10, 50, 100])
    parser.add_argument('--rf-max-depth', nargs='+', type=int, default=[None, 10, 20, 30])

    parser.add_argument('--output_params', type=str, required=True)

    args = parser.parse_args()

    model_configs = parse_model_configs(args)

    data_set = read_data()
    x, y, preprocessor = prepare_data(data_set)

    results = compare_models(x, y, preprocessor, model_configs)

    parameters_to_save = {name: results[name]['best_params'] for name in results}
    save_model_parameters(parameters_to_save, args.output_params)

    best_model_name = max(results, key=lambda x: results[x]['r2'])
    best_model = results[best_model_name]['best_model']
    export_model(best_model, best_model_name)
    