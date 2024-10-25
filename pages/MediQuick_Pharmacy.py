import streamlit as st
import qrcode
from PIL import Image
import io

# Sample data for medicines and eco-friendly products without image paths
products = {
    'Medicines': [
        {'name': 'Paracetamol', 'cost': 20, 'image': None},  # Image to be uploaded
        {'name': 'Ibuprofen', 'cost': 30, 'image': None},    # Image to be uploaded
    ],
    'Eco-Friendly Products': [
        {'name': 'Bamboo Toothbrush', 'cost': 10, 'image': None},  # Image to be uploaded
        {'name': 'Reusable Straw', 'cost': 5, 'image': None},      # Image to be uploaded
    ]
}

# Function to set images for products through upload
def set_product_images(products):
    st.subheader("Upload Images for Products")
    for category, items in products.items():
        for item in items:
            item['image'] = st.file_uploader(f"Upload image for {item['name']}", type=["png", "jpg", "jpeg"], key=item['name'])
            
# Function to display products
def display_products(products):
    for category, items in products.items():
        st.header(category)
        for item in items:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                if item['image'] is not None:
                    st.image(item['image'], width=150)
                else:
                    st.write("No image uploaded.")
            with col2:
                st.write(item['name'])
                st.write(f"Price: ₹{item['cost']}")
            with col3:
                if st.button('Add to Cart', key=f"{item['name']}_cart"):
                    st.session_state.cart.append(item)
                    st.success(f"{item['name']} added to cart!")

# Function to show cart and calculate total
def show_cart():
    st.subheader("Your Cart")
    if not st.session_state.cart:
        st.write("Your cart is empty.")
        return 0  # Return 0 when the cart is empty
    else:
        total_cost = 0
        for item in st.session_state.cart:
            st.write(f"{item['name']} - ₹{item['cost']}")
            total_cost += item['cost']
        st.write(f"Total: ₹{total_cost}")
        return total_cost

# Function to generate a QR code for payment
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

# Prompt user to set images for each product
set_product_images(products)

# Display products with uploaded images
display_products(products)

# Show cart and calculate the total cost
total_cost = show_cart()

# Order confirmation and payment
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
