#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 15:39:45 2025

@author: satkarkarki

NCAA Hoops Analysis: Predicting Win Probability from Half-Time Leads

Date: March 2025
Tools Used: Python, Pandas, PyODBC, Matplotlib, Statsmodels

Description:
This project analyzes NCAA Men's Division I Basketball Tournament data to 
determine the probability of a team winning if they were leading at half-time. 
The process involves:

1. Connecting to an Azure SQL Database to extract game data.
2. Cleaning and transforming the data for analysis.
3. Identifying game statistics such as team performance and overtime scenarios.
4. Computing the probability of a team winning when leading at half-time.
5. Conducting exploratory data analysis (EDA) with visualizations.
6. Running an Ordinary Least Squares (OLS) regression to examine the relationship 
   between total points and winning percentage.

Outputs:
- A CSV file containing cleaned game results (`gameresults.csv`).
- Data visualizations showcasing key trends.
- Statistical insights from OLS regression.
"""



import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import statsmodels.api as sm

"""
# Database connection details
# Connection between Azure database and Spyder
server = 'ncaa-hoops.database.windows.net'
database = 'ncaa-hoops'
username = 'ncaa-hoops'
password = 'paulZachChadServer!'
driver = '{SQL Server}'

# Establish connection
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Query to retrieve table names
sql2 = '''
SELECT table_name AS Game_ID
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
ORDER BY Game_ID;
'''

data2 = pd.read_sql_query(sql2, conn)

# Filtering game tables
b0x_games = data2[data2.Game_ID.str.startswith('b0x', na=False)]
b0x_games[['Prefix', 'Number']] = b0x_games['Game_ID'].str.split('x', expand=True)

# Creating an empty dataframe for game results
df_gameresults = pd.DataFrame(columns=['index', 'GAME_ID', 'Team_Name', '1st Half', '2nd Half', '1st OT', '2nd OT', '3rd OT', 'Total'])

# Looping through game tables
for row in b0x_games.index:
    GAME_ID = b0x_games['Number'][row]
    query1 = f'b0x{GAME_ID}'
    sql1_q1 = f'SELECT * FROM {query1}'
    
    result_q1 = pd.read_sql_query(sql1_q1, conn, index_col='index')
    result_q1.at[0, '0'] = 'Team_Name'
    result_q1.columns = result_q1.iloc[0]
    result_q1.drop(result_q1.index[0], inplace=True)
    result_q1['GAME_ID'] = GAME_ID
    df_gameresults = df_gameresults._append(result_q1)

# Saving results to CSV
df_gameresults.to_csv('gameresults.csv', index=False)

# Removing rows where index value is 0
df_gameresults = df_gameresults[df_gameresults['index'] != 0]

# Processing b1X tables
df_gameinfo = pd.DataFrame()

for row in b0x_games.index:
    GAME_ID = b0x_games['Number'][row]
    query2 = f'b1x{GAME_ID}'
    sql2_q2 = f'SELECT * FROM {query2}'
    
    result_q2 = pd.read_sql_query(sql2_q2, conn)
    result_q2['GAME_ID'] = GAME_ID
    df_gameinfo = result_q2._append(df_gameinfo)

# Processing b2X tables (Officials)
df_officials = pd.DataFrame()

for row in b0x_games.index:
    GAME_ID = b0x_games['Number'][row]
    query3 = f'b2x{GAME_ID}'
    sql3_q3 = f'SELECT * FROM {query3}'
    
    try:
        result_q3 = pd.read_sql_query(sql3_q3, conn)
        result_q3['GAME_ID'] = GAME_ID
        df_officials = result_q3._append(df_officials)
    except Exception as e:
        print(f"Error occurred for GAME_ID {GAME_ID}: {e}")
"""


# Loading cleaned data
df_hoops = pd.read_csv('gameresults.csv')
df_hoops = pd.read_csv(r'/Users/satkarkarki/Desktop/Portfolio/NCAA Hoops Analysis/gameresults.csv')

# Removing missing values
cleaned_data = df_hoops.dropna(subset=['Team_Name', '1st Half', 'Total'])

# Grouping by Game_ID
grouped_games = cleaned_data.groupby('GAME_ID')

# Function to determine if the team leading at half won
def determine_winner(group):
    first_half_leader = group.iloc[0]['Team_Name'] if group.iloc[0]['1st Half'] > group.iloc[1]['1st Half'] else group.iloc[1]['Team_Name']
    game_winner = group.iloc[0]['Team_Name'] if group.iloc[0]['Total'] > group.iloc[1]['Total'] else group.iloc[1]['Team_Name']
    return first_half_leader == game_winner

# Applying function
results = grouped_games.apply(determine_winner)
probability = results.mean()

print("The probability of winning when leading at the first half is:", probability)

# Win/Loss probability
win_p, loss_p = probability, 1 - probability

# Creating probability dataframe
probabilities_df = pd.DataFrame({'Outcome': ['Win', 'Loss'], 'Probability': [win_p, loss_p]})

# Pie chart visualization
probabilities_df.plot(kind='pie', y='Probability', labels=probabilities_df['Outcome'], autopct='%1.1f%%')
plt.axis('equal')
plt.title('Win vs Loss Probability for 1st Half Leaders')
plt.show()

# Cleaning team names
def clean_team_name(name):
    record_start = name.find('(')
    if record_start != -1:
        name = name[:record_start].strip()
    if '#' in name:
        rank_end = name.find(' ')
        if rank_end != -1:
            name = name[rank_end:].strip()
    return name

df_hoops['Team_Name'] = df_hoops['Team_Name'].apply(clean_team_name)

# Summing total scores
team_scores = df_hoops.groupby('Team_Name')['Total'].sum().sort_values()

# Identifying lowest and highest scoring teams
fewest_points_team, fewest_points = team_scores.index[0], team_scores.iloc[0]
most_points_team, most_points = team_scores.index[-1], team_scores.iloc[-1]

# Bar chart comparing lowest and highest scoring teams
comparison_df = pd.DataFrame({
    'Team': [f'Fewest Points - {fewest_points_team}', f'Most Points - {most_points_team}'],
    'Total Points': [fewest_points, most_points]
})

comparison_df.plot(kind='bar', x='Team', y='Total Points', color=['red', 'green'], legend=False)
plt.title('Comparison of Total Points: Fewest vs. Most')
plt.xlabel('Team')
plt.ylabel('Total Points')
plt.show()

# Sorting to determine winners
df_hoops_sorted = df_hoops.sort_values(['GAME_ID', 'Total'], ascending=[True, False])
df_hoops_sorted['Win_Flag'] = df_hoops_sorted.groupby('GAME_ID').cumcount() == 0

# Calculating wins and games played
team_wins = df_hoops_sorted.groupby('Team_Name')['Win_Flag'].sum()
team_games = df_hoops_sorted['Team_Name'].value_counts()
winning_percentage = (team_wins / team_games) * 100

# Total points scored per team
total_points = df_hoops.groupby('Team_Name')['Total'].sum()

# Aligning total points with winning percentage
total_points_aligned = total_points.reindex(winning_percentage.index, fill_value=0)

# Creating team stats dataframe
team_stats = pd.DataFrame({
    'Team_Name': winning_percentage.index,
    'Winning_Percentage': winning_percentage.values,
    'Total_Points': total_points_aligned.values
})

# Running OLS regression
X = sm.add_constant(team_stats['Total_Points'])
y = team_stats['Winning_Percentage']
model = sm.OLS(y, X).fit()

# Printing regression summary
print(model.summary())
