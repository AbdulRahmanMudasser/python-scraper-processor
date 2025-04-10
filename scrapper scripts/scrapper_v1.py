import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from link import LINK

for i in range(2, 10):
    BASE_URL = LINK
    SAVE_DIR = "scrapped_images_v1/"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def sanitize_filename(name):
        """Clean filename from special characters"""
        return "".join([c if c.isalnum() or c in ('-', '_', ' ') else '_' for c in name])

    def scrape_fertilizer_images():
        # Create directory if not exists
        os.makedirs(SAVE_DIR, exist_ok=True)
        
        # Get the page content
        response = requests.get(BASE_URL, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all product containers
        products = soup.select('div.product-wrapper')
        
        if not products:
            print("No products found! Check CSS selectors.")
            return

        for product in products:
            try:
                # Extract image URL - handles both src and srcset
                img_container = product.select_one('div.product-element-top a.product-image-link')
                if not img_container:
                    continue
                    
                img_tag = img_container.find('img')
                if not img_tag:
                    continue

                # Get best available image URL
                img_url = img_tag.get('data-src') or img_tag.get('src') or img_tag.get('srcset', '').split()[0]
                if not img_url.startswith('http'):
                    img_url = urljoin(BASE_URL, img_url)

                # Get product name for filename
                product_name = img_tag.get('alt', 'fertilizer').strip()
                product_name = sanitize_filename(product_name)
                
                # Download image
                img_data = requests.get(img_url, headers=HEADERS).content
                extension = os.path.splitext(img_url)[1].split('?')[0]  # Handle URL parameters
                filename = f"{product_name}{extension if extension else '.jpg'}"
                
                with open(os.path.join(SAVE_DIR, filename), 'wb') as f:
                    f.write(img_data)
                print(f"Downloaded: {filename}")
                
            except Exception as e:
                print(f"Error processing product: {str(e)}")
                continue

    if __name__ == "__main__":
        scrape_fertilizer_images()
        print("Scraping completed!")