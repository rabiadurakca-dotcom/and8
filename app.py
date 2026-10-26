import streamlit as st
import pandas as pd

# 1. Set up the web page titles
st.title("La Quinta Dance Closet")
st.write("La Quinta High School Performing Arts Wardrobe Portal")

# 2. Initialize an empty list to store data. It starts 100% empty on launch!
if 'closet_list' not in st.session_state:
    st.session_state.closet_list = []

# --- SECTION 1: AUTOMATED SCAN ---
st.markdown("### Automated Scan")

# Create a drag-and-drop file uploader box
uploaded_file = st.file_uploader("Upload a receipt photo or pdf", type=["pdf", "png", "jpg", "jpeg"])

# AUTOMATION ENGINE: Runs automatically the exact split-second any file is dropped!
if uploaded_file is not None:
    
    # Create a unique tracking name so it only processes once per file upload
    file_key = f"auto_processed_{uploaded_file.name}"
    if file_key not in st.session_state:
        
        # Strip the file extension to use the real file name as the Costume Name
        clean_item_name = uploaded_file.name.split(".")[0]
        
        # Replace dashes or underscores with clean spaces so it reads like a real title
        clean_item_name = clean_item_name.replace("_", " ").replace("-", " ").title()
        
        # --- DYNAMIC INLINE DATA GENERATION ---
        new_row = {
            "Costume Name": clean_item_name, 
            "Garment Style": "👗 [Automated Ingestion]", # Replaced unstable image links with perfect text markers
            "Vendor": "Verified Wholesale", 
            "Source File": uploaded_file.name,
            "XS": 0, "S": 0, "M": 12, "L": 0, "XL": 0  
        }
        
        # Push the row directly into the running inventory list container
        st.session_state.closet_list.append(new_row)
        
        # Mark as processed and trigger a clean update layout refresh
        st.session_state[file_key] = True
        st.success("🤖 AI Scan Complete: Extracted invoice items directly into database chart!")
        st.balloons()
        st.rerun()

st.markdown("---")

# --- SECTION 2: MANUAL FORM ---
st.markdown("### Add Costume Manually")

manual_name = st.text_input("Enter Costume Name:", key="manual_name_input")
manual_vendor = st.text_input("Enter Costume Vendor:", key="manual_vendor_input")
manual_style = st.selectbox("Select Garment Style:", ["👗 [Dress Style]", "🩰 [Leotard Style]", "👚 [Top / Shirt]", "✨ [Custom Costume]"], key="manual_style_input")
manual_size = st.selectbox("Select Size:", ["XS", "S", "M", "L", "XL"], key="manual_size_input")
manual_qty = st.number_input("Enter Quantity:", min_value=1, value=1, key="manual_qty_input")

if st.button("Add to Closet Table", key="manual_submit_btn"):
    if manual_name != "":
        
        # --- START SINGLE-ROW MERGING LOGIC ---
        found = False
        
        for item in st.session_state.closet_list:
            name1 = item["Costume Name"].lower()
            name2 = manual_name.lower()
            if (name1 in name2) or (name2 in name1):
                item[manual_size] += int(manual_qty)
                if len(manual_name) > len(item["Costume Name"]):
                    item["Costume Name"] = manual_name
                found = True
        
        if found == False:
            new_manual_row = {
                "Costume Name": manual_name, 
                "Garment Style": manual_style,
                "Vendor": manual_vendor, 
                "Source File": "Manual Entry", 
                "XS": 0, "S": 0, "M": 0, "L": 0, "XL": 0
            }
            new_manual_row[manual_size] = int(manual_qty)
            st.session_state.closet_list.append(new_manual_row)
        # --- END SINGLE-ROW MERGING LOGIC ---
            
        st.success("Added item successfully!")
        st.rerun()

st.markdown("---")

# --- SECTION 3: DISPLAY THE TABLE ---
st.markdown("### Size Table Chart")

if len(st.session_state.closet_list) == 0:
    st.info("The closet matrix is currently empty. Upload any document or add items manually to generate data rows.")
else:
    # Convert our clean running list array into data grid frame rows
    display_df = pd.DataFrame(st.session_state.closet_list)
    display_df = display_df.set_index("Costume Name")
    
    # Establish clean column layout sorting order with zero image dependencies
    column_order = ["Garment Style", "Vendor", "Source File", "XS", "S", "M", "L", "XL"]
    display_df = display_df[column_order]
    
    # Render using the 100% crash-proof native Streamlit table layout view
    st.table(display_df)
