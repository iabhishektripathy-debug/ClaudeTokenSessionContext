import json
import random
from pathlib import Path

random.seed(2726523)

# Output dir resolved relative to the repo root (scripts/ -> repo root -> resources).
OUT = Path(__file__).resolve().parent.parent / "src" / "main" / "resources"

# (brand, manufacturer)
BRANDS = [
    ("Luminis", "Acuity Brands"),
    ("Gotham", "Acuity Brands"),
    ("Lithonia Lighting", "Acuity Brands"),
    ("Mark Architectural", "Acuity Brands"),
    ("Peerless", "Acuity Brands"),
    ("Holophane", "Acuity Brands"),
    ("Winona Lighting", "Acuity Brands"),
    ("A-Light", "Acuity Brands"),
]

# (category, model_prefix, mounting, application, optic_type, shape)
TYPES = [
    ("Architectural Pendant Luminaire", "CT", "Catenary", "Outdoor", "Performance Optic", "pendant"),
    ("Suspended Linear Luminaire", "LN", "Suspended", "Indoor", "Diffuse Optic", "linear"),
    ("Recessed Downlight", "DL", "Recessed", "Indoor", "Reflector Optic", "round"),
    ("Wall Sconce", "WS", "Wall", "Outdoor", "Asymmetric Optic", "round"),
    ("Bollard", "BL", "Surface", "Outdoor", "Symmetric Optic", "column"),
    ("Area / Site Light", "AR", "Pole", "Outdoor", "Performance Optic", "rectangular"),
    ("Floodlight", "FL", "Yoke", "Outdoor", "Adjustable Optic", "rectangular"),
    ("Cylinder Pendant", "CY", "Pendant", "Indoor", "Performance Optic", "round"),
    ("In-Grade Luminaire", "IG", "In-grade", "Outdoor", "Narrow Optic", "round"),
    ("Surface Cylinder", "SC", "Surface", "Indoor", "Reflector Optic", "round"),
    ("Step / Path Light", "SP", "Recessed", "Outdoor", "Shielded Optic", "round"),
    ("Track Head", "TH", "Track", "Indoor", "Spot Optic", "round"),
]

CCT_SETS = [
    [2700, 3000, 3500, 4000],
    [3000, 4000],
    [2700, 3000],
    [3000, 3500, 4000, 5000],
    [4000],
    [2700, 3000, 3500, 4000, 5000],
]

DISTRIBUTIONS = [
    "Type II", "Type III", "Type IV", "Type V symmetric",
    "Narrow flood", "Medium flood", "Wide flood", "Asymmetric",
]

VOLTAGES = ["120-277V", "120-347V", "347-480V", "24V DC", "120V"]
DIMMING = ["0-10V", "DALI", "DMX", "TRIAC", "Phase-cut", "Lutron EcoSystem"]
DRIVERS = ["Constant current LED driver", "Constant voltage LED driver", "Programmable LED driver"]
SHIELDINGS = ["Fully shielded", "Semi-shielded", "Diffused", "Louvered", "Open"]
HOUSINGS = [
    "Extruded and die-cast aluminum",
    "Die-cast aluminum",
    "Extruded aluminum",
    "Stainless steel",
    "Marine-grade aluminum",
    "Powder-coated steel",
]
FINISHES = ["Black", "White", "Bronze", "Silver", "Graphite", "Custom RAL", "Brushed Aluminum", "Dark Sky Bronze"]
IP = ["IP20", "IP44", "IP65", "IP66", "IP67"]
IK = ["IK06", "IK07", "IK08", "IK09", "IK10"]
TEMP_RANGES = ["-40C to +40C", "-30C to +50C", "0C to +40C", "-20C to +45C"]
WARRANTIES = ["3-year limited warranty", "5-year limited warranty", "7-year limited warranty", "10-year limited warranty"]
LISTING_POOL = ["cULus Listed", "UL Listed", "Wet Location", "Damp Location", "Dry Location",
                "DLC Premium", "DLC Standard", "IP66 Rated", "Title 24 Compliant", "Energy Star"]
FAMILIES = ["Clermont", "Vega", "Aurora", "Helios", "Orion", "Lumen", "Solara", "Nimbus", "Atlas", "Cobalt",
            "Meridian", "Pinnacle", "Cascade", "Verve", "Halcyon"]

used_ids = {"2726523"}
def new_id():
    while True:
        pid = str(random.randint(1000000, 9999999))
        if pid not in used_ids:
            used_ids.add(pid)
            return pid

def slug(s):
    return "".join(c.lower() if c.isalnum() else "-" for c in s).strip("-").replace("--", "-")

count = 0
for _ in range(100):
    pid = new_id()
    category, prefix, mounting, application, optic_type, shape = random.choice(TYPES)
    brand, manufacturer = random.choice(BRANDS)
    family_base = random.choice(FAMILIES)
    series_num = random.choice([100, 110, 111, 200, 250, 300, 400, 500])
    model = f"{prefix}{random.randint(100, 999)}"
    family = f"{family_base} {prefix}{series_num} {mounting}"
    name = f"{family_base} {model}"

    cct = random.choice(CCT_SETS)
    cri = random.choice([70, 80, 90])
    lumens = random.choice([800, 1200, 1600, 2200, 3000, 3600, 4400, 6000, 8000, 10000, 14000, 18000])
    efficacy = round(random.uniform(95, 150), 1)
    wattage = round(lumens / efficacy, 1)
    distribution = random.choice(DISTRIBUTIONS)

    overview = (f"{model} is a {shape} {category.lower()} available in {mounting.lower()} mount. "
                f"With its {optic_type.lower().replace(' optic','')} optic it delivers up to {lumens} lumens "
                f"for {application.lower()} architectural applications.")

    if shape in ("linear",):
        dims = {"diameterMm": None, "heightMm": round(random.uniform(60, 120), 1),
                "lengthMm": round(random.choice([600, 1200, 1800, 2400]), 1)}
    elif shape in ("rectangular",):
        dims = {"diameterMm": None, "heightMm": round(random.uniform(120, 300), 1),
                "lengthMm": round(random.uniform(300, 800), 1)}
    elif shape in ("column",):
        dims = {"diameterMm": round(random.uniform(120, 200), 1),
                "heightMm": round(random.uniform(600, 1100), 1), "lengthMm": None}
    else:  # round
        dims = {"diameterMm": round(random.uniform(90, 360), 1),
                "heightMm": round(random.uniform(80, 260), 1), "lengthMm": None}

    finishes = random.sample(FINISHES, random.randint(2, 5))
    listings = random.sample(LISTING_POOL, random.randint(2, 4))
    dimming = random.sample(DIMMING, random.randint(1, 3))

    order_code = (f"{model}-{shape[:3].upper()}-{int(wattage)}W-{cct[0]//100}K-"
                  f"{cri}CRI-{mounting[:3].upper()}-{finishes[0][:3].upper()}-UNV")

    doc = {
        "productId": pid,
        "productOverview": overview,
        "modelNumber": model,
        "name": name,
        "family": family,
        "brand": brand,
        "manufacturer": manufacturer,
        "category": category,
        "mountingType": mounting,
        "application": application,
        "photometrics": {
            "maxDeliveredLumens": lumens,
            "availableCctKelvin": cct,
            "minCri": cri,
            "efficacyLumensPerWatt": efficacy,
            "distribution": distribution,
        },
        "electrical": {
            "wattage": wattage,
            "inputVoltageRange": random.choice(VOLTAGES),
            "frequencyHz": "50/60",
            "dimmingProtocols": dimming,
            "driverType": random.choice(DRIVERS),
        },
        "optics": {
            "type": optic_type,
            "beamDistribution": distribution,
            "shielding": random.choice(SHIELDINGS),
        },
        "physical": {
            "dimensions": dims,
            "weightKg": round(random.uniform(0.8, 18.0), 1),
            "housingMaterial": random.choice(HOUSINGS),
            "finishOptions": finishes,
            "ingressProtection": random.choice(IP),
        },
        "compliance": {
            "listings": listings,
            "ikRating": random.choice(IK),
            "operatingTempRange": random.choice(TEMP_RANGES),
            "darkSkyCompliant": application == "Outdoor" and random.random() < 0.6,
        },
        "warranty": random.choice(WARRANTIES),
        "ordering": {
            "catalogNumber": model,
            "sku": pid,
            "exampleOrderCode": order_code,
        },
        "datasheetUrl": (f"https://www.acuitybrands.com/products/detail/{pid}/"
                         f"{slug(brand)}/{slug(family)}/"),
    }

    (OUT / f"{pid}.json").write_text(json.dumps(doc, separators=(",", ":")))
    count += 1

print(f"wrote {count} files to {OUT}; total unique ids tracked = {len(used_ids)}")
