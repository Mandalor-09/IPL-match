import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pickle
from extra import *

#pip install streamlit folium streamlit-folium
#pip install streamlit streamlit-leaflet

import folium
from streamlit_folium import folium_static




# Load the datasets (Assuming these files exist in the specified paths)
# player_dataset = pd.read_excel(r"C:\Users\DELL\OneDrive\Desktop\ml\ipl_project\ipl_dataset\most_runs_average_strikerate.csv")
#match_dataset = pd.read_csv(r"ipl_dataset\\matches.csv")
# deliveries_dataset = pd.read_csv(r"C:\Users\DELL\OneDrive\Desktop\ml\ipl_project\ipl_dataset\deliveries.csv")
#team_dataset = pd.read_csv(r"C:\Users\DELL\OneDrive\Desktop\ml\ipl_project\ipl_dataset\teams.csv")
# most_runs = pd.read_csv(r"C:\Users\DELL\OneDrive\Desktop\ml\ipl_project\ipl_dataset\most_runs_average_strikerate.csv")
#teamwise_home_away_db = pd.read_csv(r'ipl_dataset\\teamwise_home_and_away.csv')

# Define the list of available teams and cities (Assuming these are correctly defined)
teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Gujarat Lions', 'Pune Warriors',
         'Royal Challengers Bangalore', 'Kolkata Knight Riders', 'Delhi Capitals',
         'Kings XI Punjab', 'Chennai Super Kings', 'Rajasthan Royals']

cities = ['Mumbai', 'Chandigarh', 'Delhi', 'Chennai', 'Port Elizabeth', 'Bloemfontein',
          'Pune', 'Bengaluru', 'Kolkata', 'Rajkot', 'Bangalore', 'Hyderabad', 'Ahmedabad',
          'Kochi', 'Jaipur', 'Cuttack', 'Durban', 'Centurion', 'Dharamsala', 'Cape Town',
          'Johannesburg', 'Kanpur', 'Visakhapatnam', 'Kimberley', 'Mohali', 'Indore', 'Raipur',
          'Abu Dhabi', 'Ranchi', 'East London', 'Nagpur', 'Sharjah']

# Load the pickled pipeline
pipe = pickle.load(open(r'pipe.pkl', 'rb'))

# Streamlit application starts here
st.sidebar.header('Ipl Analysis12')
# Radio button to select the analysis option
sidebar_radio_data = st.sidebar.radio('Select an Option', ('Match winner prediction',"_"))

if sidebar_radio_data == 'Match winner prediction':
    st.header('Predict Winner')
    # If 'Match winner prediction' is selected, show two select boxes for batting and bowling teams
    col1, col2 ,col3 = st.columns(3)
    with col1:
        batting_team = st.selectbox('Select the Batting Team', teams)
    with col2:
        bowling_team = st.selectbox('Select the Bowling Team', teams)
    with col3:
        city = st.selectbox('Match City',cities)
    target = st.text_input('Select the Target')
    col4, col5 ,col6 = st.columns(3)
    with col4:
        overs = st.text_input('Overs Completed')
    with col5:
        current_score = st.text_input('Enter Current Score')
    with col6:
        wickets = st.number_input('Enter Wickets Gone',min_value=0,max_value=10)

    if st.button('Predict Probablity'):
        current_score = current_score
        runs_need = int(target) - int(current_score)
        ball_left = balls_left_count(overs)
        wickets_left = 10 - int(wickets)
        req_runrate = int(runs_need) * 6 / (120 - ball_left)
        current_runrate = int(current_score) * 6 / (120 - ball_left) 

        # Assuming data contains scalar values, convert them to lists
        data = {
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [city],
            'Current_score': [int(current_score)],
            'Runs_need': [runs_need],
            'Ball_left': [ball_left],
            'Wicket_left': [wickets_left],
            'Req_runrate': [req_runrate],
            'Current_runrate': [current_runrate]
        }

    # Create the DataFrame using the modified data dictionary
        input_data = pd.DataFrame(data)
        st.table(input_data)
        #st.table(input_data.dtypes)
        result = pipe.predict_proba(input_data)
        a=int(result[0][0] * 100 )
        b=int(result[0][1] * 100 )
        
        st.header(f'{batting_team}: {a}%')
        st.header(f'{bowling_team}: {b}%')
    # Add code here to make match winner prediction using the selected teams and the 'pipe' pipeline
    # '''







