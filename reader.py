import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

with open('data1.json') as data:
    dictData = json.load(data)


df = pd.DataFrame(dict([(k,pd.Series(v)) for k, v in dictData.items() ]))
number_time = df.iloc[0,1]
number_time = int(number_time)

print(df)

df_enemies = df['enemiesKilled']


Duration_seconds = range(1, number_time)
df_duration_seconds = {'Duration_seconds' : Duration_seconds }
df_duration = pd.DataFrame(df_duration_seconds)


df = pd.concat([df, df_duration], axis=1)



df_exp_got = df['expGot']
df_exp_got.dropna(inplace=True)

df_mages = df['charsPlayed']
df_mages.dropna(inplace=True)
mages = df_mages.unique()

duration = number_time

minutes = duration/60


df_levels = df['levelsGot']
df_levels.dropna(inplace=True)
levels = len(df_levels)

hp_heal = df.iloc[0,8]

damage_given = df.iloc[0,6]

damage_per_second = damage_given/duration

damage_taken = df.iloc[0,7]

df_power_ups = df['powerupsGot'].copy()
df_power_ups.dropna(inplace=True)

df_counts = df_power_ups.value_counts()
df_counts = pd.DataFrame(df_counts).reset_index()
df_counts.rename(columns={'index':'Power ups Got', 'powerupsGot':'count'}, inplace=True)


players_died = df['playersDied'].copy()
players_died.dropna(inplace=True)

players_revived = df['playersRevived'].copy()
players_revived.dropna(inplace=True)


st.title(':sparkles: Mage Guild (Non) Magical Inteligence :mortar_board:')

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader('Mages :crystal_ball:')
    for i in mages:
        st.markdown(f'{i}')
with col2:
    st.subheader('Damage Given :boom:')
    st.markdown(f'Total: {round(damage_given)}')
    st.markdown(f'DPS: {round(damage_per_second)}')
with col3:
    st.subheader('Duration :hourglass_flowing_sand:')
    st.markdown(f'{duration} seconds')
    st.markdown(f'{minutes} minutes')

column1, column2, column3 = st.columns(3)

with column1:
    st.subheader('Damage Taken :sos:')
    st.markdown(round(damage_taken))

with column2:
    st.subheader('Level Up :arrow_up:')
    st.markdown(levels)

with column3:
    st.subheader('Enemies killed :japanese_ogre:')
    st.markdown(len(df_enemies))


fig = go.Figure()
fig.add_trace(go.Scatter(name='Enemies Killed', x=df_enemies.values, y=df_enemies.index, mode='lines'))
fig.add_trace(go.Scatter(name='Exp got', x= df_exp_got.values, y=df_exp_got.index, mode='lines'))
fig.update_layout(title='Enemies Killed and Experience Got', xaxis_title='Duration (s)', yaxis_title='Enemies x Exp got')
fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
st.plotly_chart(fig)


fig2 = px.bar(df_counts, y=df_counts['Power ups Got'], x=df_counts['count'],  orientation='h')
fig2.update_layout(title='Power Ups Got', yaxis_title='Power Ups', xaxis_title='Total')
fig2.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
st.plotly_chart(fig2)


fig3 = go.Figure()
fig3.add_trace(go.Scatter(name='Number of Deaths', x=players_died.values, y=players_died.index))
fig3.add_trace(go.Scatter(name='Players revived', x=players_revived.values, y=players_revived.index, mode='markers'))
fig3.update_layout(title='Deaths x Revives', xaxis_title='Duration (s)', yaxis_title='Deaths x Revives')
fig3.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
fig3.update_traces(marker=dict(size=12,line=dict(width=2,color='DarkSlateGrey')))
st.plotly_chart(fig3)








    
        
        