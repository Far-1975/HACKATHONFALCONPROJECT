import streamlit as st
from fpdf import FPDF
import datetime
import os
from tempfile import NamedTemporaryFile

# Sample symptoms and their associated dietary recommendations
diet_recommendations = {
    "Cough": [
        "Warm soups with garlic and ginger",
        "Honey and lemon tea",
        "Avoid cold foods and drinks",
        "Increase vitamin C intake through fruits like oranges and strawberries"
    ],
    "Shortness of Breath": [
        "Increase intake of iron-rich foods (spinach, lentils, red meat)",
        "Vitamin B12-rich foods like eggs and dairy products",
        "Avoid processed foods and high-sodium meals",
        "Stay hydrated"
    ],
    "Chest Pain": [
        "Foods rich in omega-3 (salmon, walnuts, chia seeds)",
        "Reduce caffeine and alcohol intake",
        "Low-sodium foods to support heart health",
        "Incorporate fruits and vegetables rich in antioxidants"
    ],
    "Nausea": [
        "Ginger tea or ginger-based foods",
        "Small, frequent meals with low-fat foods",
        "Avoid spicy, fried, and acidic foods",
        "Include dry foods like toast or crackers"
    ],
    "Vomiting": [
        "Clear fluids like water, apple juice, and broth",
        "Bananas, rice, applesauce, and toast (BRAT diet)",
        "Avoid dairy products temporarily",
        "Increase hydration with electrolyte-rich drinks"
    ],
    "Diarrhea": [
        "BRAT diet: bananas, rice, applesauce, and toast",
        "Avoid dairy, caffeine, and high-fiber foods",
        "Increase water intake to prevent dehydration",
        "Plain chicken or turkey, cooked carrots, and potatoes"
    ],
    "Fever": [
        "Hydrate with water, herbal teas, and clear broths",
        "Foods high in protein to maintain strength (eggs, lean meats)",
        "Include immune-boosting foods like citrus fruits and leafy greens",
        "Avoid fatty, greasy, and high-sugar foods"
    ],
    "Fatigue": [
        "Whole grains (brown rice, oats) for sustained energy",
        "Nuts and seeds for healthy fats and proteins",
        "Green leafy vegetables for iron and magnesium",
        "Avoid excessive caffeine and sugar to prevent energy crashes"
    ],
    "Headache": [
        "Hydrate with plenty of water",
        "Magnesium-rich foods like almonds, avocados, and bananas",
        "Avoid alcohol, especially red wine, and processed foods",
        "Incorporate anti-inflammatory foods like berries and leafy greens"
    ]
}
def generate_diet_plan(symptoms):
    diet_plan = {}
    for symptom in symptoms:
        if symptom in diet_recommendations:
            diet_plan[symptom] = diet_recommendations[symptom]
    return diet_plan

def format_diet_plan(diet_plan):
    formatted_plan = ""
    for symptom, recommendations in diet_plan.items():
        formatted_plan += f"For {symptom}:\n"
        for recommendation in recommendations:
            formatted_plan += f"- {recommendation}\n"
        formatted_plan += "\n"
    return formatted_plan

def generate_pdf(patient_name, patient_age, diet_plan):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Patient Diet Plan", ln=True, align="C")
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Patient Name: {patient_name}", ln=True)
    pdf.cell(0, 10, f"Patient Age: {patient_age}", ln=True)
    pdf.cell(0, 10, f"Date: {datetime.date.today()}", ln=True)
    pdf.cell(0, 10, "-" * 40, ln=True)
    
    pdf.set_font("Arial", "", 10)
    for symptom, recommendations in diet_plan.items():
        pdf.cell(0, 10, f"For {symptom}:", ln=True)
        for recommendation in recommendations:
            pdf.cell(0, 10, f" - {recommendation}", ln=True)
        pdf.cell(0, 10, "", ln=True)
    
    # Create a temporary PDF file
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        return tmp_file.name

# Streamlit app interface
st.title("Personalized Diet Plan Generator")

# Collecting patient details
patient_name = st.text_input("Patient Name")
patient_age = st.number_input("Patient Age", min_value=1, max_value=120, step=1)

# Multi-select for symptoms
selected_symptoms = st.multiselect("Choose symptoms:", list(diet_recommendations.keys()))

# Generate diet plan when button is clicked
if st.button("Generate Diet Plan"):
    if not patient_name:
        st.warning("Please enter the patient's name.")
    elif not patient_age:
        st.warning("Please enter the patient's age.")
    elif not selected_symptoms:
        st.warning("Please select at least one symptom to generate a diet plan.")
    else:
        diet_plan = generate_diet_plan(selected_symptoms)
        formatted_plan = format_diet_plan(diet_plan)
        
        # Display diet plan in the Streamlit app
        st.text_area("Diet Plan", formatted_plan, height=300)
        
        # Generate and download PDF
        pdf_file = generate_pdf(patient_name, patient_age, diet_plan)
        with open(pdf_file, "rb") as file:
            btn = st.download_button(
                label="Download Diet Plan as PDF",
                data=file,
                file_name="diet_plan.pdf",
                mime="application/pdf"
            )
