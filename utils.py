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
# 🌱 Sod Installation Estimator
# ------------------------
st.header("🌱 Sod Installation Estimator")

area = st.number_input("Total Sod Area (sq ft)", min_value=0)
cost_per_sqft = 1.20
st.write(f"**Sod Cost per Sq Ft:** ${cost_per_sqft:.2f}")

# Labor section
st.subheader("👷 Labor")
laborers = st.number_input("Number of Laborers", min_value=1, max_value=10, step=1)
labor_hours = st.number_input("Hours per Laborer (rounded)", min_value=1, step=1)
labor_rate = st.number_input("Hourly Wage ($)", min_value=1, step=1)
labor_cost = laborers * labor_hours * labor_rate

# Equipment section
st.subheader("🚜 Equipment")
equipment_totals = 0

equipment_types = ["Dump Truck", "Excavator", "Skid Steer"]
equipment_data = {}
for eq in equipment_types:
    st.markdown(f"**{eq}**")
    qty = st.number_input(f"How many {eq}s?", min_value=0, step=1, key=f"qty_{eq}")
    rate = st.number_input(f"Hourly Rate for {eq} ($)", min_value=0, step=1, key=f"rate_{eq}")
    hours = st.number_input(f"Hours on site per {eq}", min_value=0, step=1, key=f"hours_{eq}")
    trailer_km = st.number_input(f"Trailer Distance for {eq} (km)", min_value=0, step=1, key=f"trailer_km_{eq}")
    trailer_cost = (250 + max(0, trailer_km - 30) * 4.20) * 1.15  # tax included
    total_eq = qty * ((hours * rate) + trailer_cost)
    equipment_data[eq] = total_eq
    equipment_totals += total_eq

# Passenger Vehicle Travel
st.subheader("🚗 Passenger Vehicle Travel")
num_vehicles = st.number_input("Number of Passenger Vehicles", min_value=0, max_value=10, step=1)
travel_km = st.number_input("Travel Distance (km)", min_value=0, step=1)
travel_cost = num_vehicles * travel_km * 0.80

# Sod and pallet costs
pallet_coverage = 300
pallets = math.ceil(area / pallet_coverage)
sod_cost = area * cost_per_sqft
pallet_cost = pallets * 25

# Total calc
hst = 0.15
subtotal = sum(equipment_data.values()) + travel_cost + labor_cost + sod_cost + pallet_cost
total = subtotal * (1 + hst)

st.subheader("📊 Sod Quote Breakdown")
st.write(f"**Total Area:** {area} sq ft")
st.write(f"**Sod Material Cost:** ${sod_cost:.2f}")
st.write(f"**Pallets Required:** {pallets} @ $25 each = ${pallet_cost:.2f}")
st.write(f"**Labor Cost:** ${labor_cost:.2f}")
st.write(f"**Equipment Cost (with trailer):** ${equipment_totals:.2f}")
st.write(f"**Passenger Vehicle Travel:** ${travel_cost:.2f}")
st.write(f"**Subtotal:** ${subtotal:.2f}")
st.write(f"**Total with HST (15%):** ${total:.2f}")

# ------------------------
# 📍 Future Sections
# ------------------------
st.markdown("---")
st.info("More estimator tools coming soon: Walkways, Retaining Walls, Fire Pits, and Steps.")
