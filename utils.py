def calculate_material_delivery(loads, distances, base_prices):
    HST_RATE = 0.15
    EXTRA_KM_RATE = 4.20
    INCLUDED_KM = 30

    material_details = {}
    grand_total = 0

    for material in loads:
        num_loads = loads[material]import streamlit as st
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

# ✅ Updated to use the new structure: delivery_result["details"]
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

        distance = distances[material]
        base_price = base_prices[material]

        if num_loads == 0:
            continue

        extra_km = max(0, distance - INCLUDED_KM)
        extra_charge = extra_km * EXTRA_KM_RATE
        load_price_before_tax = base_price + extra_charge
        hst = load_price_before_tax * HST_RATE
        load_price_with_tax = load_price_before_tax + hst
        total_for_material = load_price_with_tax * num_loads

        material_details[material] = {
            "loads": num_loads,
            "base_price": base_price,
            "extra_km": extra_km,
            "extra_charge": round(extra_charge, 2),
            "subtotal": round(load_price_before_tax, 2),
            "hst": round(hst, 2),
            "total": round(total_for_material, 2)
        }

        grand_total += total_for_material

    return {
        "details": material_details,
        "total": round(grand_total, 2)
    }
