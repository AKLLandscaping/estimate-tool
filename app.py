import streamlit as st
from utils import calculate_material_delivery

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
            f"Delivery Distance for {name} (${price}+tx) (km)", min_value=0, step=1, key=f"distance_{name}"
        )
    base_prices[name] = price

# Perform the calculation
delivery_result = calculate_material_delivery(loads, distances, base_prices)

# Display results
st.markdown("### 🧾 Material Delivery Summary")
for material, total in delivery_result["per_material"].items():
    if total > 0:
        st.write(f"**{material}**: ${total:,.2f}")

st.markdown(f"### 💰 Total Material Delivery: **${delivery_result['total']:,.2f}**")

# ------------------------
# 📍 Future Sections (Walkway, Wall, Fire Pit, etc.)
# ------------------------
st.markdown("---")
st.info("More estimator tools coming soon: Walkways, Retaining Walls, Fire Pits, and Steps.")
