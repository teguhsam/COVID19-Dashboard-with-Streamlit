# ----------------------------------------------------------------------------
# Import
import json
import requests
import pandas as pd

# ----------------------------------------------------------------------------

def downloading_json_file(url):
    response = requests.get(url)
    response_df = pd.DataFrame(response.json())
    return response_df


# ----------------------------------------------------------------------------
# Clean JSON Export Pandas
def split_json_to_dfs(dataframe):
    """
    Input: .json file containing full information
    Output:
    country_information---information of each countries. This is the first layer of the json file dictionary
    country_key---dataframe containing dictionary. For example: ['AFG'] ['Afganistan']
    combined_df---daily records of covid
    """
    read_df = dataframe.copy()
    ### Dataframe #1
    country_information = read_df.T.drop('data', 1).reset_index()
    ### Dataframe #2
    country_key = country_information[['index', 'location', 'continent']]
    ### Datafrane #3
    covid_cases = read_df.T['data']
    combined_df = pd.DataFrame()
    for country in list(covid_cases.keys()):
        new_df = pd.DataFrame.from_dict(covid_cases[country], orient='columns')
        new_df['country_code'] = country
        combined_df = combined_df.append(new_df)

    combined_df['date']= pd.to_datetime(combined_df['date'])

    # Replacing Location
    combined_df = combined_df.merge(country_key, how='left',left_on='country_code', right_on='index').drop(['index'], axis = 1)
    #col_reorder = combined_df.columns.to_list()
    #if 'location' in col_reorder: col_reorder.remove('location')
    #col_reorder.insert(1, 'location')
    #combined_df = combined_df[col_reorder]
    
    return country_information, country_key, combined_df