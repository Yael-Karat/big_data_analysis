import duckdb
import sqlite3
import matplotlib.pyplot as plt

# Define the name of the CSV file
csv_file_name = 'central_west_hourly_weather_sample.csv'

# Connect to DuckDB
con = duckdb.connect('db_file.duckdb')

# Create the table and load data from the CSV file
con.execute(f"""
    CREATE TABLE central_west_data AS 
    SELECT * FROM read_csv_auto('{csv_file_name}');
""")

# Verify the table structure and row count
print("Table central_west_data created.")
table_info = con.execute("PRAGMA table_info('central_west_data');").fetchdf()
print("Columns in the table:")
print(table_info)

row_count = con.execute("SELECT COUNT(*) AS row_count FROM central_west_data;").fetchone()[0]
print(f"Row count in central_west_data: {row_count}")


# Function to execute DuckDB query and return as pandas DataFrame
def duckdb_to_pandas(query):
    return con.execute(query).df()


# Question 1: Average Temperature Over Time
avg_temp_over_time = duckdb_to_pandas(''' 
    SELECT DISTINCT
        strftime('%Y-%m', Data) AS YearMonth,
        AVG("TEMPERATURA DO AR - BULBO SECO, HORARIA (\u00b0C)") 
            OVER(PARTITION BY strftime('%Y-%m', Data)) AS AvgTemp
    FROM central_west_data
    ORDER BY YearMonth;
''')

# Visualization for Question 1
avg_temp_over_time.plot(x='YearMonth', y='AvgTemp', kind='line', title='Average Temperature Over Time')
plt.xlabel('Year-Month')
plt.ylabel('Average Temperature (\u00b0C)')
plt.show()

# Question 2: Monthly Precipitation by Station
monthly_precipitation = duckdb_to_pandas(''' 
    SELECT 
        strftime('%Y-%m', Data) AS YearMonth,
        station, 
        SUM("PRECIPITA\u00c7\u00c3O TOTAL, HOR\u00c1RIO (mm)") AS TotalPrecipitation
    FROM central_west_data
    GROUP BY CUBE (YearMonth, station)
    HAVING YearMonth IS NOT NULL AND station IS NOT NULL
    ORDER BY YearMonth, station;
''')

# Visualization for Question 2
monthly_precipitation.plot(x='YearMonth', y='TotalPrecipitation', kind='line', title='Monthly Precipitation by Station')
plt.xlabel('Year-Month')
plt.ylabel('Total Precipitation (mm)')
plt.show()

# Question 3: Data Count by Station
data_count_by_station = duckdb_to_pandas(''' 
    SELECT 
        station, 
        COUNT(*) AS DataCount
    FROM central_west_data
    GROUP BY station
    ORDER BY DataCount DESC
''')

# Visualization for Question 3
data_count_by_station.plot(x='station', y='DataCount', kind='bar', title='Data Count by Station')
plt.xlabel('Station')
plt.ylabel('Data Count')
plt.show()

# Question 4: Extreme Conditions by Station
extreme_conditions = duckdb_to_pandas(''' 
    SELECT 
        station, 
        MAX("TEMPERATURA DO AR - BULBO SECO, HORARIA (\u00b0C)") AS MaxTemp,
        MIN("TEMPERATURA DO AR - BULBO SECO, HORARIA (\u00b0C)") AS MinTemp,
        MAX("VENTO, VELOCIDADE HORARIA (m/s)") AS MaxWindSpeed
    FROM central_west_data
    GROUP BY station
    ORDER BY MaxTemp DESC
''')

# Visualization for Question 4
extreme_conditions.plot(x='station', y=['MaxTemp', 'MinTemp', 'MaxWindSpeed'], kind='bar', title='Extreme Conditions by Station')
plt.xlabel('Station')
plt.ylabel('Value')
plt.show()

# Create smaller sample tables (for SQLite export)
avg_temp_over_time_sample = avg_temp_over_time.head(500)
monthly_precipitation_sample = monthly_precipitation.head(500)
data_count_by_station_sample = data_count_by_station.head(500)
extreme_conditions_sample = extreme_conditions.head(500)

table_mappings = {
    'avg_temp_over_time': avg_temp_over_time_sample,
    'monthly_precipitation': monthly_precipitation_sample,
    'data_count_by_station': data_count_by_station_sample,
    'extreme_conditions': extreme_conditions_sample
}

# Save the results to SQLite
sqlite_conn = sqlite3.connect('central_west_data.db')
for table_name, df in table_mappings.items():
    df.to_sql(table_name, sqlite_conn, if_exists='replace', index=False)
    print(f"Table {table_name} saved to SQLite.")

# Verify the data in SQLite
for table_name in table_mappings.keys():
    rows = sqlite_conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    print(f"Table {table_name} in SQLite has {rows} rows.")

# Close the DuckDB connection
con.close()
print("DuckDB connection closed.")

# Close the SQLite connection
sqlite_conn.close()
print("SQLite connection closed.")
