loads = {
    "Screened Topsoil": screened_topsoil_loads,
    "Triple Mix Garden Soil": garden_soil_loads,
    "Screened Compost": compost_loads,
    "Screened Sand": screened_sand_loads,
    "Electrical Trench Sand": trench_sand_loads,
    "Crusher Dust": crusher_dust_loads,
    "Peastone": peastone_loads,
    "Clearstone/Class A/B Gravel": clearstone_loads
}

distances = {
    "Screened Topsoil": screened_topsoil_km,
    "Triple Mix Garden Soil": garden_soil_km,
    "Screened Compost": compost_km,
    "Screened Sand": screened_sand_km,
    "Electrical Trench Sand": trench_sand_km,
    "Crusher Dust": crusher_dust_km,
    "Peastone": peastone_km,
    "Clearstone/Class A/B Gravel": clearstone_km
}

base_prices = {
    "Screened Topsoil": 250,
    "Triple Mix Garden Soil": 300,
    "Screened Compost": 450,
    "Screened Sand": 200,
    "Electrical Trench Sand": 320,
    "Crusher Dust": 320,
    "Peastone": 330,
    "Clearstone/Class A/B Gravel": 250
}

delivery_result = calculate_material_delivery(loads, distances, base_prices)

st.subheader("Material Delivery Summary")
for material, total in delivery_result["per_material"].items():
    if total > 0:
        st.write(f"**{material}**: ${total:,.2f}")

st.markdown(f"### 🧾 Total Material Delivery: **${delivery_result['total']:,.2f}**")
