import requests
from bs4 import BeautifulSoup

# Test imdb page
imdb_reviews_url = "https://www.imdb.com/title/tt0468569/reviews?ref_=tt_urv"

# Send an HTTP request to IMDb
response = requests.get(imdb_reviews_url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Extract the reviews and their ratings
reviews = soup.find_all("div", class_="text show-more__control")
ratings = soup.find_all("span", class_="rating-other-user-rating")

# Display each review along with its rating
for index, review in enumerate(reviews, start=1):
    review_text = review.text.strip()
    rating_text = ratings[index - 1].text.strip()
    print(f"Review {index}:")
    print(f"Rating: {rating_text}")
    print(f"Content: {review_text}\n")

