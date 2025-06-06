from database import setup_database, get_db_connection
from weather_api import get_weather
import datetime

def save_weather_data(weather):
    """Save weather data to PostgreSQL"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO weather 
                (city, country, temperature_c, wind_kph, wind_direction, humidity, condition_text, last_updated)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                weather['city'],
                weather['country'],
                weather['temperature_c'],
                weather['wind_kph'],
                weather['wind_direction'],
                weather['humidity'],
                weather['condition'],
                weather['last_updated']
            ))
            conn.commit()
            print("Weather data saved successfully!")
        except Exception as e:
            print(f"Error saving data: {e}")
        finally:
            conn.close()

def show_recent_data():
    """Show 5 most recent weather records"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('''
                SELECT city, temperature_c, wind_kph, condition_text, recorded_at 
                FROM weather 
                ORDER BY recorded_at DESC 
                LIMIT 5
            ''')
            records = cur.fetchall()
            
            print("\nRecent Weather Data:")
            for record in records:
                print(f"{record[0]}: {record[1]}°C, Wind: {record[2]} kph, {record[3]} (at {record[4]})")
        except Exception as e:
            print(f"Error fetching data: {e}")
        finally:
            conn.close()

def main():
    # Setup database on first run
    setup_database()
    
    while True:
        print("\nWeather Data Collector")
        print("1. Get current weather")
        print("2. View recent data")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            city = input("Enter city name: ")
            weather = get_weather(city)
            if weather:
                print(f"\nCurrent weather in {weather['city']}, {weather['country']}:")
                print(f"Temperature: {weather['temperature_c']}°C")
                print(f"Wind: {weather['wind_kph']} kph from {weather['wind_direction']}")
                print(f"Conditions: {weather['condition']}")
                print(f"Humidity: {weather['humidity']}%")
                print(f"Last updated: {weather['last_updated']}")
                
                save = input("Save this data? (y/n): ").lower()
                if save == 'y':
                    save_weather_data(weather)
        
        elif choice == '2':
            show_recent_data()
        
        elif choice == '3':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()