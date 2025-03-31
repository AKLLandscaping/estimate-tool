import streamlit as st
from utils import (
    calculate_sod_needs,
    calculate_equipment_cost,
    calculate_trailer_cost,
    calculate_passenger_vehicle_cost,
    calculate_total_quote
)
from datetime import datetime
import math

st.set_page_config(page_title="🌱 AKL Sod Estimate Tool", layout="centered")
st.title("🌱 AKL Sod Installation Quote")
st.markdown("---")

# -----------------------------
# 👤 Client Information
# -----------------------------
st.header("👤 Client Information")
client_name = st.text_input("Client Name")
address = st.text_input("Job Site Address")
phone = st.text_input("Phone Number")
email = st.text_input("Email Address")

st.markdown("---")

# -----------------------------
# 📐 Sod Requirements
# -----------------------------
st.header("📐 Sod Requirements")
sqft_needed = st.number_input("Total Square Footage of Sod Needed", min_value=0)

st.markdown("---")

# -----------------------------
# 🪨 Material Delivery
# -----------------------------
st.header("🪨 Material Delivery")
gravel_km = st.number_input("Gravel Delivery Distance (km)", min_value=0, step=1)
topsoil_km = st.number_input("Topsoil Delivery Distance (km)", min_value=0, step=1)
compost_km = st.number_input("Compost Delivery Distance (km)", min_value=0, step=1)

# Base costs + extra distance charge (>30km)
def material_cost(base_price, distance):
    km_extra = max(0, distance - 30)
    return base_price + (km_extra * 4.20 * 1.15)

gravel_cost = material_cost(250 * 1.15, gravel_km) if gravel_km > 0 else 0
topsoil_cost = material_cost(250 * 1.15, topsoil_km) if topsoil_km > 0 else 0
compost_cost = material_cost(450 * 1.15, compost_km) if compost_km > 0 else 0

st.markdown("---")

# -----------------------------
# 🌿 Add-On Options Per Pallet
# -----------------------------
st.header("🌿 Add-On Services")
add_lime = st.checkbox("Lime Installed ($50 + tax per pallet)")
add_fertilizer = st.checkbox("Fertilizer Installed ($150 + tax per pallet)")
add_overseeding = st.checkbox("Overseeding Installed ($100 + tax per pallet)")
add_sprinklers = st.checkbox("Sprinklers Installed ($100 + tax per pallet)")

st.markdown("---")

# -----------------------------
# 🛏️ Overnight Stay
# -----------------------------
st.header("🛏️ Overnight Stay")
overnight_cost = st.number_input("Room Cost ($)", min_value=0, step=1)
overnight_nights = st.number_input("Nights", min_value=0, step=1)
overnight_total = overnight_cost * overnight_nights

st.markdown("---")

# -----------------------------
# 👷 Labor
# -----------------------------
st.header("👷 Labor")
laborers = st.number_input("Number of Laborers", min_value=1, max_value=10, step=1)
labor_data = []
for i in range(int(laborers)):
    st.markdown(f"**Laborer #{i+1}**")
    rate = st.number_input(f"Hourly Rate for Laborer #{i+1} (with tax)", min_value=0, step=1, key=f"rate_{i}")
    hours = st.number_input(f"Hours per Day for Laborer #{i+1}", min_value=0, step=1, key=f"hours_{i}")
    labor_data.append({"hours": hours, "rate": rate})

st.markdown("---")

# -----------------------------
# 🚜 Equipment Use
# -----------------------------
st.header("🚜 Equipment Use")
excavator_hrs = st.number_input("Excavator Hours", min_value=0, step=1)
skidsteer_hrs = st.number_input("Skid Steer Hours", min_value=0, step=1)
dumptruck_hrs = st.number_input("Dump Truck Hours", min_value=0, step=1)

excavator_trailer_km = st.number_input("Excavator Trailer Km", min_value=0, step=1, value=30)
skidsteer_trailer_km = st.number_input("Skid Steer Trailer Km", min_value=0, step=1, value=30)
dumptruck_trailer_km = st.number_input("Dump Truck Trailer Km", min_value=0, step=1, value=30)

st.markdown("---")

# -----------------------------
# 🚗 Travel
# -----------------------------
st.header("🚗 Travel")
total_passenger_km = st.number_input("Round Trip Distance (km)", min_value=0, step=1, value=30)
num_passenger_vehicles = st.number_input("Number of Passenger Vehicles", min_value=1, max_value=10, step=1)

st.markdown("---")

# -----------------------------
# 📊 Estimate Summary
# -----------------------------
st.header("📊 Estimate Summary")

pallets, sod_cost = calculate_sod_needs(sqft_needed)
equipment_cost = calculate_equipment_cost(excavator_hrs, skidsteer_hrs, dumptruck_hrs)
trailer_cost = calculate_trailer_cost(excavator_trailer_km, skidsteer_trailer_km, dumptruck_trailer_km)
vehicle_cost = calculate_passenger_vehicle_cost(total_passenger_km, num_passenger_vehicles)
labor_cost = sum([math.ceil(l['hours']) * l['rate'] for l in labor_data])

# Add-on costs per pallet
lime_cost = pallets * 50 * 1.15 if add_lime else 0
fertilizer_cost = pallets * 150 * 1.15 if add_fertilizer else 0
overseed_cost = pallets * 100 * 1.15 if add_overseeding else 0
sprinkler_cost = pallets * 100 * 1.15 if add_sprinklers else 0

addon_cost = lime_cost + fertilizer_cost + overseed_cost + sprinkler_cost
material_cost_total = gravel_cost + topsoil_cost + compost_cost

# Final total
subtotal_items = sod_cost + labor_cost + overnight_total + addon_cost + material_cost_total
total, hst, grand_total = calculate_total_quote(subtotal_items, equipment_cost, trailer_cost, vehicle_cost)

st.markdown(f"**Number of Pallets:** {pallets}")
st.markdown(f"**Sod Material Cost:** ${sod_cost:,.2f}")
st.markdown(f"**Labor Cost:** ${labor_cost:,.2f}")
st.markdown(f"**Overnight Stay:** ${overnight_total:,.2f}")
st.markdown(f"**Material Delivery (Gravel/Topsoil/Compost):** ${material_cost_total:,.2f}")
st.markdown(f"**Add-On Services:** ${addon_cost:,.2f}")
st.markdown(f"**Equipment Cost:** ${equipment_cost:,.2f}")
st.markdown(f"**Trailer Delivery:** ${trailer_cost:,.2f}")
st.markdown(f"**Passenger Vehicle Travel:** ${vehicle_cost:,.2f}")
st.markdown(f"**Subtotal:** ${total:,.2f}")
st.markdown(f"**HST (15%):** ${hst:,.2f}")
st.success(f"**Total Estimate: ${grand_total:,.2f}**")

# Footer branding
st.markdown("---")
st.caption("Built for AKL Landscaping · www.AKLLandscaping.com · 📞 902-802-4563")
