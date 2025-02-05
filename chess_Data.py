import requests
import pandas as pd

# Your Chess.com username
username = "riya123498"

# Custom headers to bypass Chess.com API restrictions
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Fetch the list of archived months
archive_url = f"https://api.chess.com/pub/player/{username}/games/archives"
archive_response = requests.get(archive_url, headers=headers)

# Ensure we got a successful response
if archive_response.status_code == 200:
    archive_data = archive_response.json()
    archive_urls = archive_data["archives"]  # Get all archive URLs
else:
    print(f"Error: Failed to fetch archive data. Status Code: {archive_response.status_code}")
    print("Response:", archive_response.text)
    exit()

# Initialize an empty list to store all game data
all_game_data = []

# Iterate through each archive URL
for month_url in archive_urls:
    # Fetch games for the current month
    games_response = requests.get(month_url, headers=headers)

    # Ensure we got a successful response
    if games_response.status_code == 200:
        games_data = games_response.json().get("games", [])
        # Extract relevant game details
        for game in games_data:
            game_info = {
                "Date": pd.to_datetime(game.get("end_time"), unit='s'),  # Convert to human-readable date
                "White": game["white"]["username"],
                "Black": game["black"]["username"],
                "Result": game["white"]["result"] if game["white"]["username"] == username else game["black"]["result"],
                "Elo White": game["white"].get("rating"),
                "Elo Black": game["black"].get("rating"),
                "Time Control": game.get("time_control"),
                "Game URL": game.get("url"),
            }
            all_game_data.append(game_info)
    else:
        print(f"Error: Failed to fetch game data for {month_url}. Status Code: {games_response.status_code}")
        print("Response:", games_response.text)

# Convert to DataFrame and save as CSV if game data exists
if all_game_data:
    df = pd.DataFrame(all_game_data)
    df.to_csv("chess_games.csv", index=False)
    print("✅ All game data saved as 'chess_games_all.csv'!")
else:
    print("No games found.")
