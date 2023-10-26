import datetime
from dateutil.relativedelta import relativedelta
import json
import logging

logger = logging.getLogger(__name__)

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
        logger.warning("Inventory:")
        for idx, product in enumerate(self.products, start=1):
            logger.warning(
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

    def find_product(self, product_name):
        for product in self.products:
            if product["name"] == product_name:
                return product
            else:
                return "Product could not be found in inventory"

    def update_product(self, product_name, field, new_value):
        for product in self.products:
            if product["name"] == product_name:
                if field == "name":
                    product["name"] = new_value
                elif field == "quantity":
                    product["quantity"] = new_value
                elif field == "expiry_month":
                    product["expiry_month"] = new_value
                elif field == "expiry_year":
                    product["expiry_year"] = new_value
                elif field == "supplier_name":
                    product["supplier_name"] = new_value
                elif field == "supplier_contact":
                    product["supplier_contact"] = new_value
                elif field == "price":
                    product["price"] = new_value
                self.save_to_json()

                logger.warning("Product updated successfully.")
                return product

        logger.warning(f"Product {product_name} was not found in inventory")

    def register_purchase(self, product_name, quantity):
        for product in self.products:
            if product["name"] == product_name:
                current_quantity = product["quantity"]
                if current_quantity >= quantity:
                    product["quantity"] -= quantity
                    self.save_to_json()

                    # Record purchase history
                    purchase_history = []
                    try:
                        with open("history.json", "r") as f:
                            purchase_history = json.load(f)
                    except FileNotFoundError:
                        pass

                    purchase_record = {
                        "product_name": product_name,
                        "quantity": quantity,
                        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    }
                    purchase_history.append(purchase_record)

                    with open("history.json", "w") as f:
                        json.dump(purchase_history, f)

                    logger.warning(f"Purchase of {quantity} {product_name} was successful.")
                    return product

                logger.warning(f"Insufficient quantity of {product_name}")
        logger.warning(f"Product {product_name} was not found in inventory")

    def delete_product(self, product_name):
        for product in self.products:
            if product["name"] == product_name:
                self.products.remove(product)
                self.save_to_json()
                logger.warning("Product deleted successfully.")
                return product
        logger.warning(f"Product with the name {product_name} was not found in the inventory.")


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
                logger.warning(f"Product '{product['name']}' has expired today!")
            else:
                logger.warning(
                    f"Product '{product['name']}' will expire in {time_until_expiration} days."
                )
            return expiry_date

        if current_date > expiry_date.date():
            logger.warning(f"Product '{product['name']}' has already expired.")
            return expiry_date

        if expiry_date.date() > six_months_from_now:
            logger.warning(f"Product '{product['name']}' is not yet near expiration.")
            return expiry_date
