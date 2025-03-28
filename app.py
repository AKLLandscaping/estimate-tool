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

# Equipment usage
st.subheader("🚜 Equipment Usage (Hourly)")
excavator_hrs = st.number_input("Excavator Hours", min_value=0, step=1)
skidsteer_hrs = st.number_input("Skid Steer Hours", min_value=0, step=1)
dumptruck_hrs = st.number_input("Dump Truck Hours", min_value=0, step=1)

# Trailer delivery per machine
st.subheader("🛻 Trailer Delivery Per Machine")
excavator_trailer_km = st.number_input("Trailer Round Trip Distance for Excavator (km)", min_value=0)
skidsteer_trailer_km = st.number_input("Trailer Round Trip Distance for Skid Steer (km)", min_value=0)
dumptruck_trailer_km = st.number_input("Trailer Round Trip Distance for Dump Truck (km)", min_value=0)

# Markup
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
equipment_cost = (
    excavator_hrs * 130 +
    skidsteer_hrs * 130 +
    dumptruck_hrs * 130
)

# Trailer delivery costs per machine
def calc_trailer_cost(trip_km):
    trips = trip_km / 25
    return math.ceil(trips) * 250 * (1 + hst_rate)

excavator_trailer_cost = calc_trailer_cost(excavator_trailer_km) if excavator_trailer_km > 0 else 0
skidsteer_trailer_cost = calc_trailer_cost(skidsteer_trailer_km) if skidsteer_trailer_km > 0 else 0
dumptruck_trailer_cost = calc_trailer_cost(dumptruck_trailer_km) if dumptruck_trailer_km > 0 else 0
trailer_cost = excavator_trailer_cost + skidsteer_trailer_cost + dumptruck_trailer_cost

# Sod pickup rules
pickup_cost = 0
if num_pallets <= 2:
    pickup_cost = dumptruck_hrs * 130
elif 3 <= num_pallets <= 6:
    pickup_cost = dumptruck_hrs * 130 + trailer_cost

# Labor (basic day estimate — customizable later)
day_hours = 8  # Full day default
labor_cost = labor_rate_main * day_hours
if laborers > 1:
    labor_cost += labor_rate_extra * day_hours * (laborers - 1)

# Totals
subtotal = material_with_markup + travel_labor_cost + passenger_vehicle_cost + equipment_cost + trailer_cost + pickup_cost + labor_cost
tax = subtotal * hst_rate
total = subtotal + tax

# Display quote
st.header("📊 Estimate Summary")
st.write(f"**Number of Pallets:** {num_pallets}")
st.write(f"**Sod Material + Pallet Cost (with {markup_percent:.0f}% markup):** ${material_with_markup:,.2f}")
st.write(f"**Labor Cost:** ${labor_cost:,.2f}")
st.write(f"**Travel Labor Cost:** ${travel_labor_cost:,.2f}")
st.write(f"**Passenger Vehicle Travel Cost (Round Trip):** ${passenger_vehicle_cost:,.2f}")
st.write(f"**Equipment Cost:** ${equipment_cost:,.2f}")
if trailer_cost > 0:
    st.write(f"**Trailer Delivery Cost (Total):** ${trailer_cost:,.2f}")
if pickup_cost > 0:
    st.write(f"**Sod Pickup Cost (based on pallet quantity):** ${pickup_cost:,.2f}")
st.write(f"**Subtotal:** ${subtotal:,.2f}")
st.write(f"**HST (15%):** ${tax:,.2f}")
st.success(f"**Total Estimate: ${total:,.2f}**")

st.markdown("---")
st.caption("Built for AKL Landscaping · www.AKLLandscaping.com · ☎ 902-802-4563")

