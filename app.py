import streamlit as st
import math

# Page setup
st.set_page_config(page_title="🌱 AKL Sod Estimate Tool", layout="centered")
st.title("🌱 AKL Sod Installation Quote")

st.markdown("---")

# Client Info
st.header("👤 Client Information")
client_name = st.text_input("Client Name")
address = st.text_input("Job Site Address")
phone = st.text_input("Phone Number")
email = st.text_input("Email Address")

st.markdown("---")

# Job Info
st.header("📐 Job Details")
sqft_needed = st.number_input("Total Square Footage of Sod Needed", min_value=0)
distance_km = st.number_input("One-Way Travel Distance to Site (km)", min_value=0.0)
laborers = st.slider("Number of Laborers", 1, 5, 2)

# Equipment selection
equipment = st.multiselect("Select Equipment Needed", [
    "Excavator ($130/hr)",
    "Skid Steer ($130/hr)",
    "Dump Truck ($130/hr)",
    "Travel Trailer ($250/day)"
])

delivery_needed = st.checkbox("Add Sod Delivery Charge?")
markup_percent = st.number_input("Markup % on Materials (0–100%)", value=20.0)

st.markdown("---")

# Constants
usable_sqft_per_pallet = 300
sod_price_per_sqft = 1.20
pallet_fee = 25
hst_rate = 0.15
passenger_vehicle_rate = 0.75
labor_rate_main = 65  # Devin
labor_rate_extra = 50  # others
prep_time_hr = 1  # 0.5 safety + 0.5 prep

# Calculations
num_pallets = math.ceil(sqft_needed / usable_sqft_per_pallet)
sod_cost = num_pallets * usable_sqft_per_pallet * sod_price_per_sqft
pallet_cost = num_pallets * pallet_fee
material_subtotal = sod_cost + pallet_cost
material_with_markup = material_subtotal * (1 + markup_percent / 100)

# Travel
round_trip_km = distance_km * 2
travel_hours = math.ceil((round_trip_km / 60))  # assume 60km/hr travel speed
travel_labor_cost = (labor_rate_main + (labor_rate_extra if laborers > 1 else 0)) * travel_hours
passenger_vehicle_cost = round_trip_km * passenger_vehicle_rate if laborers > 1 else 0

# Equipment costs
equipment_cost = 0
for item in equipment:
    if "Excavator" in item or "Skid Steer" in item or "Dump Truck" in item:
        equipment_cost += 130 * travel_hours
    elif "Travel Trailer" in item:
        equipment_cost += 250

# Delivery (optional flat fee)
delivery_cost = 150 if delivery_needed else 0

# Labor (basic day estimate — customizable later)
day_hours = 8  # Full day default
labor_cost = labor_rate_main * day_hours
if laborers > 1:
    labor_cost += labor_rate_extra * day_hours * (laborers - 1)

# Totals
subtotal = material_with_markup + travel_labor_cost + passenger_vehicle_cost + equipment_cost + delivery_cost + labor_cost
tax = subtotal * hst_rate
total = subtotal + tax

# Display quote
st.header("📊 Estimate Summary")
st.write(f"**Number of Pallets:** {num_pallets}")
st.write(f"**Sod Material + Pallet Cost (with {markup_percent:.0f}% markup):** ${material_with_markup:,.2f}")
st.write(f"**Labor Cost:** ${labor_cost:,.2f}")
st.write(f"**Travel Labor Cost:** ${travel_labor_cost:,.2f}")
st.write(f"**Passenger Vehicle Travel Cost:** ${passenger_vehicle_cost:,.2f}")
st.write(f"**Equipment Cost:** ${equipment_cost:,.2f}")
if delivery_needed:
    st.write(f"**Delivery Cost:** ${delivery_cost:,.2f}")
st.write(f"**Subtotal:** ${subtotal:,.2f}")
st.write(f"**HST (15%):** ${tax:,.2f}")
st.success(f"**Total Estimate: ${total:,.2f}**")

st.markdown("---")
st.caption("Built for AKL Landscaping · www.AKLLandscaping.com · ☎ 902-802-4563")
