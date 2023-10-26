from model import Inventory, ExpirationChecker
import arrow
import logging

logger = logging.getLogger(__name__)

def main():
    inventory = Inventory()
    inventory.load_from_json()

    while True:
        logger.warning("\nOptions:")
        logger.warning("1. Add Product to Inventory")
        logger.warning("2. List Products in Inventory")
        logger.warning("3. Check Expiration")
        logger.warning("4. Check Supplier Information")
        logger.warning("5. Search for Product")
        logger.warning("6. Update Product")
        logger.warning("7. Register Purchase")
        logger.warning("8. Delete Product")
        logger.warning("0. Exit")

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
            logger.warning("Product added to inventory.")

        if choice == "2":
            inventory.list_products()

        if choice == "3":
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
            logger.warning(f"Expiry Date: {exp}")

        if choice == "4":
            inventory.list_products()
            product_index = (
                int(input("Enter the product number to check supplier information: "))
                - 1
            )
            product = inventory.products[product_index]
            logger.warning(
                f"Supplier: {product['supplier_name']}, Contact: {product['supplier_contact']}"
            )

        if choice == "5":
            product_name = input("Enter product name: ")
            if product_name.islower():
                name = product_name.capitalize()
                inv = inventory.find_product(name)
                if inv:
                    logger.warning(inv)
                else:
                    logger.warning("Product could not be found in the inventory.")
            else:
                prod = inventory.find_product(product_name)
                if prod:
                    logger.warning(prod)
                else:
                    logger.warning("Product could not be found in the inventory.")

        if choice == "6":
            name = input("Enter Product name to update: ")
            man = name.capitalize()
            products = inventory.find_product(man)

            if products is not None:
                logger.warning("Fields you can update:")
                logger.warning("1. Name")
                logger.warning("2. Quantity")
                logger.warning("3. Expiry Month")
                logger.warning("4. Expiry Year")
                logger.warning("5. Supplier Name")
                logger.warning("6. Supplier Contact")
                logger.warning("7. Price")

                field_choice = input(
                    "Enter the number of the field you want to update (or press Enter to finish): "
                )

                if field_choice:
                    field_choice = int(field_choice)
                    new_value = input("Enter the new value: ")

                    if field_choice == 1:
                        inventory.update_product(
                            product_name=name, new_value=new_value, field="name"
                        )
                    if field_choice == 2:
                        inventory.update_product(
                            product_name=name,
                            new_value=int(new_value),
                            field="quantity",
                        )
                    if field_choice == 3:
                        inventory.update_product(
                            product_name=name,
                            new_value=int(new_value),
                            field="expiry_month",
                        )
                    if field_choice == 4:
                        inventory.update_product(
                            product_name=name,
                            new_value=int(new_value),
                            field="expiry_year",
                        )
                    if field_choice == 5:
                        inventory.update_product(
                            product_name=name,
                            new_value=new_value,
                            field="supplier_name",
                        )
                    if field_choice == 6:
                        inventory.update_product(
                            product_name=name,
                            new_value=new_value,
                            field="supplier_contact",
                        )
                    if field_choice == 7:
                        inventory.update_product(
                            product_name=name,
                            new_value=float(new_value),
                            field="price",
                        )

            else:
                logger.warning("Product could not be found in the inventory.")

        if choice == "7":
            logger.warning("Enter product name to register purchase")
            name = input("Enter product name: ")
            quantity = int(input("Enter quantity: "))  # Get the quantity first
            pos = inventory.find_product(name)
            if pos:
                inventory.register_purchase(
                    name, quantity
                )  # Register the purchase first

        if choice == "8":
            logger.warning("enter product name to delete")
            name = input("Enter product name: ")
            prod = inventory.find_product(name)
            if prod:
                inventory.delete_product(name)

        if choice == "0":
            logger.warning("Exiting program.")
            break


if __name__ == "__main__":
    main()
