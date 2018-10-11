import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#Taking users name as input
name=input('Please enter your name: ').title()
print('\n'*50)
print('Greetings,',name,'!')
print('Let\'s explore some US bikeshare data!')
print('-'*50)

def get_city():
    """
    Asks user to specify a city to analyze.

    Returns:
    (str) city - name of the city to analyze
    """

    city=input('\nWould you like to see data for Chicago, New York or Washington:').lower()
    while city not in CITY_DATA:
        print('\nLooks like the entered city is not present in our data set.')
        print('Please enter a valid input.')
        return get_city()
    return city
    print('\nWe will be showing you insights for',city.title(),'city.')

def get_filters():
    """
    Asks user to specify a month, and day to analyze.

    Returns:
    (str) month - name of the month to filter by, or "none" to apply no month filter
    (str) day - name of the day of week to filter by, or "none" to apply no day filter
    """
# get user input for month (all, january, february, ... , june)
# get user input for day of week (all, monday, tuesday, ... sunday)
    print('\nWould you like to filter data by month, day, both or not at all?')
    print('Type none for no time filter.')
    user_inp=input().lower()
    if user_inp=='month':
            print('\nPlease enter from the given months:')
            mth=['january','february','march','april','may','june']
            print(mth)
            month=input().lower()
            day='none'
            if month not in mth:
                print('\nIt seems like the entered month is not present in our data set')
                print('Please enter a valid input.')
                print('Now the program restarts....')
                return get_filters()
    elif user_inp=='day':
            print('\nPlease enter from the given days:')
            dy=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            print(dy)
            day=input().title()
            month='none'
            if day not in dy:
                print('\nIt seems like the entered day is not present in our data set')
                print('Please enter a valid input.')
                print('Now the program restarts....')
                return get_filters()
    elif user_inp=='both':
            print('\nPlease enter from the given months:')
            mth=['january','february','march','april','may','june']
            print(mth)
            month=input().lower()
            if month not in mth:
                print('\nIt seems like the entered month is not present in our data set')
                print('Please enter a valid input.')
                print('Now the program restarts.')
                return get_filters()
            print('\nPlease enter from the given days:')
            dy=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            print(dy)
            day=input().title()
            if day not in dy:
                print('\nIt seems like the entered day is not present in our data set')
                print('Please enter a valid input.')
                print('Now the program restarts.')
                return get_filters()
    elif user_inp=='none':
            month='none'
            day='none'
    else:
        print('\nLooks like you have entered an invalid input.')
        print('Please enter a valid input.')
        print('Now the program restarts.')
        return get_filters()
    print('-'*50)
    return month, day, user_inp

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "none" to apply no month filter
        (str) day - name of the day of week to filter by, or "none" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'none':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'none':
        df = df[df['day_of_week'] == day]
    return df

def time_stats(df, user_inp):
    """Displays statistics for times of travel."""
    start_time = time.time()
    print('\n** Statistics on times of travel **')
#displays the most and least common start time.
    start_time_calc(df)
#displays the the most and least common day of week and month.
    if user_inp=='month':
            weekday_calc(df)
    elif user_inp=='day':
            month_calc(df)
    elif user_inp=='none':
            weekday_calc(df)
            month_calc(df)
    else:
        print('\nSince you selected both the month and day filter.')
        print('We won\'t be able to tell you the most popular month or day of week.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)
    raw_data_view(df)

def station_stats(df):
    """Displays statistics on stations."""
    start_time = time.time()
    print('\n** Statistics on stations **')
#Displays the most most and least popular start station.
    station_ser=pd.Series(df['Start Station'])
    print('\nWhich was the most and least popular starting station ?')
    st_calc(station_ser)
#Displays the most most and least popular ending station.
    station_ser=pd.Series(df['End Station'])
    print('\nWhich was the most and least popular ending station ?')
    st_calc(station_ser)
#Displays the most most and least popular start and ending station combination.
    print('\nWhich is the most popular combination of start and end station trip ?')
    df["start_end"] = df["Start Station"] + ' - ' + df["End Station"]
    station_ser=pd.Series(df['start_end'])
    st_calc(station_ser)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)
    raw_data_view(df)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\n** Statistics on the trip duration **')
    start_time = time.time()
    trip_dur=np.array(df['Trip Duration'])
#Calculates and displays the total trip duration.
    trip_sum=trip_dur.sum()
    print('\nWhat was the total trip duration ?')
    print('The total trip duration was:',trip_sum)
#Calculates and diplays the mean of the trip duration.
    trip_mean=trip_dur.mean()
    print('\nWhat was the mean trip duration ?')
    print('The mean trip duration was:',trip_mean)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)
    raw_data_view(df)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""
    print('\n** Statistics on bikeshare users **')
    start_time = time.time()
    # Display counts of user types
    print('\nHow many types of user\'s are there and what is their count ?')
    user_types = df['User Type'].value_counts()
    print(user_types)
    # Display counts of gender
    print('\nWhat is the count of gender ?')
    if city=='washington':
        print('\nThe dataset for Washington city does not contains gender column.')
        print('So this question is not valid for Washington city.')
    else:
        gender = df['Gender'].value_counts()
        print(gender)
    # Display earliest, most recent, and most common year of birth
    print('\nWhich are the earliest, most recent, and most common year of birth ?')
    if city=='washington':
        print('\nThe dataset for Washington city does not contains birth year column.')
        print('So this question is not valid for Washington city.')
    else:
        birth_year=df['Birth Year']
        print('The earliest year of birth is:',birth_year.min())
        print('The most recent year of birth is:',birth_year.max())
        print('The most common year of birth is:',birth_year.mode()[0])
        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)
    raw_data_view(df)

#Prints raw data
def raw_data_view(df):
    print('\nWould you like to see 5 lines of raw data? Enter yes or no. ?')
    user_inp=input().lower()
    if user_inp=='yes':
        print('\nExtracting raw data...\n')
        start_time = time.time()
        print(df.head())
        print("\nThis took %s seconds." % (time.time() - start_time))
    elif user_inp=='no':
        print('-'*50)
        return
    else:
        print('\nLook\'s like you have entered something wrong.')
        print('Let\'s start again....')
        return raw_data_view(df)
    print('-'*50)

#Calculates and prints the most and least popular start times.
def start_time_calc(df):
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['hour']=df['Start Time'].dt.hour
    hour_ser=pd.Series(df['hour'])
    hour_ser_grp=hour_ser.value_counts()
    popular=hour_ser_grp.index[0]
    rare=hour_ser_grp.index[-1]
    print('\nWhat was the most and least popular start time ?')
    print('Most popular start time: ',popular)
    print('Least popular start time: ',rare)

#Calculates and prints the most and least popular day of week.
def weekday_calc(df):
    day_ser=pd.Series(df['day_of_week'])
    day_ser_grp=day_ser.value_counts()
    popular=day_ser_grp.index[0]
    rare=day_ser_grp.index[-1]
    print('\nWhat was the most and least popular day of week ?')
    print('Most popular day of week: ',popular)
    print('Least popular day of week: ',rare)

#Calculates and prints the most and least popular months.
def month_calc(df):
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    mth_ser=pd.Series(df['month'])
    mth_ser_grp=mth_ser.value_counts()
    pop=mth_ser_grp.index[0]
    rar=mth_ser_grp.index[-1]
    popular=months[pop-1]
    rare=months[rar-1]
    print('\nWhat was the most and least popular month ?')
    print('Most popular month: ',popular)
    print('Least popular month: ',rare)

#Calculates and prints the most and least popular stations.
def st_calc(station_ser):
    station_ser_grp=station_ser.value_counts()
    popular=station_ser_grp.index[0]
    rare=station_ser_grp.index[-1]
    print('Most Popular:',popular)
    print('Least Popular:',rare)

def main():
    while True:
        city = get_city()
        month, day, user_inp = get_filters()
        df = load_data(city, month, day)
        raw_data_view(df)
        time_stats(df, user_inp)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
