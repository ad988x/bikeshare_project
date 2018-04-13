import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
			  'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # Credit for if statements: Stackoverflow; Managing user input's case in Python.
    city = input('Would you like to see data for Chicago, New York, or Washington?\n'
                 'You can enter Chicago, New York City, Washington.\n')
    if city.lower() in ['chicago','new york city','washington']:
      print('You have chosen:', city)
    else:
      city = input('\nYou did not enter a valid city, please try again.\n') 
    city = CITY_DATA[city.lower()]

    # get user input for month (all, january, february, ... , june)
    # Credit for if statements: Stackoverflow; Managing user input's case in Python.
    month = input('What month would you like to see data?\n'
                  'You can enter: all or months january - june.\n')

    if month.lower() in ['january','february','march','april','may','june','all']:
      print('Lets take a look at month:', month)
    else:
      month = input('\nYou did not enter a valid entry, please try again.\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    # Credit for if statements: Stackoverflow; Managing user input's case in Python.
    day = input('\nWhat day would you like to see?\n')
    
    if day.lower() in ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','all']:
      print('Lets take a look at:', day)
    else:
      day = input('\nYou did not enter a valid day, please try again.\n')

    print('-'*40)
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
    df = pd.read_csv(city)
    start_time = pd.to_datetime(df['Start Time'])
    # Struggled with this portion to filter months, was able to get data with all
    # Credited: GITHUB found example, now able to filter by month
    
    df['month'] = start_time.dt.strftime("%B")
    df['day'] = start_time.dt.strftime("%A")
    df['hour'] = start_time.dt.strftime("%H")
    
    if month != 'all':
      df = df[df['month'] == month.title()]
    
    if day != 'all':
      df = df[df['day'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    	Returns:
        	(str)common_month - based on filters, brings back the most common month traveled
            (str)common_day - based filters, states the most common day of the week traveled
            (int)common_hour - based on filters, converts the most common hour traveled from military
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    
    print('The most common month was:', common_month)
    
    # display the most common day of week
    
    common_day = df['day'].mode()[0]
    
    print('The most common day was:', common_day)

    # display the most common start hour
	# converted military time to easier time translation
    
    common_hour = int(df['hour'].mode()[0])
    if common_hour == 0:
      print('The most common hour is: 12 a.m.')
    if common_hour == 12:
      print('The most common hour is: 12 p.m.')
    if common_hour <= 11:
      print('The most common hour is: {} a.m.'.format(common_hour))
    if common_hour > 12:
      common_hour -= 12
      print('The most common hour is: {} p.m.'.format(common_hour))
    
    #print('The most common hour was:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    	Returns:
        	(str)pop_start - based on filter, states the most commonly start station
            (str)pop_end - based on filter, states the most commonly ending station
            (str)common_trip - based on filter, brings back most frequent combination of start&end stations
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    
    pop_start = df['Start Station'].mode()[0]
    print('Most common start station was:', pop_start)

    # display most commonly used end station
	
    pop_end = df['End Station'].mode()[0]
    print('Most common end station was:', pop_end)

    # display most frequent combination of start station and end station trip
    # Attempted groupby, could not find examples or get to work properly, 
    # Credited: found example on GITHUB
    
    df['comb_start_end'] = 'Starting Station: '+ df['Start Station'] +' to Ending Station: '+df['End Station']
    common_trip = df['comb_start_end'].mode()[0]
    print('The most frequent combination: ', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    	Returns:
        	(str)total_time - based on filter, takes the difference of start and end time, then sums the difference to 								  find the total travel time
            (str)mean_time - based on filter, takes the total travel time calculated earlier in function, than takes the 							  mean
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    
    df['total_travel'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
	
    total_time = df['total_travel'].sum()
    print('Total travel time:', total_time)
    
    # display mean travel time
    mean_time = df['total_travel'].mean()
    print('Total mean travel time:', mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.
    	Returns:
        	(str)u_types - based on filters, brings back the amount of subscribers, customers and dependents
            ((washington does not have this information, if statement to handle the next 4))
            (str)gender_count - based on filters, brings back the amount of genders
            (int)early_year - based on filters, brings back the earliest year of a rider
            (int)recent_year - based on filters, brings back the most recent year of a rider
            (int)common_year - based on filters, brings back the most common year of a rider
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    
    u_types = df['User Type'].value_counts()
    print(u_types)

    # Display counts of gender
    # if statement to account for Washington not having Gender Column
    
    print('\nCalculating Gender Stats if Applicable.\n')
    if 'Gender' in df:
      gender_count = df['Gender'].value_counts()
      print(gender_count)
    else:
      print('Gender count is not available for Washington.')

    # Display earliest, most recent, and most common year of birth
    # if statement to account for Washington not having birth year Column
	
    print('\nCalculating Birth Year Stats if Applicable.\n')
    if 'Birth Year' in df:
      early_year = df['Birth Year'].min()
      print('The Earliest Birth Year is:', int(early_year))
      recent_year = df['Birth Year'].max()
      print('The Most Recent Birth Year is:', int(recent_year))
      common_year = df['Birth Year'].mode()[0]
      print('The Most Common Birth Year is:', int(common_year))
    else:
      print('Birth Year not available for Washington.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        start = 0
        while True:
          if start == 0:
            raw_data = input('\nWould you like to see rows of data used to compute these stats?\n'
                         	 'Please type yes or no\n')
          else:
            raw_data = input('\nWould you like the see 5 more rows?\n'
                             'Please type yes or no\n')

          if raw_data.lower() == 'no':
            break
          elif raw_data.lower() == 'yes':
            print(df.iloc[start:start+5])
            start += 5
            
          else:
            print('Invalid')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
