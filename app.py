import streamlit as st
from utils import calculate_material_delivery, calculate_sod_quote

st.set_page_config(page_title="AKL Sod Install Tool", layout="wide")

st.title("🌱 AKL Sod Install Tool")
st.markdown("Full estimator for sod installation, delivery, labor, equipment, travel, and materials.")

# --- Labor Section ---
st.header("👷 Labor")
num_laborers = st.number_input("Number of Laborers", min_value=1, step=1)
labor_inputs = []
for i in range(num_laborers):
    hours = st.number_input(f"Hours for Laborer #{i+1}", min_value=0, step=1, key=f"labor_hours_{i}")
    rate = st.number_input(f"Hourly Rate for Laborer #{i+1}", min_value=0, step=1, key=f"labor_rate_{i}")
    labor_inputs.append({"hours": hours, "rate": rate})

# --- Equipment Section ---
st.header("🚛 Equipment Use")
equipment_inputs = []
for eq in ["Excavator", "Skid Steer", "Dump Truck"]:
    hours = st.number_input(f"{eq} Hours", min_value=0, step=1, key=f"{eq}_hours")
    trailer_km = st.number_input(f"{eq} Trailer Km", min_value=0, step=1, key=f"{eq}_km")
    hourly_rate = st.number_input(f"{eq} Hourly Rate ($)", min_value=0, step=1, key=f"{eq}_rate")
    equipment_inputs.append({
        "hours": hours,
        "trailer_km": trailer_km,
        "hourly_rate": hourly_rate
    })

# --- Travel Section ---
st.header("🚗 Travel")
travel_km = st.number_input("Round Trip Distance (km)", min_value=0, step=1)
num_vehicles = st.number_input("Number of Passenger Vehicles", min_value=0, step=1)
travel_inputs = {"vehicles": num_vehicles, "km": travel_km}

# --- Extra Gravel Section ---
st.header("🪨 Extra Gravel")
extra_gravel_loads = st.number_input("Extra Gravel Loads", min_value=0, step=1)
gravel_price_per_load = st.number_input("Extra Gravel Price per Load ($)", min_value=0, step=1)
gravel_delivery_km = st.number_input("Delivery Distance (km)", min_value=0, step=1)
gravel_inputs = {
    "loads": extra_gravel_loads,
    "price": gravel_price_per_load,
    "km": gravel_delivery_km
}

# --- Overnight Stay Section ---
st.header("🏨 Overnight Stay")
room_cost = st.number_input("Room Cost ($)", min_value=0, step=1)
nights = st.number_input("Nights", min_value=0, step=1)
stay_inputs = {"rate": room_cost, "nights": nights}

# --- Sod Area ---
st.header("🌾 Sod Installation")
area = st.number_input("Total Sod Area (sq ft)", min_value=0, step=10)

# --- Run Calculation ---
if st.button("Calculate Quote"):
    result = calculate_sod_quote(
        area=area,
        labor_inputs=labor_inputs,
        equipment_inputs=equipment_inputs,
        travel_inputs=travel_inputs,
        gravel_inputs=gravel_inputs,
        stay_inputs=stay_inputs,
    )

    st.subheader("📊 Quote Breakdown")
    st.write(f"**Total Area:** {result['area']} sq ft")
    st.write(f"**Sod Material Cost:** ${result['sod_cost']:.2f}")
    st.write(f"**Pallets Required:** {result['pallets']}")
    st.write(f"**Pallet Cost:** ${result['pallet_cost']:.2f}")
    st.write(f"**Labor Cost:** ${result['labor_cost']:.2f}")
    st.write(f"**Equipment Cost:** ${result['equipment_cost']:.2f}")
    st.write(f"**Passenger Travel Cost:** ${result['travel_cost']:.2f}")
    st.write(f"**Extra Gravel Cost:** ${result['gravel_cost']:.2f}")
    st.write(f"**Overnight Stay:** ${result['stay_cost']:.2f}")
    st.write(f"**Subtotal:** ${result['subtotal']:.2f}")
    st.write(f"**Total (with HST):** ${result['total']:.2f}")
