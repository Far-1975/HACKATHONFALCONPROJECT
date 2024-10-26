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

st.title("☤💊MediQuick_Pharmacy")


# Display products
display_products(products)
if "name" not in st.session_state:
    st.session_state.name = ""
if "contact_info" not in st.session_state:
    st.session_state.contact_info = ""
if "address" not in st.session_state:
    st.session_state.address = ""
if "order_confirmed" not in st.session_state:
    st.session_state.order_confirmed = False
# Show cart and get total cost
total_cost = show_cart()
if total_cost > 0 and st.button("Proceed to Buy"):
    st.subheader("Fill Your Details")

    # Persist user input
    st.session_state.name = st.text_input("Name", value=st.session_state.name)
    st.session_state.contact_info = st.text_input("Contact Info", value=st.session_state.contact_info)
    st.session_state.address = st.text_area("Address", value=st.session_state.address)
    medical_report = st.file_uploader("Upload Medical Report (if any)", type=["jpg", "jpeg", "png", "pdf"])

    # Display "Confirm Order" button only if the order isn't already confirmed
    if not st.session_state.order_confirmed and st.button("Confirm Order"):
        # Check if all required details are provided
        if st.session_state.name and st.session_state.contact_info and st.session_state.address:
            # Set the order confirmation flag in session state
            st.session_state.order_confirmed = True
            # Generate payment link and QR code
            payment_link = f"http://example.com/pay?amount={total_cost}"
            qr_image = generate_qr(payment_link)
            st.image(qr_image)
            st.success("Order Confirmed! Your QR Code for payment is shown above.")
        else:
            st.error("Please complete all fields to confirm the order.")

# Show the confirmation details if the order was previously confirmed
if st.session_state.order_confirmed:
    st.success("Order Confirmed! Your QR Code for payment is shown above.")
