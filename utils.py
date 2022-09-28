import json

def calc_tax_from_bands(val, bands):
    tax = 0
    prev_cap = 0
    for cap, rate in bands:
        if cap and cap < prev_cap:
            RuntimeError("error in tax bands")
        if cap is not None and val > cap:
            tax += (cap - prev_cap) * rate
            prev_cap = cap
        else:
            tax += (val - prev_cap) * rate
            break
    return tax


def load_tax_data(filename="tax_IE.json"):
    return json.loads(open(filename).read())

