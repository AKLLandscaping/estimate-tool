import streamlit as st
from utils import calculate_material_delivery
import math

st.set_page_config(page_title="AKL Hardscape Master Tool", layout="wide")

st.title("🏗️ AKL Hardscape Master Tool")
st.markdown("Welcome to the AKL estimator for landscaping and hardscaping projects.")

# ------------------------
# 📦 Material Delivery (5 Ton Loads)
# ------------------------
st.header("🚚 Material Delivery (5 Ton Loads)")

materials = [
    ("Screened Topsoil", 250),
    ("Triple Mix Garden Soil", 300),
    ("Screened Compost", 450),
    ("Screened Sand", 200),
    ("Electrical Trench Sand", 320),
    ("Crusher Dust", 320),
    ("Peastone", 330),
    ("Clearstone/Class A/B Gravel", 250)
]

loads = {}
distances = {}
base_prices = {}

cols = st.columns(2)
for name, price in materials:
    with cols[0]:
        loads[name] = st.number_input(
            f"Number of Loads for {name} (${price}+tx)", min_value=0, step=1, key=f"load_{name}"
        )
    with cols[1]:
        distances[name] = st.number_input(
            f"Delivery Distance: local 30k + $4.2 / additional km", min_value=0, step=1, key=f"distance_{name}"
        )
    base_prices[name] = price

# Perform the calculation
delivery_result = calculate_material_delivery(loads, distances, base_prices)

st.subheader("📄 Material Delivery Summary")
for material, details in delivery_result["details"].items():
    st.markdown(f"**{material}**")
    st.write(f"- Loads: {details['loads']}")
    st.write(f"- Base Price: ${details['base_price']:.2f}")
    st.write(f"- Extra KM: {details['extra_km']} @ $4.20 = ${details['extra_charge']:.2f}")
    st.write(f"- Subtotal Before Tax: ${details['subtotal']:.2f}")
    st.write(f"- HST (15%): ${details['hst']:.2f}")
    st.write(f"- Total for {details['loads']} Load(s): ${details['total']:.2f}")
    st.markdown("---")

st.markdown(f"### 💰 Total Material Delivery: **${delivery_result['total']:,.2f}**")

# ------------------------
# 📍 Future Sections
# ------------------------
st.markdown("---")
st.info("More estimator tools coming soon: Sod Installation, Walkways, Retaining Walls, Fire Pits, and Steps.")
