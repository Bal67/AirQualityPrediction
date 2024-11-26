import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Step 1: Fetch Weather Data from OpenWeatherMap
def fetch_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return {
            "Temperature": data['main']['temp'],
            "Humidity": data['main']['humidity'],
            "Wind_Speed": data['wind']['speed']
        }
    else:
        print(f"Error fetching weather data: {response.status_code}")
        return {"Temperature": None, "Humidity": None, "Wind_Speed": None}

# Step 2: Simulate Air Quality Data (Replace with Real Data Later)
def generate_air_quality_data(weather_data):
    # Simulate AQI based on weather conditions (mock data for now)
    return 50 + (weather_data["Temperature"] * 0.5) - (weather_data["Wind_Speed"] * 0.2) + (weather_data["Humidity"] * 0.3)

# Step 3: Create Dataset
def create_dataset(api_key):
    city = "Durham"  # Replace with your city of interest
    weather_data = fetch_weather_data(city, api_key)
    
    if weather_data["Temperature"] is not None:
        # Generate mock AQI based on weather data
        air_quality = generate_air_quality_data(weather_data)
        # Combine into a single row of data
        combined_data = {
            "City": city,
            "Temperature": weather_data["Temperature"],
            "Humidity": weather_data["Humidity"],
            "Wind_Speed": weather_data["Wind_Speed"],
            "Air_Quality_Index": air_quality,
            "Traffic_Density": 150  # Mock traffic density
        }
        return pd.DataFrame([combined_data])
    else:
        print("Failed to fetch weather data.")
        return pd.DataFrame()

# Step 4: Train a Simple Linear Regression Model
def train_model(data):
    # Prepare features and target
    X = data[['Traffic_Density', 'Temperature', 'Humidity', 'Wind_Speed']]
    y = data['Air_Quality_Index']
    
    # Add mock rows for training (to expand the dataset)
    for i in range(10):  # Generate 10 mock rows
        data.loc[len(data)] = {
            "City": "Durham",
            "Temperature": data['Temperature'][0] + i,
            "Humidity": data['Humidity'][0] - i,
            "Wind_Speed": data['Wind_Speed'][0] + (i % 2),
            "Air_Quality_Index": data['Air_Quality_Index'][0] + (i % 3),
            "Traffic_Density": data['Traffic_Density'][0] + (i % 10)
        }
    
    # Redefine features and target with expanded dataset
    X = data[['Traffic_Density', 'Temperature', 'Humidity', 'Wind_Speed']]
    y = data['Air_Quality_Index']
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predict and evaluate
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")
    
    # Plot Actual vs Predicted AQI
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, predictions, alpha=0.7)
    plt.xlabel('Actual AQI')
    plt.ylabel('Predicted AQI')
    plt.title('Actual vs Predicted Air Quality Index')
    plt.show()

# Main Script
if __name__ == "__main__":
    api_key = "199249f5bd325ce6045dbf167195de7a"  # Your OpenWeatherMap API Key
    dataset = create_dataset(api_key)
    
    if not dataset.empty:
        print("Dataset Created:")
        print(dataset.head())
        train_model(dataset)
    else:
        print("No data to train the model.")
