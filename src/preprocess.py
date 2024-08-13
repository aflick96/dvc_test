import os
import pandas as pd
import json

def extract_text_from_raw():
    current_directory = os.path.dirname(__file__)
    raw_directory = os.path.join(current_directory, '../data/raw_data')
    output_directory = os.path.join(current_directory, '../data/output')

    data_frames = []

    for filename in os.listdir(raw_directory):
        raw_file = os.path.join(raw_directory, filename)

        data_set = []

        season = filename.split('.')[0]

        with open(raw_file, 'rb') as f:
            json_data = json.load(f)
            for player_hist in json_data['history']:
                data_set.append({
                    'Season': season,
                    'Name': player_hist['first_name'] + ' ' + player_hist['second_name'],
                    'Team': player_hist['team_name'],
                    'Position': player_hist['position'],
                    'Cost': player_hist['now_cost'],
                    'Season Cost Change': player_hist['cost_change_start']/10,
                    'Start Cost': player_hist['now_cost'] + (player_hist['cost_change_start']/10),
                    'Points': player_hist['total_points'],
                    'Points Per Game': player_hist['points_per_game'],
                    'Minutes Played': player_hist['minutes'],
                    'Goals Scored': player_hist['goals_scored'],
                    'Goals Conceded': player_hist['goals_conceded'],
                    'Assists': player_hist['assists'],
                    'Clean Sheets': player_hist['clean_sheets'],
                    'Saves': player_hist['saves'],
                    'Penalties Saved': player_hist['penalties_saved'],
                    'Yellow Cards': player_hist['yellow_cards'],
                    'Red Cards': player_hist['red_cards'],
                })
        df = pd.DataFrame(data_set)
        data_frames.append(df)
        df.to_csv(os.path.join(output_directory, filename.replace('json', 'csv')), index=False)
    df_combined = pd.concat(data_frames, ignore_index=True)
    df_combined.to_csv(os.path.join(output_directory, 'combined.csv'), index=False)

if __name__ == '__main__':
    extract_text_from_raw()