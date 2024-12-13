import requests
import tkinter as tk
from tkinter import messagebox

# Function to fetch weather data from OpenWeatherMap API
def fetch_weather_data(api_key, location):
    """
    Fetch weather data from OpenWeatherMap API.

    Args:
        api_key (str): OpenWeatherMap API key.
        location (str): Location (city name or zip code).

    Returns:
        dict: Parsed weather data or error message.
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"  
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"Error: {err}"}


def display_weather_gui(data):
    """
    Display weather data in a messagebox.

    Args:
        data (dict): Weather data from the API.
    """
    if not data or data.get("cod") != 200:
        error_message = data.get("error", "Invalid location or no data available.")
        messagebox.showerror("Error", error_message)
        return

    
    city = data["name"]
    country = data["sys"]["country"]
    weather = data["weather"][0]["description"].capitalize()
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    
    weather_details = (
        f"City: {city}, {country}\n"
        f"Condition: {weather}\n"
        f"Temperature: {temp} °C\n"
        f"Feels Like: {feels_like} °C\n"
        f"Humidity: {humidity}%\n"
        f"Wind Speed: {wind_speed} m/s"
    )

    messagebox.showinfo("Weather Information", weather_details)


def main():
    """
    Main function to run the weather application with GUI.
    """
    
    api_key = "e12ebfdbc89afb1dac92387d9d406b64"  

    if api_key == "your_openweathermap_api_key":
        messagebox.showerror("Error", "Please replace 'your_openweathermap_api_key' with a valid API key.")
        return

    
    root = tk.Tk()
    root.title("Weather App")

    
    tk.Label(root, text="Enter a location (city or zip code):").pack(pady=10)
    location_entry = tk.Entry(root, width=30)
    location_entry.pack(pady=5)

    def get_weather():
        location = location_entry.get().strip()
        if not location:
            messagebox.showerror("Error", "Location cannot be empty.")
            return

        
        weather_data = fetch_weather_data(api_key, location)
        display_weather_gui(weather_data)

    tk.Button(root, text="Get Weather", command=get_weather).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
