"""
Rule-based skincare recommendations for each disease class.
Includes detailed info, product images, and care guidance.
Stored locally - no external APIs.
Product/disease images use Picsum (free placeholders). Replace URLs with your own images if desired.
"""

# Images - Picsum (reliable, no API, consistent per seed)
_PIC = lambda seed, w=400, h=300: f"https://picsum.photos/seed/{seed}/{w}/{h}"
# Wikimedia Commons images (Redirects to raw file)
_WIKI = lambda filename: f"https://commons.wikimedia.org/wiki/Special:FilePath/{filename}?width=400"

RECOMMENDATIONS = {
    "Eczema": {
        "severity": "moderate",
        "description": "Eczema (Atopic Dermatitis) is a chronic inflammatory skin condition that weakens the skin's barrier function, leading to moisture loss and entry of irritants. It commonly presents as dry, itchy, red patches.",
        "symptoms": ["Intense itching (pruritus)", "Dry, sensitive skin", "Red to brownish-gray patches", "Small, raised bumps which may leak fluid", "Thickened, cracked, scaly skin"],
        "causes": ["Filaggrin gene mutation (skin barrier defect)", "Immune system dysfunction", "Environmental triggers (soaps, detergents, weather)", "Stress", "Food allergies (in some cases)"],
        "image": _WIKI("Eczema_(14100950936).jpg"),
        "products": [
            {"name": "CeraVe Moisturizing Cream", "image": " https://th.bing.com/th/id/OIP.s5lqFzPJyI_kftPPzVL5iQHaHa?w=185&h=185&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3", "url": "https://bit.ly/4r7QWtn", "description": "Contains 3 essential ceramides to restore the skin barrier."},
            {"name": "Aveeno Eczema Therapy Balm", "image": "https://m.media-amazon.com/images/I/61VhPrUCBJL._SX679_.jpg" , "url": "https://www.amazon.in/Aveeno-Baby-Eczema-Therapy-Night/dp/B07TWYKHV3", "description": "Colloidal oatmeal formula to soothe itch and irritation."},
            {"name": "Hydrocortisone 1% Cream", "image": "https://m.media-amazon.com/images/I/71j25TC7rBL._AC_SX679_.jpg", "url": "https://www.amazon.ae/Dr-Sheffields-Hydrocortisone-Itch-Cream/dp/B0032VEKY6", "description": "Anti-inflammatory steroid for mild flare-ups."},
            {"name": "La Roche-Posay Lipikar AP+", "image": "https://m.media-amazon.com/images/I/41zdDGRaw0L._SY300_SX300_QL70_FMwebp_.jpg", "url": "https://www.amazon.in/Roche-Posay-Lipikar-Lipid-Replenishing-Anti-Irritation/dp/B003QXZWYW", "description": "Prebiotic body cream to balance skin microbiome."},
        ],
        "ingredients": ["Ceramides", "Colloidal Oatmeal", "Petrolatum", "Niacinamide", "Shea Butter"],
        "remedies": ["Apply moisturizer within 3 mins of bathing", "Take lukewarm (not hot) bleach baths (diluted)", "Use wet wrap therapy for severe itching"],
        "lifestyle": ["Wear soft cotton clothing", "Avoid scratching (keep nails short)", "Use a humidifier", "Identify and avoid specific triggers"],
        "consult_when": "If signs of infection appear (pus, yellow crusts), sleep is disrupted, or OTC treatments fail.",
    },
    "Melanoma": {
        "severity": "high",
        "description": "Melanoma is the most dangerous form of skin cancer, originating in melanocytes (pigment cells). It can metastasize rapidly if not caught early. It often resembles a mole but changes over time.",
        "symptoms": ["A - Asymmetry (one half doesn't match the other)", "B - Border irregularity (ragged, notched)", "C - Color variation (black, brown, tan, red, blue)", "D - Diameter > 6mm (pencil eraser size)", "E - Evolving (changes in size, shape, or color)"],
        "causes": ["Ultraviolet (UV) radiation (sun/tanning beds)", "Fair skin/light eyes", "History of sunburns", "Family history", "Weakened immune system"],
        "image": _WIKI("Melanoma_(3).jpg"),
        "products": [
            {"name": "EltaMD UV Clear SPF 46", "image": "https://m.media-amazon.com/images/I/41-Czl9pdyL._SY300_SX300_QL70_FMwebp_.jpg", "url": " https://www.amazon.in/EltaMD-Clear-Tinted-Broad-Spectrum-Sunscreen/dp/B00ZPWR0N8", "description": "Medical-grade mineral sunscreen for sensitive skin."},
            {"name": "Coolibar UPF 50+ Hat", "image":  "https://m.media-amazon.com/images/I/71Hsrprc4qL._AC_SX569_.jpg", "url": " https://www.amazon.in/Coolibar-UPF-Mens-Ultra-Sun/dp/B00LPVKLOI", "description": "Physical protection from UV rays."},
            {"name": "ScarAway Silicone Gel Sheets", "image":  "https://m.media-amazon.com/images/I/718QcHdcUKL._SX466_.jpg", "url": "https://www.amazon.com/ScarAway-Clear-Silicone-Sheets-White/dp/B09179GNHH?th=1", "description": "For scar management after surgical removal (post-op)."},
            {"name": "DermLite DL100", "image": "https://m.media-amazon.com/images/I/31JEs38T+jL.jpg", "url": "https://www.amazon.in/3Gen-DL100SS-Silicone-Sleeve-DL100/dp/B007XAO4I4", "description": "Professional-grade dermatoscope for skin checks (optional)."},
        ],
        "ingredients": ["Zinc Oxide", "Titanium Dioxide", "Broad Spectrum filters"],
        "remedies": ["Surgical excision (primary treatment)", "Immunotherapy/Targeted therapy (for advanced cases)", "Regular strict sun protection"],
        "lifestyle": ["Avoid sun during peak hours (10 AM - 4 PM)", "Perform monthly self-exams", "Wear protective clothing", "No tanning beds"],
        "consult_when": "IMMEDIATELY if you notice any changing mole or spot fitting the ABCDE criteria.",
    },
    "Atopic Dermatitis": {
        "severity": "moderate",
        "description": "Atopic Dermatitis is the most common form of eczema. It is a chronic, relapsing condition characterized by itchy inflammation. It is often associated with asthma and hay fever (atopic triad).",
        "symptoms": ["Persistent itch", "Redness and rash", "Dryness", "Leathery skin (lichenification) from chronic scratching", "Sleep disturbance due to itch"],
        "causes": ["Genetic defects in skin barrier", "Immune system hypersensitivity", "Environmental allergens (pollen, dust mites)", "Microbes (Staph. aureus)"],
        "image": _WIKI("Atopic_dermatitis.png"),
        "products": [
            {"name": "Vanicream Gentle Body Wash", "image": "https://m.media-amazon.com/images/I/31jvsTh9FoL._SY300_SX300_QL70_FMwebp_.jpg", "url": "https://www.amazon.in/Vanicream-Sensitive-Dermatologist-Fragrance-Paraben/dp/B07FKQGN7F?th=1", "description": "Free of dyes, fragrance, masking fragrance, lanolin, parabens."},
            {"name": "Aquaphor Healing Ointment", "image": "https://m.media-amazon.com/images/I/315AWJEXLeL._SY300_SX300_QL70_FMwebp_.jpg", "url": "https://www.amazon.in/Aquaphor-Healing-Ointment-1-75-Tube/dp/B000YMFXX8?th=1", "description": "Occlusive protectant for cracked, dry skin."},
            {"name": "Eucerin Advanced Repair", "image": "https://m.media-amazon.com/images/I/61iSRF5mHfL._SX679_.jpg", "url": "https://www.amazon.in/Eucerin-Advanced-Repair-Creme-Packaging/dp/B01DIXHNUU ", "description": "Contains urea to exfoliate and moisturize."},
            {"name": "Topicort (Desoximetasone)", "image": "https://m.media-amazon.com/images/I/41w-tXU5MjL._SX522_.jpg", "url": "https://www.amazon.in/Emcor-0-25-Tube-15-Cream/dp/B09TKVFJVD", "description": "Prescription strength steroid (example, consult doctor)."},
        ],
        "ingredients": ["Ceramides", "Petrolatum", "Urea", "Glycerin"],
        "remedies": ["Daily 'Soak and Seal' method", "Bleach baths to reduce bacteria", "Avoid wool and synthetic fabrics"],
        "lifestyle": ["Minimize stress", "Keep home dust-free", "Use hypoallergenic laundry detergent"],
        "consult_when": "Widespread rash, signs of bacterial infection (weeping, honey-colored crusts), or significant impact on daily life.",
    },
    "Basal Cell Carcinoma": {
        "severity": "high",
        "description": "Basal Cell Carcinoma (BCC) is the most common skin cancer. It arises from basal cells in the epidermis. It grows slowly and rarely spreads (metastasizes) but can be locally destructive.",
        "symptoms": ["Pearly, waxy bump", "Flesh-colored or pink growth", "Bleeding or scabbing sore that heals and returns", "Flat, scaly, reddish patch", "Black/blue lesion (pigmented BCC)"],
        "causes": ["Long-term UV exposure", "Fair skin", "Radiation therapy", "Arsenic exposure", "Immunosuppression"],
        "image": _WIKI("Basal_cell_carcinoma_(2).jpg"),
        "products": [
            {"name": "La Roche-Posay Anthelios Melt-in Milk", "image": "https://m.media-amazon.com/images/I/41ufC4L5QQL._SY300_SX300_QL70_FMwebp_.jpg", "url": "https://www.amazon.in/Roche-Posay-Anthelios-MeltIn-Sunscreen-Milk/dp/B002CML1VG", "description": "High protection broad-spectrum sunscreen."},
            {"name": "Mederma Advanced Scar Gel", "image": "https://m.media-amazon.com/images/I/51dOq63t0aL._SX522_.jpg", "url": " https://www.amazon.in/Mederma-Advanced-Plus-Scar-Gel/dp/B07R914B96?th=1", "description": "Improves appearance of scars post-surgery."},
            {"name": "UPF 50+ Long Sleeve Shirt", "image": "https://m.media-amazon.com/images/I/81HhvJVqN3L._SY879_.jpg", "url": "https://www.amazon.in/Protection-Clothing-Athletic-Lightweight-Outdoor/dp/B09TWFQVJX", "description": "Essential preventative clothing."},
            {"name": "Vaseline (Post-Biopsy Care)", "image": "https://m.media-amazon.com/images/I/31MgEmlaVqL._SY300_SX300_QL70_FMwebp_.jpg", "url": "https://www.amazon.in/Vaseline-Intensive-Advanced-Repair-Lotion/dp/B00JGQDFQK", "description": "Keep wound moist after biopsy/surgery."},
        ],
        "ingredients": ["Zinc Oxide", "Avobenzone", "Silicone (for scars)"],
        "remedies": ["Mohs Surgery (gold standard for face)", "Excision", "Electrodessication and Curettage (ED&C)", "Topical chemotherapy (5-FU)"],
        "lifestyle": ["Strict sun avoidance", "Wear wide-brimmed hats", "Regular annual dermatological screenings"],
        "consult_when": "Any non-healing sore or new pearly growth that bleeds easily.",
    },
    "Melanocytic Nevi": {
        "severity": "low",
        "description": "Melanocytic Nevi (Common Moles) are benign clusters of melanocytes. While generally harmless, they must be monitored as high numbers of moles increase melanoma risk.",
        "symptoms": ["Uniform color (brown, tan, black)", "Distinct border separating mole from skin", "Oval or round shape", "Usually < 6mm diameter", "Raised or flat"],
        "causes": ["Genetics (family history)", "Sun exposure during childhood", "Light skin tone"],
        "image": _WIKI("Congenitalmelanocyticnevus.jpg"),
        "products": [
            {"name": "Supergoop! Unseen Sunscreen", "image": "https://m.media-amazon.com/images/I/51XLHzgxKZL._SX466_.jpg", "url": " https://www.amazon.com/Supergoop-Unseen-Sunscreen-Invisible-Protection/dp/B0DPNJR3F2?th=1", "description": "Invisible protection for daily use."},
            {"name": "Blue Lizard Mineral Sunscreen", "image": "https://m.media-amazon.com/images/I/31PyLdnzbGL._SY300_SX300_QL70_FMwebp_.jpg", "url": "https://www.amazon.in/Blue-Lizard-Sensitive-Mineral-Sunscreen/dp/B0862PNNLG", "description": "Reef-safe, sensitive skin friendly."},
        ],
        "ingredients": ["Broad Spectrum SPF 30+"],
        "remedies": ["Observation", "Surgical removal (if irritated or suspicious)", "Biopsy of atypical moles"],
        "lifestyle": ["Photograph body moles annually (Mole Mapping)", "Avoid tanning", "Protect skin from sunburns"],
        "consult_when": "A mole changes in size, shape, color, itches, or bleeds (ABCDE rule).",
    },
    "Benign Keratosis-like Lesions": {
        "severity": "low",
        "description": "This category includes Benign Lichenoid Keratosis (BLK) and similar non-cancerous lesions. They often mimic skin cancer but are inflammatory or regressing solar lentigines.",
        "symptoms": ["Pink, red, or brown scaly patch", "Solitary lesion", "Mild itching or stinging", "Usually on sun-exposed areas (chest, arms)"],
        "causes": ["Regression of sun spots (solar lentigo)", "Chronic sun exposure", "Inflammatory response"],
        "image": _WIKI("Seborrheic_keratosis_on_human_back.jpg"),
        "products": [
            {"name": "Amlactin Daily Moisturizing Lotion", "image": "https://m.media-amazon.com/images/I/61ubTRkWkmL._AC_UF894,1000_QL80_.jpg"  , "url": "https://www.amazon.in/AmLactin-Moisturizing-Alpha-Hydroxy-Exfoliates-Paraben-Free/dp/B07BRQC5XZ     ", "description": "12% Lactic Acid to gently exfoliate rough patches."},
            {"name": "Gold Bond Rough & Bumpy", "image": "https://images-cdn.ubuy.co.in/637130a14d58885ed2727d33-gold-bond-rough-amp-bumpy-daily.jpg ", "url": " https://www.ubuy.co.in/product/NFVXME8J6-gold-bond-ultimate-rough-bumpy-daily-skin-therapy-8-ounce-helps-exfoliate-and-moisturize-to-smooth-soften-and-reduce-the-appearance-and-feel-of?srsltid=AfmBOooCOpJ5PxSGiyoi0ijToA9WTNRYbygv0FQKycalbe5kjI2pMXmR ", "description": "Triple action formula with AHA, BHA, and PHA."},
            {"name": "CeraVe SA Cream", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSTKSEcDyPPMTAyRsYv5Kawld8_YgqHGXZjNQ&s" , "url": " https://www.clinikally.com/products/cerave-sa-smoothing-cream-for-dry-rough-bumpy-skin?srsltid=AfmBOorTUhrGrmz8UH4vIzrTDutBOx_Hf0ynY0TV6y4y9sqUSVGh4SBN", "description": "Salicylic acid cream for rough, bumpy skin."},
        ],
        "ingredients": ["Lactic Acid", "Salicylic Acid", "Urea"],
        "remedies": ["Time (often resolve on their own)", "Liquid Nitrogen (Cryotherapy)", "Topical Steroids (for itch)"],
        "lifestyle": ["Sun protection to prevent new lesions", "Moisturize regularly"],
        "consult_when": "Lesion is painful, bleeding, or diagnosis is uncertain (biopsy needed).",
    },
    "Psoriasis": {
        "severity": "moderate",
        "description": "Psoriasis is an immune-mediated disease causing rapid buildup of skin cells. This results in scaling on the skin's surface. Plaque psoriasis is the most common form.",
        "symptoms": ["Red patches covered with thick, silvery scales", "Dry, cracked skin that may bleed", "Itching, burning, or soreness", "Thickened, pitted, or ridged nails", "Swollen and stiff joints"],
        "causes": ["Immune system overactivity (T-cells)", "Genetics", "Triggers: Stress, Strep throat, Cold weather, Skin injury (Koebner phenomenon)"],
        "image": _WIKI("Psoriasis_on_back.jpg"),
        "products": [
            {"name": "MG217 Psoriasis Ointment", "image": "https://th.bing.com/th/id/OIP.Z1gz1x1kXXR8vL9qZIPwAAHaHa?w=182&h=182&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3", "url": "https://www.citymarket.com/p/mg217-psoriasis-2-coal-tar-extra-strength-multi-symptom-ointment/0001227750051?srsltid=AfmBOoriSWV59x6pBmyJHr26U6nx1Af_zJKx17JCDzxmTa9PP5hD4mmR", "description": "Coal Tar formula to slow cell growth."},
            {"name": "CeraVe Psoriasis Cleanser", "image": "https://www.cerave.com/-/media/project/loreal/brand-sites/cerave/americas/us/products/psoriasis-cleanser/psoriasis-cleanser_front.jpg?rev=b89b401ba72b442d99a01a0bf0bbdccf ", "url": "https://www.amazon.in/CeraVe-Renewing-Cleanser-Salicylic-Rough/dp/B00U1YCRD8/ref=sr_1_5?crid=1JGMD1NLKEJNL&dib=eyJ2IjoiMSJ9.m2BUQsFq4tBlP5_mquYbppZVGYotlt328IWIp18TKAzYg7S1nkasGowRfVLwDLu-Bxx-Z0A7c5OlBjG9jlFEUYHav3vxpRIpNUBP3QembDbRCi4DC3NX35U_W87Z3ZPEfejOfIcAfGPdKP5xK7JbfhMe-79RGVdsYg46LER_yA3KT2hgL1MG8edQl-XJrn5vdurA_GevUJcO7XlKd6U0XfPhiTzvNi1Ys8r0TJvcdqyuzJMjgpaHSCIhi5AFLw6Y6IzSGePeazxZLbMKOiy48VUyvus7FhlEBxDtxLGyxk4.5zYAbVZjphyuk-sT82gR-qP8Ikfrzh_gIZZjpeRDBFU&dib_tag=se&keywords=CeraVe+Psoriasis+Cleanser&qid=1770649240&sprefix=%2Caps%2C484&sr=8-5", "description": "With Salicylic Acid to remove scales."},
            {"name": "Gold Bond Psoriasis Relief", "image": "https://cdn1.skinsafeproducts.com/photo/5rjpSNbCzPCJpfCSTwD5Ow/large_1473710859.jpeg" , "url": "https://www.amazon.in/Gold-Bond-Ultimate-Healing-Therapy/dp/B000R4FHD4/ref=sr_1_7?crid=2XEFLH24ZWTII&dib=eyJ2IjoiMSJ9.0BwsDluDfZNvhkYqgxcpp2zaRKcDretr7hqIpF0Vpzh0IVK6ySxB-hR3kbPjpxUE5SFLxwgwlklBT9X9e8yNsV34lSAIjxrmiKZfcjJc62KNQBiiJtQL0uRgMr_Wp1zNJNdh-Xdy5YaDodlUCPKoCubi_uIh9Vqqj3cWotNYyf5jEcMdbWNeawm3Qpw2ChIQ.rKeEmTPLCNMHw1cgK-4ubDtVWoNoJ1wR4xWNOLI9BrI&dib_tag=se&keywords=Gold+Bond+Psoriasis+Relief&qid=1770633793&sprefix=%2Caps%2C424&sr=8-7", "description": "Controls recurrence of symptoms."},
            {"name": "Neutrogena T/Gel Shampoo", "image": "https://m.media-amazon.com/images/I/71QJgZkrsQL._AC_UF1000,1000_QL80_.jpg ", "url": "https://www.amazon.in/NEUTROGENA-GEL-THERAPEUTIC-SHAMPOO-250ML/dp/B0785KKY6F", "description": "Therapeutic shampoo for scalp psoriasis."},
        ],
        "ingredients": ["Coal Tar", "Salicylic Acid", "Vitamin D analogues", "Corticosteroids"],
        "remedies": ["Phototherapy (UVB light)", "Systemic biologics (for severe cases)", "Occlusion (wrapping skin after moisturizing)"],
        "lifestyle": ["Reduce stress (yoga, meditation)", "Avoid alcohol and smoking", "Maintain healthy weight"],
        "consult_when": "Joint pain (Psoriatic Arthritis), widespread flare-ups, or significant discomfort.",
    },
    "Seborrheic Keratosis": {
        "severity": "low",
        "description": "Seborrheic Keratosis (SK) is a common non-cancerous skin growth. People tend to get more of them as they get older. They are often described as having a 'stuck-on' waxy appearance.",
        "symptoms": ["Waxy, raised growth", "Brown, black, or light tan", "Round or oval shaped", "Flat or slightly elevated", "'Stuck-on' appearance like a dab of wax"],
        "causes": ["Aging (very common over 50)", "Genetics", "Sun exposure (debated)"],
        "image": _WIKI("Seborrheic_keratosis_(1).jpg"),
        "products": [
            {"name": "Glytone Exfoliating Body Lotion", "image": "https://m.media-amazon.com/images/I/51MDaENVVfL.jpg_BO30,255,255,255_UF750,750_SR1910,1000,0,C_QL100_.jpg " , "url": "https://www.amazon.com/Glytone-Exfoliating-Glycolic-Keratosis-Fragrance-Free/dp/B002D48QRK", "description": "High glycolic acid to smooth raised lesions."},
            {"name": "Urea 40% Gel", "image": "https://www.clinikally.com/cdn/shop/files/UreMF-Urea40_CreamGelNourishing_HydrateHand_FootCreamGel-50g8_2e5bc6c2-3e8e-4f81-b939-b55b9e10eafc.jpg?v=1736329458 ", "url": "https://www.clinikally.com/products/uremf-40-urea-hand-foot-cream-gel?srsltid=AfmBOopKGe_KtQYR_-FhwL4nEK52apn96lY5Hii0AsUNDFEQVk-FeQlv ", "description": "Keratolytic to soften and break down thick skin."},
            {"name": "Ammonium Lactate 12%", "image": "https://m.media-amazon.com/images/I/713v8aZn5ZL.jpg" , "url": "https://www.amazon.in/Ammonium-Lactate-Lotion-12-Fliptop/dp/B000WOS71I", "description": "Softens dry, scaly growths."},
        ],
        "ingredients": ["Ammonium Lactate", "Urea", "Glycolic Acid"],
        "remedies": ["Cryotherapy (Freezing)", "Electrocautery (Burning)", "Curettage (Scraping)", "None (Benign)"],
        "lifestyle": ["Harmless, purely cosmetic concern", "Don't pick or scratch (can cause infection)"],
        "consult_when": "Lesion turns black, bleeds, or is irritated by clothing/jewelry.",
    },
    "Tinea Ringworm Candidiasis": {
        "severity": "moderate",
        "description": "This category covers fungal infections. Tinea Corporis (Ringworm) is a dermatophyte infection. Candidiasis is a yeast infection often in moist skin folds.",
        "symptoms": ["Ring-shaped rash with red, scaly border (Ringworm)", "Clear center in ring", "Intense itching", "Red, macerated skin with satellite lesions (Candida)", "Cracking/peeling skin"],
        "causes": ["Dermatophytes (fungi)", "Candida albicans (yeast)", "Warm, humid environments", "Sweating", "Contact with infected pets/people"],
        "image": _WIKI("Tinea_corporis.jpg"),
        "products": [
            {"name": "Lotrimin Ultra (Butenafine)", "image": "https://www.lotrimin.com/sites/g/files/vrxlpx50606/files/2023-02/1Lotrimin-ultra-jock-itch-cream-front_0.jpg " , "url": "https://www.lotrimin.com/our-products/ultra-jock-itch-cream ", "description": "Strong antifungal for ringworm and jock itch."},
            {"name": "Lamisil AT (Terbinafine)", "image":  "https://5.imimg.com/data5/SELLER/Default/2024/9/452477239/IZ/IN/XV/144712581/terbinafine-hydrochloride-cream-1-w-w-lamisil.jpg ", "url": "https://www.indiamart.com/proddetail/terbinafine-hydrochloride-cream-1-w-w-lamisil-2854579471262.html?srsltid=AfmBOoqrUV2rEVZRwSZfymFF8ea9Q75aYogT5Nj065FiWd2wkWJmy6Ea", "description": "Fungicidal cream/gel for faster cure."},
            {"name": "Nizoral A-D Shampoo", "image": "https://cdn11.bigcommerce.com/s-ilgxsy4t82/images/stencil/1280x1280/products/76795/176208/61kx3sEmJ6L__26067.1662986716.jpg?c=1&imbypass=on"  , "url": "https://kiwla.com/products/Nizoral-AD-Shampoo-1-7oz?srsltid=AfmBOoqagNrjQ0BJjGQgknWxXy35yNu7zgb1CucML0a7oWPeV4gGqZpZ", "description": "Ketoconazole for fungal skin/scalp issues."},
            {"name": "Zeasorb Antifungal Powder", "image": "https://cloudinary.images-iherb.com/image/upload/f_auto,q_auto:eco/images/zea/zea23225/l/49.jpg" , "url": "https://in.iherb.com/pr/zeasorb-zeasorb-af-antifungal-powder-2-5-oz-71-g/137354", "description": "Keeps areas dry and treats infection."},
        ],
        "ingredients": ["Terbinafine", "Clotrimazole", "Miconazole", "Ketoconazole"],
        "remedies": ["Keep skin clean and DRY", "Wash clothes in hot water", "Don't share towels/razors"],
        "lifestyle": ["Wear loose, breathable clothing", "Change socks/underwear daily", "Treat pets if they have bald spots"],
        "consult_when": "Infection on scalp (Tinea Capitis - needs pills), nails (Onychomycosis), or no improvement after 2 weeks.",
    },
    "Warts Molluscum Viral Infections": {
        "severity": "low",
        "description": "Common viral infections. Warts (Verruca vulgaris) are caused by HPV. Molluscum Contagiosum is caused by a poxvirus and presents as pearly papules.",
        "symptoms": ["Rough, grainy bumps (Warts)", "Black pinpoints within bump (clotted vessels)", "Smooth, pearly, dome-shaped bumps with central dimple (Molluscum)", "Painless but can itch"],
        "causes": ["Human Papillomavirus (HPV)", "Molluscum Contagiosum Virus (MCV)", "Direct skin contact", "Sharing towels/gym equipment"],
        "image": _WIKI("Molluscum_Contagiosum.jpg"),
        "products": [
            {"name": "Compound W Gel", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKvAWXPgKhtkdwjeIE0ueLWOphTiRb4Wqs-Q&s" , "url": "https://www.ubuy.co.in/product/3W5A199WS-compound-w-maximum-strength-fast-acting-gel-wart-remover-1-ea?srsltid=AfmBOopdus9F1-mwwv2LkNuR4zU0mvW1Rlyg71RSY6SaTVNCxtW7RMAt ", "description": "High concentration Salicylic Acid to peel warts."},
            {"name": "Dr. Scholl's Freeze Away", "image":  "https://m.media-amazon.com/images/I/71XuFTHQMyL.jpg " , "url": "https://www.amazon.in/Dr-Scholls-Freeze-Remover-Treatments/dp/B0788BWQ8G  ", "description": "At-home cryotherapy kit."},
            {"name": "ZymaDerm for Molluscum", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwLMsfWpqc8Da3NYVsfaC2NUw3XcH6J8GoOw&s", "url": "https://www.ubereats.com/product/b/2a24e591-8727-5671-95d8-0983a9685a91?srsltid=AfmBOoqp-O0s65bYqHbN6Uj0uE40UD24U9ueluyZm0_EjCr6iPUQkVDg", "description": "Natural formula to reduce molluscum bumps."},
            {"name": "Nexcare Waterproof Bandages", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQKmarzZDL1zASOO710ghFNY4I6vAYhwWPaGA&s" , "url": "https://www.firstaidcanada.com/product/nexcare-waterproof-bandages-assorted-sizes-30-box/", "description": "Cover lesions to prevent spread."},
        ],
        "ingredients": ["Salicylic Acid", "Cantharidin (Doctor only)", "Tea Tree Oil"],
        "remedies": ["Duct Tape Occlusion Method", "Cryotherapy (Doctor)", "Wait and watch (Molluscum often clears in 6-12 months)"],
        "lifestyle": ["DO NOT scratch or pick (spreads virus)", "Wear flip-flops in public showers", "Wash hands frequently"],
        "consult_when": "Warts on face/genitals, painful, bleeding, or rapidly spreading.",
    },
    "Irrelevant/Unknown": {
        "severity": "low",
        "description": "The uploaded image does not appear to match any of the 10 skin disease categories the model was trained on, or the image quality is too low for a confident prediction.",
        "symptoms": ["N/A"],
        "causes": ["Irrelevant image (not skin)", "Blurry or poorly lit photo", "Condition outside of trained classes"],
        "image": _PIC("unknown"),
        "products": [],
        "ingredients": [],
        "remedies": ["Ensure the photo is clear and well-lit", "Focus specifically on the affected skin area", "Consult a dermatologist for any concerning skin changes"],
        "lifestyle": ["Regular skin self-examinations"],
        "consult_when": "If you have a persistent skin concern that was not identified here.",
    },
}

# Fallback image for products without specific image
DEFAULT_PRODUCT_IMG = _PIC("product")
DEFAULT_DISEASE_IMG = _PIC("disease")


def get_recommendation(disease_name: str) -> dict:
    """Get recommendations for a disease. Returns default if not found."""
    for key, val in RECOMMENDATIONS.items():
        if key.lower() in disease_name.lower() or disease_name.lower() in key.lower():
            out = val.copy()
            # Ensure products have image/url fallback
            if "products" in out and out["products"]:
                for p in out["products"]:
                    if isinstance(p, dict):
                        if "image" not in p:
                            p["image"] = DEFAULT_PRODUCT_IMG
                        if "url" not in p:
                            p["url"] = "#"
            return out
    return {
        "severity": "unknown",
        "description": "General skin concern. Consult a dermatologist for accurate diagnosis.",
        "symptoms": [],
        "causes": [],
        "image": DEFAULT_DISEASE_IMG,
        "products": [{"name": "General moisturizer", "image": DEFAULT_PRODUCT_IMG, "url": "#", "description": "Keep skin hydrated"}, {"name": "SPF 30+ Sunscreen", "image": DEFAULT_PRODUCT_IMG, "url": "#", "description": "Protect from UV damage"}],
        "ingredients": ["Consult product labels"],
        "remedies": ["Keep skin clean and moisturized"],
        "lifestyle": ["Sun protection", "Healthy diet"],
        "consult_when": "If symptoms persist or worsen",
    }