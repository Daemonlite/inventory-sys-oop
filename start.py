import datetime
from dateutil.relativedelta import relativedelta
import arrow
import json


class Inventory:
    def __init__(self):
        self.products = []

    def add_product(
        self,
        product_name,
        product_price,
        product_quantity,
        product_expiry_month,
        product_expiry_year,
        supplier_name,
        supplier_contact,
    ):
        product = {
            "name": product_name,
            "price": product_price,
            "quantity": product_quantity,
            "expiry_month": product_expiry_month,
            "expiry_year": product_expiry_year,
            "supplier_name": supplier_name,
            "supplier_contact": supplier_contact,
        }
        self.products.append(product)
        self.save_to_json()

    def list_products(self):
        print("Inventory:")
        for idx, product in enumerate(self.products, start=1):
            print(
                f"{idx}. Product: {product['name']}, Price: {product['price']}, Quantity: {product['quantity']}, Expiry: {product['expiry_month'], product['expiry_year']}, Supplier: {product['supplier_name']}, Contact: {product['supplier_contact']}"
            )

    def save_to_json(self):
        with open("inventory.json", "w") as f:
            json.dump(self.products, f)

    def load_from_json(self):
        try:
            with open("inventory.json", "r") as f:
                data = f.read()
                if data:
                    self.products = json.loads(data)
                else:
                    self.products = []  
        except FileNotFoundError:
            self.products = [] 


class ExpirationChecker:
    def __init__(self, month, year):
        self.month = month
        self.year = year

    def check_expiration(self, product):
        current_date = datetime.datetime.now().date()
        expiry_date = datetime.datetime(self.year, self.month, 1)
        six_months_from_now = current_date + relativedelta(months=6)

        if current_date <= expiry_date.date() <= six_months_from_now:
            time_until_expiration = (expiry_date.date() - current_date).days
            if time_until_expiration == 0:
                print(f"Product '{product['name']}' has expired today!")
            else:
                print(
                    f"Product '{product['name']}' will expire in {time_until_expiration} days."
                )
            return expiry_date

        if current_date > expiry_date.date():
            print(f"Product '{product['name']}' has already expired.")
            return expiry_date

        if expiry_date.date() > six_months_from_now:
            print(f"Product '{product['name']}' is not yet near expiration.")
            return expiry_date


def main():
    inventory = Inventory()
    inventory.load_from_json()

    while True:
        print("\nOptions:")
        print("1. Add Product to Inventory")
        print("2. List Products in Inventory")
        print("3. Check Expiration")
        print("4. Check Supplier Information")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            product_name = input("Enter product name: ")
            product_price = float(input("Enter product price: "))
            product_quantity = int(input("Enter product quantity: "))
            product_expiry_month = input("Enter product month of expiry: ")
            product_expiry_year = input("Enter Product's year of expiry: ")
            product_supplier_name = input("Enter supplier name: ")
            product_supplier_contact = input("Enter supplier contact: ")
            inventory.add_product(
                product_name,
                product_price,
                product_quantity,
                product_expiry_month,
                product_expiry_year,
                product_supplier_name,
                product_supplier_contact,
            )
            print("Product added to inventory.")

        elif choice == "2":
            inventory.list_products()

        elif choice == "3":
            inventory.list_products()
            product_index = (
                int(input("Enter the product number to check expiration: ")) - 1
            )
            product = inventory.products[product_index]
            expiry_month = int(product["expiry_month"])
            expiry_year = int(product["expiry_year"])
            checker = ExpirationChecker(expiry_month, expiry_year)
            expiry_date = checker.check_expiration(product)
            exp = arrow.get(expiry_date).format("YYYY-MM-DD")
            print(f"Expiry Date: {exp}")

        elif choice == "4":
            inventory.list_products()
            product_index = (
                int(input("Enter the product number to check supplier information: "))
                - 1
            )
            product = inventory.products[product_index]
            print(
                f"Supplier: {product['supplier_name']}, Contact: {product['supplier_contact']}"
            )

        elif choice == "5":
            print("Exiting program.")
            break


if __name__ == "__main__":
    main()
