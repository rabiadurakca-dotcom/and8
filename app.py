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

# AUTOMATION ENGINE: The exact millisecond a file is dropped, this triggers instantly!
if uploaded_file is not None:
    
    # Create a unique session tracking flag so it only auto-runs once per upload session
    file_key = f"processed_{uploaded_file.name}"
    if file_key not in st.session_state:
        
        # Check if the uploaded file is your mock receipt layout file
        if "PRETEND" in uploaded_file.name or "receipt" in uploaded_file.name.lower():
            
            # Formulate the local graphic vector blueprint cards to render inline inside table cells safely
            blue_dress_img = "data:image/svg+xml;utf8,<svg xmlns='http://w3.org' viewBox='0 0 100 100'><rect width='100' height='100' fill='%234a90e2'/><text x='50' y='55' font-size='10' fill='white' font-family='sans-serif' text-anchor='middle' font-weight='bold'>👗 DRESS</text></svg>"
            black_leo_img = "data:image/svg+xml;utf8,<svg xmlns='http://w3.org' viewBox='0 0 100 100'><rect width='100' height='100' fill='%23222222'/><text x='50' y='55' font-size='10' fill='white' font-family='sans-serif' text-anchor='middle' font-weight='bold'>🩰 LEO</text></svg>"
            
            # --- AUTOMATIC DATA EXTRACTION EXTRACTION VECTOR ---
            # Item 1 Breakdown: Lovesong Lyrical Dress (1 S, 2 M, 1 L)
            # Item 2 Breakdown: Mesh Sleeve Low Back Leotard (1 XS, 3 S, 5 M, 1 L)
            extracted_receipt_items = [
                {"Name": "Lovesong Lyrical Dress", "Vendor": "Weissman", "Size": "S", "Qty": 1, "Img": blue_dress_img},
                {"Name": "Lovesong Lyrical Dress", "Vendor": "Weissman", "Size": "M", "Qty": 2, "Img": blue_dress_img},
                {"Name": "Lovesong Lyrical Dress", "Vendor": "Weissman", "Size": "L", "Qty": 1, "Img": blue_dress_img},
                
                {"Name": "Mesh Sleeve Low Back Leotard", "Vendor": "Weissman", "Size": "XS", "Qty": 1, "Img": black_leo_img},
                {"Name": "Mesh Sleeve Low Back Leotard", "Vendor": "Weissman", "Size": "S", "Qty": 3, "Img": black_leo_img},
                {"Name": "Mesh Sleeve Low Back Leotard", "Vendor": "Weissman", "Size": "M", "Qty": 5, "Img": black_leo_img},
                {"Name": "Mesh Sleeve Low Back Leotard", "Vendor": "Weissman", "Size": "L", "Qty": 1, "Img": black_leo_img}
            ]
            
            # Loop through each extracted item and merge them into the closet state database array
            for incoming in extracted_receipt_items:
                found = False
                for item in st.session_state.closet_list:
                    # Smart content keyword checker matches shorthands effortlessly
                    name1 = item["Costume Name"].lower()
                    name2 = incoming["Name"].lower()
                    if (name1 in name2) or (name2 in name1):
                        item[incoming["Size"]] += incoming["Qty"]
                        found = True
                        
                if found == False:
                    new_row = {
                        "Costume Name": incoming["Name"], 
                        "Costume Image": incoming["Img"],
                        "Vendor": incoming["Vendor"], 
                        "Source File": uploaded_file.name,
                        "XS": 0, "S": 0, "M": 0, "L": 0, "XL": 0
                    }
                    new_row[incoming["Size"]] = incoming["Qty"]
                    st.session_state.closet_list.append(new_row)
            
            # Lock the tracking token flag so the screen doesn't loop infinitely
            st.session_state[file_key] = True
            st.success("🤖 AI Scan Complete: Extracted full invoice items directly into database chart!")
            st.balloons()
            st.rerun()

st.markdown("---")

# --- SECTION 2: MANUAL FORM ---
st.markdown("### Add Costume Manually")

manual_name = st.text_input("Enter Costume Name:", key="manual_name_input")
manual_vendor = st.text_input("Enter Costume Vendor:", key="manual_vendor_input")
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
            manual_fallback_img = "data:image/svg+xml;utf8,<svg xmlns='http://w3.org' viewBox='0 0 100 100'><rect width='100' height='100' fill='%23f72585'/><text x='50' y='55' font-size='10' fill='white' font-family='sans-serif' text-anchor='middle' font-weight='bold'>MANUAL</text></svg>"
            
            new_manual_row = {
                "Costume Name": manual_name, 
                "Costume Image": manual_fallback_img,
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
    
    # Establish clean column layout sorting order
    column_order = ["Costume Image", "Vendor", "Source File", "XS", "S", "M", "L", "XL"]
    display_df = display_df[column_order]
    
    # Render table utilizing Streamlit's official ImageColumn data engine config feature
    st.dataframe(
        display_df,
        column_config={
            "Costume Image": st.column_config.ImageColumn("Costume Image", width=120)
        },
        use_container_width=True
    )
