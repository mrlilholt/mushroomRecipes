from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

def scrape_recipes(mushroom):
    url = f"https://www.allrecipes.com/search?q={mushroom.replace(' ', '+')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    recipes = []

    for card in soup.find_all('div', class_='card__content'):
        try:
            # Title
            title_tag = card.find('span', class_='card__title-text')
            title = title_tag.text.strip() if title_tag else "No Title"

            # Link
            parent_a_tag = card.find_parent('a')
            link = parent_a_tag['href'] if parent_a_tag and 'href' in parent_a_tag.attrs else "No Link"

            # Image
            card_top = card.find_previous_sibling('div', class_='loc card__top')
            img_tag = card_top.find('img') if card_top else None
            image_url = img_tag.get('data-src') or img_tag.get('src', "No Image") if img_tag else "No Image"

            # Rating
            stars = len(card.find_all('use', href="#icon-star"))
            half_stars = len(card.find_all('use', href="#icon-star-half"))
            rating = stars + (0.5 * half_stars)

            # Number of ratings
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
            print(f"Error: {e}")

    return recipes

@app.route('/search', methods=['GET'])
def search_recipes():
    mushroom = request.args.get('mushroom', '')
    if not mushroom:
        return jsonify({"error": "No mushroom type provided"}), 400

    results = scrape_recipes(mushroom)
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


