def calculate_material_delivery(loads, distances, base_prices):
    HST_RATE = 0.15
    EXTRA_KM_RATE = 4.20
    INCLUDED_KM = 30

    material_totals = {}
    grand_total = 0

    for material in loads:
        num_loads = loads[material]
        distance = distances[material]
        base_price = base_prices[material]

        if num_loads == 0:
            material_totals[material] = 0
            continue

        extra_km = max(0, distance - INCLUDED_KM)
        extra_charge = extra_km * EXTRA_KM_RATE
        load_price_before_tax = base_price + extra_charge
        load_price_with_tax = load_price_before_tax * (1 + HST_RATE)
        total_for_material = load_price_with_tax * num_loads

        material_totals[material] = round(total_for_material, 2)
        grand_total += total_for_material

    return {
        "per_material": material_totals,
        "total": round(grand_total, 2)
    }

def calculate_sod_quote(area, travel_km, num_labourers, dump_truck, skid_steer, excavator, trailer_km, passenger_km):
    HST = 0.15
    SOD_COST = 1.20
    PALLET_FEE = 25
    PALLET_COVERAGE = 300
    PREP_TIME = 1  # 30 min safety + 30 min prep
    SAFETY_TIME = 1
    LABOUR_RATE = 50
    EQUIP_RATE = 130
    TRUCK_PASSENGER_KM_COST = 0.80
    TRAILER_BASE = 250
    TRAILER_EXTRA_RATE = 4.20
    TRAILER_INCLUDED_KM = 30

    pallets_needed = -(-area // PALLET_COVERAGE)
    sod_material_cost = area * SOD_COST
    pallet_cost = pallets_needed * PALLET_FEE

    labour_hours = PREP_TIME + SAFETY_TIME + (travel_km / 60) * 2 + 6
    labour_cost = labour_hours * num_labourers * LABOUR_RATE

    equip_cost = 0
    if dump_truck:
        equip_cost += EQUIP_RATE
    if skid_steer:
        equip_cost += EQUIP_RATE
    if excavator:
        equip_cost += EQUIP_RATE

    trailer_cost = TRAILER_BASE
    if trailer_km > TRAILER_INCLUDED_KM:
        trailer_cost += (trailer_km - TRAILER_INCLUDED_KM) * TRAILER_EXTRA_RATE

    travel_cost = passenger_km * TRUCK_PASSENGER_KM_COST

    subtotal = sod_material_cost + pallet_cost + labour_cost + equip_cost + trailer_cost + travel_cost
    total = subtotal * (1 + HST)

    return {
        "Sod Material": round(sod_material_cost, 2),
        "Pallet Fees": round(pallet_cost, 2),
        "Labour Cost": round(labour_cost, 2),
        "Equipment Cost": round(equip_cost, 2),
        "Trailer Transport": round(trailer_cost, 2),
        "Passenger Travel": round(travel_cost, 2),
        "Total with HST": round(total, 2)
    }
