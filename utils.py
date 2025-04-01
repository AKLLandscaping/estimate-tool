
def calculate_material_delivery(loads, distances, base_prices):
    HST_RATE = 0.15
    EXTRA_KM_RATE = 4.20
    INCLUDED_KM = 30

    material_details = {}
    grand_total = 0

    for material in loads:
        num_loads = loads[material]
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
            "total": round(total_for_material, 2),
            "included_km": INCLUDED_KM,
            "entered_km": distance
        }

        grand_total += total_for_material

    return {
        "details": material_details,
        "total": round(grand_total, 2)
    }

def calculate_sod_quote(area, laborers, labor_rate, labor_hours, machines, travel_km, pallet_price=25, pallet_coverage=300):
    HST_RATE = 0.15
    SOD_COST_PER_SQFT = 1.20
    TRAILER_BASE_COST = 250
    TRAILER_KM_RATE = 4.20
    TRAILER_INCLUDED_KM = 30
    VEHICLE_KM_RATE = 0.80

    pallets = -(-area // pallet_coverage)  # ceil division
    sod_cost = area * SOD_COST_PER_SQFT
    pallet_cost = pallets * pallet_price

    labor_cost = laborers * labor_hours * labor_rate

    equipment_cost = 0
    for m in machines:
        qty = m["qty"]
        rate = m["hourly_rate"]
        hours = m["hours"]
        trailer_km = m["trailer_km"]
        trailer_cost = (TRAILER_BASE_COST + max(0, trailer_km - TRAILER_INCLUDED_KM) * TRAILER_KM_RATE) * 1.15
        equipment_cost += qty * ((hours * rate) + trailer_cost)

    vehicle_travel_cost = travel_km["vehicles"] * travel_km["km"] * VEHICLE_KM_RATE

    subtotal = sod_cost + pallet_cost + labor_cost + equipment_cost + vehicle_travel_cost
    total = subtotal * (1 + HST_RATE)

    return {
        "area": area,
        "pallets": pallets,
        "sod_cost": sod_cost,
        "pallet_cost": pallet_cost,
        "labor_cost": labor_cost,
        "equipment_cost": equipment_cost,
        "travel_cost": vehicle_travel_cost,
        "subtotal": subtotal,
        "total": total
    }
