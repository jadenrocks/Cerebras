import requests

API_KEY = 'listed_jaden_key'
API_URL = 'https://api.cerebras.ai/inference'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

def fetch_player_data(player_name):
    query = {
        'query': player_name,
        'task': 'text-generation',
        'temperature': 0.7
    }
    response = requests.post(API_URL, headers=headers, json=query)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data:", response.status_code)
        return None
