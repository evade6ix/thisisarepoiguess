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

    def get_all_brands(self):
        brands = {}
        endpoint = f"{self.base_url}/catalog/brands?limit=250"
        while endpoint:
            resp = requests.get(endpoint, headers=self.headers)
            resp.raise_for_status()
            data = resp.json()
            for b in data['data']:
                brands[b['id']] = b['name']
            next_link = data['meta'].get('pagination', {}).get('links', {}).get('next')
            if next_link and next_link.startswith("?"):
                endpoint = self.base_url + "/catalog/brands" + next_link
            else:
                endpoint = next_link
        return brands

    def get_all_products(self):
        brands = self.get_all_brands()
        products = []
        endpoint = f"{self.base_url}/catalog/products?include=variants,images,custom_fields&limit=250"
        while endpoint:
            resp = requests.get(endpoint, headers=self.headers)
            resp.raise_for_status()
            data = resp.json()
            for p in data['data']:
                # Attach brand_name to each product
                p['brand_name'] = brands.get(p['brand_id'], "Unknown")
            products.extend(data['data'])
            next_link = data['meta'].get('pagination', {}).get('links', {}).get('next')
            if next_link and next_link.startswith("?"):
                endpoint = self.base_url + "/catalog/products" + next_link
            else:
                endpoint = next_link
        return products
