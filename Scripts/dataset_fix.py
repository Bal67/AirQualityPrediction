import feedparser
from bs4 import BeautifulSoup
import pandas as pd

# URL of the RSS feed
url = "https://feeds.enviroflash.info/rss/realtime/1029.xml?id=BAD876E6-F099-83BF-D81013A0D324A577"

# Parse the RSS feed
feed = feedparser.parse(url)

# Initialize lists to store the extracted data
locations = []
current_aqi = []
pollutants = []
agencies = []
last_updates = []

# Loop through each item in the feed and extract data
for item in feed.entries:
    # Parse the HTML in the description using BeautifulSoup
    soup = BeautifulSoup(item.description, "html.parser")

    # Extract location
    location = soup.find('b', text='Location:').next_sibling.strip()
    locations.append(location)

    # Extract current air quality information
    aqi_info = soup.find('div').find_next_sibling('div').text.strip().split("\n")
    aqi_details = [info.strip() for info in aqi_info if info.strip() != ""]
    current_aqi.append(aqi_details[0])  # AQI value and pollutant type
    pollutants.append(aqi_details[1])   # Additional pollutant information

    # Extract agency
    agency = soup.find('b', text='Agency:').next_sibling.strip()
    agencies.append(agency)

    # Extract last update
    last_update = soup.find('i').text.strip()
    last_updates.append(last_update)

# Create a DataFrame from the extracted data
data = {
    "Location": locations,
    "Current AQI": current_aqi,
    "Pollutants": pollutants,
    "Agency": agencies,
    "Last Update": last_updates
}
df = pd.DataFrame(data)

# Display the DataFrame
print(df)

# Save the DataFrame to a CSV file (optional)
df.to_csv("air_quality_data.csv", index=False)
