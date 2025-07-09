import os
import requests
from dotenv import load_dotenv

load_dotenv()

class BigCommerceAPI:
    def __init__(self):
        self.base_url = f"https://api.bigcommerce.com/stores/{os.getenv('BIGCOMMERCE_STORE_HASH')}/v3"
        self.headers = {
            "X-Auth-Token": os.getenv("BIGCOMMERCE_ACCESS_TOKEN"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def get_all_products(self):
        products = []
        endpoint = f"{self.base_url}/catalog/products?include=variants,images,custom_fields&limit=250"
        while endpoint:
            resp = requests.get(endpoint, headers=self.headers)
            resp.raise_for_status()
            data = resp.json()
            products.extend(data['data'])

            # Handle relative pagination URLs
            next_link = data['meta'].get('pagination', {}).get('links', {}).get('next')
            if next_link and next_link.startswith("?"):
                endpoint = f"{self.base_url}/catalog/products{next_link}"
            else:
                endpoint = next_link
        return products
