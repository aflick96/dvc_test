import os
import json

def extract_text_from_raw():
    current_directory = os.path.dirname(__file__)
    raw_directory = os.path.join(current_directory, '../data/raw_data')
    output_directory = os.path.join(current_directory, '../data/output')

    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    processed_data_path = os.path.join(output_directory, 'combined.txt')

    with open(processed_data_path, 'w', encoding='utf-8') as out:
        for filename in os.listdir(raw_directory):
            # Read season data
            file = os.path.join(raw_directory, filename)
            season = filename.split('.')[0]

            with open(file, 'r') as f:
                data = json.load(f)
                # Write player data to output file
                for player_hist in data['history']:
                    out.write(f"{season},{player_hist['first_name']} {player_hist['second_name']},{player_hist['team_name']},{player_hist['position']},{player_hist['now_cost']},{player_hist['cost_change_start']/10},{player_hist['now_cost'] + (player_hist['cost_change_start']/10)},{player_hist['total_points']},{player_hist['points_per_game']},{player_hist['minutes']},{player_hist['goals_scored']},{player_hist['goals_conceded']},{player_hist['assists']},{player_hist['clean_sheets']},{player_hist['saves']},{player_hist['penalties_saved']},{player_hist['yellow_cards']},{player_hist['red_cards']}\n")
    
if __name__ == '__main__':
    extract_text_from_raw()