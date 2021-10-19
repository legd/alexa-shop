from flask import Flask
import requests

API_KEY = "12420d8d5641aca0f72f5aad518eebcf"
API_PASSWORD = "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"
API_BASE_URL = "https://{}:{}@devstorelegd.myshopify.com/admin/api/2021-10".format(API_KEY, API_PASSWORD)

app = Flask(__name__)

shopping_cart = {}
products_list = []

def get_product_by_id(product_id):
    """Helper function to get product deatils from the Shopify API."""
    endpoint_parameter = "/products/{}.json".format(product_id)
    response = requests.get("{}{}".format(API_BASE_URL, endpoint_parameter))
    if response.status_code == 200:
        res = response.json()
        product = res['product']
        return "A {} is {}, the price is {} and the availability is {}".format(product['title'], product['body_html'], product['variants'][0]['price'], product['variants'][0]['inventory_quantity']) 
    else:
        return "I had trouble getting the product you ask."

def get_product_by_name(product_name):
    """Helper function to search product by name in the list of products."""
    response = requests.get("{}{}".format(API_BASE_URL, "/products.json"))
    if response.status_code == 200:
        products = response.json()
        for product in products['products']:
            if product['title'].lower() == product_name.lower():
                return get_product_by_id(product['id'])

        return "Sorry! I couldn't find any result for {}".format(product_name) 
    else:
        return "I had trouble getting the available products."

@app.route("/")
def home():
    """home route"""
    return "Hello! welcome to test page."

@app.route("/products")
def list_products():
    """Endpoint to get all the available products."""
    products_names = []
    response = requests.get("{}{}".format(API_BASE_URL, "/products.json"))
    if response.status_code == 200:
        products = response.json()
        for product in products['products']:
            products_list.append(product)
            products_names.append(product['title'])
        return "The available products are: {}".format(",".join(products_names)) 
    else:
        return "I had trouble getting the available products."

@app.route("/products/<product_name>")
def get_product(product_name):
    """Endpoint to get information about a product."""
    if len(products_list) > 0:
        for product in products_list:
            if product['title'].lower() == product_name.lower():
                return get_product_by_id(product['id'])
                
        return "Sorry! I couldn't find any result for {}".format(product_name)
    else:
        return get_product_by_name(product_name)

@app.route("/cart/<product_name>/<quantity>")
def add_product(product_name, quantity):
    """Endpoint to add a product to the shopping cart."""
    for product in products_list:
        if product['title'].lower() == product_name.lower():
            if int(product['variants'][0]['inventory_quantity']) < int(quantity):
                return "Sorry! we don't have that number in the inventory, please try again!"
            else:
                shopping_cart[product['title']] = (quantity, product)
                return "{} {} added to the shopping cart".format(quantity, product_name)

@app.route("/cart")
def list_shopping_cart():
    """Endpoint to list all item in the shopping cart plus the total amount."""
    total = 0.0
    products_and_quantities = []
    if len(shopping_cart) > 0:
        for key in shopping_cart:
            quantity = shopping_cart[key][0]
            product = shopping_cart[key][1]
            total += float(product['variants'][0]['price']) * float(quantity)
            products_and_quantities.append("{} {}".format(quantity, key))

        return "Your shopping cart has {} for a total of {}".format(",".join(products_and_quantities), total)
    else:
        return "You don't have products in your shopping cart, please add products."

@app.route("/order")
def place_order():
    """Endpoint to palce an order."""
    if len(shopping_cart) > 0:
        total = 0.0
        products_list = []
        for key in shopping_cart:
            quantity = shopping_cart[key][0]
            product = shopping_cart[key][1]
            total += float(product['variants'][0]['price']) * float(quantity)
            products_list.append({'id':product['id'],'title':product['title'],'price':product['variants'][0]['price'],'taxable':False,'quantity':int(quantity)})

        url = "https://devstorelegd.myshopify.com/admin/api/2021-10/draft_orders.json"
        headers = {'X-Shopify-Access-Token': API_PASSWORD}
        order = {'draft_order': {'line_items': products_list}}
        response = requests.post(url, json=order, headers=headers)
        if response.status_code == 201:
            shopping_cart.clear()
            return "Your order for a total of {} was placed.".format(total)
        else :
            return "I had trouble creating the order."
    else:
        return "You don't have products in your shopping cart, please add products."

if __name__ == "__main__":
    app.run()
