import string
import time
from datetime import datetime, timedelta
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
    print("The most common month of travel is {} with count {}".format(MONTH_DATA[idx].capitalize(), temp_df.max()))

    # display the most common day of week
    df['Weekday'] = df['Start Time'].dt.weekday_name
    temp_df = df.groupby(by='Weekday').size()
    weekday = temp_df.idxmax()
    print("The most common day of week is {} with count {}".format(weekday, temp_df.max()))

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    temp_df = df.groupby(by='Hour').size()
    hour = temp_df.idxmax()
    print("The most common start hour is {}:00 with count {}".format(hour, temp_df.max()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """ Displays statistics on the most popular stations and trips """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    temp_df = df.groupby(by='Start Station').size()
    idx = temp_df.idxmax()
    print("The most commonly used start station is {} with count {}".format(idx, temp_df.max()))

    # display most commonly used end station
    temp_df = df.groupby(by='End Station').size()
    idx = temp_df.idxmax()
    print("The most commonly used end station is {} with count {}".format(idx, temp_df.max()))

    # display most frequent combination of start station and end station trip
    temp_df = df.groupby(by=['Start Station', 'End Station']).size()
    idx = temp_df.idxmax()
    print(idx)
    print("The most common trip starts from {} and ends at {} with count {}".format(idx[0], idx[1], temp_df.max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_stats(df):
    """ Displays total and mean travel times statistics """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_secs = df['Trip Duration'].sum()
    dt = datetime(1,1,1) + timedelta(seconds=int(total_secs))
    print("Total travel time is {} seconds which is equivalent to {} days, {} hours, "\
          "{} minutes and {} seconds.".format(total_secs, dt.day-1, dt.hour, dt.minute, dt.second ))

    # display mean travel time
    avg_time = df['Trip Duration'].mean()
    print("Average travel time is {} seconds".format(avg_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """ Displays statistics on bikeshare riders """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of different user types: ")
    print(df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print("\nCounts of each gender: ")
        print(df['Gender'].value_counts())

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, most common year of birth
        earliest_year = df['Birth Year'].min()
        print("\nEarliest year of birth: {}".format(earliest_year))

        most_recent = df['Birth Year'].max()
        print("Most recent year of birth: {}".format(most_recent))

        most_common = df.groupby(by='Birth Year').size()
        print("Most common year of birth: {}".format(most_common.idxmax()))
    else:
        print("\nNo gender or birth year data to share.")

    # Display earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_individual_stats(df):
    """ Display individual stats from the dataset """
    count = 0
    while True:
        trip_data = input("\nWould you like to view individual trip data? Type 'yes' or 'no': ")
        if trip_data.lower() != "yes":
            break
        else:
            print(df.iloc[10*count:10*(count+1)])
            count += 1
    return None

def main():

    while True:
        city, month, day = getfilters()
        df = load_data(city, month, day)

        # Calculate descriptive statistics
        time_stats(df)
        station_stats(df)
        trip_stats(df)
        user_stats(df)

        show_individual_stats(df)

        restart = input("\nDo you want to start over? Enter 'yes' or 'no'\n")
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
