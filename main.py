# ----------------------------------------------------------------------------
# Import
import pandas as pd
import json
import requests
import streamlit as st
import matplotlib.pyplot as plt
from specific_func import downloading_json_file, split_json_to_dfs
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ----------------------------------------------------------------------------
url_json = "https://covid.ourworldindata.org/data/owid-covid-data.json"
@st.cache
def download_json(url): 
    return downloading_json_file(url)
response = download_json(url_json)

@st.cache
def call_split_json_to_dfs(dataframe):
    return split_json_to_dfs(dataframe)

country_information, country_key, combined_df = call_split_json_to_dfs(response)


# ----------------------------------------------------------------------------
# Streamlit
st.title("COVID-19 Dashboard")

# Dropdown Option
drop_option = country_key['location'].to_list()
country_select = st.sidebar.selectbox("Country", drop_option, index=214)

# Selection Confirmation and Data Update
st.write("Country Selected: {}".format(country_select))
today = combined_df['date'].max()
st.write("Data last updated: {}".format(str(today.date())))

# Data Card
def filter_country_information(country_selected):
    df = country_information.copy()
    filtered_dict = df[df['location']==country_selected].to_dict('records')[0]
    return filtered_dict

country_stat_dict = filter_country_information(country_select)

fig_dc = go.Figure()
fig_dc.add_trace(
        go.Indicator(mode = "number",
        value = country_stat_dict['population'],
        #delta = {'position': "top", 'reference': 320},
        domain = {'row': 0, 'column': 0},
        title = {'text': 'Population'}
        ))
fig_dc.add_trace(
        go.Indicator(mode = "number",
        value = country_stat_dict['median_age'],
        #delta = {'position': "top", 'reference': 320},
        domain = {'row': 0, 'column': 1},
        title = {'text': 'Median Age'}
        ))
fig_dc.add_trace(
        go.Indicator(mode = "number",
        value = country_stat_dict['life_expectancy'],
        #delta = {'position': "top", 'reference': 320},
        domain = {'row': 0, 'column': 2},
        title = {'text': 'Life Expectancy'}
        ))
fig_dc.update_layout(
        grid = {'rows': 1, 'columns': 3, 'pattern': "independent"},
        width = 800,
        height = 200)
st.plotly_chart(fig_dc)

# Plots
def filter_combine_df(country_selected):
    df = combined_df[combined_df.location == country_selected]
    df['new_cases'] = np.where(df['new_cases'] <0, np.nan, df['new_cases'])
    df['new_deaths'] = np.where(df['new_deaths'] <0, np.nan, df['new_deaths'])
    df['total_cases'] = np.where(df['total_cases'] <0, np.nan, df['total_cases'])
    df['new_cases_MA'] = df['new_cases'].rolling(window = 7).mean()
    return df

# New Cases Plot
current_country = filter_combine_df(country_select)
new_cases = px.line(
        data_frame=current_country,
        x = 'date',
        y = ['new_cases', 'new_cases_MA'],
        title= 'New Cases in {}'.format(country_select),
        height = 600,
        width = 800)
st.plotly_chart(new_cases)


new_deaths = px.line(
        data_frame=current_country,
        x = 'date',
        y = 'new_deaths',
        title= 'New Deaths in {}'.format(country_select),
        width = 600,
        height = 800)
st.plotly_chart(new_deaths)

total_cases = px.line(
        data_frame=current_country,
        x = 'date',
        y = 'total_cases',
        title= 'Total Cases in {}'.format(country_select),
        width = 600,
        height = 800)
st.plotly_chart(total_cases)