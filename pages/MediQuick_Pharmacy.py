import streamlit as st
import pandas as pd
import qrcode
from PIL import Image
import io

# Sample data for medicines and eco-friendly products
products = {
    'Medicines': [
        {'name': 'Paracetamol', 'cost': 20, 'image': r"C:\Users\shara\OneDrive\Desktop\Screenshot 2024-10-26 001639.png"},
        {'name': 'Ibuprofen', 'cost': 30, 'image': r"C:\Users\shara\OneDrive\Desktop\Screenshot 2024-10-26 001804.png"},
    ],
    'Eco-Friendly Products': [
        {'name': 'Bamboo Toothbrush', 'cost': 10, 'image': r"C:\Users\shara\OneDrive\Desktop\Screenshot 2024-10-26 002012.png"},
        {'name': 'Reusable Straw', 'cost': 5, 'image': r"C:\Users\shara\OneDrive\Desktop\Screenshot 2024-10-26 002130.png"},
    ]
}

# Function to display products
def display_products(products):
    for category, items in products.items():
        st.header(category)
        for item in items:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.image(item['image'], width=150)
            with col2:
                st.write(item['name'])
                st.write(f"Price: ₹{item['cost']}")
            with col3:
                if st.button('Add to Cart', key=item['name']):
                    st.session_state.cart.append(item)
                    st.success(f"{item['name']} added to cart!")

# Function to show cart
def show_cart():
    total_cost = 0  # Initialize total_cost to 0
    # Suppose you have a list of items in the cart
    cart_items = [("Item1", 10), ("Item2", 20)]  # Example items with costs
    
    for item, price in cart_items:
        total_cost += price  # Add the price of each item to total_cost

    return total_cost  # Return the total cost for use later


# Function to generate QR code for payment
def generate_qr(payment_link):
    qr = qrcode.make(payment_link)
    buf = io.BytesIO()
    qr.save(buf)
    buf.seek(0)
    return Image.open(buf)

# Initialize session state for cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

st.title("Medicines and Eco-Friendly Products Platform")

# Display products
display_products(products)

# Show cart and get total cost
total_cost = show_cart()

# User details and order confirmation
if st.button("Proceed to Buy"):
    st.subheader("Fill Your Details")
    name = st.text_input("Name")
    contact_info = st.text_input("Contact Info")
    address = st.text_area("Address")
    medical_report = st.file_uploader("Upload Medical Report (if any)", type=["jpg", "jpeg", "png", "pdf"])

    if st.button("Confirm Order"):
        # Validate that all required fields are filled
        if name and contact_info and address and total_cost > 0:
            # Generate payment link and QR code
            payment_link = f"http://example.com/pay?amount={total_cost}"
            qr_image = generate_qr(payment_link)
            st.image(qr_image)
            st.success("Order Confirmed! Your QR Code for payment is shown above.")
            # Optionally, you can add code to save the order details to a database or CSV
            # Clear cart after order confirmation
            st.session_state.cart.clear()
        else:
            st.warning("Please fill in all details and add items to your cart before confirming the order.")

