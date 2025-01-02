import pandas as pd
import numpy as np
import streamlit as st
from sklearn.linear_model import LinearRegression
from cerebras_api import fetch_with_retry

def parse_player_data(data):
    """Parses raw player data into structured statistics."""
    return {
        'name': data.get('name', 'Unknown Player'),
        'points_per_game': data.get('points', np.nan),
        'assists_per_game': data.get('assists', np.nan),
        'rebounds_per_game': data.get('rebounds', np.nan),
        'performance_index': data.get('performance_index', np.nan)  # New metric
    }

def train_performance_model(player_stats_df):
    """Trains a linear regression model on player stats."""
    X = player_stats_df[['points_per_game', 'assists_per_game', 'rebounds_per_game']].values
    y = player_stats_df['performance_index'].fillna(0)
    model = LinearRegression()
    model.fit(X, y)
    return model

def interactive_dashboard(player_stats_df):
    """Displays an interactive dashboard using Streamlit."""
    st.title("Player Performance Analytics")

    # Player selection and details
    player_name = st.selectbox("Choose Player", player_stats_df['name'].unique())
    player_data = player_stats_df[player_stats_df['name'] == player_name]
    st.write("### Player Stats")
    st.dataframe(player_data)

    # Performance projection
    st.write("### Performance Projection")
    model = train_performance_model(player_stats_df)
    if not player_data.empty:
        performance_projection = model.predict(player_data[['points_per_game', 'assists_per_game', 'rebounds_per_game']])
        st.write(f"Projected Performance Index: {performance_projection[0]:.2f}")
    else:
        st.write("No data available for the selected player.")

if __name__ == "__main__":
    st.sidebar.title("Options")
    player_names = st.sidebar.text_area("Enter Player Names (comma-separated):", "Player1, Player2").split(',')
    player_stats_list = [parse_player_data(fetch_with_retry(player.strip())) for player in player_names]

    # Convert to DataFrame
    player_stats_df = pd.DataFrame(player_stats_list).dropna()
    if not player_stats_df.empty:
        interactive_dashboard(player_stats_df)
    else:
        st.write("No data available.")
