import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io

# OpenWeather API
API_KEY = '6e6f9659fef62e5c5d1103979100d281'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Function to fetch and display weather
def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    request_url = f"{BASE_URL}?appid={API_KEY}&q={city}"
    response = requests.get(request_url)

    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description'].capitalize()
        temperature = round(data['main']['temp'] - 273.15, 2)  # Convert Kelvin to Celsius
        icon_code = data['weather'][0]['icon']

        weather_label.config(text=f"Weather: {weather}", foreground="black")
        temp_label.config(text=f"Temperature: {temperature}°C", foreground="black")

        # Fetch and display weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
        icon_response = requests.get(icon_url)
        if icon_response.status_code == 200:
            img_data = Image.open(io.BytesIO(icon_response.content))
            img_resized = img_data.resize((70, 70), Image.LANCZOS)
            weather_icon = ImageTk.PhotoImage(img_resized)
            icon_label.config(image=weather_icon)
            icon_label.image = weather_icon
    else:
        messagebox.showerror("Error", "City not found. Try again.")

# Creating the GUI window
root = tk.Tk()
root.title("Weather App 🌤")
root.geometry("400x450")
root.resizable(False, False)
root.configure(bg="#E3F2FD")

# Title Label
title_label = ttk.Label(root, text="Weather Checker 🌍", font=("Arial", 18, "bold"), background="#E3F2FD")
title_label.pack(pady=10)

# Entry Frame
frame = tk.Frame(root, bg="#E3F2FD")
frame.pack(pady=10)

city_entry = ttk.Entry(frame, width=30, font=("Arial", 12))
city_entry.grid(row=0, column=0, padx=10)

get_weather_btn = ttk.Button(frame, text="Get Weather", command=get_weather)
get_weather_btn.grid(row=0, column=1)

# Weather Icon
icon_label = tk.Label(root, bg="#E3F2FD")
icon_label.pack(pady=10)

# Weather Info Labels
weather_label = ttk.Label(root, text="", font=("Arial", 14), background="#E3F2FD")
weather_label.pack(pady=5)

temp_label = ttk.Label(root, text="", font=("Arial", 14), background="#E3F2FD")
temp_label.pack(pady=5)

# Run the GUI
root.mainloop()
