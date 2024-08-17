import sqlite3
import os

def store_data_in_db():
    current_directory = os.path.dirname(__file__)
    output_directory = os.path.join(current_directory, '../data/output')
    db_path = os.path.join(current_directory, '../data/database/fantasy.db')

    combined_data_path = os.path.join(output_directory, 'combined.txt')

    #Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #Create table if it doesn't exist
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS fantasy_data (
            Season TEXT,
            Name TEXT,
            Team TEXT,
            Position TEXT,
            Cost REAL,
            Season_Cost_Change REAL,
            Start_Cost REAL,
            Points REAL,
            Points_Per_Game REAL,
            Minutes_Played INTEGER,
            Goals_Scored INTEGER,
            Goals_Conceded INTEGER,
            Assists INTEGER,
            Clean_Sheets INTEGER,
            Saves INTEGER,
            Penalties_Saved INTEGER,
            Yellow_Cards INTEGER,
            Red_Cards INTEGER
        )
        '''
    )

    with open(combined_data_path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            cursor.execute('''INSERT INTO fantasy_data VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                           line.strip().split(','))
            
    conn.commit()
    conn.close()

if __name__ == '__main__':
    store_data_in_db()