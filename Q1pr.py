from datetime import datetime



class User:

    def __init__(self, username, password, role):

        self.username = username

        self.password = password

        self.role = role # Role assigned to be stored here



class Product:

    def __init__(self, product_id, name, category, price, stock_quantity):

        self.product_id = product_id

        self.name = name

        self.category = category

        self.price = price

        self.stock_quantity = stock_quantity



    def update_stock(self, amount):

        self.stock_quantity += amount



class InventorySystem:

    def __init__(self):

        self.products = {}

        self.users = {}

        self.workers = {}

        self.current_user = None

        self.low_stock_threshold = 5  # Threshold for low stock

        self.stock_adjustments = []  # Record stock changes made by workers



    def add_user(self, username, password, role):

        if role == "Worker":

            self.workers[username] = User(username, password, role)

        else:

            self.users[username] = User(username, password, role)



    def login(self, username, password):

        user = self.users.get(username) or self.workers.get(username)

        if user and user.password == password:

            self.current_user = user

            print(f"Logged in as {user.username} ({user.role})")

            return True

        else:

            print("Invalid username or password.")

            return False



    def logout(self):

        self.current_user = None

        print("Logged out successfully.")



    def add_product(self, product_id, name, category, price, stock_quantity):

        if self.current_user.role != "Admin":

            print("Permission denied: Only Admins can add products.")

            return



        if product_id in self.products:

            print("Product ID already exists. Please use a unique ID.")

        else:

            self.products[product_id] = Product(product_id, name, category, price, stock_quantity)

            print("Product added successfully.")



    def update_product(self, product_id, **kwargs):

        if self.current_user.role != "Admin":

            print("Permission denied: Only Admins can update products.")

            return



        product = self.products.get(product_id)

        if not product:

            print("Product not found.")

            return



        for key, value in kwargs.items():

            if hasattr(product, key):

                setattr(product, key, value)

        print("Product updated successfully.")



    def delete_product(self, product_id):

        if self.current_user.role != "Admin":

            print("Permission denied: Only Admins can delete products.")

            return



        if product_id in self.products:

            del self.products[product_id]

            print("Product deleted successfully.")

        else:

            print("Product not found.")



    def view_inventory(self):

        if not self.products:

            print("No products in inventory.")

            return



        print("\nInventory List:")

        for product in self.products.values():

            self.display_product(product)

            if product.stock_quantity <= self.low_stock_threshold:

                print("Warning: Low stock")

        print()



    def search_product(self, keyword):

        results = [p for p in self.products.values() if keyword.lower() in p.name.lower() or keyword.lower() in p.category.lower()]

        if results:

            print("\nSearch Results:")

            for product in results:

                self.display_product(product)

            print()

        else:

            print("No products found matching the search criteria.")



    def adjust_stock(self, product_id, quantity):

        product = self.products.get(product_id)

        if not product:

            print("Product not found.")

            return



        # Stock cannot go below zero

        if product.stock_quantity + quantity < 0:

            print(f"Cannot reduce stock below 0. Current stock for '{product.name}' is {product.stock_quantity}.")

        else:

            product.update_stock(quantity)

            print(f"Stock updated. New quantity of '{product.name}' is {product.stock_quantity}")



            # Track adjustments made by workers

            if self.current_user.role == "Worker":

                self.stock_adjustments.append({

                    "worker": self.current_user.username,

                    "product_id": product_id,

                    "product_name": product.name,

                    "quantity": quantity,

                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                })



    def display_product(self, product):

        print(f"ID: {product.product_id}, Name: {product.name}, Category: {product.category}, "

              f"Price: ${product.price:.2f}, Stock: {product.stock_quantity}")



    def view_workers(self):

        if self.current_user.role != "Admin":

            print("Permission denied: Only Admins can view worker details.")

            return



        if not self.workers:

            print("No workers registered.")

            return



        print("\nWorkers List:")

        for worker in self.workers.values():

            print(f"Username: {worker.username}, Role: {worker.role}")



        # Display stock adjustments made by workers

        if self.stock_adjustments:

            print("\nStock Adjustments by Workers:")

            for adjustment in self.stock_adjustments:

                print(f"Worker: {adjustment['worker']}, Product: {adjustment['product_name']} "

                      f"(ID: {adjustment['product_id']}), Quantity: {adjustment['quantity']}, "

                      f"Date: {adjustment['date']}")

        print()



    def add_worker(self):

        if self.current_user.role != "Admin":

            print("Permission denied: Only Admins can add workers.")

            return



        username = input("Enter new worker's username: ")

        password = input("Enter new worker's password: ")

        

        if username in self.workers:

            print("Worker username already exists. Please choose a different username.")

        else:

            self.workers[username] = User(username, password, "Worker")

            print("Worker added successfully.")



    def run(self):

        print("Welcome to the Inventory Management System!")

        while True:

                if not self.current_user:

                    username = input("Username: ")

                    password = input("Password: ")

                    if not self.login(username, password):

                        continue



                if self.current_user.role == "Admin":

                    print("\n0. Exit\n1. Add Product\n2. Update Product\n3. Delete Product\n4. View Inventory\n5. Search Product\n"

                        "6. Adjust Stock\n7. View Workers\n8. Add Worker\n9. Logout\n")

                    choice = input("Choose an option: ")

                    if choice == "0":

                        print("Exiting program. Goodbye!")

                        break

                    elif choice == "1":

                        product_id = input("Product ID: ")

                        name = input("Name: ")

                        category = input("Category: ")

                        price = float(input("Price: "))

                        stock_quantity = int(input("Stock Quantity: "))

                        self.add_product(product_id, name, category, price, stock_quantity)

                    elif choice == "2":

                        product_id = input("Product ID to update: ")

                        updates = {}

                        while True:

                            field = input("Field to update (name, category, price, stock_quantity) or 'done': ")

                            if field == "done":

                                break

                            value = input(f"New value for {field}: ")

                            updates[field] = float(value) if field == "price" else int(value) if field == "stock_quantity" else value

                        self.update_product(product_id, **updates)

                    elif choice == "3":

                        product_id = input("Product ID to delete: ")

                        self.delete_product(product_id)

                    elif choice == "4":

                        self.view_inventory()

                    elif choice == "5":

                        keyword = input("Enter product name or category to search: ")

                        self.search_product(keyword)

                    elif choice == "6":

                        product_id = input("Product ID to adjust stock: ")

                        quantity = int(input("Enter quantity to add or subtract: "))

                        self.adjust_stock(product_id, quantity)

                    elif choice == "7":

                        self.view_workers()

                    elif choice == "8":

                        self.add_worker()

                    elif choice == "9":

                        self.logout()

                    else:

                        print("Invalid choice. Please try again.")



                elif self.current_user.role == "Worker":

                    print("\n0. Exit\n1. View Inventory\n2. Adjust Stock\n3. Logout\n")

                    choice = input("Choose an option: ")

                    if choice == "0":

                        print("Exiting program. Goodbye!")

                        break

                    elif choice == "1":

                        self.view_inventory()

                    elif choice == "2":

                        product_id = input("Product ID to adjust stock: ")

                        quantity = int(input("Enter quantity to add or subtract: "))

                        self.adjust_stock(product_id, quantity)

                    elif choice == "3":

                        self.logout()

                    else:

                        print("Invalid choice. Please try again.")



                elif self.current_user.role == "User":

                    print("\n0. Exit\n1. View Inventory\n2. Search Product\n3. Logout\n")

                    choice = input("Choose an option: ")

                    if choice == "0":

                        print("Exiting program. Goodbye!")

                        break

                    elif choice == "1":

                        self.view_inventory()

                    elif choice == "2":

                        keyword = input("Enter product name or category to search: ")

                        self.search_product(keyword)

                    elif choice == "3":

                        self.logout()

                    else:

                        print("Invalid choice. Please try again.")


if __name__ == "__main__":

    inventory_system = InventorySystem()

    # Adding initial users

    inventory_system.add_user("admin", "password123", "Admin")

    inventory_system.add_user("worker1", "workerpass", "Worker")

    inventory_system.add_user("user", "userpass", "User")

    inventory_system.run()