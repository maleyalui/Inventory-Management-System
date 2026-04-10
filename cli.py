import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def fetch_product_details(barcode=None, product_name=None):
    
    if barcode:
        url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == 1 and "product" in data:
                    p= data["product"]
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
                products = data.get("products", [])
                if products:
                    p=products[0]
                    return {
                        "product_name": p.get("product_name"),
                        "brands": p.get("brands"),
                        "ingredients_text": p.get("ingredients_text")
                    }
        except Exception as e:
            print("Error:", e)
            return None
    return None


def main():
    print("-- Inventory Management --")
    
    while True:
        print("\n1. View all inventory")
        print("2. View single item by ID")
        print("3. Add new item")
        print("4. Update item")
        print("5. Delete item")
        print("6. Search")
        print("7. Exit")
        choice = input("Choose 1-7: ").strip()
        
        if choice == "1":
            r =requests.get(f"{BASE_URL}/inventory")
            print(json.dumps(r.json(), indent=2) if r.ok else "Error")
            
        elif choice == "2":
            iid = input("Enter ID: ")
            r =requests.get(f"{BASE_URL}/inventory/{iid}")
            print(json.dumps(r.json(), indent=2) if r.ok else r.json())
            
        elif choice == "3":
            name = input("Product name: ")
            barcode = input("Barcode: ") or None
            stock = input("Stock quantity: ") or "0"
            price = input("Price: ") or 0
            payload = {"product_name": name, "stock": int(stock), "price":float(price)}
            if barcode:
                payload["barcode"] = barcode
            
            r = requests.post(f"{BASE_URL}/inventory", json = payload)
            print(json.dumps(r.json(), indent=2) if r.ok else r.json())
        
        elif choice == "4":
            iid = input("Item Id to update: ")
            stock = input("New stock: ")
            price = input("New price: ")
            payload = {}
            if stock:
                payload["stock"] = int(stock)
            if price:
                payload["price"] = float(price)
                if not payload:
                    print("Nothing changed: ")
                    continue
            
            r = requests.patch(f"{BASE_URL}/inventory/{iid}", json=payload)
            print(json.dumps(r.json(), indent=2) if r.ok else r.json())
            
        elif choice == "5":
            iid = input("Item Id to delete: ")
            r =requests.delete(f"{BASE_URL}/inventory/{iid}")
            print(r.json() if r.ok else "Error")
            
        elif choice == "6":
            typ = input("Search by 1. Barcode or 2. Name? ")
            if typ == "1":
                bd = input("Barcode: ")
                data =fetch_product_details(barcode=bd)
            else:
                name = input("Product name: ")
                data = fetch_product_details(product_name=name)
            print(json.dumps(data, indent=2) if data else "No data found or API error")
                
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")
            
if __name__ == "__main__":
    main()