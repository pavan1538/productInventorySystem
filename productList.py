import json

class Product:
    def __init__(self, product_id, name, quantity, price):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.price = price

    def to_dict(self):
        """Convert Product object to dictionary."""
        return {
            'product_id': self.product_id,
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price
        }

    def from_dict(data):
        """Create Product object from dictionary."""
        return Product(data['product_id'], data['name'], data['quantity'], data['price'])


class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        """Add a new product to the inventory."""
        if product.product_id in self.products:
            print("Product ID already exists.")
        else:
            self.products[product.product_id] = product
            print(f"Product {product.name} added successfully.")

    def view_products(self):
        """Display all products in the inventory."""
        if not self.products:
            print("No products in inventory.")
            return
        print("\nInventory:")
        for product in self.products.values():
            print(f"ID: {product.product_id}, Name: {product.name}, Quantity: {product.quantity}, Price: ${product.price:.2f}")

    def update_product(self, product_id, name=None, quantity=None, price=None):
        """Update an existing product's details."""
        product = self.products.get(product_id)
        if product:
            if name:
                product.name = name
            if quantity is not None:
                product.quantity = quantity
            if price is not None:
                product.price = price
            print(f"Product {product_id} updated successfully.")
        else:
            print("Product not found.")

    def delete_product(self, product_id):
        """Remove a product from the inventory."""
        if product_id in self.products:
            del self.products[product_id]
            print(f"Product {product_id} deleted successfully.")
        else:
            print("Product not found.")

    def save_to_file(self, filename):
        """Save inventory data to a file."""
        with open(filename, 'w') as file:
            json.dump([product.to_dict() for product in self.products.values()], file)
        print(f"Inventory saved to {filename}.")

    def load_from_file(self, filename):
        """Load inventory data from a file."""
        try:
            with open(filename, 'r') as file:
                products_data = json.load(file)
                for product_data in products_data:
                    product = Product.from_dict(product_data)
                    self.products[product.product_id] = product
            print(f"Inventory loaded from {filename}.")
        except FileNotFoundError:
            print("File not found. Starting with an empty inventory.")


def main():
    inventory = Inventory()
    inventory.load_from_file('inventory.json')

    while True:
        print("\nOptions:")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Save Inventory")
        print("6. Exit")

        choice = input("Choose an option (1-6): ")

        if choice == '1':
            product_id = int(input("Enter product ID: "))
            name = input("Enter product name: ")
            quantity = int(input("Enter product quantity: "))
            price = float(input("Enter product price: "))
            product = Product(product_id, name, quantity, price)
            inventory.add_product(product)

        elif choice == '2':
            inventory.view_products()

        elif choice == '3':
            product_id = input("Enter product ID to update: ")
            name = input("Enter new product name (leave blank to keep current): ")
            quantity = input("Enter new product quantity (leave blank to keep current): ")
            price = input("Enter new product price (leave blank to keep current): ")

            # Convert quantity and price to appropriate types if provided
            quantity = int(quantity) if quantity else None
            price = float(price) if price else None

            inventory.update_product(product_id, name if name else None, quantity, price)

        elif choice == '4':
            product_id = input("Enter product ID to delete: ")
            inventory.delete_product(product_id)

        elif choice == '5':
            inventory.save_to_file('inventory.json')

        elif choice == '6':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid option. Please choose again.")


if __name__ == "__main__":
    main()
