from model import Inventory,ExpirationChecker
import arrow

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