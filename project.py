import json
import time
import pwinput


# Load users from JSON file
def load_function():
    try:
        with open("atm_json.file", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# Save users to JSON file
def save_function(users):
    with open("atm_json.file", "w") as f:
        return json.dump(users, f, indent=4)


# Find user based on card_number and pin
def find_users(users, card_number, pin):
    for user in users:
        if user["card_number"] == card_number and user["pin"] == pin:
            return user
    return None


# Get positive float input
def get_positive_float(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount > 0:
                return amount
            else:
                print("⚠️ Amount must be greater than 0.")
        except ValueError:
            print("❌ Please enter a valid numeric amount.")


# Deposit money
def deposit_money(user):
    amount = get_positive_float("💰 Enter deposit amount (PKR): ")
    user["balance"] += amount
    user["transactions"].append({
        "type": "Deposit",
        "amount": amount,
        "time": time.ctime(),
        "Remaining Balance": user["balance"]
    })
    print(
        f"✅ {amount:.2f} PKR successfully deposited to {user['name'].title()}'s account 💳")


# Show balance
def show_balance(user):
    print(
        f"💰 Current Balance: {user['balance']:.2f} PKR\n👤 Account Holder: {user['name'].title()}")


# Withdraw money
def withdraw_money(user):
    amount = get_positive_float("💸 Enter withdrawal amount (PKR): ")
    if amount > user["balance"]:
        print("❌ Insufficient balance. Please try a smaller amount.")
        return
    user["balance"] -= amount
    user["transactions"].append({
        "type": "Withdraw",
        "amount": amount,
        "time": time.ctime(),
        "Remaining Balance": user["balance"]
    })
    print(f"✅ {amount:.2f} PKR successfully withdrawn from your account 💵")


# Change PIN
def change_pin(user):
    old_pin = pwinput.pwinput("🔑 Enter your old PIN: ", mask="*")
    if old_pin != user["pin"]:
        print("❌ Incorrect old PIN. Please try again.")
        return

    new_pin = pwinput.pwinput("🔒 Enter your new 4-digit PIN: ", mask="*")
    if len(new_pin) == 4 and new_pin.isdigit():
        user["pin"] = new_pin
        print("✅ Your PIN has been successfully changed 🔐")
    else:
        print("⚠️ Invalid PIN. It must be a 4-digit number.")
        return


# Transfer money
def transfer_money(users, user):
    receiver_card = input("💳 Enter receiver's card number: ").strip()
    amount = get_positive_float("💸 Enter amount to transfer (PKR): ")

    receiver = next(
        (u for u in users if u["card_number"] == receiver_card), None)
    if not receiver:
        print("❌ Receiver card not found.")
        return

    if amount > user["balance"]:
        print("❌ Insufficient balance for transfer.")
        return

    user["balance"] -= amount
    receiver["balance"] += amount

    user["transactions"].append({
        "type": "Transfer sent",
        "amount": amount,
        "to": receiver["name"],
        "time": time.ctime(),
        "Remaining Balance": user["balance"]
    })
    receiver["transactions"].append({
        "type": "Transfer received",
        "amount": amount,
        "from": user["name"],
        "time": time.ctime(),
        "Remaining Balance": receiver["balance"]
    })
    print(
        f"✅ Successfully transferred {amount:.2f} PKR to {receiver['name'].title()} 💸")


# View transactions
def view_transactions(user):
    if not user["transactions"]:
        print("🧾 No transactions found for this account.")
        return

    print("\n📜 Transaction History:")
    for t in user["transactions"]:
        print(
            f"➡️ {t['type']} | 💰 Amount: {t['amount']} PKR | 🕒 {t['time']} | 💳 Balance: {t.get('Remaining Balance', t.get('remaining balance', 0)):.2f}"
        )


# ATM system
def atm_system():
    while True:
        users = load_function()
        print("\n===== 💳 Welcome to Python Bank ATM 💳 =====")
        print("1️⃣  Existing User Login")
        print("2️⃣  Create New Account")
        print("3️⃣  Exit")
        choice = input("👉 Enter choice (1-3): ").strip()

        if choice == "1":
            card_number = input("💳 Enter your card number: ").strip()
            pin = pwinput.pwinput("🔑 Enter your PIN: ").strip()
            user = find_users(users, card_number, pin)

            if not user:
                print("❌ Invalid card number or PIN. Please try again.")
                continue

            print(f"\n👋 Welcome, {user['name'].title()}! Access granted ✅")

        elif choice == "2":
            name = input("👤 Enter your name: ").strip().lower()
            card_number = input("💳 Enter your card number: ").strip()
            new_pin = pwinput.pwinput("🔒 Enter your 4-digit PIN: ").strip()

            if any(u["card_number"] == card_number for u in users):
                print("⚠️ Card number already exists. Try a different one.")
                continue

            if len(new_pin) != 4 or not new_pin.isdigit():
                print("❌ Invalid PIN. Must be a 4-digit number.")
                continue

            new_user = {
                "name": name,
                "pin": new_pin,
                "card_number": card_number,
                "balance": 0.0,
                "transactions": []
            }
            users.append(new_user)
            save_function(users)
            print("✅ Account successfully created! Please login to continue.")
            continue

        elif choice == "3":
            close = input(
                "⚙️ Do you want to exit the program? (yes/no): ").lower().strip()
            if close == "yes":
                print("👋 Thank you for using Python Bank ATM. Goodbye!")
                break
            else:
                continue
        else:
            print("❌ Invalid option. Please select 1, 2, or 3.")
            continue

        # ATM menu after login
        while True:
            print("\n===== 🏧 ATM MENU =====")
            print("1️⃣  Check Balance")
            print("2️⃣  Deposit Money")
            print("3️⃣  Withdraw Money")
            print("4️⃣  View Transactions")
            print("5️⃣  Change PIN")
            print("6️⃣  Transfer Money")
            print("7️⃣  Logout")

            option = input("👉 Select option (1-7): ").strip()

            if option == "1":
                show_balance(user)
            elif option == "2":
                deposit_money(user)
            elif option == "3":
                withdraw_money(user)
            elif option == "4":
                view_transactions(user)
            elif option == "5":
                change_pin(user)
            elif option == "6":
                transfer_money(users, user)
            elif option == "7":
                print("👋 Logging out...")
                save_function(users)
                break
            else:
                print("⚠️ Invalid option. Please select between 1-7.")

            save_function(users)


if __name__ == "__main__":
    atm_system()
