import requests
import os

def fetch_player_data(player_name):
    API_KEY = os.getenv("given_jadenc_key")  
    API_URL = "https://api.cerebras.ai/inference"

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    query = {
        'query': player_name,
        'task': 'text-generation',
        'temperature': 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=query)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def fetch_multiple_players(player_names):
    """Fetches data for multiple players."""
    return [fetch_player_data(player) for player in player_names]

def fetch_with_retry(player_name, retries=3):
    """Fetches player data with retry logic."""
    for attempt in range(retries):
        data = fetch_player_data(player_name)
        if data:
            return data
        print(f"Retry {attempt + 1}/{retries} failed.")
    return None


{
    "name": "Python 3",
    "features": {
        "ghcr.io/devcontainers-extra/features/coverage-py:2": {}
    },
    "postCreateCommand": "pip install -r requirements.txt",
    "forwardPorts": [8501, 5000, 5432],
    "customizations": {
        "vscode": {
            "extensions": [
                "ms-python.python",
                "ms-toolsai.jupyter",
                "donjayamanne.python-extension-pack"
            ]
        }
    },
    "settings": {
        "python.testing.unittestEnabled": true,
        "python.linting.enabled": true
    },
    "runArgs": ["--env-file", "dev.env"]
}

