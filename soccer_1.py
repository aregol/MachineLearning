#https://towardsdatascience.com/sports-analytics-an-exploratory-analysis-of-international-football-matches-part-1-e133798295f7

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.title('Internationa Football matches')
df = pd.read_csv("results.csv")
if st.checkbox('Show dataframe'):
    st.write(df)
st.subheader('Filtering dataset per team')
teams = st.multiselect('Pick your teams', df['home_team'].unique())
new_df = df[(df['home_team'].isin(teams)) | (df['away_team'].isin(teams)) ]
if st.checkbox('Show only home matches'):
    st.write(df[(df['home_team'].isin(teams))])
if st.checkbox('Show only away matches'):
    st.write(df[(df['away_team'].isin(teams))])
if st.checkbox('Show entire dataset'):    
    st.write(new_df)
    
st.subheader('Filtering dataset per event')
events = st.multiselect('Pick your events', df['tournament'].unique())
new_df_event = new_df[(new_df['tournament'].isin(events))]
st.write(new_df_event) 
            
st.subheader('Showing wins, losses and draws per team')
team_wins = st.selectbox('Pick your teams', df['home_team'].unique()) 
new_df_wins = df[(df['home_team']==team_wins)|(df['away_team']==team_wins)]
new_df_wins=new_df_wins.reset_index(drop=True)
    
    
    
wins = 0
losses = 0
draw = 0
x = []    
    
for i in range(len(new_df_wins)):
    if new_df_wins['home_team'][i]==team_wins:
        if new_df_wins['home_score'][i]>new_df_wins['away_score'][i]:
            wins+=1
            x.append(1)
        elif new_df_wins['home_score'][i]<new_df_wins['away_score'][i]:
            losses+=1
            x.append(-1)
        else:
            draw +=1
            x.append(0)
    else:
        if new_df_wins['home_score'][i]<new_df_wins['away_score'][i]:
            wins+=1
            x.append(1)
        elif new_df_wins['home_score'][i]>new_df_wins['away_score'][i]:
            losses+=1
            x.append(-1)
        else:
            draw +=1
            x.append(0)
    
    
labels = ['Wins','Losses','Draws']
values = [wins, losses, draw]
fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
st.plotly_chart(fig)
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=list(new_df_wins['date']), y=x))
# Add range slider
    
fig2.update_layout(
    xaxis=go.layout.XAxis(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)
st.plotly_chart(fig2)
wins_h = 0
losses_h = 0
draw_h = 0
wins_a = 0
losses_a = 0
draw_a = 0
for i in range(len(new_df_wins)):
    if new_df_wins['home_team'][i]==team_wins:
        if new_df_wins['home_score'][i]>new_df_wins['away_score'][i]:
            wins_h+=1
        elif new_df_wins['home_score'][i]<new_df_wins['away_score'][i]:
            losses_h+=1
        else:
            draw_h+=1
for i in range(len(new_df_wins)):
    if not new_df_wins['home_team'][i]==team_wins:
        if new_df_wins['home_score'][i]<new_df_wins['away_score'][i]:
            wins_a+=1
        elif new_df_wins['home_score'][i]>new_df_wins['away_score'][i]:
            losses_a+=1
        else:
            draw_a +=1
values_home = [wins_h, losses_h, draw_h]
values_away = [wins_a, losses_a, draw_a]
fig3 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
fig3.add_trace(go.Pie(labels=labels, values=values_home, name="Home"),
              1, 1)
fig3.add_trace(go.Pie(labels=labels, values=values_away, name="Away"),
              1, 2)
fig3.update_layout(
    title_text="Wins, losses and draws home vs away",
    annotations=[dict(text='Home', x=0.18, y=0.5, font_size=20, showarrow=False),
                 dict(text='Away', x=0.82, y=0.5, font_size=20, showarrow=False)])
fig3.update_traces(hole=.4, hoverinfo="label+percent+name")
st.plotly_chart(fig3)
#4 subplots to see whether playing in a neutral field is causal
wins_h_neutral = 0
losses_h_neutral = 0
draw_h_neutral = 0
wins_h_notneutral = 0
losses_h_notneutral = 0
draw_h_notneutral = 0
wins_a_neutral = 0
losses_a_neutral = 0
draw_a_neutral = 0
wins_a_notneutral = 0
losses_a_notneutral = 0
draw_a_notneutral = 0
for i in range(len(new_df_wins)):
    if new_df_wins['home_team'][i]==team_wins and new_df_wins['neutral'][i]:
        if new_df_wins['home_score'][i]>new_df_wins['away_score'][i]:
            wins_h_neutral+=1
        elif new_df_wins['home_score'][i]<new_df_wins['away_score'][i]:
            losses_h_neutral+=1
        else:
            draw_h_neutral+=1
            
            
for i in range(len(new_df_wins)):
    if new_df_wins['home_team'][i]==team_wins and not new_df_wins['neutral'][i]:
        if new_df_wins['home_score'][i]>new_df_wins['away_score'][i]:
            wins_h_notneutral+=1
        elif new_df_wins['home_score'][i]<new_df_wins['away_score'][i]:
            losses_h_notneutral+=1
        else:
            draw_h_notneutral+=1            
            
for i in range(len(new_df_wins)):
    if new_df_wins['home_team'][i]!=team_wins and new_df_wins['neutral'][i]:
        if new_df_wins['home_score'][i]<new_df_wins['away_score'][i]:
            wins_a_neutral+=1
        elif new_df_wins['home_score'][i]>new_df_wins['away_score'][i]:
            losses_a_neutral+=1
        else:
            draw_a_neutral +=1
            
for i in range(len(new_df_wins)):
    if new_df_wins['home_team'][i]!=team_wins and not new_df_wins['neutral'][i]:
        if new_df_wins['home_score'][i]<new_df_wins['away_score'][i]:
            wins_a_notneutral+=1
        elif new_df_wins['home_score'][i]>new_df_wins['away_score'][i]:
            losses_a_notneutral+=1
        else:
            draw_a_notneutral +=1            
            
            
            
values_home_neutral = [wins_h_neutral, losses_h_neutral, draw_h_neutral]
values_away_neutral = [wins_a_neutral, losses_a_neutral, draw_a_neutral]
values_home_notneutral = [wins_h_notneutral, losses_h_notneutral, draw_h_notneutral]
values_away_notneutral = [wins_a_notneutral, losses_a_notneutral, draw_a_notneutral]
fig4 = make_subplots(rows=2, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}], [{'type':'domain'}, {'type':'domain'}]],
                    subplot_titles=['Home neutral', 'Away neutral', 'Home not neutral', 'Away not neutral'])
fig4.add_trace(go.Pie(labels=labels, values=values_home_neutral, name="Home neutral"),
              1, 1)
fig4.add_trace(go.Pie(labels=labels, values=values_away_neutral, name="Away neutral"),
              1, 2)
fig4.add_trace(go.Pie(labels=labels, values=values_home_notneutral, name="Home not neutral"),
              2, 1)
fig4.add_trace(go.Pie(labels=labels, values=values_away_notneutral, name="Away not neutral"),
              2, 2)
fig4.update_layout(title_text='Wins, losses and draws home vs away, neutral vs not neutral')
fig4.update_traces(hole=.4, hoverinfo="label+percent+name")
st.plotly_chart(fig4)
#best performance
st.subheader('Best Performance')
t = []
for i in range(len(new_df_wins)):
    if new_df_wins['home_team'][i]==team_wins:
        t.append(new_df_wins['home_score'][i])
    else:
        t.append(new_df_wins['away_score'][i])
        
        
m = np.argmax(np.array(t), axis=0)
out = new_df_wins.iloc[m]
st.write(out)