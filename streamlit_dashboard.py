import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Set Streamlit page configuration
st.set_page_config(page_title="Weather Data Dashboard", layout="wide")

def load_data_from_sqlite():
    """
    Load weather data from an SQLite database.
    Returns:
        dict: A dictionary where keys are table names and values are corresponding DataFrames.
    """
    conn = sqlite3.connect('central_west_data.db')
    table_names = [
        'avg_temp_over_time',
        'monthly_precipitation',
        'data_count_by_station',
        'extreme_conditions'
    ]
    data = {name: pd.read_sql(f"SELECT * FROM {name}", conn) for name in table_names}
    conn.close()
    return data

data = load_data_from_sqlite()

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Story", "Questions", "Summary and Insights", "Sample Rows", "Visualizations"])

if page == "Story":
    # Display the story and data background
    st.title("The Story")
    st.markdown("""
    ### Central West Brazil Weather Analysis
    This dashboard explores weather patterns in Central West Brazil using data from 623 weather stations. 

    #### About the Data:
    - **Source**: INMET (National Meteorological Institute of Brazil).
    - **Data Points**: The dataset contains over 11 million rows, covering hourly weather data.
    - **Key Variables**: Temperature, precipitation, wind speed, solar radiation, and more.
    - **Focus Area**: Central West Brazil, a region known for its diverse climate and critical agricultural activities.

    #### Objectives:
    The analysis aims to:
    - Identify seasonal patterns in temperature and precipitation.
    - Understand the spatial distribution of extreme weather conditions.
    - Provide actionable insights for agriculture and environmental planning.
    """)

elif page == "Questions":
    # Display key research questions
    st.title("Key Questions")
    st.markdown("""
    ### The key questions our analysis answers:
    1. What is the average temperature throughout each period?
    2. What is the total amount of precipitation at each station and month?
    3. How many lines(Measurements) are there at each station?
    4. What are the maximum and minimum temperatures and maximum wind speed at each station?
    """)

elif page == "Summary and Insights":
    # Display key findings and recommendations
    st.title("Summary and Insights")
    st.markdown("""
    ### Key Findings:
    - **Temperature Trends**: The northern areas of Central West Brazil consistently show higher average temperatures.
    - **Rainfall Patterns**: Rainfall peaks during January and February, with notable dry seasons in mid-year.
    - **Extreme Conditions**: High wind speeds are strongly associated with mountainous regions, suggesting increased vulnerability to extreme weather.

    ### Recommendations:
    - Implement water management systems to utilize peak rainfall periods.
    - Monitor northern regions for heatwaves and their potential impact on agriculture.
    - Enhance infrastructure in mountainous areas to withstand extreme wind conditions.
    """)

elif page == "Sample Rows":
    # Display sample data from the database tables
    st.title("Sample Data from Tables")
    for name, df in data.items():
        st.subheader(f"Table: {name}")
        st.dataframe(df.style.background_gradient(cmap="viridis"))

elif page == "Visualizations":
    # Display visualizations
    st.title("Visualizations")

    # Display average temperature over time with a line plot
    st.header("Average Temperature Over Time")
    avg_temp_data = data['avg_temp_over_time']
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(avg_temp_data['YearMonth'], avg_temp_data['AvgTemp'], marker='o')
    ax.set_title('Average Temperature Over Time', fontsize=16)
    ax.set_xlabel('Year-Month', fontsize=12)
    ax.set_ylabel('Average Temperature (°C)', fontsize=12)
    st.pyplot(fig)

    # Display monthly precipitation by station with a bar plot
    st.header("Monthly Precipitation by Station")
    precipitation_data = data['monthly_precipitation']
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(x='YearMonth', y='TotalPrecipitation', data=precipitation_data.head(50), ax=ax)
    ax.set_title('Monthly Precipitation by Station', fontsize=16)
    ax.set_xlabel('Year-Month', fontsize=12)
    ax.set_ylabel('Total Precipitation (mm)', fontsize=12)
    st.pyplot(fig)

    # Display a word cloud for weather stations
    st.header("Weather Stations Word Cloud")
    stations_text = ' '.join(data['data_count_by_station']['station'])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(stations_text)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

    # Display temperature extremes for a selected weather station
    st.header("Temperature Extremes by Station")
    selected_station = st.selectbox("Select a Station:", data['extreme_conditions']['station'].unique())
    station_data = data['extreme_conditions'][data['extreme_conditions']['station'] == selected_station]
    st.write(station_data)

    # Display monthly precipitation trends with a slider to select a specific month
    st.header("Monthly Precipitation Trends")
    month_filter = st.slider("Select Year-Month (index):", 0, len(precipitation_data) - 1, 0)
    st.write(precipitation_data.iloc[month_filter])
