"""
Agri Link — Plant Disease Treatments Directory
================================================
Pre-configured treatment and prevention details for supported plant diseases.
"""

TREATMENTS = {
    "Apple___Apple_scab": {
        "disease_name": "Apple Scab",
        "suggested_treatment": (
            "Apply fungicides such as copper, captan, or sulfur compounds early in the season. "
            "Prune infected branches to improve air circulation."
        ),
        "prevention": (
            "Rake and destroy fallen leaves in autumn to remove overwintering spores. "
            "Plant resistant apple varieties. Keep tree canopy open with regular pruning."
        ),
    },
    "Apple___Black_rot": {
        "disease_name": "Apple Black Rot",
        "suggested_treatment": (
            "Prune out dead wood, mummified fruit, and cankers. Apply protective fungicides "
            "such as captan or thiophanate-methyl during the blossom period."
        ),
        "prevention": (
            "Remove all infected debris and fruit from the orchard. Minimize tree stress "
            "and control insect wounds that allow entry to the fungus."
        ),
    },
    "Apple___Cedar_apple_rust": {
        "disease_name": "Cedar Apple Rust",
        "suggested_treatment": (
            "Apply preventative fungicides containing myclobutanil or mancozeb at the first sign of leaf emerge."
        ),
        "prevention": (
            "Remove nearby red cedar or juniper trees (which host the fungus) within a 2-mile radius if possible. "
            "Choose rust-resistant apple cultivars."
        ),
    },
    "Apple___healthy": {
        "disease_name": "Healthy Apple Leaf",
        "suggested_treatment": "No treatment required. The apple tree is healthy.",
        "prevention": (
            "Maintain optimal watering, balanced fertilization, and monitor regularly for early symptoms of pests."
        ),
    },
    "Blueberry___healthy": {
        "disease_name": "Healthy Blueberry Leaf",
        "suggested_treatment": "No treatment required. The blueberry bush is healthy.",
        "prevention": "Ensure acidic soil pH (4.5 to 5.2), adequate mulching, and steady watering.",
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "disease_name": "Cherry Powdery Mildew",
        "suggested_treatment": (
            "Apply sulfur-based fungicides or potassium bicarbonate sprays. Ensure good tree pruning "
            "to increase sunlight penetration."
        ),
        "prevention": (
            "Space trees properly to encourage air flow. Avoid overhead irrigation, and prune away "
            "infected shoots early in the season."
        ),
    },
    "Cherry_(including_sour)___healthy": {
        "disease_name": "Healthy Cherry Leaf",
        "suggested_treatment": "No treatment required. The cherry tree is healthy.",
        "prevention": "Prune during dry winter weather, fertilize in early spring, and irrigate at the base.",
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "disease_name": "Corn Gray Leaf Spot",
        "suggested_treatment": (
            "Apply foliar fungicides such as strobilurin or triazole compounds if infection starts before tasseling."
        ),
        "prevention": (
            "Rotate crops with non-grasses. Till crop residues to accelerate breakdown of spores. "
            "Plant high-yield resistant corn hybrids."
        ),
    },
    "Corn_(maize)___Common_rust_": {
        "disease_name": "Corn Common Rust",
        "suggested_treatment": (
            "Apply fungicides immediately if rust pustules appear on lower leaves before silking. "
            "Usually not cost-effective late in the season."
        ),
        "prevention": (
            "Use hybrid corn seeds with genetic resistance. Plant crops early to avoid peak warm-humid rust seasons."
        ),
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "disease_name": "Northern Corn Leaf Blight",
        "suggested_treatment": (
            "Apply recommended fungicides (e.g. pyraclostrobin) if disease symptoms emerge early and weather is wet."
        ),
        "prevention": (
            "Rotate crops annually. Manage residual stubble with tillage. Select resistant seed hybrids."
        ),
    },
    "Corn_(maize)___healthy": {
        "disease_name": "Healthy Corn Leaf",
        "suggested_treatment": "No treatment required. The corn crop is healthy.",
        "prevention": "Ensure nitrogen-rich fertilization, appropriate weeding, and proper drainage.",
    },
    "Grape___Black_rot": {
        "disease_name": "Grape Black Rot",
        "suggested_treatment": (
            "Remove and destroy all mummified fruit clusters. Apply copper or mancozeb fungicides "
            "from early shoot growth until post-bloom."
        ),
        "prevention": (
            "Prune grapevines to maximize air flow and sun exposure. Clean trellis structures of old vegetative debris."
        ),
    },
    "Grape___Esca_(Black_Measles)": {
        "disease_name": "Grape Esca (Black Measles)",
        "suggested_treatment": (
            "No direct chemical cure exists. Protect pruning wounds immediately using sealants or biological "
            "fungicide agents (e.g., Trichoderma species)."
        ),
        "prevention": (
            "Prune vines in dry weather. Disinfect pruning tools between vines. Remove severely infected vines."
        ),
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "disease_name": "Grape Leaf Blight",
        "suggested_treatment": (
            "Apply foliar fungicides such as copper oxychloride or carbendazim at the first sign of spot formation."
        ),
        "prevention": (
            "Collect and burn fallen leaves. Avoid overhead watering to minimize leaf wetness duration."
        ),
    },
    "Grape___healthy": {
        "disease_name": "Healthy Grape Leaf",
        "suggested_treatment": "No treatment required. The grapevine is healthy.",
        "prevention": "Perform canopy management, clean weeds, and check regularly for grape berry moths.",
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "disease_name": "Citrus Greening (HLB)",
        "suggested_treatment": (
            "No chemical cure is available. Remove and destroy infected trees immediately to prevent vector spread. "
            "Control Asian citrus psyllid insects using imidacloprid or chemical sprays."
        ),
        "prevention": (
            "Use only certified disease-free nursery stock. Monitor tree health regularly. Maintain high "
            "nutrient programs to prolong tree vitality."
        ),
    },
    "Peach___Bacterial_spot": {
        "disease_name": "Peach Bacterial Spot",
        "suggested_treatment": (
            "Apply copper-based sprays or oxytetracycline during the growing season according to guidelines."
        ),
        "prevention": (
            "Avoid planting susceptible cultivars. Maintain balanced soil fertility, and prune trees to "
            "improve sunlight and fast leaf drying."
        ),
    },
    "Peach___healthy": {
        "disease_name": "Healthy Peach Leaf",
        "suggested_treatment": "No treatment required. The peach tree is healthy.",
        "prevention": "Irrigate deeply, thin fruit appropriately, and apply organic mulch to protect roots.",
    },
    "Pepper,_bell___Bacterial_spot": {
        "disease_name": "Bell Pepper Bacterial Spot",
        "suggested_treatment": (
            "Apply copper-containing bactericides early in the disease outbreak. Streptomycin sprays "
            "can be used in seedlings."
        ),
        "prevention": (
            "Use certified disease-free seeds. Rotate crops with non-solanaceous plants. Avoid working in "
            "fields when foliage is wet."
        ),
    },
}


def get_treatment_info(class_name):
    """
    Lookup treatment and prevention information for a given class name.
    """
    return TREATMENTS.get(
        class_name,
        {
            "disease_name": class_name.replace("___", " ").replace("_", " "),
            "suggested_treatment": "Consult a local agriculture extension officer for treatment options.",
            "prevention": "Maintain overall plant hygiene and monitor crop parameters.",
        },
    )
