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
    df = pd.read_csv(city)

    # Convert to datetime datatype
    df[['Start Time', 'End Time']] = df[['Start Time', 'End Time']].apply(pd.to_datetime, errors='coerce')

    # Filter rows by month
    if month != 'all':
        df = df.loc[df['Start Time'].dt.month == MONTH_DATA.index(month), :]

    # Filter rows by day of week
    if day != 'all':
        df = df.loc[df['Start Time'].dt.weekday_name == day.capitalize(), :]

    # Filter sanity checks
    #print(df['Start Time'].dt.weekday_name.head())
    #print(df['Start Time'].dt.month.head())

    return df

def time_stats(df):
    """ Displays statistics on the most common times of travel """

    print("\nCalculating most frequent times of travel statistics...\n")
    start_time = time.time()

    # Calculate most popular month
    df['Month'] = df['Start Time'].dt.month
    temp_df = df.groupby(by='Month').size()
    idx = temp_df.idxmax()
    print("The most common month of travel is {}".format(MONTH_DATA[idx].capitalize()))

    # display the most common day of week
    df['Weekday'] = df['Start Time'].dt.weekday_name
    temp_df = df.groupby(by='Weekday').size()
    weekday = temp_df.idxmax()
    print("The most common day of week is {}".format(weekday))

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    temp_df = df.groupby(by='Hour').size()
    hour = temp_df.idxmax()
    print("The most common start hour is {}:00".format(hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """ Displays statistics on the most popular stations and trips """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    temp_df = df.groupby(by='Start Station').size()
    idx = temp_df.idxmax()
    print("The most commonly used start station is {}".format(idx))

    # display most commonly used end station
    temp_df = df.groupby(by='End Station').size()
    idx = temp_df.idxmax()
    print("The most commonly used end station is {}".format(idx))

    # display most frequent combination of start station and end station trip
    temp_df = df.groupby(by=['Start Station', 'End Station']).size()
    idx = temp_df.idxmax()
    print("The most common trip starts from {} and ends at {}".format(idx[0], idx[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():

    df = load_data('chicago.csv', 'all', 'all')
    #df.info()
    #time_stats(df)
    station_stats(df)

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

    city_df = pd.DataFrame(CITY_DATA,
                    index=[1],
                    columns=['chicago', 'new york city', 'washington'])
    #city_df.info()
    #print(city_df.describe())
    print(city_df.head())
    print('-'*10)
    print(city_df.loc[[1],['chicago']])
    print('-'*40)

    city_s = pd.Series(CITY_DATA)
    print(city_s.head())
    print(city_s.iloc[2])
"""


if __name__ == "__main__":
    main()
