import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# Load your data
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    df_hour = pd.read_csv(os.path.join(current_dir, 'hour.csv'))
    df_day = pd.read_csv(os.path.join(current_dir, 'day.csv'))
    df_day['dteday'] = pd.to_datetime(df_day['dteday'])
    df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])
    return df_day, df_hour


df_day, df_hour = load_data()

st.title('Bike-Sharing Data Analysis Dashboard (Dicoding Data Analysis Project)')

st.write("""
---
Name : Fizio Ramadhan Herman\n
Group : ML-20\n
This project analyzes a bike-sharing dataset to understand rental patterns over a one-year period. We'll explore the data to answer three main questions:\n
Weather & Seasonal Impact : Which weather situation & season has the highest/lowest number of bike rentals?\n
Peak Hours : What time of day is most popular for bike rentals?\n
Weekday vs Weekend : How do bike rental patterns differ between weekdays and weekends?\n
To answer these questions, we'll use data visualization and statistical analysis techniques. Our goal is to uncover insights that could be useful for managing bike-sharing systems more effectively.
""")

# Seasonal Analysis
st.header('Seasonal Analysis')
season_rentals = df_day.groupby('season')['cnt'].sum().reset_index()
season_names = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
season_rentals['season_name'] = season_rentals['season'].map(season_names)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season_name', y='cnt', data=season_rentals, ax=ax, palette='viridis')
ax.set_title('Total Bike Rentals by Season')
ax.set_xlabel('Season')
ax.set_ylabel('Total Rentals')
st.pyplot(fig)
st.write("""
We can see from the chart that fall season has the highest number of rental (1,061,029).\n
And on the other hand, spring season has the lowest number of rental (471,348).
""")

# Weather Condition Analysis
st.header('Weather Condition Analysis')
weather_condition_rental = df_day.groupby('weathersit')['cnt'].sum().reset_index()
condition_names = {1: "Clear | Few clouds", 2: "Mist | Cloudy", 3: "Light Snow | Light Rain",
                   4: 'Heavy Rain + Ice Pallets + Thunderstorm'}
weather_condition_rental['weather_condition'] = weather_condition_rental['weathersit'].map(condition_names)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='weather_condition', y='cnt', data=weather_condition_rental, ax=ax, palette='viridis')
ax.set_title('Total Bike Rentals by Weather Condition')
ax.set_xlabel('Weather Condition')
ax.set_ylabel('Total Rentals')
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)
st.write("""
We can see from the chart that people tend to rent a bike when the weather condition is clear, and very less of a people rent a bike when the weather condition has a light snow. And also none of them are renting a bike when the weather is really bad (4th category).
""")

# Hourly Analysis
st.header('Hourly Analysis')
hourly_rentals = df_hour.groupby('hr')['cnt'].sum().reset_index()
hourly_rentals['period'] = hourly_rentals['hr'].apply(lambda x: 'AM' if x < 12 else 'PM')
am_top4 = hourly_rentals[hourly_rentals['period'] == 'AM'].nlargest(4, 'cnt')
pm_top4 = hourly_rentals[hourly_rentals['period'] == 'PM'].nlargest(4, 'cnt')
selected_hours = pd.concat([am_top4, pm_top4])
selected_hours['hour_label'] = selected_hours.apply(lambda row: f"{row['hr'] % 12 or 12} {row['period']}", axis=1)
selected_hours = selected_hours.sort_values('hr')

fig, ax = plt.subplots(figsize=(14, 6))
sns.barplot(x='hour_label', y='cnt', hue='period', data=selected_hours, ax=ax, palette='viridis')
ax.set_title('Top 4 Bike Rental Hours for AM and PM')
ax.set_xlabel('Hour')
ax.set_ylabel('Total Rentals')
st.pyplot(fig)
st.write("""
The peak hours of bike renting is on 8AM (on the morning) and 5PM (on the afternoon)
""")

# Weekday vs Weekend Analysis
st.header('Weekday vs Weekend Analysis')
df_day['day_type'] = df_day['weekday'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
day_type_rentals = df_day.groupby('day_type')['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='day_type', y='cnt', data=day_type_rentals, ax=ax, palette='viridis')
ax.set_title('Average Bike Rentals: Weekday vs Weekend')
ax.set_xlabel('Day Type')
ax.set_ylabel('Average Rentals')
st.pyplot(fig)
st.write("""
Also that the average of bike rental within a weekday/weekend is pretty similar, but considering a weekend is only 2/7 days, this conclude that the number of bike rental on the weekend is far more than on the weekday.
""")

# Yearly Trend
st.header('Yearly Trend')
daily_rentals = df_day.groupby('dteday')['cnt'].sum().reset_index()

fig, ax = plt.subplots(figsize=(15, 6))
sns.lineplot(x='dteday', y='cnt', data=daily_rentals, ax=ax, palette='viridis')
ax.set_title('Bike Rentals Over the Year')
ax.set_xlabel('Date')
ax.set_ylabel('Total Rentals')
plt.xticks(rotation=45)
st.pyplot(fig)

st.write("""
We can see a trend where the bike rental tend to lower on each early years (these might come from the weather issues).
""")

st.header('Conclusion')

st.write("""
Based on our analysis of the bike-sharing data, we can draw several key conclusions about usage patterns and the factors that influence bike rentals:

**Seasonal Impact:**

Fall emerges as the most popular season for bike rentals, with more than double the rentals of spring, the least popular season. This suggests a strong seasonal influence on bike-sharing usage.


**Weather Sensitivity:**


Weather conditions play a crucial role in rental decisions. Clear weather significantly boosts rentals, while adverse conditions like snow or heavy rain drastically reduce usage. This highlights the importance of weather forecasting in predicting and managing bike availability.


**Daily Usage Patterns:**


Two distinct peak rental periods are observed at 8 AM and 5 PM, coinciding with typical commute times. This pattern indicates that a significant portion of users likely use the bike-sharing service for commuting to and from work or school.


**Weekend vs. Weekday Usage:**


While the average daily rentals are similar for weekdays and weekends, the fact that weekends account for only 2/7 of the week implies a much higher rental rate on weekends. This suggests different usage patterns and purposes between weekdays (likely commuting) and weekends (likely leisure).


**Yearly Trends:**


The observation of lower rental numbers at the beginning of each year, possibly due to weather issues, points to consistent yearly cycles in the bike-sharing system usage.


""")
