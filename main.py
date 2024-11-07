import pandas as pd
import numpy as np
import streamlit as st
from sklearn.linear_model import LinearRegression
from cerebras_api import fetch_player_data

def parse_player_data(data):
    player_stats = {
        'name': data.get('name'),
        'points_per_game': data.get('points'),
        'assists_per_game': data.get('assists'),
        'rebounds_per_game': data.get('rebounds')
    }
    return player_stats

def train_performance_model(player_stats_df):
    X = player_stats_df[['points_per_game', 'assists_per_game', 'rebounds_per_game']].values
    y = player_stats_df['performance_index']
    model = LinearRegression()
    model.fit(X, y)
    return model

def interactive_dashboard(player_stats_df):
    st.title("Player Performance Analytics")
    player_name = st.selectbox("Choose Player", player_stats_df['name'].unique())
    player_data = player_stats_df[player_stats_df['name'] == player_name]
    st.write("Player Stats")
    st.write(player_data)
    st.write("Performance Projection")
    model = train_performance_model(player_stats_df)
    performance_projection = model.predict(player_data[['points_per_game', 'assists_per_game', 'rebounds_per_game']])
    st.write("Projected Performance Index:", performance_projection[0])

if __name__ == "__main__":
    player_name = "Sample Player"
    raw_data = fetch_player_data(player_name)
    if raw_data:
        player_stats = parse_player_data(raw_data)
        player_stats_df = pd.DataFrame([player_stats])
        interactive_dashboard(player_stats_df)
    else:
        print("No data retrieved for the player.")