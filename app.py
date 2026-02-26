import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# ==========================================
# 🛑 PASTE YOUR API KEY BETWEEN THE QUOTES
# ==========================================
MY_GEMINI_API_KEY = "AIzaSyDjzeZXkqXx_4Qa2CgxX_ohLVH0x40Zzxk"

# --- 1. THE DIAMOND PRICING MATRIX ---
DIAMOND_PRICING = {
    "round": {"0":[195,145,145], "0.007":[180,130,130], "0.009":[125,75,75], "0.021":[90,40,40], "0.074":[90,40,40], "0.091":[90,40,40], "0.12":[90,40,40], "0.14":[90,40,40], "0.18":[95,45,45], "0.23":[110,60,60], "0.3":[110,60,60], "0.38":[110,60,60], "0.46":[116,66,66], "0.58":[116,66,66], "0.7":[116,66,66], "0.8":[116,66,66], "0.9":[116,66,66], "0.96":[165,115,105], "1.16":[165,115,105], "1.46":[175,125,110], "1.66":[175,125,110], "1.96":[185,135,120], "2.16":[185,135,120], "2.46":[185,135,120], "2.61":[185,135,120], "2.96":[190,140,120], "3.16":[190,140,120], "3.96":[190,140,120], "4.96":[200,150,130], "5.96":[215,165,140], "6.96":[225,175,150], "7.96":[250,200,170], "8.96":[250,200,170]},
    "oval": {"0":[137,87,87], "0.09":[137,87,87], "0.12":[137,87,87], "0.14":[137,87,87], "0.18":[130,82,82], "0.23":[130,82,82], "0.3":[130,82,82], "0.38":[130,82,82], "0.46":[130,82,82], "0.58":[130,82,82], "0.7":[130,82,82], "0.8":[130,82,82], "0.9":[130,82,82], "0.96":[160,105,100], "1.16":[160,105,100], "1.46":[165,110,105], "1.66":[165,110,105], "1.96":[175,125,110], "2.16":[175,125,110], "2.46":[175,125,110], "2.61":[175,125,110], "2.96":[190,130,120], "3.16":[190,130,120], "3.96":[190,135,120], "4.96":[190,130,115], "5.96":[250,145,125], "6.96":[275,150,130], "7.96":[300,175,145], "8.96":[350,200,170]},
    "pear": {"0":[137,87,87], "0.09":[137,87,87], "0.12":[137,87,87], "0.14":[137,87,87], "0.18":[132,82,82], "0.23":[132,82,82], "0.3":[132,82,82], "0.38":[132,82,82], "0.46":[132,82,82], "0.58":[132,82,82], "0.7":[132,82,82], "0.8":[132,82,82], "0.9":[132,82,82], "0.96":[145,95,85], "1.16":[145,95,85], "1.46":[155,105,95], "1.66":[155,105,95], "1.96":[165,115,105], "2.16":[165,115,105], "2.46":[165,115,105], "2.61":[165,115,105], "2.96":[180,130,110], "3.16":[180,130,110], "3.96":[180,130,110], "4.96":[180,130,110], "5.96":[185,135,120], "6.96":[200,150,130], "7.96":[225,175,145], "8.96":[250,200,170]},
    "emerald": {"0":[137,87,87], "0.09":[137,87,87], "0.12":[137,87,87], "0.14":[137,87,87], "0.18":[132,82,82], "0.23":[132,82,82], "0.3":[132,82,82], "0.38":[132,82,82], "0.46":[132,82,82], "0.58":[132,82,82], "0.7":[132,82,82], "0.8":[132,82,82], "0.9":[132,82,82], "0.96":[145,95,87], "1.16":[145,95,87], "1.46":[145,95,87], "1.66":[145,95,87], "1.96":[145,95,87], "2.16":[145,95,87], "2.46":[145,95,87], "2.61":[145,95,87], "2.96":[160,110,95], "3.16":[160,110,95], "3.96":[160,110,95], "4.96":[165,115,100], "5.96":[175,125,110], "6.96":[185,135,110], "7.96":[200,150,120], "8.96":[220,170,140]},
    "marquise": {"0":[137,87,87], "0.09":[137,87,87], "0.12":[137,87,87], "0.14":[137,87,87], "0.18":[132,82,82], "0.23":[132,82,82], "0.3":[132,82,82], "0.38":[132,82,82], "0.46":[132,82,82], "0.58":[132,82,82], "0.7":[132,82,82], "0.8":[132,82,82], "0.9":[132,82,82], "0.96":[145,95,85], "1.16":[145,95,85], "1.46":[150,100,90], "1.66":[150,100,90], "1.96":[160,110,100], "2.16":[160,110,100], "2.46":[160,110,100], "2.61":[160,110,100], "2.96":[180,130,115], "3.16":[180,130,115], "3.96":[190,140,115], "4.96":[190,140,115], "5.96":[200,150,120], "6.96":[200,150,130], "7.96":[225,175,145], "8.96":[250,200,170]},
    "radiant": {"0":[137,87,87], "0.09":[137,87,87], "0.12":[137,87,87], "0.14":[137,87,87], "0.18":[132,82,82], "0.23":[132,82,82], "0.3":[132,82,82], "0.38":[132,82,82], "0.46":[132,82,82], "0.58":[132,82,82], "0.7":[132,82,82], "0.8":[132,82,82], "0.9":[132,82,82], "0.96":[145,95,85], "1.16":[145,95,85], "1.46":[150,100,85], "1.66":[150,100,85], "1.96":[150,100,90], "2.16":[150,100,90], "2.46":[150,100,90], "2.61":[150,100,90], "2.96":[175,125,110], "3.16":[175,125,110], "3.96":[175,125,110], "4.96":[180,130,115], "5.96":[190,140,110], "6.96":[200,150,120], "7.96":[225,175,145], "8.96":[250,200,170]},
    "cushion_e": {"0":[137,87,87], "0.09":[137,87,87], "0.12":[137,87,87], "0.14":[137,87,87], "0.18":[132,82,82], "0.23":[132,82,82], "0.3":[132,82,82], "0.38":[132,82,82], "0.46":[132,82,82], "0.58":[132,82,82], "0.7":[132,82,82], "0.8":[132,82,82], "0.9":[132,82,82], "0.96":[150,100,87], "1.16":[150,100,87], "1.46":[150,100,87], "1.66":[150,100,87], "1.96":[160,110,90], "2.16":[160,110,90], "2.46":[160,110,90], "2.61":[160,110,90], "2.96":[180,130,110], "3.16":[180,130,110], "3.96":[185,135,115], "4.96":[185,135,115], "5.96":[200,150,120], "6.96":[225,175,150], "7.96":[250,200,170], "8.96":[250,200,170]},
    "princess": {"0":[137,87,87], "0.09":[137,87,87], "0.12":[137,87,87], "0.14":[137,87,87], "0.18":[132,82,82], "0.23":[132,82,82], "0.3":[132,82,82], "0.38":[132,82,82], "0.46":[132,82,82], "0.58":[132,82,82], "0.7":[132,82,82], "0.8":[132,82,82], "0.9":[132,82,82], "0.96":[165,115,105], "1.16":[165,115,105], "1.46":[165,115,105], "1.66":[165,115,105], "1.96":[180,130,110], "2.16":[180,130,110], "2.46":[180,130,110], "2.61":[180,130,110], "2.96":[190,140,115], "3.16":[190,140,115], "3.96":[190,140,115], "4.96":[195,145,120], "5.96":[200,150,125], "6.96":[225,175,150], "7.96":[250,200,170], "8.96":[250,200,170]},
    "heart": {"0":[137,87,87], "0.09":[137,87,87], "0.12":[137,87,87], "0.14":[137,87,87], "0.18":[132,82,82], "0.23":[132,82,82], "0.3":[132,82,82], "0.38":[132,82,82], "0.46":[132,82,82], "0.58":[132,82,82], "0.7":[132,82,82], "0.8":[132,82,82], "0.9":[132,82,82], "0.96":[170,120,110], "1.16":[170,120,110], "1.46":[175,125,115], "1.66":[175,125,115], "1.96":[190,140,120], "2.16":[190,140,120], "2.46":[190,140,120], "2.61":[190,140,120], "2.96":[205,155,130], "3.16":[205,155,130], "3.96":[215,165,140], "4.96":[225,175,140], "5.96":[230,180,150], "6.96":[250,200,160], "7.96":[270,220,175], "8.96":[290,240,185]},
    "asscher": {"0":[137,87,87], "0.09":[137,87,87], "0.12":[137,87,87], "0.14":[137,87,87], "0.18":[132,82,82], "0.23":[132,82,82], "0.3":[132,82,82], "0.38":[132,82,82], "0.46":[132,82,82], "0.58":[132,82,82], "0.7":[132,82,82], "0.8":[132,82,82], "0.9":[132,82,82], "0.96":[160,110,95], "1.16":[160,110,95], "1.46":[160,110,100], "1.66":[160,110,100], "1.96":[170,120,105], "2.16":[170,120,105], "2.46":[170,120,105], "2.61":[170,120,105], "2.96":[180,130,110], "3.16":[180,130,110], "3.96":[180,130,110], "4.96":[185,135,120], "5.96":[200,150,130], "6.96":[225,175,150], "7.96":[250,200,170], "8.96":[250,200,170]}
}

# --- 2. THE MATH ENGINES ---
def get_gold_price_per_gram(gold_fix_oz, purity_string):
    pure_price_per_gram = gold_fix_oz / 31.1035
    purity_string = str(purity_string).upper().replace(" ", "")
    
    if '10K' in purity_string: multiplier = 10 / 24
    elif '14K' in purity_string: multiplier = 14 / 24
    elif '18K' in purity_string: multiplier = 18 / 24
    elif '22K' in purity_string: multiplier = 22 / 24
    elif '24K' in purity_string: multiplier = 24 / 24
    else: multiplier = 14 / 24
        
    return pure_price_per_gram * multiplier

def get_rhod_and_assembly(item_type):
    costs = {'ring': 7.00, 'earring': 9.50, 'pendant': 7.00, 'necklace': 105.00, 'bracelet': 53.00, '2 pc': 11.00}
    for key in costs:
        if key in str(item_type).lower():
            return costs[key]
    return 0.00

def get_setting_cost(total_carats, total_stones, style):
    if 'micro' in str(style).lower(): return 0.35
    if int(total_stones) == 0: return 0.00
    
    individual_wt = float(total_carats) / int(total_stones)
    if 0 <= individual_wt <= 0.95: return 1.00
    elif 0.96 <= individual_wt <= 2.99: return 2.00
    elif 3.00 <= individual_wt <= 4.99: return 3.00
    elif 5.00 <= individual_wt <= 9.99: return 5.00
    elif individual_wt >= 10.00: return 8.00
    return 0.00

def get_diamond_price(shape, total_carats, total_stones, quality_index):
    shape = str(shape).lower().replace(" ", "_")
    if "cushion" in shape: shape = "cushion_e"
    if shape not in DIAMOND_PRICING: shape = "round"
    
    if int(total_stones) == 0: return 0.00
    individual_wt = float(total_carats) / int(total_stones)
    
    shape_dict = DIAMOND_PRICING[shape]
    sorted_brackets = sorted([(float(k), k) for k in shape_dict.keys()])
    
    best_key = sorted_brackets[0][1] 
    for val, k_str in sorted_brackets:
        if val <= individual_wt:
            best_key = k_str
        else:
            break
            
    return shape_dict[best_key][quality_index]

# --- 3. THE STREAMLIT APP UI ---
st.set_page_config(page_title="Kira Jewels AI Quoter", page_icon="💎", layout="wide")
st.title("💎 Kira Jewels AI Quoting Bot")
st.write("Upload a CAD technical drawing, and the AI will extract the details and generate a B2B quote and Tag Price.")

with st.sidebar:
    st.header("⚙️ Settings")
    gold_fix_oz = st.number_input("Live Gold Fix ($/oz)", min_value=0.0, value=2030.00)
    
    quality_mapping = {"F+VVS+": 0, "F+VS+": 1, "G+VS+": 2}
    selected_quality = st.selectbox("Select Diamond Quality", options=list(quality_mapping.keys()), index=2)
    quality_index = quality_mapping[selected_quality]

uploaded_file = st.file_uploader("Upload CAD Drawing (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded CAD", use_container_width=True)
    
    if st.button("Extract & Quote with AI", type="primary"):
        with st.spinner("AI is analyzing the CAD..."):
            try:
                genai.configure(api_key=MY_GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-3-flash-preview')
                
                prompt = """
                Analyze this jewelry CAD technical drawing. Extract the following details and return ONLY a raw JSON object with these exact keys. Do not include markdown formatting.
                {
                    "item_type": "Determine if it is a Ring, Earring, Pendant, Necklace, Bracelet, or 2 PC",
                    "metal_purity": "Extract metal purity (e.g., '14K', '18K')",
                    "metal_net_wt_g": <float of the Net WT in grams>,
                    "total_stone_qty": <integer of total stones/QTY>,
                    "stone_shape": "Determine the shape (e.g. Round, Oval, Emerald, Pear, etc.)",
                    "total_carat_weight": <float of the Total Weight/T.WT>,
                    "setting_style": "<string of the setting style (e.g. BAZZEL, micro prong)>"
                }
                """
                
                response = model.generate_content([prompt, image])
                raw_json = response.text.strip().replace("```json", "").replace("```", "")
                cad_data = json.loads(raw_json)
                
                st.success("CAD Data Successfully Extracted!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Item Type:** {cad_data['item_type']}")
                    st.write(f"**Metal Specs:** {cad_data['metal_purity']} | {cad_data['metal_net_wt_g']} g")
                    st.write(f"**Setting Style:** {cad_data['setting_style']}")
                with col2:
                    st.write(f"**Stone Shape:** {cad_data['stone_shape']}")
                    st.write(f"**Stone Quantity:** {cad_data['total_stone_qty']}")
                    st.write(f"**Total Carat Weight:** {cad_data['total_carat_weight']} ct")

                # CALCULATE COSTS
                calculated_gram_price = get_gold_price_per_gram(gold_fix_oz, cad_data['metal_purity'])
                metal_cost = (float(cad_data['metal_net_wt_g']) * 1.10) * calculated_gram_price
                
                assembly_cost = get_rhod_and_assembly(cad_data['item_type'])
                setting_cost = int(cad_data['total_stone_qty']) * get_setting_cost(cad_data['total_carat_weight'], cad_data['total_stone_qty'], cad_data['setting_style'])
                
                price_per_carat = get_diamond_price(cad_data['stone_shape'], cad_data['total_carat_weight'], cad_data['total_stone_qty'], quality_index)
                diamond_cost = float(cad_data['total_carat_weight']) * price_per_carat
                
                final_cost = metal_cost + assembly_cost + setting_cost + diamond_cost
                
                # TAG PRICE MATH: (Cost + 13%) * 1.8
                tag_price = (final_cost * 1.13) * 1.8
                
                st.divider()
                st.header(f"💰 Final B2B Cost: **${final_cost:,.2f}**")
                st.success(f"🏷️ **Suggested Tag Price:** **${tag_price:,.2f}**")
                
                with st.expander("View Cost Breakdown"):
                    st.write(f"- Billed Metal Cost ({cad_data['metal_purity']} at ${calculated_gram_price:,.2f}/g + 10% loss): ${metal_cost:,.2f}")
                    st.write(f"- Assembly & Rhodium: ${assembly_cost:,.2f}")
                    st.write(f"- Setting Labor ({cad_data['total_stone_qty']} stones): ${setting_cost:,.2f}")
                    st.write(f"- Diamonds ({selected_quality} at ${price_per_carat}/ct): ${diamond_cost:,.2f}")
                    
            except Exception as e:
                st.error(f"An error occurred during extraction. Check your API key. Details: {e}")