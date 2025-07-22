import subprocess
import json

def ask_ollama(prompt):
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt.encode(),
        capture_output=True
    )
    return result.stdout.decode().strip()

PIZZA_TYPES = ["Margarita", "Chicken Fury", "Salami", "Pepperoni", "Tuna", "Veggie Supreme"]
SIZES = ["Small", "Medium", "Large"]
DRINKS = ["Pepsi", "Cola", "Mountain Dew", "Water", "Fanta"]
SIDES = ["Nuggets", "Nachos", "French Fries", "Chicken Wings"]

class PizzaOrder:
    def __init__(self):
        self.pizza_type = None
        self.size = None
        self.drink = None
        self.side = None
        self.address = None
        self.price = 8

    def summary(self):
        return (
            f"🍕 Pizza: {self.pizza_type if self.pizza_type else 'Not selected'} ({self.size if self.size else 'No size'})\n"
            f"🥤 Drink: {self.drink if self.drink else 'None'}\n"
            f"🍟 Side: {self.side if self.side else 'None'}\n"
            f"📍 Address: {self.address if self.address else 'Not provided'}\n"
            f"💰 Total Price: {self.price}€"
        )

def parse_user_input(user_input):
    ai_prompt = f"""
You are a pizza ordering AI assistant.
Menu:
Pizzas: {', '.join(PIZZA_TYPES)}
Sizes: {', '.join(SIZES)}
Drinks: {', '.join(DRINKS)}
Sides: {', '.join(SIDES)}

The user said: "{user_input}".

Output ONLY a JSON object with this exact structure:
{{
    "intent": "order" | "menu" | "greeting" | "address" | "unknown",
    "pizza_type": "Name" or null,
    "size": "Small" | "Medium" | "Large" or null,
    "drinks": ["List of drinks"],
    "sides": ["List of sides"],
    "address": "Address string or null"
}}
"""
    response = ask_ollama(ai_prompt).strip()
    try:
        json_start = response.find("{")
        json_end = response.rfind("}") + 1
        if json_start >= 0 and json_end > 0:
            response = response[json_start:json_end]
        return json.loads(response)
    except Exception:
        return {"intent": "unknown", "pizza_type": None, "size": None, "drinks": [], "sides": [], "address": None}

def pizza_conversation():
    order = PizzaOrder()

    print("\n🤖 Welcome! Here’s our pizza menu:")
    print(f"🍕 Pizzas: {', '.join(PIZZA_TYPES)}")

    while not order.pizza_type:
        user_input = input("\nWhich pizza would you like? ").strip()
        parsed = parse_user_input(user_input)
        if parsed.get("pizza_type") and parsed["pizza_type"] in PIZZA_TYPES:
            order.pizza_type = parsed["pizza_type"]
            print(f"✅ Pizza selected: {order.pizza_type}")
        else:
            print("❌ Sorry, I didn't get that. Please choose a pizza from the list.")

    while not order.size:
        user_input = input("\nWhat size would you like? (Small, Medium, Large): ").strip()
        parsed = parse_user_input(user_input)
        if parsed.get("size") and parsed["size"] in SIZES:
            order.size = parsed["size"]
            print(f"✅ Size selected: {order.size}")
        else:
            print("❌ Please select a valid size.")

    combo = input("\nWould you like a combo (sides + drinks) for 10€? (yes/no): ").strip().lower()
    if combo == "yes":
        order.price = 10
        print(f"\n🍟 Available sides: {', '.join(SIDES)}")
        while not order.side:
            user_input = input("Which side would you like? (Choose one): ").strip()
            parsed = parse_user_input(user_input)
            if parsed.get("sides") and len(parsed["sides"]) > 1:
                print("❌ Please choose only ONE side.")
                continue
            if parsed.get("sides"):
                valid_side = next((s for s in parsed["sides"] if s in SIDES), None)
                if valid_side:
                    order.side = valid_side
                    print(f"✅ Side added: {order.side}")
                else:
                    print("❌ Please choose a valid side.")

        print(f"\n🥤 Available drinks: {', '.join(DRINKS)}")
        while not order.drink:
            user_input = input("Which drink would you like? (Choose one): ").strip()
            parsed = parse_user_input(user_input)
            if parsed.get("drinks") and len(parsed["drinks"]) > 1:
                print("❌ Please choose only ONE drink.")
                continue
            if parsed.get("drinks"):
                valid_drink = next((d for d in parsed["drinks"] if d in DRINKS), None)
                if valid_drink:
                    order.drink = valid_drink
                    print(f"✅ Drink added: {order.drink}")
                else:
                    print("❌ Please choose a valid drink.")

    while not order.address:
        user_input = input("\nWhat's your delivery address? ").strip()
        parsed = parse_user_input(user_input)
        if parsed.get("address"):
            order.address = parsed["address"]
            print(f"📍 Address set: {order.address}")
        else:
            order.address = user_input
            print(f"📍 Address set: {order.address}")

    print("\n📝 Order summary:")
    print(order.summary())
    confirm = input("Confirm order? (yes/no): ").strip().lower()
    if confirm == "yes":
        print("🎉 Your order is placed! Thank you.")
    else:
        print("❌ Order cancelled.")

def main_menu():
    while True:
        print("\n🤖 How can I help you?")
        print("1. I want to order 🍕")
        print("2. Exit ❌")

        choice = input("Enter your choice (1/2): ").strip()
        if choice == "1":
            pizza_conversation()
        elif choice == "2":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please choose 1 or 2.")

if __name__ == "__main__":
    main_menu()
