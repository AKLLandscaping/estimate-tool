
def calculate_sod_needs(sqft_needed):
    cost_per_sqft = 1.20
    usable_sqft_per_pallet = 300
    pallet_fee = 25
    pallets = -(-sqft_needed // usable_sqft_per_pallet)  # round up
    sod_cost = (sqft_needed * cost_per_sqft) + (pallets * pallet_fee)
    return int(pallets), round(sod_cost, 2)

def calculate_equipment_cost(excavator_hrs, skidsteer_hrs, dumptruck_hrs):
    hourly_rate = 130
    total = (excavator_hrs + skidsteer_hrs + dumptruck_hrs) * hourly_rate
    return round(total, 2)

def calculate_trailer_cost(excavator_km, skidsteer_km, dumptruck_km):
    base_km = 30
    extra_km_rate = 4.20
    base_fee = 250
    def trailer_fee(km):
        if km == 0:
            return 0
        elif km <= base_km:
            return base_fee
        else:
            extra_km = km - base_km
            return base_fee + (extra_km * extra_km_rate)
    total = trailer_fee(excavator_km) + trailer_fee(skidsteer_km) + trailer_fee(dumptruck_km)
    return round(total, 2)

def calculate_passenger_vehicle_cost(round_trip_km, vehicles):
    rate_per_km = 0.80
    return round(round_trip_km * vehicles * rate_per_km, 2)

def calculate_total_quote(sod, equipment, trailer, vehicle):
    subtotal = sod + equipment + trailer + vehicle
    hst = round(subtotal * 0.15, 2)
    total = round(subtotal + hst, 2)
    return subtotal, hst, total
