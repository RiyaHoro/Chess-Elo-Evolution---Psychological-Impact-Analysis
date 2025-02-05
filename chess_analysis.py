import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV
df = pd.read_csv('chess_games.csv')

# ------------------------- Basic Analysis -------------------------
# Calculate Win/Loss ratio
wins = len(df[df['Result'] == 'win'])
losses = len(df[df['Result'] == 'loss'])
draws = len(df[df['Result'] == 'draw'])
total_games = len(df)

win_loss_ratio = wins / losses if losses != 0 else wins  # Avoid division by zero

# Average Elo Rating for White and Black
average_elo_white = df['Elo White'].mean()
average_elo_black = df['Elo Black'].mean()

# Print the basic results
print(f"Total Games: {total_games}")
print(f"Wins: {wins} | Losses: {losses} | Draws: {draws}")
print(f"Win/Loss Ratio: {win_loss_ratio:.2f}")
print(f"Average Elo (White): {average_elo_white:.2f}")
print(f"Average Elo (Black): {average_elo_black:.2f}")


# ------------------------- Winning and Losing Streaks -------------------------
df['Streak'] = df['Result'].apply(lambda x: 1 if x == 'win' else -1 if x == 'loss' else 0)
df['Streak ID'] = (df['Streak'] != df['Streak'].shift()).cumsum()
df['Streak Length'] = df.groupby('Streak ID')['Streak'].transform('size')

# Filter out only the winning and losing streaks
winning_streaks = df[df['Streak'] == 1]['Streak Length']
losing_streaks = df[df['Streak'] == -1]['Streak Length']

# Get the longest winning and losing streak
longest_winning_streak = winning_streaks.max()
longest_losing_streak = losing_streaks.max()

print(f"Longest Winning Streak: {longest_winning_streak} games")
print(f"Longest Losing Streak: {longest_losing_streak} games")


# ------------------------- Impact of Time Control -------------------------
time_control_performance = df.groupby('Time Control')['Result'].value_counts(normalize=True).unstack().fillna(0)

# Plot the results for Time Control Performance
time_control_performance.plot(kind='bar', stacked=True, figsize=(10,6))
plt.title('Performance by Time Control')
plt.xlabel('Time Control')
plt.ylabel('Win Rate')
plt.xticks(rotation=45)
plt.show()


# ------------------------- Monthly Elo Rating Trends -------------------------
# Convert the Date column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

df['Year-Month'] = df['Date'].dt.to_period('M')

elo_monthly_trend = df.groupby('Year-Month')[['Elo White', 'Elo Black']].mean()

# Plot Elo trends for Monthly Elo Ratings
plt.figure(figsize=(10,6))
plt.plot(elo_monthly_trend.index.astype(str), elo_monthly_trend['Elo White'], label='White Elo')
plt.plot(elo_monthly_trend.index.astype(str), elo_monthly_trend['Elo Black'], label='Black Elo')
plt.title('Monthly Elo Rating Trends')
plt.xlabel('Month')
plt.ylabel('Average Elo Rating')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
#---------------------------------------
# Calculate the change in Elo between consecutive games (for both white and black)
df['Elo Change White'] = df['Elo White'].diff().fillna(0)
df['Elo Change Black'] = df['Elo Black'].diff().fillna(0)

# You can also calculate overall Elo change for the game by considering whether you played as white or black
# Assign Elo change based on the color (White or Black)
df['Elo Change'] = df.apply(lambda row: row['Elo Change White'] if row['Elo White'] != 0 else row['Elo Change Black'], axis=1)

# Plot the Elo change over time (to see patterns)
plt.figure(figsize=(10,6))
plt.plot(df['Date'], df['Elo Change'], label="Elo Change")
plt.title('Elo Change Per Game')
plt.xlabel('Date')
plt.ylabel('Elo Change')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#-----------------------------------------------
# Identify streaks and their lengths (as done earlier)
df['Streak'] = df['Result'].apply(lambda x: 1 if x == 'win' else -1 if x == 'loss' else 0)
df['Streak ID'] = (df['Streak'] != df['Streak'].shift()).cumsum()
df['Streak Length'] = df.groupby('Streak ID')['Streak'].transform('size')

# Identify if the next game is part of a winning or losing streak
df['Next Streak'] = df['Streak'].shift(-1)
df['Next Streak Result'] = df['Next Streak'].apply(lambda x: "Win" if x == 1 else "Loss" if x == -1 else "Neutral")

# Track how your performance changes after winning and losing streaks
performance_after_streaks = df.groupby('Next Streak Result')['Result'].value_counts(normalize=True).unstack().fillna(0)

# Plot the results
performance_after_streaks.plot(kind='bar', stacked=True, figsize=(10,6))
plt.title('Performance After Winning and Losing Streaks')
plt.xlabel('Next Streak Result')
plt.ylabel('Win Rate')
plt.xticks(rotation=45)
plt.show()
#-----------------------------------------------------
# Group by Time Control and track average Elo changes
time_control_elo_change = df.groupby('Time Control').agg(
    avg_elo_white_change=('Elo White', 'mean'),
    avg_elo_black_change=('Elo Black', 'mean'),
    avg_elo_change=('Elo Change', 'mean')
)

# Plot the results
time_control_elo_change.plot(kind='bar', figsize=(10,6))
plt.title('Elo Change by Time Control')
plt.xlabel('Time Control')
plt.ylabel('Average Elo Change')
plt.xticks(rotation=45)
plt.show()
