import streamlit as st
import qrcode
from PIL import Image
import io

# Sample data for medicines and eco-friendly products
products = {
    'Medicines': [
        {'name': 'Paracetamol', 'cost': 20, 'image': 'https://www.pharmacyonline.co.uk/uploads/images/products/verylarge/pharmacy-online-paracetamol-soluble-paracetamol-500mg-100-effervescent-soluble-tablets-1603455187paracetamol-soluble-500mg-effervescent.jpg'},
        {'name': 'Ibuprofen', 'cost': 30, 'image': 'https://th.bing.com/th/id/OIP.HktCBpPfL6BOdsHlb0kVdgHaEi?w=296&h=181&c=7&r=0&o=5&dpr=1.3&pid=1.7'},
        {'name': 'Cough Syrup', 'cost': 50, 'image': 'https://th.bing.com/th/id/OIP.FxakDZU1cFXkh6sbcR-KAQHaEK?w=306&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7'},
        {'name': 'Divon Plus', 'cost': 40, 'image': 'https://th.bing.com/th/id/OIP.OIXJuBgmXUQNEZeoIRLzzgHaFj?w=261&h=195&c=7&r=0&o=5&dpr=1.3&pid=1.7'},
        {'name': 'Dart', 'cost': 35, 'image': 'https://th.bing.com/th/id/OIP.7KWWzM6_JFRtHqjPBGw68AHaE8?w=285&h=190&c=7&r=0&o=5&dpr=1.3&pid=1.7'},
    ],
    'Eco-Friendly Products': [
        {'name': 'Bamboo Toothbrush', 'cost': 10, 'image': 'https://th.bing.com/th/id/OIP.59d9Rh228jTYrcPiGxakIQHaF7?w=244&h=195&c=7&r=0&o=5&dpr=1.3&pid=1.7'},
        {'name': 'Reusable Straw', 'cost': 5, 'image': 'https://th.bing.com/th/id/OIP.G3oC21ZA2GW-qNXAyNqWKgHaHa?rs=1&pid=ImgDetMain'},
        {'name': 'Jute Bag', 'cost': 15, 'image': 'https://th.bing.com/th/id/OIP.NF-XfRVu2JfGn3rURumFwQHaFj?w=233&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7'},
        {'name': 'Recycled Notebook', 'cost': 8, 'image': 'https://th.bing.com/th/id/OIP.WgNuRQ_GZVs09czSBe3dMQHaFj?w=225&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7'},
        {'name': 'Compostable Cutlery Set', 'cost': 12, 'image': 'https://th.bing.com/th/id/OIP.O4VqYbtJIVNnbJzp2fZg7gHaHa?w=215&h=215&c=7&r=0&o=5&dpr=1.3&pid=1.7'},
    ]
}

# Initialize session states
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'order_confirmed' not in st.session_state:
    st.session_state.order_confirmed = False

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
    total_cost = 0
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

# Main app title
st.title("☤💊 MediQuick Pharmacy")

# Display products and add to cart functionality
display_products(products)

# Show cart and get total cost
total_cost = show_cart()

# Proceed to Buy and form for user details
if total_cost > 0 and st.button("Proceed to Buy"):
    st.session_state.proceed_to_buy = True  # Set a flag to show the form

# Show the form for filling user details if Proceed to Buy was clicked
if st.session_state.get('proceed_to_buy', False):
    with st.form("order_form"):
        st.subheader("Fill Your Details")
        
        # Input fields with state persistence in form
        name = st.text_input("Name")
        contact_info = st.text_input("Contact Info")
        address = st.text_area("Address")
        medical_report = st.file_uploader("Upload Medical Report (if any)", type=["jpg", "jpeg", "png", "pdf"])

        # Confirm Order button inside the form
        confirm_order = st.form_submit_button("Confirm Order")

        # Check if Confirm Order button is clicked
        if confirm_order:
            if name and contact_info and address:
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
