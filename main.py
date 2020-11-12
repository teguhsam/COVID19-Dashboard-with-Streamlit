# ----------------------------------------------------------------------------
# Import
import pandas as pd
import json
import requests
import streamlit as st
import matplotlib.pyplot as plt
from specific_func import downloading_json_file, split_json_to_dfs

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
st.title("Hello")

drop_option = country_key['location'].to_list()

country_select = st.sidebar.selectbox("Country", drop_option, index=213)
def filter_combine_df(country_selected):
    df = combined_df[combined_df.location == country_selected]
    df['new_cases_MA'] = df['new_cases'].rolling(window = 7).mean()
    return df

st.write("Country Selected: {}".format(country_select))

today = combined_df['date'].max()
st.write("Data last updated: {}".format(str(today.date())))

# New Cases Plot
current_country = filter_combine_df(country_select)
fig = plt.figure()
plt.plot('date', 'new_cases', data = current_country, label = "New Cases")
plt.plot('date', 'new_cases_MA', data = current_country, label = "7-Day Moving Average")
plt.xlabel("Date")
plt.ylabel("New Cases")
plt.title("New COVID-19 Cases in {}".format(country_select))
plt.legend()
st.pyplot(fig)

