from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

inventory = [
    {
    "id": 1,
    "product_name": "Organic Almond Milk",
    "brands": "Silk",
    "ingredients_text": "Filtered water, almonds, cane sugar, vitamin D2, sea salt.",
    "stock": 50,
    "price": 500,
    "barcode": "073002001000"
    },
    {
    "id": 2,
    "product_name": "Whole Wheat Bread",
    "brands": "Nature's Own",
    "ingredients_text": "Whole wheat flour, water, honey, yeast, salt.",
    "stock": 30,
    "price": 250,
    "barcode": None
    }
]


def fetch_product_details(barcode=None, product_name=None):
    
    if barcode:
        url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == 1 and "product" in data:
                    p =data["product"]
                    return {
                        "product_name": p.get("product_name"),
                        "brands": p.get("brands"),
                        "ingredients_text": p.get("ingredients_text")
                    }
        except:
            return None
        
    elif product_name:
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        params = {
            "search_terms": product_name,
            "search_simple": 1,
            "json": 1,
            "page_size": 1
        }
        try:
            resp = requests.get(url, params=params, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                products = data.get("products, []")
                if products:
                    p = products[0]
                    return {
                        "product_name": p.get("product_name"),
                        "brands": p.get("brands"),
                        "ingredients_text": p.get("ingredients_text")
                    }
                    
        except:
            return None
    return None

@app.route('/inventory', methods=['GET'])
def get_inventory():
    #Fetch all items
    return jsonify(inventory)

@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    #Get only one item
    item = next((i for i in inventory if i['id'] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

@app.route('/inventory', methods=['POST'])
def add_item():
    #adds a new item
    data =request.get_json()
    if not data or 'product_name' not in data:
        return jsonify({"error": "product name is required"}), 400
    
    barcode = data.get('barcode')
    details = fetch_product_details(barcode=barcode) if barcode else None
    
    if details:
        if not data.get('brands'):
            data['brands'] = details.get('brands')
        if not data.get('ingredients_text'):
            data['ingredients_text'] = details.get('ingredients_text')
            
    
    #Generate a ner ID
    new_id = max((i['id'] for i in inventory), default=0) + 1
    new_item = {
        "id": new_id,
        "product_name": data['product_name'],
        "brands": data.get('brands', 'Unknown'),
        "ingredients_text": data.get('ingredients_text', 'N/A'),
        "stock": int(data.get('stock', 0)),
        "price": float(data.get('price', 0.0)),
        "barcode": barcode
    }
    inventory.append(new_item)
    return jsonify(new_item), 201

@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    #to update an item
    item = next((i for i in inventory if i['id'] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    data = request.get_json()
    if 'stock' in data:
        item['stock'] = int(data['stock'])
    if 'price' in data:
        item['price'] = float(data['price'])
        
    return jsonify(item)

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory
    item = next((i for i in inventory if i['id'] == item_id), None)
    if not item:
        return jsonify({"error": "item not found"}), 404
    
    inventory = [i for i in inventory if i['id'] != item_id]
    return jsonify({"message": "Item deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)