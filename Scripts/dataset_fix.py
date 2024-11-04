import feedparser

# URL of the RSS feed
url = "https://feeds.enviroflash.info/rss/realtime/1029.xml?id=97FA79B0-C12F-4FBC-801D34F8ED6AE707"

# Parse the RSS feed
feed = feedparser.parse(url)

# Print out feed information
print("Feed Title:", feed.feed.title)
print("Feed Link:", feed.feed.link)
print("Feed Description:", feed.feed.description)

# Loop through each item in the feed
for item in feed.entries:
    print("\nTitle:", item.title)
    print("Link:", item.link)
    print("Description:", item.description)
    print("Published Date:", item.published)

