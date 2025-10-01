import psycopg2

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        database="bankamat",
        user="postgres",
        password="Java_0420",
        port="5432"
    )
    cur = conn.cursor()

    # --- User login ---
    user_id = input("Enter your user ID: ")

    cur.execute("SELECT first_name, last_name FROM users WHERE user_id = %s", (user_id,))
    user = cur.fetchone()
    if not user:
        print("User not found!")
        cur.close()
        conn.close()
        exit()

    print(f"Hello {user[0]} {user[1]}! Welcome to your account.\n")

    # --- Show user's cards ---
    cur.execute("SELECT card_id, money FROM card WHERE user_id = %s", (user_id,))
    cards = cur.fetchall()
    if not cards:
        print("No cards found for this user.")
        cur.close()
        conn.close()
        exit()

    print("Your cards:")
    for c in cards:
        balance = c[1] if c[1] is not None else 0
        print(f"Card ID: {c[0]}, Balance: {balance}")
    print()

    # --- Choose card ---
    card_id = input("Enter card ID to operate: ")

    # --- Operations menu ---
    while True:
        print("\nSelect operation:")
        print("1. Deposit money")
        print("2. Withdraw money")
        print("3. Check balance")
        print("4. Exit")

        choice = input("Enter choice (1-4): ")

        if choice == '1':
            money_to_add = float(input("Enter amount to deposit: "))
            cur.execute("""
                UPDATE card
                SET money = COALESCE(money,0) + %s
                WHERE card_id = %s
            """, (money_to_add, card_id))
            conn.commit()
            print(f"{money_to_add} deposited successfully!")

        elif choice == '2':
            money_to_withdraw = float(input("Enter amount to withdraw: "))
            cur.execute("SELECT money FROM card WHERE card_id = %s", (card_id,))
            current_balance = cur.fetchone()[0] or 0
            if money_to_withdraw > current_balance:
                print("Insufficient balance!")
            else:
                cur.execute("""
                    UPDATE card
                    SET money = money - %s
                    WHERE card_id = %s
                """, (money_to_withdraw, card_id))
                conn.commit()
                print(f"{money_to_withdraw} withdrawn successfully!")

        elif choice == '3':
            cur.execute("SELECT money FROM card WHERE card_id = %s", (card_id,))
            balance = cur.fetchone()[0] or 0
            print(f"Current balance: {balance}")

        elif choice == '4':
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Try again.")

    # Close cursor and connection
    cur.close()
    conn.close()

except Exception as e:
    print("Error:", e)
