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
