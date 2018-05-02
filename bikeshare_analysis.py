import string
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}
MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june',
              'july', 'august', 'september', 'october', 'november', 'december']
DAY_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']

def getfilters():
    """
    Asks user to specify a city, month and day to analyze

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no filter
        (str) day - name of the day of week to filter by, or "all" to apply no filter
    """
    print("\nWelcome to Bikeshare data exploration!\n")

    # get name of city to analyze
    while True:
        city = input("\nEnter the city you wish to analyze (chicago, new york city, washington): ")
        try:
            city_csv = CITY_DATA[city.lower()]
            break
        except KeyError:
            print("Invalid city \"{}\" entered. Please try again".format(city))

    print('-'*40)

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nEnter the month to filter by (all, january, february, ... , december): ")
        if month.lower() in MONTH_DATA:
            month = month.lower()
            break
        else:
            print("Invalid value \"{}\" entered. Please try again".format(month))

    print('-'*40)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nEnter the day to filter by (all, monday, tuesday, ... , sunday): ")
        if day.lower() in DAY_DATA:
            day = day.lower()
            break
        else:
            print("Invalid value \"{}\" entered. Please try again".format(day))

    return city_csv, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable

    Args:
        (str) city: name of city to analyze
        (str) month: name of month to filter by, or "all" to apply no filter
        (str) day: name of day of week to filter by, or "all" to apply no filter

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    data = pd.read_csv(city)
    print(data.head())

    return df


def main():

    city, month, day = getfilters()
    print(city)
    df = load_data(city, month, day)
    """while True:
        city, month, day = getfilters()
        df = load_data(city, month, day)

        # Calculate descriptive statistics
        time_stats(df)
        station_stats(df)
        trip_stats(df)
        user_stats(df)

        restart = input('\nDo you want to start over? Enter yes or no\n')
        if restart.lower() != 'yes':
            break
"""
    city_df = pd.DataFrame(CITY_DATA,
                    index=[1],
                    columns=['chicago', 'new_york_city', 'washington'])
    #city_df.info()
    #print(city_df.describe())
    print(city_df.head())
    print('-'*10)
    print(city_df.loc[[1],['chicago']])
    print('-'*40)

    city_s = pd.Series(CITY_DATA)
    print(city_s.head())
    print(city_s.iloc[2])



if __name__ == "__main__":
    main()
