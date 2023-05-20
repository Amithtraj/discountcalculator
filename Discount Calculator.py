# Product prices
product_prices = {
    "Product A": 20,
    "Product B": 40,
    "Product C": 50
}

# Discount rules
discount_rules = {
    "flat_10_discount": {
        "condition": lambda cart_total, quantity, total_quantity: cart_total > 200,
        "discount": 10
    },
    "bulk_5_discount": {
        "condition": lambda cart_total, quantity, total_quantity: quantity > 10,
        "discount": 5
    },
    "bulk_10_discount": {
        "condition": lambda cart_total, quantity, total_quantity: total_quantity > 20,
        "discount": 10
    },
    "tiered_50_discount": {
        "condition": lambda cart_total, quantity, total_quantity: quantity > 15 and total_quantity > 30,
        "discount": 50
    }
}

# Constants
GIFT_WRAP_FEE = 1
SHIPPING_FEE_PER_PACKAGE = 5
PRODUCTS_PER_PACKAGE = 10

def calculate_discount(cart_total, quantity, total_quantity):
    applicable_discounts = {}

    for rule, discount_info in discount_rules.items():
        if discount_info["condition"](cart_total, quantity, total_quantity):
            applicable_discounts[rule] = discount_info["discount"]

    if applicable_discounts:
        return max(applicable_discounts, key=applicable_discounts.get)
    else:
        return None

def calculate_total():
    cart_total = 0
    total_quantity = 0
    shipping_fee = 0
    gift_wrap_fee = 0
    items = []

    for product, price in product_prices.items():
        quantity = int(input(f"Enter the quantity of {product}: "))
        is_gift_wrapped = input(f"Is {product} wrapped as a gift? (yes/no): ").lower() == "yes"

        product_total = price * quantity
        cart_total += product_total
        total_quantity += quantity

        if is_gift_wrapped:
            gift_wrap_fee += quantity * GIFT_WRAP_FEE

        items.append((product, quantity, product_total))

    discount = calculate_discount(cart_total, total_quantity, total_quantity)

    if discount:
        if discount == "tiered_50_discount":
            for i, (product, quantity, product_total) in enumerate(items):
                if quantity > 15:
                    original_price = price * 15
                    discounted_price = (price * (1 - discount_rules[discount]["discount"] / 100)) * (quantity - 15)
                    items[i] = (product, quantity, original_price + discounted_price)
        else:
            cart_total -= discount_rules[discount]["discount"]

    shipping_fee += (total_quantity // PRODUCTS_PER_PACKAGE) * SHIPPING_FEE_PER_PACKAGE

    subtotal = cart_total + shipping_fee + gift_wrap_fee

    print("Product Details:")
    for product, quantity, product_total in items:
        print(f"Product: {product}\t Quantity: {quantity}\t Total: ${product_total}")

    print(f"\nSubtotal: ${subtotal}")

    if discount:
        print(f"Discount Applied: {discount}\t Amount: ${discount_rules[discount]['discount']}")
    else:
        print("No discount applied.")

    print(f"Shipping Fee: ${shipping_fee}")
    print(f"Gift Wrap Fee: ${gift_wrap_fee}")

    total = subtotal
    print(f"\nTotal: ${total}")

calculate_total()
