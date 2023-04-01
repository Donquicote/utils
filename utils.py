import requests
import pandas as pd

def get_children_leis(targetLei):
    """
    Gets a list of LEIs for all ultimate children of a given LEI.

    Parameters
    ----------
    targetLei : str
        The LEI of the parent entity for which the ultimate children LEIs are to be retrieved.

    Returns
    -------
    df : DataFrame
        A Pandas DataFrame containing the LEI values for all ultimate children of the parent entity.

    """
    # Create the API URL to retrieve the list of ultimate children for the parent entity
    url = "https://api.gleif.org/api/v1/lei-records/" + targetLei + "/ultimate-children?page[size]=50&page[number]=1"

    # Get the first page of the response to extract the last page number
    response = requests.request("GET", url, headers={'Accept': 'application/vnd.api+json'}, data={})

    # Extract the JSON data from the response
    data = response.json()
    # Extract the last page number from the JSON data
    lastPage = data['meta']['pagination']['lastPage']

    df_list = []
    for currentPage in range(1, lastPage + 1):
        print('Processing page ' + str(currentPage) + ' of ' + str(lastPage))
        url = url[0:-1] + str(currentPage)
        response = requests.request("GET", url, headers={'Accept': 'application/vnd.api+json'}, data={})

        # Extract the JSON data from the response
        data = response.json()

        # Create an empty list to store the LEIs of the ultimate children
        ultimate_children_leis = []

        # Iterate over the JSON data to extract the LEI values for each ultimate child entity
        for child in data['data']:
            ultimate_children_leis.append(child['attributes']['lei'])

        # Create a Pandas DataFrame from the list of ultimate children LEIs
        df_list.append(pd.DataFrame({'LEI': ultimate_children_leis}))

    # Concatenate the DataFrames into a single DataFrame
    df = pd.concat(df_list)
    return df


targetLei = '5493006QMFDDMYWIAM13'
get_children_leis(targetLei)