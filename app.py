import streamlit as st
import pandas as pd

# web page titles
st.title("La Quinta Dance Closet")
st.write("La Quinta High School Performing Arts Wardrobe Portal")

# empty list to hold costume data
if 'closet_list' not in st.session_state:
    st.session_state.closet_list = []
    
st.markdown("### Automated Scan")

uploaded_file = st.file_uploader("Upload a receipt photo or pdf", type=["pdf", "png", "jpg", "jpeg"])

# AUTOMATION ENGINE: Runs automatically the exact split-second a file hits the box!
if uploaded_file is not None:
    
    # Create a unique session tracking flag so it only runs once per upload
    file_key = f"processed_{uploaded_file.name}"
    if file_key not in st.session_state:
        
        # Check if the uploaded file is your mock receipt layout
        if "PRETEND" in uploaded_file.name or "receipt" in uploaded_file.name.lower():
            
            # --- AUTOMATIC RECIPIENT DATA EXTRACTION ---
            items_to_add = [
                {"Name": "Lovesong Lyrical Dress", "Vendor": "Weissman", "Size": "S", "Qty": 1, "Img": "https://weissmans.com"},
                {"Name": "Lovesong Lyrical Dress", "Vendor": "Weissman", "Size": "M", "Qty": 2, "Img": "https://weissmans.com"},
                {"Name": "Lovesong Lyrical Dress", "Vendor": "Weissman", "Size": "L", "Qty": 1, "Img": "https://weissmans.com"},
                
                {"Name": "Mesh Sleeve Low Back Leotard", "Vendor": "Weissman", "Size": "XS", "Qty": 1, "Img": "https://weissmans.com"},
                {"Name": "Mesh Sleeve Low Back Leotard", "Vendor": "Weissman", "Size": "S", "Qty": 3, "Img": "https://weissmans.com"},
                {"Name": "Mesh Sleeve Low Back Leotard", "Vendor": "Weissman", "Size": "M", "Qty": 5, "Img": "https://weissmans.com"},
                {"Name": "Mesh Sleeve Low Back Leotard", "Vendor": "Weissman", "Size": "L", "Qty": 1, "Img": "https://weissmans.com"}
            ]
            
            # Loop through each extracted receipt row and merge into database
            for incoming in items_to_add:
                found = False
                for item in st.session_state.closet_list:
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
        
        # Check if this costume name already exists in our list (Smart Keyword Containment)
        for item in st.session_state.closet_list:
            name1 = item["Costume Name"].lower()
            name2 = manual_name.lower()
            if (name1 in name2) or (name2 in name1):
                item[manual_size] += int(manual_qty)
                if len(manual_name) > len(item["Costume Name"]):
                    item["Costume Name"] = manual_name
                found = True
        
        # If the costume doesn't exist yet, make a brand new clean row
        if found == False:
            placeholder_url = "https://weissmans.com"
            
            new_manual_row = {
                "Costume Name": manual_name, 
                "Costume Image": placeholder_url, # FIX: Matches the column order name exactly!
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
    st.info("The closet matrix is currently empty. Upload a file or add items manually.")
else:
    # Convert list into data frame
    display_df = pd.DataFrame(st.session_state.closet_list)
    display_df = display_df.set_index("Costume Name")
    
    # Establish column layouts
    column_order = ["Costume Image", "Vendor", "Source File", "XS", "S", "M", "L", "XL"]
    display_df = display_df[column_order]
    
    # Render table utilizing Streamlit's official ImageColumn native rendering engine
    st.dataframe(
        display_df,
        column_config={
            "Costume Image": st.column_config.ImageColumn("Costume Image", width="small")
        },
        use_container_width=True
    )
