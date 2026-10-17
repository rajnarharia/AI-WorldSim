"""
Phase 10.5 — Role-Specific Condition Containers & Library
Contains comprehensive conditions (60-80 per role) for:
1. POLICE
2. GOVERNMENT
3. CITIZEN
4. BUSINESS
5. CAR
"""

import random
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class RoleCondition(BaseModel):
    condition_id: str
    role: str
    category: str
    description: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    possible_effects: List[str]
    resource_relevance: List[str]
    priority: int  # 1 to 5 (5 highest)
    tags: List[str]

# ---------------------------------------------------------------------------
# 1. POLICE CONDITIONS (70 conditions)
# ---------------------------------------------------------------------------
POLICE_CONDITIONS: List[Dict[str, Any]] = [
    {"id": "POL_001", "cat": "CRIME", "desc": "Armed robbery in progress at commercial bank", "sev": "CRITICAL", "eff": ["Hostage risk", "Public panic"], "res": ["officers", "vehicles", "tactical"], "pri": 5, "tags": ["violent", "bank", "armed"]},
    {"id": "POL_002", "cat": "CRIME", "desc": "Violent assault reported in downtown entertainment district", "sev": "HIGH", "eff": ["Victim injury", "Suspect fleeing"], "res": ["officers", "vehicles"], "pri": 4, "tags": ["assault", "downtown"]},
    {"id": "POL_003", "cat": "CRIME", "desc": "Shoplifting gang targeting retail shopping mall", "sev": "MEDIUM", "eff": ["Property loss"], "res": ["officers"], "pri": 2, "tags": ["theft", "retail"]},
    {"id": "POL_004", "cat": "CRIME", "desc": "Burglary alarm triggered at high-value jewelry boutique", "sev": "HIGH", "eff": ["Property theft", "Potential standoff"], "res": ["officers", "vehicles"], "pri": 4, "tags": ["burglary", "commercial"]},
    {"id": "POL_005", "cat": "CRIME", "desc": "Armed suspect spotted fleeing into subway transit station", "sev": "CRITICAL", "eff": ["Transit shutdown", "Civilian danger"], "res": ["officers", "tactical"], "pri": 5, "tags": ["armed", "transit"]},
    {"id": "POL_006", "cat": "CRIME", "desc": "Vehicle theft reported in residential parking facility", "sev": "LOW", "eff": ["Vehicle loss"], "res": ["officers"], "pri": 2, "tags": ["auto-theft", "residential"]},
    {"id": "POL_007", "cat": "CRIME", "desc": "Domestic dispute with reports of escalating violence", "sev": "HIGH", "eff": ["Domestic harm"], "res": ["officers"], "pri": 4, "tags": ["domestic", "residential"]},
    {"id": "POL_008", "cat": "CRIME", "desc": "Narcotics distribution hub suspected in warehouse area", "sev": "MEDIUM", "eff": ["Neighborhood illicit trade"], "res": ["investigators", "officers"], "pri": 3, "tags": ["narcotics", "investigation"]},
    {"id": "POL_009", "cat": "CRIME", "desc": "Vandalism and property defacement at government monument", "sev": "LOW", "eff": ["Aesthetic damage"], "res": ["officers"], "pri": 1, "tags": ["vandalism", "public"]},
    {"id": "POL_010", "cat": "CRIME", "desc": "Drive-by shooting reported near Central Park perimeter", "sev": "CRITICAL", "eff": ["Casualties", "Fleeing vehicle"], "res": ["officers", "vehicles", "medical"], "pri": 5, "tags": ["shooting", "violent", "drive-by"]},
    {"id": "POL_011", "cat": "RESOURCES", "desc": "Severe officer shortage due to departmental flu outbreak", "sev": "HIGH", "eff": ["Longer response times"], "res": ["officers"], "pri": 4, "tags": ["shortage", "health", "personnel"]},
    {"id": "POL_012", "cat": "RESOURCES", "desc": "Patrol vehicles grounded for urgent fleet brake repairs", "sev": "HIGH", "eff": ["Reduced mobility"], "res": ["vehicles"], "pri": 4, "tags": ["maintenance", "fleet", "vehicles"]},
    {"id": "POL_013", "cat": "RESOURCES", "desc": "Radio communication repeater failure in North sector", "sev": "HIGH", "eff": ["Dispatch blackout in sector"], "res": ["communications"], "pri": 4, "tags": ["comms", "technical"]},
    {"id": "POL_014", "cat": "RESOURCES", "desc": "Dispatch center computer system intermittent lagging", "sev": "MEDIUM", "eff": ["Call queuing delay"], "res": ["dispatch"], "pri": 3, "tags": ["software", "dispatch"]},
    {"id": "POL_015", "cat": "RESOURCES", "desc": "Tactical ballistic gear undergoing recertification inspection", "sev": "LOW", "eff": ["Limited tactical readiness"], "res": ["tactical"], "pri": 2, "tags": ["equipment", "tactical"]},
    {"id": "POL_016", "cat": "RESOURCES", "desc": "K-9 unit deployed at airport security drill", "sev": "LOW", "eff": ["K-9 support unavailable"], "res": ["k9"], "pri": 1, "tags": ["k9", "availability"]},
    {"id": "POL_017", "cat": "RESOURCES", "desc": "Officer shift change underway causing temporary gap", "sev": "MEDIUM", "eff": ["15-minute coverage dip"], "res": ["officers"], "pri": 3, "tags": ["shift", "coverage"]},
    {"id": "POL_018", "cat": "RESOURCES", "desc": "Fuel rationing in place at precinct pump station", "sev": "MEDIUM", "eff": ["Vehicle mileage constraints"], "res": ["vehicles", "fuel"], "pri": 3, "tags": ["fuel", "fleet"]},
    {"id": "POL_019", "cat": "RESOURCES", "desc": "Holding cells at 95% capacity pending court transfers", "sev": "HIGH", "eff": ["Arrest processing bottleneck"], "res": ["jail", "officers"], "pri": 4, "tags": ["custody", "overcrowding"]},
    {"id": "POL_020", "cat": "RESOURCES", "desc": "Backup units delayed by highway bridge maintenance work", "sev": "MEDIUM", "eff": ["Arrival lag of 12 minutes"], "res": ["backup"], "pri": 3, "tags": ["backup", "traffic"]},
    {"id": "POL_021", "cat": "PUBLIC_ORDER", "desc": "Unauthorized protest blocking main arterial boulevard", "sev": "HIGH", "eff": ["Gridlock", "Civil tension"], "res": ["officers", "crowd_control"], "pri": 4, "tags": ["protest", "traffic", "crowd"]},
    {"id": "POL_022", "cat": "PUBLIC_ORDER", "desc": "Brawl erupting outside sports arena after playoff match", "sev": "HIGH", "eff": ["Spectator injuries", "Vandalism"], "res": ["officers", "vehicles"], "pri": 4, "tags": ["brawl", "sports", "crowd"]},
    {"id": "POL_023", "cat": "PUBLIC_ORDER", "desc": "Large street party exceeding noise and occupancy limits", "sev": "LOW", "eff": ["Noise complaints"], "res": ["officers"], "pri": 1, "tags": ["noise", "party"]},
    {"id": "POL_024", "cat": "PUBLIC_ORDER", "desc": "Counter-demonstrators clashing near City Hall gates", "sev": "CRITICAL", "eff": ["Physical violence", "Civic disruption"], "res": ["officers", "crowd_control", "medical"], "pri": 5, "tags": ["protest", "clash", "civic"]},
    {"id": "POL_025", "cat": "PUBLIC_ORDER", "desc": "Aggressive panhandling ring reported at metro entrances", "sev": "LOW", "eff": ["Commuter harassment"], "res": ["officers"], "pri": 2, "tags": ["disorder", "transit"]},
    {"id": "POL_026", "cat": "PUBLIC_ORDER", "desc": "Flash mob organizing disruptive gathering at plaza", "sev": "MEDIUM", "eff": ["Pedestrian blockage"], "res": ["officers"], "pri": 3, "tags": ["crowd", "plaza"]},
    {"id": "POL_027", "cat": "PUBLIC_ORDER", "desc": "Heated argument between street vendors over market spots", "sev": "LOW", "eff": ["Minor disturbance"], "res": ["officers"], "pri": 2, "tags": ["dispute", "market"]},
    {"id": "POL_028", "cat": "PUBLIC_ORDER", "desc": "Crowd surging past security barricades at outdoor concert", "sev": "CRITICAL", "eff": ["Crush danger", "Stampede risk"], "res": ["officers", "medical", "vehicles"], "pri": 5, "tags": ["crowd", "stampede", "concert"]},
    {"id": "POL_029", "cat": "PUBLIC_ORDER", "desc": "Intoxicated individuals harassing patrons outside tavern", "sev": "MEDIUM", "eff": ["Public annoyance", "Brawl risk"], "res": ["officers"], "pri": 2, "tags": ["intoxication", "nightlife"]},
    {"id": "POL_030", "cat": "PUBLIC_ORDER", "desc": "Illegal street racing meetup taking over industrial bypass", "sev": "HIGH", "eff": ["High-speed collision risk"], "res": ["vehicles", "officers"], "pri": 4, "tags": ["racing", "traffic", "hazard"]},
    {"id": "POL_031", "cat": "TRAFFIC_ACCIDENT", "desc": "Multi-car pileup blocking Highway 101 westbound", "sev": "CRITICAL", "eff": ["Massive gridlock", "Injuries"], "res": ["officers", "vehicles", "medical"], "pri": 5, "tags": ["accident", "highway", "pileup"]},
    {"id": "POL_032", "cat": "TRAFFIC_ACCIDENT", "desc": "Pedestrian struck in marked crosswalk on 5th Avenue", "sev": "HIGH", "eff": ["Severe trauma", "Lane closure"], "res": ["officers", "medical"], "pri": 4, "tags": ["pedestrian", "trauma", "traffic"]},
    {"id": "POL_033", "cat": "TRAFFIC_ACCIDENT", "desc": "Overturned cargo delivery van spilling fuel on expressway", "sev": "HIGH", "eff": ["Fire hazard", "Evacuation"], "res": ["officers", "fire", "hazmat"], "pri": 4, "tags": ["spill", "expressway", "hazmat"]},
    {"id": "POL_034", "cat": "TRAFFIC_ACCIDENT", "desc": "Fender bender causing minor rubbernecking slowdown", "sev": "LOW", "eff": ["Minor delay"], "res": ["officers"], "pri": 1, "tags": ["minor", "traffic"]},
    {"id": "POL_035", "cat": "TRAFFIC_ACCIDENT", "desc": "Traffic signals dark at major 4-way intersection", "sev": "HIGH", "eff": ["Severe collision risk"], "res": ["officers", "traffic_control"], "pri": 4, "tags": ["signals", "intersection"]},
    {"id": "POL_036", "cat": "TRAFFIC_ACCIDENT", "desc": "Bicyclist collided with car door in commercial lane", "sev": "MEDIUM", "eff": ["Minor injury", "Lane blocked"], "res": ["officers", "medical"], "pri": 3, "tags": ["cyclist", "accident"]},
    {"id": "POL_037", "cat": "TRAFFIC_ACCIDENT", "desc": "School bus stalled with flat tire on morning commute route", "sev": "MEDIUM", "eff": ["Child safety concern", "Congestion"], "res": ["officers", "tow"], "pri": 3, "tags": ["school-bus", "commute"]},
    {"id": "POL_038", "cat": "TRAFFIC_ACCIDENT", "desc": "Hit and run vehicle collision with license plate logged", "sev": "HIGH", "eff": ["Fleeing driver", "Victim shock"], "res": ["officers", "vehicles"], "pri": 4, "tags": ["hit-and-run", "investigation"]},
    {"id": "POL_039", "cat": "TRAFFIC_ACCIDENT", "desc": "Construction crane debris fallen onto avenue roadway", "sev": "HIGH", "eff": ["Structural obstruction"], "res": ["officers", "public_works"], "pri": 4, "tags": ["debris", "construction"]},
    {"id": "POL_040", "cat": "TRAFFIC_ACCIDENT", "desc": "Emergency ambulance stuck behind double-parked delivery trucks", "sev": "CRITICAL", "eff": ["Patient transport delay"], "res": ["officers", "tow"], "pri": 5, "tags": ["ambulance", "obstruction"]},
    {"id": "POL_041", "cat": "EMERGENCY", "desc": "Structure fire with people reported trapped on upper floors", "sev": "CRITICAL", "eff": ["Life hazard", "Perimeter cordon needed"], "res": ["officers", "fire", "medical"], "pri": 5, "tags": ["fire", "perimeter", "emergency"]},
    {"id": "POL_042", "cat": "EMERGENCY", "desc": "Suspected gas leak prompting precautionary neighborhood evacuation", "sev": "CRITICAL", "eff": ["Explosion hazard", "Evacuation"], "res": ["officers", "evacuation"], "pri": 5, "tags": ["gas-leak", "evacuation"]},
    {"id": "POL_043", "cat": "EMERGENCY", "desc": "Missing 6-year-old child last seen in Central Park playground", "sev": "CRITICAL", "eff": ["High-priority search urgency"], "res": ["officers", "k9", "volunteers"], "pri": 5, "tags": ["missing", "child", "urgent"]},
    {"id": "POL_044", "cat": "EMERGENCY", "desc": "Water main rupture causing localized flooding on Main Street", "sev": "MEDIUM", "eff": ["Road closure", "Property water damage"], "res": ["officers", "traffic_control"], "pri": 3, "tags": ["flood", "water-main"]},
    {"id": "POL_045", "cat": "EMERGENCY", "desc": "Power substation blackout plunging three wards into darkness", "sev": "HIGH", "eff": ["Traffic lights out", "Looting risk"], "res": ["officers", "patrols"], "pri": 4, "tags": ["blackout", "infrastructure"]},
    {"id": "POL_046", "cat": "INVESTIGATION", "desc": "Forensic evidence backlog delaying critical homicide trial", "sev": "MEDIUM", "eff": ["Court continuance"], "res": ["investigators", "forensics"], "pri": 3, "tags": ["forensics", "backlog"]},
    {"id": "POL_047", "cat": "INVESTIGATION", "desc": "Key witness in protection program expressing safety doubts", "sev": "HIGH", "eff": ["Risk of witness flight"], "res": ["officers", "protection"], "pri": 4, "tags": ["witness", "protection"]},
    {"id": "POL_048", "cat": "INVESTIGATION", "desc": "Financial fraud scheme unraveling in executive business tower", "sev": "MEDIUM", "eff": ["Document seizure required"], "res": ["investigators"], "pri": 2, "tags": ["fraud", "white-collar"]},
    {"id": "POL_049", "cat": "INVESTIGATION", "desc": "Counterfeit currency circulating rapidly among street kiosks", "sev": "LOW", "eff": ["Merchant financial loss"], "res": ["investigators"], "pri": 2, "tags": ["counterfeit", "commerce"]},
    {"id": "POL_050", "cat": "INVESTIGATION", "desc": "Cyber extortion threat against municipal utility databases", "sev": "HIGH", "eff": ["Critical system compromise"], "res": ["cyber_unit"], "pri": 4, "tags": ["cyber", "threat"]},
    {"id": "POL_051", "cat": "SPECIAL_EVENTS", "desc": "VIP dignitary motorcade traversing metropolitan corridor", "sev": "HIGH", "eff": ["Rolling closures", "Escort needed"], "res": ["officers", "motorcycle", "vehicles"], "pri": 4, "tags": ["vip", "motorcade", "escort"]},
    {"id": "POL_052", "cat": "SPECIAL_EVENTS", "desc": "Annual city marathon route requiring 40 road intersections secured", "sev": "MEDIUM", "eff": ["High personnel deployment"], "res": ["officers", "barricades"], "pri": 3, "tags": ["marathon", "event"]},
    {"id": "POL_053", "cat": "SPECIAL_EVENTS", "desc": "City holiday fireworks show drawing 50,000 spectators to waterfront", "sev": "MEDIUM", "eff": ["Crowd and traffic control"], "res": ["officers", "boats"], "pri": 3, "tags": ["fireworks", "holiday"]},
    {"id": "POL_054", "cat": "SPECIAL_EVENTS", "desc": "Film production closing financial district for action stunts", "sev": "LOW", "eff": ["Permitted closure"], "res": ["traffic_officers"], "pri": 1, "tags": ["filming", "permitted"]},
    {"id": "POL_055", "cat": "COMMUNITY", "desc": "Neighborhood watch group requesting officer presence at town hall", "sev": "LOW", "eff": ["Public relations"], "res": ["community_officers"], "pri": 1, "tags": ["community", "outreach"]},
    {"id": "POL_056", "cat": "COMMUNITY", "desc": "Dispute over unpermitted street food carts near university campus", "sev": "LOW", "eff": ["Sanitation complaint"], "res": ["officers"], "pri": 1, "tags": ["vendors", "ordinance"]},
    {"id": "POL_057", "cat": "COMMUNITY", "desc": "Elderly citizen reported disoriented and wandering near railway", "sev": "HIGH", "eff": ["Imminent safety hazard"], "res": ["officers"], "pri": 4, "tags": ["welfare", "vulnerable"]},
    {"id": "POL_058", "cat": "COMMUNITY", "desc": "Feral dog pack reported menacing children near elementary school", "sev": "MEDIUM", "eff": ["Bite hazard"], "res": ["animal_control", "officers"], "pri": 3, "tags": ["animals", "school"]},
    {"id": "POL_059", "cat": "CRIME", "desc": "Carjacking reported at gunpoint in shopping mall underground garage", "sev": "CRITICAL", "eff": ["Armed suspect on loose"], "res": ["officers", "vehicles"], "pri": 5, "tags": ["carjacking", "armed", "garage"]},
    {"id": "POL_060", "cat": "CRIME", "desc": "Identity theft ring using skimming devices at gas station pumps", "sev": "MEDIUM", "eff": ["Citizen financial data stolen"], "res": ["investigators"], "pri": 3, "tags": ["skimming", "theft"]},
    {"id": "POL_061", "cat": "CRIME", "desc": "Suspicious unattended briefcase sitting inside courthouse lobby", "sev": "CRITICAL", "eff": ["Bomb squad protocol", "Building evacuate"], "res": ["bomb_squad", "officers"], "pri": 5, "tags": ["bomb-threat", "evacuation", "court"]},
    {"id": "POL_062", "cat": "PUBLIC_ORDER", "desc": "Riotous celebration turning violent after championship victory", "sev": "CRITICAL", "eff": ["Arson", "Store looting"], "res": ["officers", "tactical", "vehicles"], "pri": 5, "tags": ["riot", "looting", "celebration"]},
    {"id": "POL_063", "cat": "RESOURCES", "desc": "Emergency fuel truck delayed by state highway blizzard conditions", "sev": "MEDIUM", "eff": ["Fuel reserves dropping"], "res": ["fuel", "fleet"], "pri": 3, "tags": ["fuel", "weather"]},
    {"id": "POL_064", "cat": "TRAFFIC_ACCIDENT", "desc": "Chemical transport tanker leaking non-toxic coolant onto roadway", "sev": "MEDIUM", "eff": ["Slippery surface", "Hazmat scan"], "res": ["officers", "hazmat"], "pri": 3, "tags": ["leak", "hazmat"]},
    {"id": "POL_065", "cat": "EMERGENCY", "desc": "Earthquake tremors causing structural cracks in precinct headquarters", "sev": "HIGH", "eff": ["Building safety assessment"], "res": ["engineers", "officers"], "pri": 4, "tags": ["earthquake", "building"]},
    {"id": "POL_066", "cat": "INVESTIGATION", "desc": "Anonymous tip alleging organized crime rendezvous at marina dock", "sev": "HIGH", "eff": ["Surveillance opportunity"], "res": ["investigators", "surveillance"], "pri": 4, "tags": ["tip", "surveillance"]},
    {"id": "POL_067", "cat": "SPECIAL_EVENTS", "desc": "High school graduation procession crossing university bridge", "sev": "LOW", "eff": ["Brief pedestrian bottleneck"], "res": ["officers"], "pri": 1, "tags": ["graduation", "pedestrians"]},
    {"id": "POL_068", "cat": "COMMUNITY", "desc": "Graffiti vandal caught red-handed by local merchant association", "sev": "LOW", "eff": ["Suspect detained by public"], "res": ["officers"], "pri": 2, "tags": ["vandalism", "citizen-arrest"]},
    {"id": "POL_069", "cat": "CRIME", "desc": "Pickpocketing ring targeting tourists at botanical garden", "sev": "LOW", "eff": ["Tourist wallet loss"], "res": ["plainclothes"], "pri": 2, "tags": ["pickpocket", "tourist"]},
    {"id": "POL_070", "cat": "CRIME", "desc": "Extortion phone calls targeting independent bakery owners", "sev": "MEDIUM", "eff": ["Merchant intimidation"], "res": ["investigators"], "pri": 3, "tags": ["extortion", "small-biz"]}
]

# ---------------------------------------------------------------------------
# 2. GOVERNMENT CONDITIONS (70 conditions)
# ---------------------------------------------------------------------------
GOVERNMENT_CONDITIONS: List[Dict[str, Any]] = [
    {"id": "GOV_001", "cat": "BUDGET", "desc": "Annual municipal budget deficit projected at 12%", "sev": "CRITICAL", "eff": ["Austerity cuts needed", "Credit downgrade"], "res": ["budget", "finance"], "pri": 5, "tags": ["deficit", "fiscal"]},
    {"id": "GOV_002", "cat": "BUDGET", "desc": "Unexpected windfall from federal infrastructure stimulus grant", "sev": "LOW", "eff": ["Capital project surplus"], "res": ["budget", "grants"], "pri": 2, "tags": ["stimulus", "grant"]},
    {"id": "GOV_003", "cat": "BUDGET", "desc": "Emergency contingency reserves depleted to 15% threshold", "sev": "HIGH", "eff": ["Limited disaster buffer"], "res": ["reserves"], "pri": 4, "tags": ["reserves", "fiscal"]},
    {"id": "GOV_004", "cat": "BUDGET", "desc": "Property tax collection revenues lagging 8% below target", "sev": "MEDIUM", "eff": ["Cash flow squeeze"], "res": ["revenue"], "pri": 3, "tags": ["taxes", "revenue"]},
    {"id": "GOV_005", "cat": "BUDGET", "desc": "Public employee pension fund liability recalculation deficit", "sev": "HIGH", "eff": ["Long-term debt obligation"], "res": ["pension"], "pri": 4, "tags": ["pension", "debt"]},
    {"id": "GOV_006", "cat": "INFRASTRUCTURE", "desc": "Central suspension bridge showing micro-fractures in primary cable", "sev": "CRITICAL", "eff": ["Closure or load limits", "Commuter chaos"], "res": ["engineers", "budget"], "pri": 5, "tags": ["bridge", "safety", "transport"]},
    {"id": "GOV_007", "cat": "INFRASTRUCTURE", "desc": "Sewage treatment plant operating at 98% design capacity", "sev": "HIGH", "eff": ["Overflow risk", "Environmental breach"], "res": ["public_works", "budget"], "pri": 4, "tags": ["sewage", "environment"]},
    {"id": "GOV_008", "cat": "INFRASTRUCTURE", "desc": "Aging water mains causing frequent boil-water advisories", "sev": "HIGH", "eff": ["Public health concern", "Citizen outrage"], "res": ["water_dept"], "pri": 4, "tags": ["water", "utilities"]},
    {"id": "GOV_009", "cat": "INFRASTRUCTURE", "desc": "High-speed broadband fiber rollout stalled in low-income districts", "sev": "MEDIUM", "eff": ["Digital divide widened"], "res": ["telecom_budget"], "pri": 3, "tags": ["digital", "equity"]},
    {"id": "GOV_010", "cat": "INFRASTRUCTURE", "desc": "Pothole complaints up 400% following harsh winter thaw", "sev": "LOW", "eff": ["Vehicle damage claims"], "res": ["road_crews"], "pri": 2, "tags": ["roads", "maintenance"]},
    {"id": "GOV_011", "cat": "POLICY", "desc": "Controversial zoning reform proposal for high-density apartments", "sev": "HIGH", "eff": ["Public hearing uproar", "NIMBY opposition"], "res": ["planning_board"], "pri": 4, "tags": ["zoning", "housing"]},
    {"id": "GOV_012", "cat": "POLICY", "desc": "Proposed congestion tax on private vehicles entering business core", "sev": "HIGH", "eff": ["Merchant resistance", "Commuter protests"], "res": ["transport_council"], "pri": 4, "tags": ["congestion-tax", "transit"]},
    {"id": "GOV_013", "cat": "POLICY", "desc": "New emissions compliance mandate for local factory operations", "sev": "MEDIUM", "eff": ["Corporate pushback", "Clean air gain"], "res": ["environmental_board"], "pri": 3, "tags": ["emissions", "regulation"]},
    {"id": "GOV_014", "cat": "POLICY", "desc": "Minimum wage ordinance debated in City Council chamber", "sev": "HIGH", "eff": ["Labor vs business lobbying"], "res": ["council"], "pri": 4, "tags": ["labor", "wage", "economy"]},
    {"id": "GOV_015", "cat": "POLICY", "desc": "Universal pre-K education program awaiting funding approval", "sev": "MEDIUM", "eff": ["Family welfare boost"], "res": ["education_fund"], "pri": 3, "tags": ["education", "children"]},
    {"id": "GOV_016", "cat": "PUBLIC_HEALTH", "desc": "Seasonal respiratory illness surge overwhelming city clinic capacity", "sev": "HIGH", "eff": ["ICU bed shortage"], "res": ["health_dept", "clinics"], "pri": 4, "tags": ["health", "epidemic"]},
    {"id": "GOV_017", "cat": "PUBLIC_HEALTH", "desc": "Lead paint contamination discovered in older public housing units", "sev": "CRITICAL", "eff": ["Remediation lawsuit", "Child hazard"], "res": ["housing_authority"], "pri": 5, "tags": ["lead", "housing", "health"]},
    {"id": "GOV_018", "cat": "PUBLIC_HEALTH", "desc": "Mosquito-borne virus detected in stagnant stormwater basins", "sev": "MEDIUM", "eff": ["Vector spraying needed"], "res": ["pest_control"], "pri": 3, "tags": ["vector", "health"]},
    {"id": "GOV_019", "cat": "PUBLIC_HEALTH", "desc": "Food hygiene violations discovered in 22 school cafeteria kitchens", "sev": "MEDIUM", "eff": ["Parental outcry", "Sanitation audits"], "res": ["inspectors"], "pri": 3, "tags": ["schools", "food-safety"]},
    {"id": "GOV_020", "cat": "PUBLIC_HEALTH", "desc": "Heatwave advisory: cooling centers needed for vulnerable seniors", "sev": "HIGH", "eff": ["Heat stroke risk"], "res": ["social_services"], "pri": 4, "tags": ["heatwave", "seniors"]},
    {"id": "GOV_021", "cat": "CIVIL_SERVICE", "desc": "Transit bus drivers union voting on potential strike action", "sev": "CRITICAL", "eff": ["Complete metro transit shutdown"], "res": ["labor_negotiators"], "pri": 5, "tags": ["transit", "strike", "labor"]},
    {"id": "GOV_022", "cat": "CIVIL_SERVICE", "desc": "Sanitation workers contract expired with overtime disputes", "sev": "HIGH", "eff": ["Trash accumulation on curbs"], "res": ["sanitation_mgmt"], "pri": 4, "tags": ["sanitation", "labor"]},
    {"id": "GOV_023", "cat": "CIVIL_SERVICE", "desc": "Fire department recruitment drive yielding record-low applicants", "sev": "MEDIUM", "eff": ["Future staffing deficits"], "res": ["fire_commission"], "pri": 3, "tags": ["recruitment", "fire"]},
    {"id": "GOV_024", "cat": "CIVIL_SERVICE", "desc": "Ethics commission investigating conflict of interest in zoning chief", "sev": "HIGH", "eff": ["Public trust erosion"], "res": ["ethics_board"], "pri": 4, "tags": ["ethics", "corruption"]},
    {"id": "GOV_025", "cat": "CIVIL_SERVICE", "desc": "City IT department upgrading main administrative enterprise portal", "sev": "LOW", "eff": ["Weekend portal maintenance"], "res": ["it_staff"], "pri": 1, "tags": ["it", "upgrade"]},
    {"id": "GOV_026", "cat": "HOUSING", "desc": "Homeless shelter bed occupancy exceeding 110% amid freezing spell", "sev": "CRITICAL", "eff": ["Hypothermia fatalities risk"], "res": ["shelters", "emergency_fund"], "pri": 5, "tags": ["homelessness", "winter"]},
    {"id": "GOV_027", "cat": "HOUSING", "desc": "Average apartment rent up 18% in 12 months, displacing residents", "sev": "HIGH", "eff": ["Out-migration of workforce"], "res": ["housing_policy"], "pri": 4, "tags": ["rent", "affordability"]},
    {"id": "GOV_028", "cat": "HOUSING", "desc": "Derelict industrial parcel proposed for affordable housing land trust", "sev": "MEDIUM", "eff": ["Brownfield cleanup needed"], "res": ["urban_renewal"], "pri": 3, "tags": ["brownfield", "housing"]},
    {"id": "GOV_029", "cat": "HOUSING", "desc": "Tenant association demanding strict enforcement of heating bylaws", "sev": "MEDIUM", "eff": ["Landlord compliance fines"], "res": ["code_enforcement"], "pri": 3, "tags": ["heating", "tenants"]},
    {"id": "GOV_030", "cat": "HOUSING", "desc": "Subsidized homeownership lottery flooded with 40,000 applications", "sev": "LOW", "eff": ["High civic demand"], "res": ["housing_office"], "pri": 2, "tags": ["lottery", "housing"]},
    {"id": "GOV_031", "cat": "ENVIRONMENT", "desc": "Smog air quality index reaches hazardous code purple", "sev": "HIGH", "eff": ["Outdoor sports canceled"], "res": ["air_control"], "pri": 4, "tags": ["smog", "air-quality"]},
    {"id": "GOV_032", "cat": "ENVIRONMENT", "desc": "Illegal industrial toxic waste dumping in scenic city riverbank", "sev": "CRITICAL", "eff": ["Ecological devastation", "Fine enforcement"], "res": ["epa_team", "police"], "pri": 5, "tags": ["toxic", "river", "crime"]},
    {"id": "GOV_033", "cat": "ENVIRONMENT", "desc": "Tree canopy reduction due to invasive beetle infestation", "sev": "LOW", "eff": ["Urban heat island increase"], "res": ["forestry"], "pri": 2, "tags": ["trees", "environment"]},
    {"id": "GOV_034", "cat": "ENVIRONMENT", "desc": "Citywide recycling facility contract renewal negotiations stalled", "sev": "MEDIUM", "eff": ["Recyclables diverted to landfill"], "res": ["waste_authority"], "pri": 3, "tags": ["recycling", "contract"]},
    {"id": "GOV_035", "cat": "ENVIRONMENT", "desc": "Solar panel subsidy program exhaustively oversubscribed", "sev": "LOW", "eff": ["Green transition momentum"], "res": ["energy_fund"], "pri": 2, "tags": ["solar", "clean-energy"]},
    {"id": "GOV_036", "cat": "EDUCATION", "desc": "Teacher shortage forcing combined multi-grade classrooms", "sev": "HIGH", "eff": ["Lower learning metrics"], "res": ["school_board"], "pri": 4, "tags": ["teachers", "education"]},
    {"id": "GOV_037", "cat": "EDUCATION", "desc": "Vocational technical institute requests expansion funding", "sev": "MEDIUM", "eff": ["Workforce pipeline upgrade"], "res": ["education_budget"], "pri": 3, "tags": ["vocational", "jobs"]},
    {"id": "GOV_038", "cat": "EDUCATION", "desc": "School district bus routing software malfunction causing chaos", "sev": "MEDIUM", "eff": ["Parents stranded at stops"], "res": ["transport"], "pri": 3, "tags": ["buses", "schools"]},
    {"id": "GOV_039", "cat": "EDUCATION", "desc": "Literacy intervention initiative reports 14% improvement in reading", "sev": "LOW", "eff": ["Program expansion proposed"], "res": ["curriculum_dept"], "pri": 1, "tags": ["literacy", "achievement"]},
    {"id": "GOV_040", "cat": "EDUCATION", "desc": "Aging school HVAC system failures during heatwave", "sev": "HIGH", "eff": ["Early school dismissals"], "res": ["facilities_fund"], "pri": 4, "tags": ["school", "hvac"]},
    {"id": "GOV_041", "cat": "ECONOMIC_DEVELOPMENT", "desc": "Major tech enterprise considering headquarters relocation to city", "sev": "HIGH", "eff": ["15,000 jobs", "Tax incentive request"], "res": ["economic_council"], "pri": 4, "tags": ["investment", "jobs"]},
    {"id": "GOV_042", "cat": "ECONOMIC_DEVELOPMENT", "desc": "Local retail district struggling against e-commerce competition", "sev": "MEDIUM", "eff": ["Commercial vacancy rise"], "res": ["small_biz_dept"], "pri": 3, "tags": ["commerce", "retail"]},
    {"id": "GOV_043", "cat": "ECONOMIC_DEVELOPMENT", "desc": "Tourism revenue sets quarterly record due to international expo", "sev": "LOW", "eff": ["Hotel tax surplus"], "res": ["tourism_board"], "pri": 2, "tags": ["tourism", "revenue"]},
    {"id": "GOV_044", "cat": "ECONOMIC_DEVELOPMENT", "desc": "Port authority cargo container volume down 9% from global delays", "sev": "MEDIUM", "eff": ["Dockworker hour reductions"], "res": ["port_commission"], "pri": 3, "tags": ["shipping", "port"]},
    {"id": "GOV_045", "cat": "ECONOMIC_DEVELOPMENT", "desc": "Downtown business improvement district requests security grants", "sev": "MEDIUM", "eff": ["Merchant association matching"], "res": ["commerce_fund"], "pri": 3, "tags": ["security", "downtown"]},
    {"id": "GOV_046", "cat": "PUBLIC_SAFETY", "desc": "Fire department requests ladder truck fleet modernizations", "sev": "HIGH", "eff": ["High capital expenditure"], "res": ["capital_budget"], "pri": 4, "tags": ["fire", "equipment"]},
    {"id": "GOV_047", "cat": "PUBLIC_SAFETY", "desc": "Municipal flood wall certification renewal requires reinforcement", "sev": "HIGH", "eff": ["Federal flood insurance risk"], "res": ["corps_engineers"], "pri": 4, "tags": ["flood", "infrastructure"]},
    {"id": "GOV_048", "cat": "PUBLIC_SAFETY", "desc": "Emergency 911 dispatch center operator staffing below minimum", "sev": "CRITICAL", "eff": ["Call hold times up to 4 minutes"], "res": ["dispatch_budget"], "pri": 5, "tags": ["911", "dispatch"]},
    {"id": "GOV_049", "cat": "PUBLIC_SAFETY", "desc": "Earthquake readiness drill scheduled across all municipal offices", "sev": "LOW", "eff": ["One-hour civil simulation"], "res": ["emergency_mgmt"], "pri": 1, "tags": ["drill", "readiness"]},
    {"id": "GOV_050", "cat": "PUBLIC_SAFETY", "desc": "Public park lighting upgrade project reduces night crime by 30%", "sev": "LOW", "eff": ["Positive safety metric"], "res": ["parks_budget"], "pri": 1, "tags": ["lighting", "parks"]},
    {"id": "GOV_051", "cat": "LEGAL", "desc": "Class action lawsuit filed over contaminated municipal tap water", "sev": "CRITICAL", "eff": ["Multi-million liability risk"], "res": ["city_attorney"], "pri": 5, "tags": ["lawsuit", "liability"]},
    {"id": "GOV_052", "cat": "LEGAL", "desc": "Supreme Court ruling invalidates municipal short-term rental ban", "sev": "HIGH", "eff": ["Regulatory overhaul needed"], "res": ["legal_counsel"], "pri": 4, "tags": ["ruling", "rentals"]},
    {"id": "GOV_053", "cat": "LEGAL", "desc": "Contract dispute with primary asphalt road paving contractor", "sev": "MEDIUM", "eff": ["Roadwork halt for 60 days"], "res": ["contracts_dept"], "pri": 3, "tags": ["contract", "dispute"]},
    {"id": "GOV_054", "cat": "LEGAL", "desc": "Public records request backlog triggers transparency court order", "sev": "LOW", "eff": ["Administrative overtime"], "res": ["clerk_office"], "pri": 2, "tags": ["records", "compliance"]},
    {"id": "GOV_055", "cat": "LEGAL", "desc": "Eminent domain dispute over light rail extension transit path", "sev": "HIGH", "eff": ["Project timeline delayed 1 yr"], "res": ["transit_legal"], "pri": 4, "tags": ["transit", "land"]},
    {"id": "GOV_056", "cat": "COMMUNITY_RELATIONS", "desc": "City council public comment period overwhelmed by angry citizens", "sev": "HIGH", "eff": ["Meeting adjourned in chaos"], "res": ["council"], "pri": 4, "tags": ["civic", "protest"]},
    {"id": "GOV_057", "cat": "COMMUNITY_RELATIONS", "desc": "Community garden land lease up for renewal vs commercial sale", "sev": "LOW", "eff": ["Neighborhood petition campaign"], "res": ["parks_board"], "pri": 2, "tags": ["garden", "land"]},
    {"id": "GOV_058", "cat": "COMMUNITY_RELATIONS", "desc": "Participatory budgeting program allows citizens to vote on projects", "sev": "LOW", "eff": ["High citizen engagement"], "res": ["civic_fund"], "pri": 1, "tags": ["democracy", "budget"]},
    {"id": "GOV_059", "cat": "COMMUNITY_RELATIONS", "desc": "Youth summer jobs program funding expanded to 2,500 teens", "sev": "LOW", "eff": ["Youth employment boost"], "res": ["youth_services"], "pri": 1, "tags": ["youth", "jobs"]},
    {"id": "GOV_060", "cat": "COMMUNITY_RELATIONS", "desc": "Multilingual municipal communication channels launched on web", "sev": "LOW", "eff": ["Immigrant inclusion"], "res": ["communications"], "pri": 1, "tags": ["multilingual", "equity"]},
    {"id": "GOV_061", "cat": "EMERGENCY_MANAGEMENT", "desc": "Hurricane warning issued: mandatory coastal ward evacuations", "sev": "CRITICAL", "eff": ["Mass evacuation logistics"], "res": ["all_departments"], "pri": 5, "tags": ["hurricane", "evacuation"]},
    {"id": "GOV_062", "cat": "EMERGENCY_MANAGEMENT", "desc": "Severe winter blizzard forecasts 24 inches of snow accumulation", "sev": "HIGH", "eff": ["Plow mobilization", "Parking bans"], "res": ["snow_plows"], "pri": 4, "tags": ["blizzard", "weather"]},
    {"id": "GOV_063", "cat": "EMERGENCY_MANAGEMENT", "desc": "Wildfire smoke plume grounding regional commercial flights", "sev": "HIGH", "eff": ["Emergency shelter N95 mask push"], "res": ["health_dept"], "pri": 4, "tags": ["wildfire", "smoke"]},
    {"id": "GOV_064", "cat": "EMERGENCY_MANAGEMENT", "desc": "Major cyber ransom attack locks municipal property deed records", "sev": "CRITICAL", "eff": ["Real estate transactions halted"], "res": ["cyber_defense"], "pri": 5, "tags": ["cyber", "ransomware"]},
    {"id": "GOV_065", "cat": "EMERGENCY_MANAGEMENT", "desc": "Chemical train derailment 10 miles upwind of metropolitan area", "sev": "CRITICAL", "eff": ["Shelter-in-place alerts"], "res": ["hazmat", "police"], "pri": 5, "tags": ["train", "chemical"]},
    {"id": "GOV_066", "cat": "INFRASTRUCTURE", "desc": "Subway electrical third rail short causes morning system halt", "sev": "HIGH", "eff": ["300,000 commuters delayed"], "res": ["metro_transit"], "pri": 4, "tags": ["subway", "transit"]},
    {"id": "GOV_067", "cat": "INFRASTRUCTURE", "desc": "Municipal airport runways resurfacing grant awarded from state", "sev": "LOW", "eff": ["Long-term airport efficiency"], "res": ["aviation_fund"], "pri": 2, "tags": ["airport", "infrastructure"]},
    {"id": "GOV_068", "cat": "BUDGET", "desc": "Bond rating agency upgrades city credit from A- to AA+", "sev": "LOW", "eff": ["Lower borrowing interest rates"], "res": ["treasury"], "pri": 2, "tags": ["bonds", "credit"]},
    {"id": "GOV_069", "cat": "POLICY", "desc": "Autonomous vehicle commercial testing permit application submitted", "sev": "MEDIUM", "eff": ["Safety regulation guidelines needed"], "res": ["transport_commission"], "pri": 3, "tags": ["autonomous", "testing"]},
    {"id": "GOV_070", "cat": "PUBLIC_HEALTH", "desc": "Citywide mental health crisis response teams dispatch 500 calls", "sev": "MEDIUM", "eff": ["Diversion from jail to care"], "res": ["health_dept"], "pri": 3, "tags": ["mental-health", "crisis"]}
]

# ---------------------------------------------------------------------------
# 3. CITIZEN CONDITIONS (70 conditions)
# ---------------------------------------------------------------------------
CITIZEN_CONDITIONS: List[Dict[str, Any]] = [
    {"id": "CIT_001", "cat": "FINANCIAL", "desc": "Monthly apartment rent payment due in 48 hours", "sev": "HIGH", "eff": ["Eviction risk if unpaid"], "res": ["money"], "pri": 4, "tags": ["rent", "housing", "bills"]},
    {"id": "CIT_002", "cat": "FINANCIAL", "desc": "Unexpected medical bill from emergency room visit received", "sev": "HIGH", "eff": ["Savings depleted", "Debt burden"], "res": ["money", "savings"], "pri": 4, "tags": ["medical", "debt"]},
    {"id": "CIT_003", "cat": "FINANCIAL", "desc": "Received quarterly performance bonus from employer", "sev": "LOW", "eff": ["Discretionary cash boost"], "res": ["money"], "pri": 1, "tags": ["bonus", "income"]},
    {"id": "CIT_004", "cat": "FINANCIAL", "desc": "Bank checking account balance drops below minimum fee threshold", "sev": "MEDIUM", "eff": ["Overdraft charges"], "res": ["money"], "pri": 3, "tags": ["bank", "fees"]},
    {"id": "CIT_005", "cat": "FINANCIAL", "desc": "Credit card interest rate spike increases monthly minimums", "sev": "MEDIUM", "eff": ["Disposable income cut"], "res": ["money"], "pri": 3, "tags": ["credit", "finance"]},
    {"id": "CIT_006", "cat": "EMPLOYMENT", "desc": "Employer announces corporate restructuring and layoffs", "sev": "CRITICAL", "eff": ["Imminent loss of primary income"], "res": ["job", "money"], "pri": 5, "tags": ["layoffs", "unemployment"]},
    {"id": "CIT_007", "cat": "EMPLOYMENT", "desc": "Offered overtime shifts with 1.5x hourly compensation", "sev": "LOW", "eff": ["Higher pay, fatigue risk"], "res": ["energy", "money"], "pri": 2, "tags": ["overtime", "work"]},
    {"id": "CIT_008", "cat": "EMPLOYMENT", "desc": "Interview invitation received for senior career advancement role", "sev": "LOW", "eff": ["Preparation needed"], "res": ["education", "time"], "pri": 2, "tags": ["interview", "career"]},
    {"id": "CIT_009", "cat": "EMPLOYMENT", "desc": "Workplace conflict with supervisor creating hostile environment", "sev": "MEDIUM", "eff": ["Stress, resignation contemplation"], "res": ["mental_health"], "pri": 3, "tags": ["workplace", "stress"]},
    {"id": "CIT_010", "cat": "EMPLOYMENT", "desc": "Freelance contract gig completed with payment pending clearance", "sev": "LOW", "eff": ["Cash inflow delayed"], "res": ["money"], "pri": 2, "tags": ["freelance", "gig"]},
    {"id": "CIT_011", "cat": "HEALTH", "desc": "Severe dental abscess causing excruciating pain and fever", "sev": "HIGH", "eff": ["Immediate dentist visit needed"], "res": ["health", "money"], "pri": 4, "tags": ["dental", "pain"]},
    {"id": "CIT_012", "cat": "HEALTH", "desc": "Chronic insomnia and fatigue reducing workplace alertness", "sev": "MEDIUM", "eff": ["Low energy, cognitive haze"], "res": ["energy", "health"], "pri": 3, "tags": ["insomnia", "energy"]},
    {"id": "CIT_013", "cat": "HEALTH", "desc": "Prescription medication refill denied by insurance provider", "sev": "HIGH", "eff": ["Treatment disruption"], "res": ["health", "insurance"], "pri": 4, "tags": ["meds", "insurance"]},
    {"id": "CIT_014", "cat": "HEALTH", "desc": "Sprained ankle from slipping on icy sidewalk steps", "sev": "MEDIUM", "eff": ["Reduced walking mobility"], "res": ["health", "mobility"], "pri": 3, "tags": ["injury", "mobility"]},
    {"id": "CIT_015", "cat": "HEALTH", "desc": "Completed annual wellness checkup with clear blood work results", "sev": "LOW", "eff": ["Peace of mind"], "res": ["health"], "pri": 1, "tags": ["wellness", "positive"]},
    {"id": "CIT_016", "cat": "LIVING_CONDITIONS", "desc": "Apartment heating radiator broken during freezing cold snap", "sev": "HIGH", "eff": ["Hypothermia danger inside home"], "res": ["health", "shelter"], "pri": 4, "tags": ["heat", "housing"]},
    {"id": "CIT_017", "cat": "LIVING_CONDITIONS", "desc": "Persistent ceiling water leak dripping onto bedroom furniture", "sev": "MEDIUM", "eff": ["Property damage, mold risk"], "res": ["housing"], "pri": 3, "tags": ["leak", "damage"]},
    {"id": "CIT_018", "cat": "LIVING_CONDITIONS", "desc": "Noisy upstairs neighbors partying late into weeknights", "sev": "LOW", "eff": ["Sleep deprivation"], "res": ["energy"], "pri": 2, "tags": ["noise", "sleep"]},
    {"id": "CIT_019", "cat": "LIVING_CONDITIONS", "desc": "Home kitchen pantry empty with only expired dry goods remaining", "sev": "HIGH", "eff": ["Hunger, urgent grocery shopping needed"], "res": ["food", "money"], "pri": 4, "tags": ["groceries", "food"]},
    {"id": "CIT_020", "cat": "LIVING_CONDITIONS", "desc": "Apartment electrical fuse blown after appliance power surge", "sev": "LOW", "eff": ["No lights or refrigerator power"], "res": ["utilities"], "pri": 2, "tags": ["power", "appliances"]},
    {"id": "CIT_021", "cat": "SOCIAL", "desc": "Close friend hosting wedding celebration in another district", "sev": "LOW", "eff": ["Travel cost, social joy"], "res": ["money", "social"], "pri": 2, "tags": ["wedding", "friendship"]},
    {"id": "CIT_022", "cat": "SOCIAL", "desc": "Prolonged social isolation leading to feelings of loneliness", "sev": "MEDIUM", "eff": ["Depression risk, motivation drop"], "res": ["social", "mental_health"], "pri": 3, "tags": ["isolation", "social"]},
    {"id": "CIT_023", "cat": "SOCIAL", "desc": "Family member asking to borrow significant money for bail", "sev": "HIGH", "eff": ["Financial risk, family conflict"], "res": ["money", "social"], "pri": 4, "tags": ["family", "loan"]},
    {"id": "CIT_024", "cat": "SOCIAL", "desc": "Invited to join neighborhood cooperative gardening association", "sev": "LOW", "eff": ["Community bonding"], "res": ["social", "time"], "pri": 1, "tags": ["community", "garden"]},
    {"id": "CIT_025", "cat": "SOCIAL", "desc": "Bitter dispute with neighbor over assigned parking spot boundaries", "sev": "LOW", "eff": ["Interpersonal tension"], "res": ["social"], "pri": 2, "tags": ["dispute", "parking"]},
    {"id": "CIT_026", "cat": "TRANSPORT", "desc": "Personal bicycle stolen from locked street bike rack", "sev": "MEDIUM", "eff": ["Loss of primary commute transport"], "res": ["transport", "money"], "pri": 3, "tags": ["theft", "bike"]},
    {"id": "CIT_027", "cat": "TRANSPORT", "desc": "Subway transit pass expired with fare gate access denied", "sev": "LOW", "eff": ["Must recharge card"], "res": ["money"], "pri": 2, "tags": ["subway", "transit"]},
    {"id": "CIT_028", "cat": "TRANSPORT", "desc": "Commuter train delayed by 45 minutes due to signal failure", "sev": "LOW", "eff": ["Late for work appointment"], "res": ["time"], "pri": 2, "tags": ["delay", "train"]},
    {"id": "CIT_029", "cat": "TRANSPORT", "desc": "Rideshare surge pricing rates tripled during downpour", "sev": "LOW", "eff": ["Exorbitant transit cost"], "res": ["money"], "pri": 2, "tags": ["rideshare", "weather"]},
    {"id": "CIT_030", "cat": "TRANSPORT", "desc": "Walking shoes worn through sole, causing blisters on commute", "sev": "LOW", "eff": ["Discomfort"], "res": ["money"], "pri": 1, "tags": ["shoes", "walking"]},
    {"id": "CIT_031", "cat": "EDUCATION_SKILLS", "desc": "University night class midterm exam scheduled tomorrow evening", "sev": "MEDIUM", "eff": ["Study time required"], "res": ["energy", "time"], "pri": 3, "tags": ["study", "exam"]},
    {"id": "CIT_032", "cat": "EDUCATION_SKILLS", "desc": "Completed technical coding certification credential", "sev": "LOW", "eff": ["Qualification for higher jobs"], "res": ["education"], "pri": 1, "tags": ["certificate", "career"]},
    {"id": "CIT_033", "cat": "EDUCATION_SKILLS", "desc": "Tuition fee installment due for professional diploma course", "sev": "HIGH", "eff": ["Course drop risk if unpaid"], "res": ["money"], "pri": 4, "tags": ["tuition", "education"]},
    {"id": "CIT_034", "cat": "EDUCATION_SKILLS", "desc": "Library book loans overdue with minor cumulative fines", "sev": "LOW", "eff": ["Return books needed"], "res": ["money"], "pri": 1, "tags": ["library", "fines"]},
    {"id": "CIT_035", "cat": "EDUCATION_SKILLS", "desc": "Language conversation meetup offering free practice sessions", "sev": "LOW", "eff": ["Language proficiency boost"], "res": ["social", "time"], "pri": 1, "tags": ["language", "learning"]},
    {"id": "CIT_036", "cat": "SAFETY", "desc": "Mugging attempt narrowly avoided on dark pedestrian walkway", "sev": "HIGH", "eff": ["Acute fear, trauma, route change"], "res": ["safety", "mental_health"], "pri": 4, "tags": ["crime", "fear"]},
    {"id": "CIT_037", "cat": "SAFETY", "desc": "Suspicious person lingering near apartment building entrance door", "sev": "MEDIUM", "eff": ["Security concern"], "res": ["safety"], "pri": 3, "tags": ["suspicious", "building"]},
    {"id": "CIT_038", "cat": "SAFETY", "desc": "Smoke detector alarm battery beeping loudly every 30 seconds", "sev": "LOW", "eff": ["Annoyance, battery replacement"], "res": ["appliances"], "pri": 1, "tags": ["smoke-detector", "battery"]},
    {"id": "CIT_039", "cat": "SAFETY", "desc": "Received fraudulent phishing SMS claiming bank account frozen", "sev": "LOW", "eff": ["Scam awareness required"], "res": ["security"], "pri": 2, "tags": ["scam", "phishing"]},
    {"id": "CIT_040", "cat": "SAFETY", "desc": "Stray aggressive dog barking aggressively at bus stop bench", "sev": "LOW", "eff": ["Detour required"], "res": ["safety"], "pri": 2, "tags": ["dog", "safety"]},
    {"id": "CIT_041", "cat": "FAMILY", "desc": "Child caught high fever requiring immediate pediatrician visit", "sev": "HIGH", "eff": ["Leave work early, medical cost"], "res": ["health", "money", "time"], "pri": 4, "tags": ["child", "pediatric"]},
    {"id": "CIT_042", "cat": "FAMILY", "desc": "Elderly parent needing assistance moving into assisted living", "sev": "MEDIUM", "eff": ["Emotional and time toll"], "res": ["family", "time"], "pri": 3, "tags": ["parent", "care"]},
    {"id": "CIT_043", "cat": "FAMILY", "desc": "Daycare center closed tomorrow due to staff development day", "sev": "MEDIUM", "eff": ["Emergency childcare dilemma"], "res": ["childcare", "work"], "pri": 3, "tags": ["daycare", "child"]},
    {"id": "CIT_044", "cat": "FAMILY", "desc": "Spouse received promotion with exciting relocation offer", "sev": "MEDIUM", "eff": ["Major life decision"], "res": ["social", "career"], "pri": 3, "tags": ["spouse", "relocation"]},
    {"id": "CIT_045", "cat": "FAMILY", "desc": "Family pet dog swallowed foreign object needing vet surgery", "sev": "HIGH", "eff": ["High veterinary expense"], "res": ["money"], "pri": 4, "tags": ["pet", "vet"]},
    {"id": "CIT_046", "cat": "COMMERCE", "desc": "Essential smartphone screen cracked after drop onto concrete", "sev": "MEDIUM", "eff": ["Repair cost or replacement"], "res": ["money", "technology"], "pri": 3, "tags": ["phone", "repair"]},
    {"id": "CIT_047", "cat": "COMMERCE", "desc": "Local grocery supermarket running 50% discount sale on staples", "sev": "LOW", "eff": ["Opportunity to stock up"], "res": ["money", "food"], "pri": 1, "tags": ["discount", "groceries"]},
    {"id": "CIT_048", "cat": "COMMERCE", "desc": "Online parcel package marked delivered but stolen from porch", "sev": "MEDIUM", "eff": ["Refund claim filing"], "res": ["money"], "pri": 2, "tags": ["porch-pirate", "package"]},
    {"id": "CIT_049", "cat": "COMMERCE", "desc": "Laundromat machines out of order in entire apartment block", "sev": "LOW", "eff": ["Must find external laundry"], "res": ["time"], "pri": 1, "tags": ["laundry", "chores"]},
    {"id": "CIT_050", "cat": "COMMERCE", "desc": "Winter coat zipper jammed beyond repair before cold front", "sev": "LOW", "eff": ["Warm clothes needed"], "res": ["money"], "pri": 2, "tags": ["clothing", "winter"]},
    {"id": "CIT_051", "cat": "FINANCIAL", "desc": "Identity theft alert: fraudulent online charges on debit card", "sev": "HIGH", "eff": ["Card cancelled, temporary cash lock"], "res": ["money", "bank"], "pri": 4, "tags": ["fraud", "debit"]},
    {"id": "CIT_052", "cat": "EMPLOYMENT", "desc": "Company introducing automated AI tools threatening role duties", "sev": "HIGH", "eff": ["Job security anxiety"], "res": ["job"], "pri": 4, "tags": ["automation", "career"]},
    {"id": "CIT_053", "cat": "HEALTH", "desc": "Food poisoning symptoms after eating seafood lunch special", "sev": "HIGH", "eff": ["Bedridden, hydration needed"], "res": ["health", "energy"], "pri": 4, "tags": ["food-poisoning", "illness"]},
    {"id": "CIT_054", "cat": "LIVING_CONDITIONS", "desc": "Landlord notifying non-renewal of lease at end of month", "sev": "CRITICAL", "eff": ["Forced relocation in 30 days"], "res": ["housing", "money"], "pri": 5, "tags": ["eviction", "lease"]},
    {"id": "CIT_055", "cat": "SOCIAL", "desc": "Best friend moving overseas for new employment opportunity", "sev": "LOW", "eff": ["Emotional goodbye party"], "res": ["social"], "pri": 2, "tags": ["friendship", "farewell"]},
    {"id": "CIT_056", "cat": "TRANSPORT", "desc": "Expressway bus caught in total gridlock due to bridge accident", "sev": "LOW", "eff": ["Two hours stuck in traffic"], "res": ["time"], "pri": 2, "tags": ["traffic", "bus"]},
    {"id": "CIT_057", "cat": "EDUCATION_SKILLS", "desc": "Accepted into selective coding bootcamp scholarship program", "sev": "LOW", "eff": ["Intense study schedule ahead"], "res": ["education"], "pri": 1, "tags": ["bootcamp", "skills"]},
    {"id": "CIT_058", "cat": "SAFETY", "desc": "Apartment building fire alarm evacuates residents at 3 AM", "sev": "MEDIUM", "eff": ["Exhaustion, standing in cold"], "res": ["energy"], "pri": 3, "tags": ["alarm", "evacuation"]},
    {"id": "CIT_059", "cat": "COMMERCE", "desc": "Bank card eaten by malfunctioning automated teller machine", "sev": "MEDIUM", "eff": ["Must wait for branch open"], "res": ["money"], "pri": 3, "tags": ["atm", "bank"]},
    {"id": "CIT_060", "cat": "FAMILY", "desc": "Family reunion gathering planned for upcoming holiday weekend", "sev": "LOW", "eff": ["Gift shopping, travel prep"], "res": ["money", "family"], "pri": 1, "tags": ["reunion", "holiday"]},
    {"id": "CIT_061", "cat": "FINANCIAL", "desc": "Tax refund check arrives unexpectedly higher than estimated", "sev": "LOW", "eff": ["Savings boost"], "res": ["money"], "pri": 1, "tags": ["tax-refund", "savings"]},
    {"id": "CIT_062", "cat": "HEALTH", "desc": "Seasonal allergy pollen count at extreme levels", "sev": "LOW", "eff": ["Sneezing, eye irritation"], "res": ["health"], "pri": 1, "tags": ["allergies", "pollen"]},
    {"id": "CIT_063", "cat": "LIVING_CONDITIONS", "desc": "Cockroach infestation discovered in kitchen cabinetry", "sev": "MEDIUM", "eff": ["Exterminator cost needed"], "res": ["sanitation", "money"], "pri": 3, "tags": ["pests", "housing"]},
    {"id": "CIT_064", "cat": "EMPLOYMENT", "desc": "Selected for jury duty summons next Tuesday morning", "sev": "MEDIUM", "eff": ["Absence from normal job"], "res": ["time", "civic"], "pri": 3, "tags": ["jury-duty", "civic"]},
    {"id": "CIT_065", "cat": "SOCIAL", "desc": "Organized volunteer shift at local soup kitchen shelter", "sev": "LOW", "eff": ["Sense of civic purpose"], "res": ["social", "time"], "pri": 1, "tags": ["volunteer", "shelter"]},
    {"id": "CIT_066", "cat": "TRANSPORT", "desc": "Heavy snowstorm makes walking sidewalks treacherous", "sev": "MEDIUM", "eff": ["Slip and fall hazard"], "res": ["mobility"], "pri": 3, "tags": ["snow", "walking"]},
    {"id": "CIT_067", "cat": "COMMERCE", "desc": "Grocery store loyalty points expire tomorrow unless redeemed", "sev": "LOW", "eff": ["Small savings incentive"], "res": ["money"], "pri": 1, "tags": ["loyalty", "rewards"]},
    {"id": "CIT_068", "cat": "SAFETY", "desc": "Street lights repaired on previously pitch-black evening commute route", "sev": "LOW", "eff": ["Increased safety confidence"], "res": ["safety"], "pri": 1, "tags": ["lighting", "safety"]},
    {"id": "CIT_069", "cat": "HEALTH", "desc": "Fitness tracker milestone reached: 10,000 steps daily streak", "sev": "LOW", "eff": ["Improved cardiovascular stamina"], "res": ["energy"], "pri": 1, "tags": ["fitness", "health"]},
    {"id": "CIT_070", "cat": "FINANCIAL", "desc": "Utility gas heating bill doubled due to winter rate hike", "sev": "MEDIUM", "eff": ["Tightened monthly grocery budget"], "res": ["money"], "pri": 3, "tags": ["utilities", "gas"]}
]

# ---------------------------------------------------------------------------
# 4. BUSINESS CONDITIONS (70 conditions)
# ---------------------------------------------------------------------------
BUSINESS_CONDITIONS: List[Dict[str, Any]] = [
    {"id": "BIZ_001", "cat": "FINANCE", "desc": "Operating cash flow projected to fall into negative within 14 days", "sev": "CRITICAL", "eff": ["Payroll default risk", "Emergency credit needed"], "res": ["capital", "credit"], "pri": 5, "tags": ["cash-flow", "insolvency"]},
    {"id": "BIZ_002", "cat": "FINANCE", "desc": "Commercial bank line of credit approved for $250,000 expansion", "sev": "LOW", "eff": ["Liquidity for investment"], "res": ["capital"], "pri": 2, "tags": ["credit", "expansion"]},
    {"id": "BIZ_003", "cat": "FINANCE", "desc": "Corporate invoice payment of $45,000 delayed by 60 days overdue", "sev": "HIGH", "eff": ["Accounts receivable crunch"], "res": ["cash_flow"], "pri": 4, "tags": ["receivables", "debt"]},
    {"id": "BIZ_004", "cat": "FINANCE", "desc": "Commercial property lease renewal demands 35% rent escalation", "sev": "HIGH", "eff": ["Fixed overhead spike", "Relocation dilemma"], "res": ["capital", "location"], "pri": 4, "tags": ["lease", "rent"]},
    {"id": "BIZ_005", "cat": "FINANCE", "desc": "Sales revenue surpasses quarterly fiscal projections by 22%", "sev": "LOW", "eff": ["Retained earnings surplus"], "res": ["profit"], "pri": 1, "tags": ["revenue", "profit"]},
    {"id": "BIZ_006", "cat": "SUPPLY_CHAIN", "desc": "Primary raw material supplier factory shuts down due to strike", "sev": "CRITICAL", "eff": ["Production halt in 5 days"], "res": ["inventory", "suppliers"], "pri": 5, "tags": ["supplier", "strike", "shortage"]},
    {"id": "BIZ_007", "cat": "SUPPLY_CHAIN", "desc": "Shipping container freight charges triple across ocean trade lanes", "sev": "HIGH", "eff": ["Gross profit margin erosion"], "res": ["margins"], "pri": 4, "tags": ["freight", "logistics"]},
    {"id": "BIZ_008", "cat": "SUPPLY_CHAIN", "desc": "Warehouse inventory of fast-moving products depleted to 0 units", "sev": "HIGH", "eff": ["Lost customer sales orders"], "res": ["inventory", "sales"], "pri": 4, "tags": ["stockout", "inventory"]},
    {"id": "BIZ_009", "cat": "SUPPLY_CHAIN", "desc": "Defective components batch discovered in warehouse assembly line", "sev": "HIGH", "eff": ["Product recall risk", "Wasted stock"], "res": ["quality", "inventory"], "pri": 4, "tags": ["quality", "defect"]},
    {"id": "BIZ_010", "cat": "SUPPLY_CHAIN", "desc": "New alternative local supplier offers 12% lower unit pricing", "sev": "LOW", "eff": ["Cost reduction opportunity"], "res": ["procurement"], "pri": 2, "tags": ["supplier", "savings"]},
    {"id": "BIZ_011", "cat": "LABOR", "desc": "Chief technical architect resigns to join direct market rival", "sev": "HIGH", "eff": ["Knowledge drain, project delay"], "res": ["personnel", "leadership"], "pri": 4, "tags": ["turnover", "talent"]},
    {"id": "BIZ_012", "cat": "LABOR", "desc": "Factory assembly line employees demand wage increase or slowdown", "sev": "HIGH", "eff": ["Labor tension, output drop"], "res": ["payroll", "labor"], "pri": 4, "tags": ["labor", "wages"]},
    {"id": "BIZ_013", "cat": "LABOR", "desc": "Candidate recruitment campaign attracts 150 qualified applicants", "sev": "LOW", "eff": ["Hiring pipeline expansion"], "res": ["recruiting"], "pri": 1, "tags": ["hiring", "talent"]},
    {"id": "BIZ_014", "cat": "LABOR", "desc": "Workplace injury on warehouse loading dock triggers OSHA review", "sev": "HIGH", "eff": ["Compliance fines, safety audit"], "res": ["safety", "insurance"], "pri": 4, "tags": ["injury", "safety"]},
    {"id": "BIZ_015", "cat": "LABOR", "desc": "Employee morale survey reveals high burnout and turnover risk", "sev": "MEDIUM", "eff": ["Productivity decline"], "res": ["hr", "retention"], "pri": 3, "tags": ["morale", "burnout"]},
    {"id": "BIZ_016", "cat": "MARKET_COMPETITION", "desc": "Aggressive competitor opens mega-store across the avenue", "sev": "CRITICAL", "eff": ["Foot traffic loss estimated at 30%"], "res": ["sales", "customers"], "pri": 5, "tags": ["competitor", "retail"]},
    {"id": "BIZ_017", "cat": "MARKET_COMPETITION", "desc": "Competitor engages in predatory price cutting on flagship products", "sev": "HIGH", "eff": ["Margin compression to match"], "res": ["pricing", "margins"], "pri": 4, "tags": ["price-war", "competition"]},
    {"id": "BIZ_018", "cat": "MARKET_COMPETITION", "desc": "Market rival files patent infringement lawsuit seeking injunction", "sev": "CRITICAL", "eff": ["Product sales injunction risk"], "res": ["legal", "capital"], "pri": 5, "tags": ["patent", "lawsuit"]},
    {"id": "BIZ_019", "cat": "MARKET_COMPETITION", "desc": "Competitor suffers catastrophic public data breach, losing trust", "sev": "LOW", "eff": ["Customer migration opportunity"], "res": ["sales", "marketing"], "pri": 2, "tags": ["market-share", "opportunity"]},
    {"id": "BIZ_020", "cat": "MARKET_COMPETITION", "desc": "Consumer preferences shift toward eco-friendly sustainable packaging", "sev": "MEDIUM", "eff": ["Product repackaging needed"], "res": ["packaging", "r&d"], "pri": 3, "tags": ["trends", "eco"]},
    {"id": "BIZ_021", "cat": "OPERATIONS", "desc": "Primary manufacturing plant conveyor motor burns out", "sev": "HIGH", "eff": ["Factory output halted 48 hours"], "res": ["equipment", "maintenance"], "pri": 4, "tags": ["machinery", "downtime"]},
    {"id": "BIZ_022", "cat": "OPERATIONS", "desc": "Cloud server infrastructure outage crashes corporate e-store", "sev": "CRITICAL", "eff": ["$20,000 lost sales per hour"], "res": ["it", "sales"], "pri": 5, "tags": ["server", "e-commerce"]},
    {"id": "BIZ_023", "cat": "OPERATIONS", "desc": "Commercial refrigeration failure in perishable foods warehouse", "sev": "HIGH", "eff": ["$60,000 inventory spoilage"], "res": ["inventory", "cold_chain"], "pri": 4, "tags": ["spoilage", "refrigeration"]},
    {"id": "BIZ_024", "cat": "OPERATIONS", "desc": "Commercial delivery van fleet routes optimized by new GPS tool", "sev": "LOW", "eff": ["15% fuel cost reduction"], "res": ["fleet", "fuel"], "pri": 1, "tags": ["logistics", "efficiency"]},
    {"id": "BIZ_025", "cat": "OPERATIONS", "desc": "Night shift break-in and inventory theft at perimeter depot", "sev": "MEDIUM", "eff": ["Property loss, security upgrade"], "res": ["security", "insurance"], "pri": 3, "tags": ["theft", "security"]},
    {"id": "BIZ_026", "cat": "MARKETING", "desc": "Viral social media video brings deluge of 5,000 new orders", "sev": "MEDIUM", "eff": ["Order fulfillment backlog"], "res": ["fulfillment", "inventory"], "pri": 3, "tags": ["viral", "demand"]},
    {"id": "BIZ_027", "cat": "MARKETING", "desc": "Influencer marketing campaign fails to deliver targeted returns", "sev": "LOW", "eff": ["Wasted ad expenditure"], "res": ["marketing_budget"], "pri": 2, "tags": ["marketing", "roi"]},
    {"id": "BIZ_028", "cat": "MARKETING", "desc": "Customer satisfaction index reaches all-time high of 94%", "sev": "LOW", "eff": ["High customer retention"], "res": ["reputation"], "pri": 1, "tags": ["satisfaction", "reviews"]},
    {"id": "BIZ_029", "cat": "MARKETING", "desc": "Viral customer complaint over customer support gains traction", "sev": "MEDIUM", "eff": ["Reputation damage control needed"], "res": ["pr", "support"], "pri": 3, "tags": ["pr", "complaint"]},
    {"id": "BIZ_030", "cat": "MARKETING", "desc": "Annual trade show awards business 'Product of the Year'", "sev": "LOW", "eff": ["Brand prestige surge"], "res": ["marketing"], "pri": 1, "tags": ["award", "branding"]},
    {"id": "BIZ_031", "cat": "REGULATORY", "desc": "New city carbon tax increases commercial utility bills by 18%", "sev": "HIGH", "eff": ["Energy costs surge"], "res": ["utilities", "overhead"], "pri": 4, "tags": ["carbon-tax", "compliance"]},
    {"id": "BIZ_032", "cat": "REGULATORY", "desc": "Food hygiene inspection awards prestigious 'Grade A' status", "sev": "LOW", "eff": ["Customer dining confidence"], "res": ["reputation"], "pri": 1, "tags": ["inspection", "food"]},
    {"id": "BIZ_033", "cat": "REGULATORY", "desc": "Commercial waste disposal regulations mandate expensive sorting", "sev": "MEDIUM", "eff": ["Operational compliance cost"], "res": ["waste_budget"], "pri": 3, "tags": ["waste", "regulations"]},
    {"id": "BIZ_034", "cat": "REGULATORY", "desc": "Municipal building inspectors issue code violation on signage", "sev": "LOW", "eff": ["Signage replacement fine"], "res": ["permits"], "pri": 2, "tags": ["signage", "permits"]},
    {"id": "BIZ_035", "cat": "REGULATORY", "desc": "Data privacy regulation audit mandates comprehensive user consent audit", "sev": "MEDIUM", "eff": ["Legal and IT workload"], "res": ["compliance"], "pri": 3, "tags": ["privacy", "gdpr"]},
    {"id": "BIZ_036", "cat": "EXPANSION", "desc": "Commercial real estate site scouting identifies prime corner location", "sev": "LOW", "eff": ["Second storefront opportunity"], "res": ["capital", "expansion"], "pri": 2, "tags": ["expansion", "real-estate"]},
    {"id": "BIZ_037", "cat": "EXPANSION", "desc": "Franchise inquiry received from regional business investor group", "sev": "LOW", "eff": ["Franchise royalty model prospective"], "res": ["legal", "growth"], "pri": 2, "tags": ["franchise", "investment"]},
    {"id": "BIZ_038", "cat": "EXPANSION", "desc": "International distribution inquiry for wholesale merchandise export", "sev": "MEDIUM", "eff": ["Customs and shipping requirements"], "res": ["export", "inventory"], "pri": 3, "tags": ["export", "wholesale"]},
    {"id": "BIZ_039", "cat": "EXPANSION", "desc": "Merger proposal received from complementary service provider", "sev": "HIGH", "eff": ["Board valuation deliberations"], "res": ["executive", "legal"], "pri": 4, "tags": ["merger", "acquisition"]},
    {"id": "BIZ_040", "cat": "EXPANSION", "desc": "New online B2B portal launch captures 40 enterprise accounts", "sev": "LOW", "eff": ["Recurring subscription revenue"], "res": ["sales", "b2b"], "pri": 1, "tags": ["b2b", "growth"]},
    {"id": "BIZ_041", "cat": "TECHNOLOGY", "desc": "Ransomware encryption strikes corporate bookkeeping workstations", "sev": "CRITICAL", "eff": ["Financial record lockout, extortion"], "res": ["cyber_defense", "backups"], "pri": 5, "tags": ["cyber", "ransomware"]},
    {"id": "BIZ_042", "cat": "TECHNOLOGY", "desc": "AI customer service automation deployment reduces wait times 70%", "sev": "LOW", "eff": ["Support overhead savings"], "res": ["it", "support"], "pri": 1, "tags": ["ai", "automation"]},
    {"id": "BIZ_043", "cat": "TECHNOLOGY", "desc": "Enterprise ERP accounting software upgrade corrupts tax tables", "sev": "HIGH", "eff": ["Audit delay, invoice re-runs"], "res": ["it", "finance"], "pri": 4, "tags": ["erp", "bug"]},
    {"id": "BIZ_044", "cat": "TECHNOLOGY", "desc": "Credit card POS terminals offline due to cellular carrier failure", "sev": "HIGH", "eff": ["Cash only transactions, customer drop"], "res": ["pos", "telecom"], "pri": 4, "tags": ["pos", "connectivity"]},
    {"id": "BIZ_045", "cat": "TECHNOLOGY", "desc": "Patent granted for proprietary automated inventory restocking system", "sev": "LOW", "eff": ["Intellectual property asset"], "res": ["ip", "patent"], "pri": 1, "tags": ["patent", "innovation"]},
    {"id": "BIZ_046", "cat": "FINANCE", "desc": "Commercial liability insurance premiums increase 40% after claim", "sev": "HIGH", "eff": ["Annual expense increase"], "res": ["insurance", "capital"], "pri": 4, "tags": ["insurance", "premium"]},
    {"id": "BIZ_047", "cat": "SUPPLY_CHAIN", "desc": "Packaging supplier switches to biodegradable plastics without delay", "sev": "LOW", "eff": ["Green marketing compliance"], "res": ["packaging"], "pri": 1, "tags": ["packaging", "eco"]},
    {"id": "BIZ_048", "cat": "LABOR", "desc": "Key sales manager poaches three top sales reps to new startup", "sev": "HIGH", "eff": ["Immediate quarterly sales drop"], "res": ["sales", "retention"], "pri": 4, "tags": ["sales", "poaching"]},
    {"id": "BIZ_049", "cat": "OPERATIONS", "desc": "Energy grid blackout causes manufacturing shift cancellation", "sev": "MEDIUM", "eff": ["Lost production output"], "res": ["production", "energy"], "pri": 3, "tags": ["blackout", "factory"]},
    {"id": "BIZ_050", "cat": "MARKETING", "desc": "Local sports team sponsorship delivers high brand recognition", "sev": "LOW", "eff": ["Community goodwill"], "res": ["marketing"], "pri": 1, "tags": ["sponsorship", "sports"]},
    {"id": "BIZ_051", "cat": "FINANCE", "desc": "Foreign exchange currency devaluation cuts export profit margins", "sev": "MEDIUM", "eff": ["Foreign revenue worth less"], "res": ["forex", "margins"], "pri": 3, "tags": ["forex", "currency"]},
    {"id": "BIZ_052", "cat": "LABOR", "desc": "Annual employee bonus pool announced at 120% of target", "sev": "LOW", "eff": ["High staff morale boost"], "res": ["payroll", "morale"], "pri": 1, "tags": ["bonus", "morale"]},
    {"id": "BIZ_053", "cat": "SUPPLY_CHAIN", "desc": "Customs clearance delay at international shipping harbor", "sev": "MEDIUM", "eff": ["Imported inventory delayed 10 days"], "res": ["customs", "logistics"], "pri": 3, "tags": ["customs", "import"]},
    {"id": "BIZ_054", "cat": "MARKET_COMPETITION", "desc": "Trade magazine ranks business #1 in customer satisfaction", "sev": "LOW", "eff": ["Inbound sales leads spike"], "res": ["sales"], "pri": 1, "tags": ["ranking", "satisfaction"]},
    {"id": "BIZ_055", "cat": "OPERATIONS", "desc": "Commercial waste hauler misses weekly trash pickup, creating odor", "sev": "LOW", "eff": ["Customer aesthetic complaint"], "res": ["waste"], "pri": 1, "tags": ["trash", "sanitation"]},
    {"id": "BIZ_056", "cat": "REGULATORY", "desc": "State sales tax audit initiated for past three calendar years", "sev": "MEDIUM", "eff": ["Document production burden"], "res": ["accounting"], "pri": 3, "tags": ["tax", "audit"]},
    {"id": "BIZ_057", "cat": "TECHNOLOGY", "desc": "Warehouse barcode scanner upgrade reduces packing errors to 0.1%", "sev": "LOW", "eff": ["Shipping accuracy gains"], "res": ["equipment"], "pri": 1, "tags": ["barcode", "packing"]},
    {"id": "BIZ_058", "cat": "FINANCE", "desc": "Angel investor group offers seed funding for new tech venture", "sev": "LOW", "eff": ["New venture capital funding"], "res": ["investors"], "pri": 2, "tags": ["investors", "seed"]},
    {"id": "BIZ_059", "cat": "EXPANSION", "desc": "Construction permits approved for new suburban distribution center", "sev": "LOW", "eff": ["Groundbreaking ceremony scheduled"], "res": ["real-estate"], "pri": 2, "tags": ["permits", "warehouse"]},
    {"id": "BIZ_060", "cat": "MARKETING", "desc": "Black Friday retail rush overwhelms store registers and staff", "sev": "HIGH", "eff": ["Record sales but long lines"], "res": ["staff", "cash_registers"], "pri": 4, "tags": ["black-friday", "rush"]},
    {"id": "BIZ_061", "cat": "OPERATIONS", "desc": "Fire sprinkler system false alarm soaks retail display merchandise", "sev": "HIGH", "eff": ["$30,000 inventory water loss"], "res": ["inventory", "insurance"], "pri": 4, "tags": ["sprinklers", "damage"]},
    {"id": "BIZ_062", "cat": "LABOR", "desc": "Company health insurance premiums quote 15% annual increase", "sev": "MEDIUM", "eff": ["Employee benefit costs climb"], "res": ["benefits", "payroll"], "pri": 3, "tags": ["health-insurance", "costs"]},
    {"id": "BIZ_063", "cat": "SUPPLY_CHAIN", "desc": "Critical microchip shortage delays smart device product shipment", "sev": "HIGH", "eff": ["Backorders mount"], "res": ["chips", "supply"], "pri": 4, "tags": ["microchips", "shortage"]},
    {"id": "BIZ_064", "cat": "MARKET_COMPETITION", "desc": "Direct competitor files for Chapter 11 bankruptcy liquidation", "sev": "MEDIUM", "eff": ["Opportunity to acquire accounts"], "res": ["market_share"], "pri": 3, "tags": ["bankruptcy", "competitor"]},
    {"id": "BIZ_065", "cat": "REGULATORY", "desc": "Municipal green building code mandates solar installation on roof", "sev": "MEDIUM", "eff": ["Capital investment requirement"], "res": ["capital", "green"], "pri": 3, "tags": ["solar", "code"]},
    {"id": "BIZ_066", "cat": "FINANCE", "desc": "Venture debt balloon payment maturity arrives in 90 days", "sev": "CRITICAL", "eff": ["Refinancing needed immediately"], "res": ["debt", "cash"], "pri": 5, "tags": ["debt", "maturity"]},
    {"id": "BIZ_067", "cat": "TECHNOLOGY", "desc": "Fiber optic internet line severed by construction excavator nearby", "sev": "HIGH", "eff": ["Total office internet outage"], "res": ["telecom"], "pri": 4, "tags": ["fiber", "excavation"]},
    {"id": "BIZ_068", "cat": "MARKETING", "desc": "Customer loyalty reward program signups surpass 50,000 members", "sev": "LOW", "eff": ["Direct marketing audience built"], "res": ["marketing"], "pri": 1, "tags": ["loyalty", "database"]},
    {"id": "BIZ_069", "cat": "LABOR", "desc": "Remote work policy adjustment sparks employee retention debates", "sev": "LOW", "eff": ["Hybrid policy formulated"], "res": ["hr"], "pri": 2, "tags": ["remote-work", "hr"]},
    {"id": "BIZ_070", "cat": "OPERATIONS", "desc": "HVAC compressor failure causes unbearable heat in corporate call center", "sev": "MEDIUM", "eff": ["Agents sent home early"], "res": ["facilities"], "pri": 3, "tags": ["hvac", "call-center"]}
]

# ---------------------------------------------------------------------------
# 5. CAR CONDITIONS (70 conditions)
# ---------------------------------------------------------------------------
CAR_CONDITIONS: List[Dict[str, Any]] = [
    {"id": "CAR_001", "cat": "NAVIGATION", "desc": "Major traffic accident on highway route: 35-minute delay ahead", "sev": "HIGH", "eff": ["Reroute calculation needed", "Late arrival"], "res": ["route", "time", "battery"], "pri": 4, "tags": ["accident", "reroute", "highway"]},
    {"id": "CAR_002", "cat": "NAVIGATION", "desc": "Emergency construction lane closure on suspension bridge", "sev": "HIGH", "eff": ["Bottleneck funnel, 25-min lag"], "res": ["route", "time"], "pri": 4, "tags": ["construction", "bridge"]},
    {"id": "CAR_003", "cat": "NAVIGATION", "desc": "GPS satellite signal lost while inside subterranean tunnel", "sev": "MEDIUM", "eff": ["Inertial dead reckoning mode active"], "res": ["sensors", "gps"], "pri": 3, "tags": ["gps", "tunnel"]},
    {"id": "CAR_004", "cat": "NAVIGATION", "desc": "Unmapped detour signs directing vehicles down residential alley", "sev": "MEDIUM", "eff": ["Tight clearance, slow speed"], "res": ["route", "speed"], "pri": 3, "tags": ["detour", "narrow"]},
    {"id": "CAR_005", "cat": "NAVIGATION", "desc": "Scenic bypass road completely clear with zero traffic slowdowns", "sev": "LOW", "eff": ["On-time arrival projected"], "res": ["time"], "pri": 1, "tags": ["clear", "efficient"]},
    {"id": "CAR_006", "cat": "VEHICLE_HEALTH", "desc": "Tire pressure monitoring warning: front right tire at 18 PSI", "sev": "HIGH", "eff": ["Blowout danger at highway speeds"], "res": ["tires", "speed"], "pri": 4, "tags": ["tire", "pressure", "safety"]},
    {"id": "CAR_007", "cat": "VEHICLE_HEALTH", "desc": "Engine cooling temperature gauge climbing toward redline", "sev": "CRITICAL", "eff": ["Overheating engine seizure risk"], "res": ["engine", "coolant"], "pri": 5, "tags": ["overheating", "engine"]},
    {"id": "CAR_008", "cat": "VEHICLE_HEALTH", "desc": "Brake pad sensor indicator warning: 10% wear life remaining", "sev": "MEDIUM", "eff": ["Increased stopping distance"], "res": ["brakes"], "pri": 3, "tags": ["brakes", "wear"]},
    {"id": "CAR_009", "cat": "VEHICLE_HEALTH", "desc": "Battery state of charge critical at 7%: charging station needed", "sev": "CRITICAL", "eff": ["Immobilization risk within 8 miles"], "res": ["battery", "range"], "pri": 5, "tags": ["battery", "charge", "ev"]},
    {"id": "CAR_010", "cat": "VEHICLE_HEALTH", "desc": "Windshield washer fluid reservoir empty with salt spray blinding glass", "sev": "MEDIUM", "eff": ["Impaired driver/sensor visibility"], "res": ["visibility"], "pri": 3, "tags": ["windshield", "visibility"]},
    {"id": "CAR_011", "cat": "ROAD_HAZARDS", "desc": "Black ice patch detected on elevated highway overpass", "sev": "CRITICAL", "eff": ["Severe loss of traction / spinout"], "res": ["traction", "speed"], "pri": 5, "tags": ["ice", "traction", "winter"]},
    {"id": "CAR_012", "cat": "ROAD_HAZARDS", "desc": "Deep pothole hidden under muddy standing puddle water", "sev": "HIGH", "eff": ["Rim damage, suspension shock"], "res": ["suspension", "tires"], "pri": 4, "tags": ["pothole", "hazard"]},
    {"id": "CAR_013", "cat": "ROAD_HAZARDS", "desc": "Fallen tree limb obstructing right passenger travel lane", "sev": "HIGH", "eff": ["Emergency swerve or stop required"], "res": ["steering", "brakes"], "pri": 4, "tags": ["obstruction", "tree"]},
    {"id": "CAR_014", "cat": "ROAD_HAZARDS", "desc": "Loose gravel scattered across sharp curved highway exit ramp", "sev": "MEDIUM", "eff": ["Reduced cornering grip"], "res": ["traction", "speed"], "pri": 3, "tags": ["gravel", "curve"]},
    {"id": "CAR_015", "cat": "ROAD_HAZARDS", "desc": "Flash flooding submerging downtown roadway under 14 inches water", "sev": "CRITICAL", "eff": ["Hydroplaning, engine water intake"], "res": ["route", "engine"], "pri": 5, "tags": ["flood", "water"]},
    {"id": "CAR_016", "cat": "TRAFFIC_INTERACTIONS", "desc": "Emergency fire engine approaching rapidly with sirens behind", "sev": "CRITICAL", "eff": ["Must safely yield and pull over right"], "res": ["steering", "speed"], "pri": 5, "tags": ["emergency", "yield", "siren"]},
    {"id": "CAR_017", "cat": "TRAFFIC_INTERACTIONS", "desc": "Erratic driver tailgating aggressively and weaving between lanes", "sev": "HIGH", "eff": ["Collision hazard, defensive space needed"], "res": ["speed", "buffer"], "pri": 4, "tags": ["tailgating", "aggressive"]},
    {"id": "CAR_018", "cat": "TRAFFIC_INTERACTIONS", "desc": "Jaywalking pedestrian stepping into traffic looking at smartphone", "sev": "CRITICAL", "eff": ["Emergency braking collision avoidance"], "res": ["brakes", "sensors"], "pri": 5, "tags": ["pedestrian", "braking", "hazard"]},
    {"id": "CAR_019", "cat": "TRAFFIC_INTERACTIONS", "desc": "Commercial tractor trailer merging blind without signaling", "sev": "HIGH", "eff": ["Blind spot squeeze risk"], "res": ["horn", "brakes"], "pri": 4, "tags": ["truck", "merge", "blindspot"]},
    {"id": "CAR_020", "cat": "TRAFFIC_INTERACTIONS", "desc": "School bus flashing yellow lights preparing to extend stop arm", "sev": "HIGH", "eff": ["Mandatory full stop required"], "res": ["brakes"], "pri": 4, "tags": ["school-bus", "stop"]},
    {"id": "CAR_021", "cat": "WEATHER", "desc": "Dense morning fog reducing forward visual range to under 30 feet", "sev": "HIGH", "eff": ["Slow speed, fog lights required"], "res": ["visibility", "speed"], "pri": 4, "tags": ["fog", "weather", "speed"]},
    {"id": "CAR_022", "cat": "WEATHER", "desc": "Torrential downpour causing widespread hydroplaning on expressway", "sev": "HIGH", "eff": ["Loss of tire water displacement"], "res": ["speed", "traction"], "pri": 4, "tags": ["rain", "hydroplane"]},
    {"id": "CAR_023", "cat": "WEATHER", "desc": "Severe crosswinds of 55 MPH buffeting vehicle on suspension bridge", "sev": "HIGH", "eff": ["Steering drift, speed reduction"], "res": ["steering", "speed"], "pri": 4, "tags": ["wind", "bridge"]},
    {"id": "CAR_024", "cat": "WEATHER", "desc": "Blinding sun glare reflecting off wet pavement during evening rush", "sev": "MEDIUM", "eff": ["Sensor saturation, visor needed"], "res": ["visibility"], "pri": 3, "tags": ["glare", "sun"]},
    {"id": "CAR_025", "cat": "WEATHER", "desc": "Heavy hail storm denting vehicle roof and cracking windshield", "sev": "HIGH", "eff": ["Emergency overpass shelter needed"], "res": ["chassis", "safety"], "pri": 4, "tags": ["hail", "shelter"]},
    {"id": "CAR_026", "cat": "AUTONOMOUS_SENSORS", "desc": "Forward LiDAR sensor aperture obscured by heavy mud spatter", "sev": "HIGH", "eff": ["Degraded 3D depth perception"], "res": ["sensors", "lidar"], "pri": 4, "tags": ["lidar", "sensor", "autonomous"]},
    {"id": "CAR_027", "cat": "AUTONOMOUS_SENSORS", "desc": "Optical camera blinded by oncoming high-beam truck lights", "sev": "MEDIUM", "eff": ["Lane detection confidence drop"], "res": ["cameras", "vision"], "pri": 3, "tags": ["camera", "glare"]},
    {"id": "CAR_028", "cat": "AUTONOMOUS_SENSORS", "desc": "Ultrasonic proximity sensor failure in rear left bumper", "sev": "LOW", "eff": ["Blind spot radar fallback active"], "res": ["ultrasonic"], "pri": 2, "tags": ["sensors", "ultrasonic"]},
    {"id": "CAR_029", "cat": "AUTONOMOUS_SENSORS", "desc": "Vehicle-to-Infrastructure (V2I) communication handshake confirmed", "sev": "LOW", "eff": ["Traffic light timing synchronization"], "res": ["v2x", "efficiency"], "pri": 1, "tags": ["v2x", "infrastructure"]},
    {"id": "CAR_030", "cat": "AUTONOMOUS_SENSORS", "desc": "Autonomous control system confidence rating drop to 82%", "sev": "HIGH", "eff": ["Disengagement prompt or speed cap"], "res": ["autonomy", "safety"], "pri": 4, "tags": ["autonomous", "disengagement"]},
    {"id": "CAR_031", "cat": "ENERGY_EFFICIENCY", "desc": "High-speed highway travel consuming battery 25% faster than model", "sev": "MEDIUM", "eff": ["Recomputed range estimate reduced"], "res": ["battery", "range"], "pri": 3, "tags": ["efficiency", "highway"]},
    {"id": "CAR_032", "cat": "ENERGY_EFFICIENCY", "desc": "Cabin air conditioning operating at maximum cooling in 100°F heat", "sev": "LOW", "eff": ["Minor auxiliary energy draw"], "res": ["battery"], "pri": 2, "tags": ["hvac", "battery"]},
    {"id": "CAR_033", "cat": "ENERGY_EFFICIENCY", "desc": "Regenerative braking recovering 18% energy during mountain descent", "sev": "LOW", "eff": ["Battery state of charge increasing"], "res": ["battery", "regen"], "pri": 1, "tags": ["regen", "efficiency"]},
    {"id": "CAR_034", "cat": "ENERGY_EFFICIENCY", "desc": "Fast-charging DC supercharger queue has 4 vehicles waiting", "sev": "MEDIUM", "eff": ["25-minute charging wait time"], "res": ["charging", "time"], "pri": 3, "tags": ["charger", "queue"]},
    {"id": "CAR_035", "cat": "ENERGY_EFFICIENCY", "desc": "Eco-routing mode active: selecting flatter terrain to save 12% kwH", "sev": "LOW", "eff": ["Optimized energy expenditure"], "res": ["range"], "pri": 1, "tags": ["eco-route", "efficiency"]},
    {"id": "CAR_036", "cat": "PARKING_DESTINATION", "desc": "Destination parking garage full with 'NO VACANCY' sign displayed", "sev": "MEDIUM", "eff": ["Search for street parking needed"], "res": ["parking", "time"], "pri": 3, "tags": ["parking", "garage"]},
    {"id": "CAR_037", "cat": "PARKING_DESTINATION", "desc": "Curbside automated parallel parking spot detected with ample clearance", "sev": "LOW", "eff": ["Self-parking maneuver ready"], "res": ["parking"], "pri": 1, "tags": ["parking", "curbside"]},
    {"id": "CAR_038", "cat": "PARKING_DESTINATION", "desc": "Reserved EV charging parking space occupied by non-electric vehicle", "sev": "MEDIUM", "eff": ["ICE-ing obstruction"], "res": ["charging"], "pri": 3, "tags": ["charging", "blocked"]},
    {"id": "CAR_039", "cat": "PARKING_DESTINATION", "desc": "Low ceiling clearance in underground garage: 6'4\" warning barrier", "sev": "MEDIUM", "eff": ["Roof cargo height verification needed"], "res": ["clearance"], "pri": 3, "tags": ["clearance", "height"]},
    {"id": "CAR_040", "cat": "PARKING_DESTINATION", "desc": "Destination drop-off loading zone blocked by parked delivery vans", "sev": "LOW", "eff": ["Must circle the block"], "res": ["time"], "pri": 2, "tags": ["dropoff", "loading"]},
    {"id": "CAR_041", "cat": "VEHICLE_HEALTH", "desc": "Power steering hydraulic fluid pressure alert chime sounds", "sev": "HIGH", "eff": ["Heavy steering resistance"], "res": ["steering"], "pri": 4, "tags": ["steering", "fluid"]},
    {"id": "CAR_042", "cat": "ROAD_HAZARDS", "desc": "Loose metal ladder fallen from contractor truck lying across lane", "sev": "CRITICAL", "eff": ["Severe vehicle undercarriage impalement"], "res": ["brakes", "steering"], "pri": 5, "tags": ["debris", "ladder", "critical"]},
    {"id": "CAR_043", "cat": "TRAFFIC_INTERACTIONS", "desc": "Motorcycle lane splitting at 45 MPH in stopped bumper-to-bumper queue", "sev": "MEDIUM", "eff": ["Lateral mirror check mandatory"], "res": ["mirrors", "sensors"], "pri": 3, "tags": ["motorcycle", "lane-split"]},
    {"id": "CAR_044", "cat": "NAVIGATION", "desc": "Traffic roundabout entry: heavy circulating flow with few merge gaps", "sev": "LOW", "eff": ["Yield waiting at roundabout entry"], "res": ["speed", "timing"], "pri": 2, "tags": ["roundabout", "yield"]},
    {"id": "CAR_045", "cat": "WEATHER", "desc": "Sudden thunderstorm with high lightning strike density near highway", "sev": "MEDIUM", "eff": ["Reduced sensor radio clarity"], "res": ["sensors"], "pri": 3, "tags": ["storm", "lightning"]},
    {"id": "CAR_046", "cat": "AUTONOMOUS_SENSORS", "desc": "Faded lane markings completely invisible under road salt residue", "sev": "HIGH", "eff": ["Vision system cannot find lane lines"], "res": ["vision", "lane_keep"], "pri": 4, "tags": ["lane-markings", "salt"]},
    {"id": "CAR_047", "cat": "TRAFFIC_INTERACTIONS", "desc": "Police officer using manual hand signals to direct intersection flow", "sev": "HIGH", "eff": ["Traffic light override, must obey gestures"], "res": ["vision", "speed"], "pri": 4, "tags": ["police", "hand-signals"]},
    {"id": "CAR_048", "cat": "VEHICLE_HEALTH", "desc": "Transmission gear slippage detected when accelerating onto ramp", "sev": "HIGH", "eff": ["Hesitant acceleration"], "res": ["transmission", "speed"], "pri": 4, "tags": ["transmission", "acceleration"]},
    {"id": "CAR_049", "cat": "ROAD_HAZARDS", "desc": "Fresh roadkill deer carcass in right travel lane", "sev": "HIGH", "eff": ["Immediate avoidance lane shift"], "res": ["steering", "sensors"], "pri": 4, "tags": ["hazard", "animal"]},
    {"id": "CAR_050", "cat": "NAVIGATION", "desc": "Toll plaza approaching: electronic transponder lane clear", "sev": "LOW", "eff": ["Seamless toll deduction"], "res": ["toll"], "pri": 1, "tags": ["toll", "highway"]},
    {"id": "CAR_051", "cat": "VEHICLE_HEALTH", "desc": "Alternator voltage drop warning: electrical system running off 12V", "sev": "HIGH", "eff": ["Impending complete shutdown"], "res": ["electrical"], "pri": 4, "tags": ["alternator", "battery"]},
    {"id": "CAR_052", "cat": "ROAD_HAZARDS", "desc": "Active steam pipe vent cloud blinding visibility at curb", "sev": "MEDIUM", "eff": ["Zero visibility for 50 feet"], "res": ["visibility"], "pri": 3, "tags": ["steam", "visibility"]},
    {"id": "CAR_053", "cat": "TRAFFIC_INTERACTIONS", "desc": "Bicycle delivery courier cutting across vehicle bow without look", "sev": "HIGH", "eff": ["Near collision, hard braking"], "res": ["brakes"], "pri": 4, "tags": ["courier", "cyclist"]},
    {"id": "CAR_054", "cat": "WEATHER", "desc": "Freezing rain coating wiper blades in thick ice crust", "sev": "HIGH", "eff": ["Wipers chattering, smeared glass"], "res": ["wipers", "defrost"], "pri": 4, "tags": ["freezing-rain", "ice"]},
    {"id": "CAR_055", "cat": "AUTONOMOUS_SENSORS", "desc": "Radar sensor detecting phantom obstacle from metal expansion joint", "sev": "MEDIUM", "eff": ["False positive braking risk"], "res": ["radar", "filtering"], "pri": 3, "tags": ["phantom-braking", "radar"]},
    {"id": "CAR_056", "cat": "NAVIGATION", "desc": "Railroad crossing arm lowering with red flashing signals", "sev": "CRITICAL", "eff": ["Mandatory stop for freight train"], "res": ["brakes"], "pri": 5, "tags": ["train", "crossing"]},
    {"id": "CAR_057", "cat": "ENERGY_EFFICIENCY", "desc": "Headwind of 35 MPH blowing directly against frontal vehicle area", "sev": "LOW", "eff": ["Aerodynamic drag increasing"], "res": ["fuel", "battery"], "pri": 2, "tags": ["headwind", "drag"]},
    {"id": "CAR_058", "cat": "PARKING_DESTINATION", "desc": "Automated valet parking garage guidance interface synced", "sev": "LOW", "eff": ["Vehicle handoff to depot robotics"], "res": ["valet"], "pri": 1, "tags": ["valet", "smart-parking"]},
    {"id": "CAR_059", "cat": "TRAFFIC_INTERACTIONS", "desc": "Funeral procession with headlights on proceeding across red light", "sev": "MEDIUM", "eff": ["Yield right of way courtesy"], "res": ["speed"], "pri": 3, "tags": ["procession", "yield"]},
    {"id": "CAR_060", "cat": "ROAD_HAZARDS", "desc": "Open manhole cover marked only by solitary orange traffic cone", "sev": "CRITICAL", "eff": ["Severe catastrophic axle damage"], "res": ["steering", "suspension"], "pri": 5, "tags": ["manhole", "hazard"]},
    {"id": "CAR_061", "cat": "VEHICLE_HEALTH", "desc": "Exhaust muffler hanger detached, scraping loudly on asphalt", "sev": "MEDIUM", "eff": ["Sparks, noise, repair needed"], "res": ["exhaust"], "pri": 3, "tags": ["exhaust", "noise"]},
    {"id": "CAR_062", "cat": "AUTONOMOUS_SENSORS", "desc": "High-definition mapping layer mismatch due to newly paved bypass", "sev": "MEDIUM", "eff": ["Localization fallback to vision"], "res": ["hd_maps", "localization"], "pri": 3, "tags": ["hd-maps", "bypass"]},
    {"id": "CAR_063", "cat": "NAVIGATION", "desc": "Express lanes open with free toll waiver for multi-passenger cars", "sev": "LOW", "eff": ["15-minute commute time savings"], "res": ["hov", "route"], "pri": 1, "tags": ["express-lane", "hov"]},
    {"id": "CAR_064", "cat": "TRAFFIC_INTERACTIONS", "desc": "Garbage collection truck making frequent stops every 20 feet", "sev": "LOW", "eff": ["Slow crawl, pass when safe"], "res": ["speed", "patience"], "pri": 2, "tags": ["garbage-truck", "slow"]},
    {"id": "CAR_065", "cat": "WEATHER", "desc": "Tornado watch sirens sounding across metropolitan county", "sev": "CRITICAL", "eff": ["Seek sturdy shelter immediately"], "res": ["safety", "route"], "pri": 5, "tags": ["tornado", "extreme-weather"]},
    {"id": "CAR_066", "cat": "ROAD_HAZARDS", "desc": "Spilled box of construction roofing nails scattered across lane", "sev": "HIGH", "eff": ["Puncture risk to multiple tires"], "res": ["tires", "steering"], "pri": 4, "tags": ["nails", "puncture"]},
    {"id": "CAR_067", "cat": "VEHICLE_HEALTH", "desc": "Headlight low beam bulb burned out on driver side", "sev": "MEDIUM", "eff": ["Reduced nighttime forward illumination"], "res": ["lighting"], "pri": 3, "tags": ["headlight", "lighting"]},
    {"id": "CAR_068", "cat": "ENERGY_EFFICIENCY", "desc": "Downhill highway stretch enables gravity coasting for 3 miles", "sev": "LOW", "eff": ["Zero fuel/battery consumption"], "res": ["efficiency"], "pri": 1, "tags": ["coasting", "gravity"]},
    {"id": "CAR_069", "cat": "PARKING_DESTINATION", "desc": "Valet charging station completed 100% full charge top-off", "sev": "LOW", "eff": ["Maximum driving range available"], "res": ["battery"], "pri": 1, "tags": ["full-charge", "ready"]},
    {"id": "CAR_070", "cat": "AUTONOMOUS_SENSORS", "desc": "Over-the-air (OTA) firmware update ready for installation upon park", "sev": "LOW", "eff": ["Autonomous perception enhancements"], "res": ["software"], "pri": 1, "tags": ["ota", "firmware"]}
]

# ---------------------------------------------------------------------------
# CONDITION REGISTRY & SELECTOR
# ---------------------------------------------------------------------------
PRIMARY_ROLES = ["POLICE", "GOVERNMENT", "CITIZEN", "BUSINESS", "CAR"]

ROLE_CONTAINERS: Dict[str, List[Dict[str, Any]]] = {
    "POLICE": POLICE_CONDITIONS,
    "GOVERNMENT": GOVERNMENT_CONDITIONS,
    "CITIZEN": CITIZEN_CONDITIONS,
    "BUSINESS": BUSINESS_CONDITIONS,
    "CAR": CAR_CONDITIONS
}

class ConditionSelector:
    @staticmethod
    def get_all_conditions_for_role(role: str) -> List[RoleCondition]:
        norm_role = role.upper().strip()
        raw_list = ROLE_CONTAINERS.get(norm_role, [])
        return [
            RoleCondition(
                condition_id=c["id"],
                role=norm_role,
                category=c["cat"],
                description=c["desc"],
                severity=c["sev"],
                possible_effects=c["eff"],
                resource_relevance=c["res"],
                priority=c["pri"],
                tags=c["tags"]
            )
            for c in raw_list
        ]

    @staticmethod
    def select_active_conditions(role: str, count: Optional[int] = None, seed: Optional[int] = None) -> List[RoleCondition]:
        """
        Selects between 3 and 7 active conditions STRICTLY from the specified role's container.
        Deterministic when seed is provided. No duplicates within the same cycle.
        """
        all_conditions = ConditionSelector.get_all_conditions_for_role(role)
        if not all_conditions:
            return []

        rng = random.Random(seed) if seed is not None else random.Random()
        
        # Determine count between 3 and 7 (or clamp requested count)
        if count is None:
            num = rng.randint(3, 7)
        else:
            num = max(3, min(7, count))
            
        num = min(num, len(all_conditions))
        
        # Sample without replacement (no duplicates)
        selected = rng.sample(all_conditions, num)
        return selected
