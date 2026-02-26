import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

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

# --- 2. MULTI-FACTORY MATH ENGINES ---

def get_metal_loss(factory, purity_string):
    """Calculates metal loss multiplier based on Factory and Purity"""
    p = str(purity_string).lower()
    if factory == "Jewel One":
        return 1.10
    else: # Creations
        if 'plat' in p or 'pt' in p:
            return 1.10 # 10% for Plat
        return 1.08 # 8% for Gold

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

def get_assembly_cost(factory, item_type, ring_type):
    """Calculates Assembly + Rhodium combined"""
    it = str(item_type).lower()
    if factory == "Jewel One":
        if 'ring' in it: return 7.00
        if 'earring' in it: return 9.50
        if 'pendant' in it: return 7.00
        if 'necklace' in it: return 105.00
        if 'bracelet' in it: return 53.00
        if '2 pc' in it: return 11.00
        return 0.00
    else: # Creations
        if 'necklace' in it: return 100.00 # $80 CFP + $20 Rhod
        if 'bracelet' in it: return 40.00 # $30 CFP + $10 Rhod
        if 'earring' in it or 'pendant' in it or '2 pc' in it: return 16.00 # Bands cost fallback
        if 'ring' in it:
            rt = str(ring_type).lower()
            if 'band' in rt: return 16.00 # $12 CFP + $4 Rhod
            if 'bridal' in rt: return 19.00 # $15 CFP + $4 Rhod
            if 'eternity' in rt: return 22.00 # $18 CFP + $4 Rhod
            return 22.00 # Max fee fallback
        return 16.00

def get_setting_cost(factory, total_carats, total_stones, style, shape, purity_string):
    if int(total_stones) == 0: return 0.00
    individual_wt = float(total_carats) / int(total_stones)
    style = str(style).lower()
    shape = str(shape).lower()
    is_plat = 'plat' in str(purity_string).lower() or 'pt' in str(purity_string).lower()

    if factory == "Jewel One":
        if 'micro' in style: return 0.35
        if 0 <= individual_wt <= 0.95: return 1.00
        elif 0.96 <= individual_wt <= 2.99: return 2.00
        elif 3.00 <= individual_wt <= 4.99: return 3.00
        elif 5.00 <= individual_wt <= 9.99: return 5.00
        elif individual_wt >= 10.00: return 8.00
        return 0.00
    else: # Creations
        micro_rate = 0.50 if is_plat else 0.35
        round_1_2_rate = 3.00 if is_plat else 2.00
        fancy_or_large_rate = 6.00 if is_plat else 5.00
        claw_extra = 2.00 if 'claw' in style else 0.00

        if 'micro' in style:
            base = micro_rate
        elif 'round' in shape:
            if individual_wt < 1.00:
                base = micro_rate
            elif 1.00 <= individual_wt <= 2.00:
                base = round_1_2_rate
            else:
                base = fancy_or_large_rate
        else: # Fancy Shapes
            base = fancy_or_large_rate
        
        return base + claw_extra

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
        if val <= individual_wt: best_key = k_str
        else: break
            
    return shape_dict[best_key][quality_index]

# --- 3. THE STREAMLIT APP UI ---
st.set_page_config(page_title="Kira Jewels AI Quoter", page_icon="💎", layout="wide")
st.title("💎 Kira Jewels AI Quoting Bot")
st.write("Upload a CAD technical drawing, and the AI will extract the details and generate a B2B quote and Tag Price.")

with st.sidebar:
    st.header("⚙️ Settings")
    
    # NEW: Factory Selection Dropdown
    selected_factory = st.selectbox("Select Factory", ["Jewel One", "Creations"])
    st.divider()
    
    gold_fix_oz = st.number_input("Live Gold Fix ($/oz)", min_value=0.0, value=2030.00)
    
    quality_mapping = {"F+VVS+": 0, "F+VS+": 1, "G+VS+": 2}
    selected_quality = st.selectbox("Select Diamond Quality", options=list(quality_mapping.keys()), index=2)
    quality_index = quality_mapping[selected_quality]

uploaded_file = st.file_uploader("Upload CAD Drawing (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded CAD", use_container_width=True)
    
    if st.button("Extract & Quote with AI", type="primary"):
        with st.spinner(f"AI is analyzing the CAD for {selected_factory}..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-3-flash-preview')
                
                # UPDATED PROMPT: Asks to categorize the ring type for Creations logic
                prompt = """
                Analyze this jewelry CAD technical drawing. Extract the following details and return ONLY a raw JSON object with these exact keys. Do not include markdown formatting.
                {
                    "item_type": "Determine if it is a Ring, Earring, Pendant, Necklace, Bracelet, or 2 PC",
                    "ring_type": "If item_type is Ring, classify as 'Band', 'Bridal', 'Eternity', or 'Unknown'. If not a ring, output 'N/A'",
                    "metal_purity": "Extract metal purity (e.g., '14K', '18K', 'PLAT')",
                    "metal_net_wt_g": <float of the Net WT in grams>,
                    "setting_style": "<string of the setting style (e.g. BAZZEL, micro prong, claw prong)>",
                    "stones": [
                        {
                            "shape": "Determine the shape (e.g. Round, Oval, Emerald, Pear, etc.)",
                            "qty": <integer of total stones for this specific shape>,
                            "carat_weight": <float of the total carat weight for this specific shape>
                        }
                    ]
                }
                """
                
                response = model.generate_content([prompt, image])
                raw_json = response.text.strip().replace("```json", "").replace("```", "")
                cad_data = json.loads(raw_json)
                
                st.success("CAD Data Successfully Extracted!")
                
                # Setup Display Variables
                metal_purity = cad_data.get('metal_purity', '14K')
                ring_type = cad_data.get('ring_type', 'Unknown')
                loss_multiplier = get_metal_loss(selected_factory, metal_purity)
                loss_percentage = int(round((loss_multiplier - 1.0) * 100))
                
                # Display Top-Level Details
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Item Type:** {cad_data['item_type']} ({ring_type})")
                    st.write(f"**Metal Specs:** {metal_purity} | {cad_data.get('metal_net_wt_g', 0)} g")
                with col2:
                    st.write(f"**Factory Pricing:** {selected_factory}")
                    st.write(f"**Setting Style:** {cad_data.get('setting_style', 'Standard')}")

                # CALCULATE COSTS
                calculated_gram_price = get_gold_price_per_gram(gold_fix_oz, metal_purity)
                metal_cost = (float(cad_data.get('metal_net_wt_g', 0)) * loss_multiplier) * calculated_gram_price
                assembly_cost = get_assembly_cost(selected_factory, cad_data['item_type'], ring_type)
                
                total_setting_cost = 0
                total_diamond_cost = 0
                total_stone_count = 0
                stone_breakdowns = []
                
                st.write("---")
                st.write("### 💎 Stone Breakdown")
                
                for stone in cad_data.get('stones', []):
                    shape = stone['shape']
                    qty = int(stone['qty'])
                    carats = float(stone['carat_weight'])
                    
                    if qty > 0 and carats > 0:
                        total_stone_count += qty
                        
                        group_setting_cost = qty * get_setting_cost(selected_factory, carats, qty, cad_data.get('setting_style', ''), shape, metal_purity)
                        total_setting_cost += group_setting_cost
                        
                        price_per_carat = get_diamond_price(shape, carats, qty, quality_index)
                        group_diamond_cost = carats * price_per_carat
                        total_diamond_cost += group_diamond_cost
                        
                        st.write(f"- **{shape}**: {qty} stones | {carats} ct total | (${price_per_carat}/ct)")
                        stone_breakdowns.append(f"{shape} ({qty} stones): ${group_diamond_cost:,.2f} + ${group_setting_cost:,.2f} setting")

                # Final Math
                final_cost = metal_cost + assembly_cost + total_setting_cost + total_diamond_cost
                tag_price = (final_cost * 1.13) * 1.8
                
                st.divider()
                st.header(f"💰 Final B2B Cost ({selected_factory}): **${final_cost:,.2f}**")
                st.success(f"🏷️ **Suggested Tag Price:** **${tag_price:,.2f}**")
                
                with st.expander("View Detailed Cost Breakdown"):
                    st.write(f"- **Billed Metal Cost** ({metal_purity} at ${calculated_gram_price:,.2f}/g + {loss_percentage}% loss): ${metal_cost:,.2f}")
                    st.write(f"- **Assembly & Rhodium**: ${assembly_cost:,.2f}")
                    st.write(f"- **Total Setting Labor** ({total_stone_count} total stones): ${total_setting_cost:,.2f}")
                    st.write(f"- **Total Diamond Cost** ({selected_quality}): ${total_diamond_cost:,.2f}")
                    st.write("--- *Stone Group Breakdown* ---")
                    for breakdown in stone_breakdowns:
                        st.write(f"  - {breakdown}")
                    
            except Exception as e:
                st.error(f"An error occurred during extraction. Details: {e}")
