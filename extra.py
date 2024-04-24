import pandas as pd
import numpy as np
import streamlit as st
import folium
from streamlit_folium import folium_static
import plotly.graph_objects as go

def current_runrate(row):
    return row['Current_score'] * 6 / (120 - row['Ball_left'])

def req_runrate(row):
    return row['Runs_need'] * 6 / (120 - row['Ball_left'])

def win(row):
  if row['batting_team'] == row['winner']:
    return 1
  return 0

def balls_left_count(over):
   integer_part, decimal_part = divmod(float(over), 1)
   ball_count = 120 - [int(integer_part)*6 + int(decimal_part*10)][0]
   return ball_count

def India_map():
    st.title("India Map Example")
    st.write("This is an example of displaying an India map using Folium in Streamlit.")

    # Create a Folium map centered on India
    india_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

    # Add any markers, popups, or other map elements as needed
    folium.Marker([28.6139, 77.2090], popup='Delhi').add_to(india_map)
    folium.Marker([19.0760, 72.8777], popup='Mumbai').add_to(india_map)

    # Display the Folium map in Streamlit using folium_static
    folium_static(india_map)

def cleaningdataset(match_dataset):
    match_dataset.replace(
        {
            'team1': {'Delhi Daredevils': 'Delhi Capitals', 'Deccan Chargers': 'Sunrisers Hyderabad', 'Rising Pune Supergiant': 'Rising Pune Supergiants'},
            'team2': {'Delhi Daredevils': 'Delhi Capitals', 'Deccan Chargers': 'Sunrisers Hyderabad', 'Rising Pune Supergiant': 'Rising Pune Supergiants'},
            'winner': {'Delhi Daredevils': 'Delhi Capitals', 'Deccan Chargers': 'Sunrisers Hyderabad', 'Rising Pune Supergiant': 'Rising Pune Supergiants'},
            'toss_winner': {'Delhi Daredevils': 'Delhi Capitals', 'Deccan Chargers': 'Sunrisers Hyderabad', 'Rising Pune Supergiant': 'Rising Pune Supergiants'}
        },
        inplace=True
    )
    match_dataset.replace(
        {
            'team1': {'Rising Pune Supergiants': 'Pune Warriors'},
            'team2': {'Rising Pune Supergiants': 'Pune Warriors'},
            'winner': {'Rising Pune Supergiants': 'Pune Warriors'},
            'toss_winner': {'Rising Pune Supergiants': 'Pune Warriors'}
        },
        inplace=True
    )
    return match_dataset

def total_matches(match_dataset):
    match_dataset = cleaningdataset(match_dataset)
    total_match_count = pd.DataFrame({'team': pd.concat([match_dataset['team1'], match_dataset['team2']], axis=0)})

    total_match_count = total_match_count['team'].value_counts().reset_index(name='Total Matches').rename(columns={'index': 'Team'})
    return total_match_count

def win_matches_count(match_dataset):
    match_dataset = cleaningdataset(match_dataset)
    best_team = match_dataset[['team1', 'team2', 'winner']]
    best_team = best_team[['winner']].value_counts().reset_index(name='win_matches').rename(columns={'winner': 'Team'})
    return best_team

def best_team(match_dataset):
    last_column_name = match_dataset.columns[-1]
    match_dataset = match_dataset.drop(columns=last_column_name)
    match_dataset = match_dataset.dropna()
    total_match_dataset = total_matches(match_dataset)
    win_match_dataset = win_matches_count(match_dataset)
    
    print("Total Match Dataset Columns:", total_match_dataset.columns)
    print("Win Match Dataset Columns:", win_match_dataset.columns)

    dataset = total_match_dataset.merge(win_match_dataset, left_on='team',right_on='Team')
    return dataset



# Your functions for data cleaning and processing (cleaningdataset, total_matches, win_matches_count, and best_team)

# Assuming you have already defined the best_team function



'''
if sidebar_radio_data == 'Team Performance':

    team = st.selectbox('Select Your Team',teams)
    if team == 'Mumbai Indians':
        col1,col2 = st.columns(2)
        with col1:
            st.image('https://hindubabynames.info/downloads/wp-content/themes/hbn_download/download/sports-ipl/mumbai-indians-logo.png', caption='Mumbai Indians', use_column_width=True)
        with col2:
            searched_team = best_team(match_dataset)
            searched_team=searched_team[searched_team['Team']==str(team)]
            match_won = int(searched_team['win_matches'].values)
            total_match = int(searched_team['Total Matches'].values)
        col3,col4 = st.columns(2)
        with col3:
            st.subheader('Total Match Played')
            st.header(total_match)

        with col4:
            st.subheader('Total Match Won')
            st.header(match_won)




    st.image('https://hindubabynames.info/downloads/wp-content/themes/hbn_download/download/sports-ipl/royal-challengers-bangalore-logo.png', caption='Royal Challenger Banglore', use_column_width=True)

    with col3:
        st.image('https://hindubabynames.info/downloads/wp-content/themes/hbn_download/download/sports-ipl/chennai-super-kings-logo.png', caption='Chennai Super Kings', use_column_width=True)

    with col4:
        st.image('https://hindubabynames.info/downloads/wp-content/themes/hbn_download/download/sports-ipl/sunrisers-hyderabad-logo.png', caption='Sunriser Hydrabad', use_column_width=True)

    teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Gujarat Lions', 'Pune Warriors',
         'Royal Challengers Bangalore', 'Kolkata Knight Riders', 'Delhi Capitals',
         'Kings XI Punjab', 'Chennai Super Kings', 'Rajasthan Royals']
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.image('https://hindubabynames.info/downloads/wp-content/themes/hbn_download/download/sports-ipl/kolkata-knight-riders-logo.png', caption='Kolkata Knight Riders', use_column_width=True)
    with col2:
        st.image('https://hindubabynames.info/downloads/wp-content/themes/hbn_download/download/sports-ipl/delhi-capitals-logo.png', caption='Delhi Capitals', use_column_width=True)

    with col3:
        st.image('https://hindubabynames.info/downloads/wp-content/themes/hbn_download/download/sports-ipl/gujarat-titans.png', caption='Gujarat Lions', use_column_width=True)

    with col4:
        st.image('https://www.pngfind.com/pngs/m/671-6719734_srh-ipl-team-logo-2019-hd-png-download.png', caption='Pune Warriors', use_column_width=True)    
    
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        pass
    with col2:
        st.image('https://hindubabynames.info/downloads/wp-content/themes/hbn_download/download/sports-ipl/punjab-kings-logo.png', caption='Kings XI Punjab', use_column_width=True)

    with col3:
        st.image('https://hindubabynames.info/downloads/wp-content/themes/hbn_download/download/sports-ipl/rajasthan-royals-logo.png', caption='Rajasthan Royals', use_column_width=True)

    with col4:
        pass

#elif sidebar_radio_data == 'Player Performance':
    # Add code here to analyze and display player performance data

# Add more sections for other analysis options if needed
'''