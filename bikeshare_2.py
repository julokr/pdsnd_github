import time
import pandas as pd
import numpy as np

# Note: Ensure that the script is run from the same directory containing the data files. Alternatively, 
# import the os module and change your directory to that of the data files.
 
CITY_DATA = { 'chicago': 'chicago.csv','new york city': 'new_york_city.csv','washington': 'washington.csv' }

months = ['all','january', 'february', 'march', 'april', 'may', 'june', 'july']

days = ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():    
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please enter the name of the city whose data you would like to explore(chicago, new york city, or washington):").lower()
        if city in CITY_DATA:
            print("You have selected {}".format(city))
            break
        else:
            print("You entered an invalid city name, please try again!")
    
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please enter the month for which you would like to explore the data(all, january, february,..., june):").lower()
        if month in months:
            print("You have selected {}.".format(month))
            break
        else:
            print("You entered an invalid month, please try again!")
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please enter the day of the week for which you would like to explore the data(all, monday, tuesday,..., sunday):").lower()
        if day in days:
            print("You have selected {}.".format(day))
            break
        else:
           print("You entered an invalid day, please try again.")
    

    print('='*100)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file of selected city into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
        
    print('='*100)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['Start Time'].dt.month.mode()[0]
    print("The most frequent month of travel is month {}.".format(most_common_month))

    # display the most common day of week
    most_common_day = df['Start Time'].dt.weekday_name.mode()[0]
    print("The most frequent day of travel is {}.".format(most_common_day))

    # display the most common start hour
    most_common_hour = df['Start Time'].dt.hour.mode()[0]
    print("The most frequent start hour is {}.".format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*100)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most popular start station is {}.".format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df["End Station"].mode()[0]
    print("The most popular end station is {}.".format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    
    # use reset_index to return default index values and generate column of trip counts as 'counts'
    freq_trip_combination = df.groupby(['Start Station','End Station']).size().reset_index(name = 'counts')

    # arrange from most to least frequent(highest to lowest count)
    order_trips = freq_trip_combination.sort_values('counts', ascending = False)
    
    # select highest start station count(first value)
    start_trip = order_trips['Start Station'].iloc[0]
    
    # select highest end station count(first value)
    end_trip = order_trips['End Station'].iloc[0]
    
    print("Most frequent combination of start and end trips are {} and {}.".format(start_trip,end_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*100)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time is {}.".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time is {}.".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*100)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        # count while excluding NaN values
        counts_user_types = df['User Type'].value_counts()
        print("The number of user types are: {}".format(counts_user_types))
    else:
        print("There are no user types for this city.")

    # Display counts of gender
    if 'Gender' in df.columns:
        # count while excluding NaN values
        counts_gender = df['Gender'].value_counts()
        print("The gender counts are: {}.".format(counts_gender))
    else:
        print("There is no data on gender for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        print("The earliest year of birth is {}.".format(earliest_year)) 

        most_recent_year = df['Birth Year'].max()
        print("The most recent year of birth is {}.".format(most_recent_year))

        most_common_year = df['Birth Year'].mode()[0]
        print("The most common year of birth is {}.".format(most_common_year))
    else:
        print("There is no data on birth year for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*100)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
