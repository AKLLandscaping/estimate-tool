import streamlit as st
from utils import calculate_material_delivery, calculate_sod_quote

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

delivery_result = calculate_material_delivery(loads, distances, base_prices)

st.markdown("### 🧾 Material Delivery Summary")
for material, total in delivery_result["per_material"].items():
    if total > 0:
        st.write(f"**{material}**: ${total:,.2f}")

st.markdown(f"### 💰 Total Material Delivery: **${delivery_result['total']:,.2f}**")

# ------------------------
# 🌱 Sod Installation Estimator
# ------------------------
st.header("🌱 Sod Installation Estimator")

area = st.number_input("Total Area (sq ft)", min_value=0)
distance_km = st.number_input("Travel Distance (km)", min_value=0)
num_labourers = st.selectbox("Number of Laborers", list(range(1, 6)), index=1)
dump_truck = st.checkbox("Dump Truck")
skid_steer = st.checkbox("Skid Steer")
excavator = st.checkbox("Excavator")
travel_trailer_km = st.number_input("Travel Trailer Distance (km)", min_value=0)
passenger_vehicle_km = st.number_input("Passenger Vehicle Distance (km)", min_value=0)

if st.button("Calculate Sod Quote"):
    sod_result = calculate_sod_quote(
        area,
        distance_km,
        num_labourers,
        dump_truck,
        skid_steer,
        excavator,
        travel_trailer_km,
        passenger_vehicle_km
    )

    st.subheader("Sod Installation Quote")
    for k, v in sod_result.items():
        st.write(f"**{k}**: ${v:,.2f}")

# ------------------------
# 📍 Future Sections
# ------------------------
st.markdown("---")
st.info("More estimator tools coming soon: Walkways, Retaining Walls, Fire Pits, and Steps.")
