#Initial project setup with Streamlit structure
Added user signup and login functionality
Created menu categories and item list
Implemented cart system and quantity selection
Added order placement with JSON storage
Created order history view for users
Cleaned code and improved layout
Updated README with project details
Uploaded SRS and documentation

import streamlit as st
import json
import os
import uuid
from datetime import datetime

# ========== Helper File Functions ==========
def load_data(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)
    with open(file, "r") as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ========== Authentication ==========
def signup(username, password):
    users = load_data("users.json")
    if username in users:
        return False, "Username already exists!"
    users[username] = {"password": password}
    save_data("users.json", users)
    return True, "Signup successful!"

def login(username, password):
    users = load_data("users.json")
    if username in users and users[username]["password"] == password:
        return True, "Login successful!"
    return False, "Invalid credentials!"

# ========== Food Menu ==========
menu = {
    "Pizzas": {"Margherita": 200, "Veggie Delight": 250, "Paneer Pizza": 300},
    "Burgers": {"Veg Burger": 120, "Cheese Burger": 150},
    "Biryani": {"Veg Biryani": 180, "Hyd Veg Biryani": 220},
    "Drinks": {"Coke": 50, "Mango Shake": 90}
}

# ========== UI ==========
st.set_page_config(page_title="Online Food Ordering System", layout="wide")
st.title("🍽️ Online Food Ordering System")

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "cart" not in st.session_state:
    st.session_state.cart = {}

# Sidebar login/signup
if not st.session_state.logged_in:
    action = st.sidebar.selectbox("Menu", ["Login", "Signup"])

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if action == "Login":
        if st.sidebar.button("Login"):
            success, msg = login(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(msg)
                st.experimental_rerun()
            else:
                st.error(msg)

    else:
        if st.sidebar.button("Signup"):
            success, msg = signup(username, password)
            if success:
                st.success(msg)
            else:
                st.error(msg)

else:
    st.sidebar.write(f"👋 Welcome, {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.cart = {}
        st.experimental_rerun()

    choice = st.sidebar.radio("Navigation", ["Menu", "Cart", "Order History"])

    # ----- MENU PAGE -----
    if choice == "Menu":
        st.subheader("📖 Menu")
        for category, items in menu.items():
            with st.expander(category):
                for item, price in items.items():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{item}** — ₹{price}")
                    with col2:
                        qty = st.number_input(f"Qty_{item}", min_value=0, max_value=10, value=0, key=item)
                        if qty > 0:
                            st.session_state.cart[item] = {"price": price, "qty": qty}

    # ----- CART PAGE -----
    if choice == "Cart":
        st.subheader("🛒 Your Cart")

        if not st.session_state.cart:
            st.info("Your cart is empty.")
        else:
            total = 0
            for item, details in st.session_state.cart.items():
                st.write(f"{item} x {details['qty']} = ₹{details['price'] * details['qty']}")
                total += details['price'] * details['qty']

            st.success(f"Total Amount: ₹{total}")

            if st.button("Place Order"):
                orders = load_data("orders.json")
                order_id = str(uuid.uuid4())[:8]

                orders[order_id] = {
                    "username": st.session_state.username,
                    "items": st.session_state.cart,
                    "total": total,
                    "date": datetime.now().strftime("%d-%m-%Y %H:%M")
                }
                save_data("orders.json", orders)

                st.session_state.cart = {}
                st.success("Order placed successfully! 🎉")

    # ----- ORDER HISTORY -----
    # Displaying previous orders for the logged-in user
    Added explanation comments to the order history and menu sections


    if choice == "Order History":
        st.subheader("📜 Your Orders")
        orders = load_data("orders.json")

        found_orders = False
        for order_id, details in orders.items():
            if details["username"] == st.session_state.username:
                found_orders = True
                st.write(f"**Order ID:** {order_id}")
                st.write(f"Date: {details['date']}")

                for item, info in details["items"].items():
                    st.write(f"- {item}: {info['qty']} x ₹{info['price']}")

                st.write(f"💰 Total: ₹{details['total']}")
                st.markdown("---")

        if not found_orders:
            st.info("No order history found.")
Added comment for code clarity
Updated header comments
Improved code formatting for readability
Added descriptive comment to menu section
Added comment explaining login function






