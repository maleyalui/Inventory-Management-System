# Inventory-Management-System
    **Author: ** Luie

A simple Inventory Management System built with Flask and a Python CLI client.
It supports CRUD operations and intergrates with Open Food Facts API to fetch product details.

---

## Features
    - View all inventory items
    - View a single item by id
    - Add new items
    - Update existing items (stock, price, name)
    - Delete item
    - Search products via external API(Open Food Facts)
    - CLI based interaction

---

## Installation & Setup

### 1. Clone the repository
```bash
    git clone <your-repo-url>
    cd Inventory-Management-System
```

### 2. Create a virtual enviroment
```bash
    python -m venv venv
    source venv/bin/activate
```

### 3. Install dependancies
```bash
    pip install flask requests pytest
```

## Running the Application

### Start Flask Server
```bash
    python app.py
```

### Server runs on:
``` bash
    http://127.0.0.1:5000
```

## Run CLI
In a new terminal:
```bash
    python cli.py
```

## API Endpoints

### 1. Get All Inventory
```bash
    GET /inventory
```

### 2. Get Single Item
```bash
    GET /inventory/<id>
```

### 3. Add New Item
```bash
    POST /inventory
```

#### Body:
    ```bash
    {
        "product_name": "Milk",
        "stock": 10,
        "price": 200,
        "barcode": "12345678"
    }
    ```
### 4. Update Item
``` bash
PATCH /inventory/<id>
```

#### Body:
```bash
{
    "stock": 50,
    "price": 300,
    "product_name": "Updated Name"
}
```

### 5. Delete Item
```bash
DELETE /inventory/<id>
```

## CLI Usage Example

After running python cli.py:

### View Inventory
```bash
    Choose 1-7: 1
```

### View Single Item
```bash
Choose 1-7: 2
Enter ID: 1
```

### Add Item
``` bash
Choose 1-7: 3
Product name: Milk
Barcode: 123456
Stock quantity: 10
Price: 200
```

### Update Item
``` bash
Choose 1-7: 4
Item Id to update: 1
New stock: 100
New price: 500
```

### Delete Item
```bash
Choose 1-7: 5
Item Id to delete: 1
```

### Search Product
```bash
Choose 1-7: 6
Search by 1. Barcode or 2. Name? 2
Product name: milk
```

## Running tests
``` bash
python -m pytest
```

## Author
Luis Maleya.