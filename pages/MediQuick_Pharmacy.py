import streamlit as st
import pandas as pd
import qrcode
from PIL import Image
import io

# Sample data for medicines and eco-friendly products
products = {
    'Medicines': [
        {'name': 'Paracetamol', 'cost': 20, 'image': 'https://www.pharmacyonline.co.uk/uploads/images/products/verylarge/pharmacy-online-paracetamol-soluble-paracetamol-500mg-100-effervescent-soluble-tablets-1603455187paracetamol-soluble-500mg-effervescent.jpg'},
        {'name': 'Ibuprofen', 'cost': 30, 'image': 'https://th.bing.com/th/id/OIP.HktCBpPfL6BOdsHlb0kVdgHaEi?w=296&h=181&c=7&r=0&o=5&dpr=1.3&pid=1.7'},
    ],
    'Eco-Friendly Products': [
        {'name': 'Bamboo Toothbrush', 'cost': 10, 'image': 'https://th.bing.com/th/id/OIP.59d9Rh228jTYrcPiGxakIQHaF7?w=244&h=195&c=7&r=0&o=5&dpr=1.3&pid=1.7'},
        {'name': 'Reusable Straw', 'cost': 5, 'image': 'https://th.bing.com/th/id/OIP.G3oC21ZA2GW-qNXAyNqWKgHaHa?rs=1&pid=ImgDetMain'},
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
    st.subheader("Your Cart")
    total_cost = 0  # Initialize total_cost
    if not st.session_state.cart:
        st.write("Your cart is empty.")
    else:
        for item in st.session_state.cart:
            st.write(f"{item['name']} - ₹{item['cost']}")
            total_cost += item['cost']
        st.write(f"Total: ₹{total_cost}")
    return total_cost

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

st.title("MediQuick_Pharmacy")
st.title("

# Display products
display_products(products)

# Show cart and get total cost
total_cost = show_cart()

# User details and order confirmation
if total_cost > 0 and st.button("Proceed to Buy"):
    st.subheader("Fill Your Details")
    name = st.text_input("Name")
    contact_info = st.text_input("Contact Info")
    address = st.text_area("Address")
    medical_report = st.file_uploader("Upload Medical Report (if any)", type=["jpg", "jpeg", "png", "pdf"])
    
    if st.button("Confirm Order"):
        if name and contact_info and address:
            payment_link = f"http://example.com/pay?amount={total_cost}"
            qr_image = generate_qr(payment_link)
            st.image(qr_image)
            st.success("Order Confirmed! Your QR Code for payment is shown above.")
