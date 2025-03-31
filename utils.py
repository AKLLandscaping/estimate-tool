import streamlit as st
from utils import (
    calculate_sod_needs,
    calculate_equipment_cost,
    calculate_trailer_cost,
    calculate_passenger_vehicle_cost,
    calculate_total_quote
)
from datetime import datetime

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
# 🛏️ Overnight Stay
# -----------------------------
st.header("🛏️ Overnight Stay")
overnight_cost = st.number_input("Room Cost ($)", min_value=0)
overnight_nights = st.selectbox("Nights", list(range(0, 8)))
overnight_total = overnight_cost * overnight_nights

st.markdown("---")

# -----------------------------
# 👷 Labor
# -----------------------------
st.header("👷 Labor")
laborers = st.selectbox("Number of Laborers", list(range(1, 11)))
labor_data = []
for i in range(laborers):
    with st.container():
        st.markdown(f"**Laborer #{i+1}**")
        hours = st.selectbox(f"Hours for Laborer #{i+1}", list(range(1, 13)), key=f"hours_{i}")
        rate = st.selectbox(f"Hourly Rate for Laborer #{i+1}", [35, 40, 45, 50, 55, 60, 65], key=f"rate_{i}")
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
total_passenger_km = st.number_input("Round Trip Distance (km)", min_value=0, value=30)
num_passenger_vehicles = st.selectbox("Number of Passenger Vehicles", options=list(range(1, 11)), index=0)

st.markdown("---")

# -----------------------------
# 📊 Estimate Summary
# -----------------------------
st.header("📊 Estimate Summary")

pallets, sod_cost = calculate_sod_needs(sqft_needed)
equipment_cost = calculate_equipment_cost(excavator_hrs, skidsteer_hrs, dumptruck_hrs)
trailer_cost = calculate_trailer_cost(excavator_trailer_km, skidsteer_trailer_km, dumptruck_trailer_km)
vehicle_cost = calculate_passenger_vehicle_cost(total_passenger_km, num_passenger_vehicles)
labor_cost = sum([l['hours'] * l['rate'] for l in labor_data])
total, hst, grand_total = calculate_total_quote(sod_cost + labor_cost + overnight_total, equipment_cost, trailer_cost, vehicle_cost)

st.markdown(f"**Number of Pallets:** {pallets}")
st.markdown(f"**Sod Material Cost:** ${sod_cost:,.2f}")
st.markdown(f"**Labor Cost:** ${labor_cost:,.2f}")
st.markdown(f"**Overnight Stay:** ${overnight_total:,.2f}")
st.markdown(f"**Equipment Cost:** ${equipment_cost:,.2f}")
st.markdown(f"**Trailer Delivery:** ${trailer_cost:,.2f}")
st.markdown(f"**Passenger Vehicle Travel:** ${vehicle_cost:,.2f}")
st.markdown(f"**Subtotal:** ${total:,.2f}")
st.markdown(f"**HST (15%):** ${hst:,.2f}")
st.success(f"**Total Estimate: ${grand_total:,.2f}**")

# Footer branding
st.markdown("---")
st.caption("Built for AKL Landscaping · www.AKLLandscaping.com · 📞 902-802-4563")
