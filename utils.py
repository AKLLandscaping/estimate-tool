import streamlit as st
from utils import calculate_material_delivery, calculate_sod_quote
import math

st.set_page_config(page_title="AKL Sod Install Tool", layout="wide")

st.title("🌱 AKL Sod Install Tool")
st.markdown("Full estimator for sod installation, delivery, labor, equipment, travel, and materials.")

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
            f"Delivery Distance for {name} (Extra KM only - local 30km included)",
            min_value=0, step=1, key=f"distance_{name}"
        )
    base_prices[name] = price

# Perform delivery calculation
delivery_result = calculate_material_delivery(loads, distances, base_prices)

st.subheader("📄 Material Delivery Summary")
for material, details in delivery_result["details"].items():
    st.markdown(f"**{material}**")
    st.write(f"- Loads: {details['loads']}")
    st.write(f"- Base Price (includes first {details['included_km']} km): ${details['base_price']:.2f}")
    st.write(f"- Entered Distance: {details['entered_km']} km")
    st.write(f"- Extra KM: {details['extra_km']} × $4.20 = ${details['extra_charge']:.2f}")
    st.write(f"- Subtotal Before Tax: ${details['subtotal']:.2f}")
    st.write(f"- HST (15%): ${details['hst']:.2f}")
    st.write(f"- Total for {details['loads']} Load(s): ${details['total']:.2f}")
    st.markdown("---")

st.markdown(f"### 💰 Total Material Delivery: **${delivery_result['total']:,.2f}**")

# ------------------------
# 🌱 Sod Installation Estimator
# ------------------------
st.header("🌾 Sod Installation Estimator")

area = st.number_input("Total Sod Area (sq ft)", min_value=0, step=10)
laborers = st.number_input("Number of Laborers", min_value=1, max_value=10, step=1)
labor_rate = st.number_input("Hourly Wage per Laborer ($)", min_value=1, step=1)
labor_hours = st.number_input("Hours per Laborer (rounded)", min_value=1, step=1)

st.subheader("🚜 Equipment")
equipment_types = ["Dump Truck", "Excavator", "Skid Steer"]
machine_inputs = []

for eq in equipment_types:
    st.markdown(f"**{eq}**")
    qty = st.number_input(f"How many {eq}s?", min_value=0, step=1, key=f"qty_{eq}")
    rate = st.number_input(f"Hourly Rate for {eq} ($)", min_value=0, step=1, key=f"rate_{eq}")
    hours = st.number_input(f"Hours on site per {eq}", min_value=0, step=1, key=f"hours_{eq}")
    trailer_km = st.number_input(f"Trailer Distance for {eq} (km)", min_value=0, step=1, key=f"trailer_km_{eq}")
    machine_inputs.append({"qty": qty, "hourly_rate": rate, "hours": hours, "trailer_km": trailer_km})

st.subheader("🚗 Passenger Vehicle Travel")
num_vehicles = st.number_input("Number of Passenger Vehicles", min_value=0, max_value=10, step=1)
travel_km = st.number_input("Travel Distance (km)", min_value=0, step=1)

sod_result = calculate_sod_quote(
    area=area,
    laborers=laborers,
    labor_rate=labor_rate,
    labor_hours=labor_hours,
    machines=machine_inputs,
    travel_km={"vehicles": num_vehicles, "km": travel_km},
)

st.subheader("📊 Sod Quote Breakdown")
st.write(f"**Total Area:** {sod_result['area']} sq ft")
st.write(f"**Sod Material Cost:** ${sod_result['sod_cost']:.2f}")
st.write(f"**Pallets Required:** {sod_result['pallets']} @ $25 = ${sod_result['pallet_cost']:.2f}")
st.write(f"**Labor Cost:** ${sod_result['labor_cost']:.2f}")
st.write(f"**Equipment Cost:** ${sod_result['equipment_cost']:.2f}")
st.write(f"**Passenger Vehicle Travel:** ${sod_result['travel_cost']:.2f}")
st.write(f"**Subtotal:** ${sod_result['subtotal']:.2f}")
st.write(f"**Total with HST:** ${sod_result['total']:.2f}")
