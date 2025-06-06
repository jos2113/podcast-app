from flask import Flask, jsonify
from flask_cors import CORS  # Importing CORS for handling cross-origin requests
import pandas as pd

app = Flask(__name__)  # Instantiating the Flask app

# Enable CORS
CORS(app)  # This allows all domains to access the Flask API

# Path to your Excel file
file_path = 'C:/Users/USER/podcast-app/Categorized_Podcasts.xlsx'

def categorize_podcast(row):
    if row['is_matched'] == 1 and row['Apple_found'] == 0:
        return 'Database Podcasts', None, None
    elif row['is_matched'] == 0 and row['Apple_found'] == 0:
        return 'Spotify Exclusive Podcasts', row['spotify_url'], None
    elif row['is_matched'] == 0 and row['Apple_found'] == 1:
        return 'Podcasts present on Apple', None, row['Found_url']
    else:
        return 'Others', None, None

@app.route('/api/get-podcasts', methods=['GET'])
def get_podcasts():
    # Load data from Excel file
    df = pd.read_excel(file_path, sheet_name='Categorized_Podcasts', engine='openpyxl')
    df[['Category', 'Spotify_Link', 'Apple_Link']] = df.apply(categorize_podcast, axis=1, result_type="expand")
    podcasts = df[['id', 'title', 'Category', 'Spotify_Link', 'Apple_Link']].to_dict(orient='records')
    return jsonify(podcasts)

if __name__ == '__main__':
    app.run(debug=True)
