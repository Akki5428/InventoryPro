from products import Products
from electronics import Electronics
from grocery import Grocery
from furniture import Furniture
from toys import Toys
from cloths import Cloths

def main():
    Products.loadFromCSV()
    print(f"Loaded {len([p for p in Products.all_products if p is not None])} products.")
    
    while True:
        print("\nInventory Management System")
        print("1. Add new product")
        print("2. Delete a product")
        print("3. View product details")
        print("4. Edit product details")
        print("5. View entire inventory")
        print("6. Exit")

        try:
            op = int(input("Enter your choice: "))
            
            if op == 1:
                add_new_product()
            elif op == 2:
                delete_product()
            elif op == 3:
                view_product_details()
            elif op == 4:
                edit_product_details()
            elif op == 5:
                Products.showInventory()
            elif op == 6:
                Products.writeToCSV()
                print("Thank you for using the Inventory Management System.")
                break
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def add_new_product():
    print("\nProduct Types:")
    print("1. Electronics")
    print("2. Furniture")
    print("3. Grocery")
    print("4. Cloth")
    print("5. Toy")
    
    try:
        item_type = int(input("Enter product type: "))
        if item_type not in range(1, 6):
            raise ValueError
        
        lookup = {
            1: Electronics.addNewItem,
            2: Furniture.addNewItem,
            3: Grocery.addNewItem,
            4: Cloths.addNewItem,
            5: Toys.addNewItem
        }
        new_product = lookup[item_type]()
        print(f"{new_product.name} has been added to the inventory.")
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 5.")

def delete_product():
    index = Products.showInventory()
    if index is not False:
        removed_product = Products.all_products[index]
        Products.all_products[index] = None
        print(f"{removed_product.name} has been successfully removed!")

def view_product_details():
    index = Products.showInventory()
    if index is not False:
        Products.all_products[index].show_details()

def edit_product_details():
    index = Products.showInventory()
    if index is not False:
        Products.all_products[index].editDetails()

if __name__ == "__main__":
    main()
