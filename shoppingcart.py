from productList import Inventory


class ShoppingCart:
    def _init_(self):
        self.items = {}

    def add_item(self, product, quantity):
        """Add item to cart or update quantity."""
        if quantity > product.quantity:
            print(f"Error: Not enough stock for {product.name}")
            return False

        if product.product_id in self.items:
            self.items[product.product_id]['quantity'] += quantity
        else:
            self.items[product.product_id] = {
                'product': product,
                'quantity': quantity
            }
        return True

    def remove_item(self, product_id, quantity=None):
        """Remove item from cart or reduce quantity."""
        if product_id not in self.items:
            print("Product not in cart.")
            return False

        if quantity is None or quantity >= self.items[product_id]['quantity']:
            del self.items[product_id]
        else:
            self.items[product_id]['quantity'] -= quantity
        return True

    def calculate_total(self):
        """Calculate total cart value."""
        return sum(
            item['product'].price * item['quantity']
            for item in self.items.values()
        )

    def display_cart(self):
        """Show cart contents."""
        if not self.items:
            print("Cart is empty.")
            return

        print("\n--- Shopping Cart ---")
        for item in self.items.values():
            print(f"{item['product'].name}: {item['quantity']} x ${item['product'].price:.2f} = "
                  f"${item['product'].price * item['quantity']:.2f}")
        print(f"Total: ${self.calculate_total():.2f}")


class ShoppingInterface:
    def _init_(self, inventory_file='inventory.json'):
        self.inventory = Inventory()
        self.inventory.load_from_file(inventory_file)
        self.cart = ShoppingCart()

    def browse_products(self):
        """Display available products."""
        self.inventory.view_products()

    def add_to_cart(self, product_id, quantity):
        """Add product to shopping cart."""
        product = self.inventory.products.get(str(product_id))
        if not product:
            print("Product not found.")
            return False

        if quantity > product.quantity:
            print(f"Error: Only {product.quantity} items available.")
            return False

        success = self.cart.add_item(product, quantity)
        if success:
            # Reduce inventory
            product.quantity -= quantity
        return success

    def checkout(self):
        """Complete purchase and update inventory."""
        if not self.cart.items:
            print("Cart is empty.")
            return False

        print("\n--- Checkout ---")
        self.cart.display_cart()

        confirm = input("Confirm purchase? (yes/no): ").lower()
        if confirm == 'yes':
            # Save updated inventory
            self.inventory.save_to_file()
            print("Purchase completed successfully!")
            self.cart = ShoppingCart()  # Reset cart
            return True
        else:
            print("Purchase cancelled.")
            return False

    def run(self):
        """Main shopping interface."""
        while True:
            print("\n--- Product Shop ---")
            print("1. Browse Products")
            print("2. Add to Cart")
            print("3. View Cart")
            print("4. Remove from Cart")
            print("5. Checkout")
            print("6. Exit")

            choice = input("Choose an option (1-6): ")

            try:
                if choice == '1':
                    self.browse_products()

                elif choice == '2':
                    product_id = input("Enter product ID: ")
                    quantity = int(input("Enter quantity: "))
                    self.add_to_cart(product_id, quantity)

                elif choice == '3':
                    self.cart.display_cart()

                elif choice == '4':
                    product_id = input("Enter product ID to remove: ")
                    quantity = input("Enter quantity to remove (leave blank to remove all): ")
                    quantity = int(quantity) if quantity else None
                    self.cart.remove_item(product_id, quantity)

                elif choice == '5':
                    self.checkout()

                elif choice == '6':
                    print("Thank you for shopping!")
                    break

                else:
                    print("Invalid option. Try again.")

            except ValueError:
                print("Invalid input. Please enter valid numbers.")
            except Exception as e:
                print(f"An error occurred: {e}")


shop = ShoppingInterface()
shop.run()