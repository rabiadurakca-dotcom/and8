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

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    
    # Safety Check: Only show a preview if the file is an actual picture image
    if uploaded_file.name.endswith(".pdf") == False:
        st.image(uploaded_file, caption="Uploaded Document Preview", width=200)
    else:
        st.info(f"📄 Processing document layout metrics for: {uploaded_file.name}")
    
    # Input boxes open up dynamically so you can type whatever real data is on your document
    scanned_name = st.text_input("Enter Costume Name:", key="scan_name_input")
    scanned_vendor = st.text_input("Enter Costume Vendor:", key="scan_vendor_input")
    scanned_size = st.selectbox("Select Costume Size:", ["XS", "S", "M", "L", "XL"], key="scan_size_input")
    scanned_qty = st.number_input("Enter Costume Quantity:", min_value=1, value=1, key="scan_qty_input")

    # When clicked, capture the exact information entered on screen
    if st.button("Process Document and Add to Table", key="scan_submit_btn"):
        if scanned_name != "":
            
            # --- START SINGLE-ROW MERGING LOGIC ---
            found = False
            
            # Use basic string containment to look for matching items in our closet list
            for item in st.session_state.closet_list:
                name1 = item["Costume Name"].lower()
                name2 = scanned_name.lower()
                if (name1 in name2) or (name2 in name1):
                    item[scanned_size] += int(scanned_qty)
                    if len(scanned_name) > len(item["Costume Name"]):
                        item["Costume Name"] = scanned_name
                    found = True
            
            # If it's a completely new item, build a brand new dictionary row container
            if found == False:
                # Generate a secure local graphic blueprint card dynamically using the name typed on screen
                custom_img_blueprint = f"data:image/svg+xml;utf8,<svg xmlns='http://w3.org' viewBox='0 0 100 100'><rect width='100' height='100' fill='%234a154b'/><text x='50' y='55' font-size='10' fill='white' font-family='sans-serif' text-anchor='middle' font-weight='bold'>LQ CLOSET</text></svg>"
                
                new_file_row = {
                    "Costume Name": scanned_name, 
                    "Costume Image": custom_img_blueprint, # Assigns the dynamic visual blueprint right to the cell
                    "Vendor": scanned_vendor, 
                    "Source File": uploaded_file.name, # Automatically tracks your real uploaded file name
                    "XS": 0, "S": 0, "M": 0, "L": 0, "XL": 0
                }
                new_file_row[scanned_size] = int(scanned_qty)
                st.session_state.closet_list.append(new_file_row)
            # --- END SINGLE-ROW MERGING LOGIC ---
            
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
