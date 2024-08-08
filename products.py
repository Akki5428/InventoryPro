# products.py
import csv
import datetime
from abc import ABC, abstractmethod

class Products(ABC):
    all_products = []
    country = "India"

    def __init__(self, name: str, cost_price: float, mrp: float, quantity: int):
        self.name = name
        self.__cost_price = cost_price
        self._mrp = mrp
        self.quantity = quantity
        self.generateBarcode()
        if None in self.all_products:
            index = self.all_products.index(None)
            Products.all_products[index] = self
        else:
            Products.all_products.append(self)
        self.generateBarcode()

    def generateBarcode(self):
        purchase_date = datetime.datetime.today()
        existing_barcodes = [p.barcode for p in Products.all_products if p is not None and hasattr(p, 'barcode')]
        index = 101
        while True:
            barcode = f"{purchase_date.year}{purchase_date.month:02d}{self.category_code}{index}"
            if barcode not in existing_barcodes:
                self.barcode = barcode
                break
            index += 1

    @abstractmethod
    def show_details(self):
        print(f"------------- Details of {self.name} -------------")
        print(f"Category: {self.category}")
        print(f"Cost price: {self.__cost_price}")
        print(f"MRP: {self._mrp}")
        print(f"Stock: {self.quantity}")
        print(f"Barcode: {self.barcode}")

    @staticmethod
    @abstractmethod
    def addNewItem():
        name = input("Name: ")
        cost_price = float(input("Cost Price: "))
        mrp = float(input("MRP: "))
        quantity = int(input("Quantity: "))
        return name, cost_price, mrp, quantity
    
    def editDetails(self):
        print("\nEnter new details (Press 'Enter' to keep old detail):")
        print("Field\tOld Value\tNew Value".expandtabs(20))
        
        name = input(f"Name\t{self.name}:\t".expandtabs(20))
        if name:
            self.name = name

        cost_price = input(f"Cost price\t{self._Products__cost_price}:\t".expandtabs(20))
        if cost_price:
            self._Products__cost_price = float(cost_price)

        mrp = input(f"MRP\t{self._mrp}:\t".expandtabs(20))
        if mrp:
            self._mrp = float(mrp)

        quantity = input(f"Stock\t{self.quantity}:\t".expandtabs(20))
        if quantity:
            self.quantity = int(quantity)

        # Add any additional fields specific to subclasses here
        
        print("Product details updated successfully!")

    @staticmethod
    def showInventory():
        active_products = [p for p in Products.all_products if p is not None]
        if not active_products:
            print("Your inventory is empty!")
            return False
        print("\nCurrent Inventory:")
        print("Barcode\t\tItem Name")
        for item in active_products:
            print(f"{item.barcode}\t{item.name}")
        barcode = input("Enter barcode number (or press Enter to go back): ")
        if not barcode:
            return False
        for index, product in enumerate(Products.all_products):
            if product and product.barcode == barcode:
                return index
        print("Product not found.")
        return False

    @staticmethod
    def loadFromCSV():
        Products.all_products.clear()  # Clear existing products before loading
        try:
            with open('database.csv', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row:  # Skip empty rows
                        continue
                    try:
                        class_name = row[0]
                        attributes = {}
                        for item in row[1:]:
                            key, value = item.split(':', 1)
                            attributes[key] = value
                        
                        # Ensure cost_price and mrp are included in attributes
                        if '_Products__cost_price' not in attributes or '_mrp' not in attributes:
                            print(f"Warning: Missing cost price or MRP for product {attributes.get('name', 'Unknown')}. Skipping.")
                            continue

                        obj = Products.create_product(class_name, attributes)
                        if obj:
                            print(f"Loaded product: {obj.name} with barcode: {obj.barcode}")
                        else:
                            print(f"Failed to create product from row: {row}")
                    except Exception as e:
                        print(f"Error processing row: {row}. Error: {e}")
                
                print(f"Loaded {len(Products.all_products)} products from database.csv")
        except FileNotFoundError:
            print("No existing inventory found (database.csv). Starting with an empty inventory.")
        except Exception as e:
            print(f"An error occurred while loading the inventory: {e}")
            
    @staticmethod
    def writeToCSV():
        with open('database.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for obj in Products.all_products:
                if obj is not None:
                    row = [obj.__class__.__name__]
                    attributes = {
                        'name': obj.name,
                        '_Products__cost_price': obj._Products__cost_price,
                        '_mrp': obj._mrp,
                        'quantity': obj.quantity,
                        'barcode': obj.barcode
                    }
                    # Add any additional attributes specific to subclasses
                    for key, value in obj.__dict__.items():
                        if key not in attributes and not key.startswith('_'):
                            attributes[key] = value
                    row.extend([f"{key}:{value}" for key, value in attributes.items()])
                    writer.writerow(row)
        print("Inventory saved to database.csv")


    @staticmethod
    def create_product(class_name, attributes):
        try:
            # Set default values for missing attributes
            name = attributes.get('name', 'Unknown')
            cost_price = float(attributes.get('_Products__cost_price', 0))
            mrp = float(attributes.get('_mrp', 0))
            quantity = int(attributes.get('quantity', 0))

            if class_name == "Electronics":
                from electronics import Electronics
                power_option = attributes.get('power_option', 'Unknown')
                return Electronics(name, cost_price, mrp, quantity, power_option)
            elif class_name == "Grocery":
                from grocery import Grocery
                exp_date = attributes.get('exp_date', 'Unknown')
                return Grocery(name, cost_price, mrp, quantity, exp_date)
            elif class_name == "Furniture":
                from furniture import Furniture
                material = attributes.get('material', 'Unknown')
                return Furniture(name, cost_price, mrp, quantity, material)
            elif class_name == "Toys":
                from toys import Toys
                age_group = attributes.get('age_group', 'Unknown')
                return Toys(name, cost_price, mrp, quantity, age_group)
            elif class_name == "Cloths":
                from cloths import Cloths
                size = attributes.get('size', 'Unknown')
                return Cloths(name, cost_price, mrp, quantity, size)
            else:
                print(f"Warning: Unknown class '{class_name}' encountered. Skipping this item.")
                return None
        except ImportError as e:
            print(f"Warning: Unable to import {class_name} class. Error: {e}. Skipping this item.")
        except ValueError as e:
            print(f"Warning: Invalid value in {class_name} data. Error: {e}. Skipping this item.")
        except Exception as e:
            print(f"Unexpected error creating {class_name} product: {e}")
        return None
