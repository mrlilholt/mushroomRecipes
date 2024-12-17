from bs4 import BeautifulSoup
import requests
import re  # For cleaning text

def scrape_recipes(mushroom):
    url = f"https://www.allrecipes.com/search?q={mushroom.replace(' ', '+')}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    recipes = []

    # Find recipe cards
    for card in soup.find_all('div', class_='card__content'):
        try:
            # Extract title
            title_tag = card.find('span', class_='card__title-text')
            title = title_tag.text.strip() if title_tag else "No Title"

            # Extract link
            parent_a_tag = card.find_parent('a')
            link = parent_a_tag['href'] if parent_a_tag and 'href' in parent_a_tag.attrs else "No Link"

            # Extract image from the card__top div
            card_top = card.find_previous_sibling('div', class_='loc card__top')
            img_tag = card_top.find('img') if card_top else None
            image_url = img_tag.get('data-src') or img_tag.get('src', "No Image") if img_tag else "No Image"

            # Extract star rating
            stars = len(card.find_all('use', href="#icon-star"))
            half_stars = len(card.find_all('use', href="#icon-star-half"))
            rating = stars + (0.5 * half_stars)

            # Extract number of ratings
            ratings_count_tag = card.find('div', class_='mm-recipes-card-meta__rating-count-number')
            ratings_count = re.sub(r'\D', '', ratings_count_tag.text.strip()) if ratings_count_tag else "0"

            # Append the data
            recipes.append({
                'title': title,
                'link': link,
                'image_url': image_url,
                'rating': rating,
                'ratings_count': int(ratings_count) if ratings_count.isdigit() else 0
            })
        except Exception as e:
            print(f"Error parsing recipe card: {e}")

    return recipes

# Example usage
mushroom_type = "chanterelle"
results = scrape_recipes(mushroom_type)

# Display results
if results:
    print(f"Recipes for {mushroom_type.capitalize()}:")
    for recipe in results:
        print(f"- {recipe['title']}: {recipe['link']}")
        print(f"  Image: {recipe['image_url']}")
        print(f"  Rating: {recipe['rating']} stars ({recipe['ratings_count']} ratings)")
else:
    print(f"No recipes found for {mushroom_type}.")
