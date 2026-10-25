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

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    
    if uploaded_file.name.endswith(".pdf") == False:
        st.image(uploaded_file, caption="Uploaded Document Preview", width=200)
    else:
        st.info(f"📄 Processing document metadata for: {uploaded_file.name}")
    
    scanned_name = st.text_input("Enter Costume Name:", key="scan_name_input")
    scanned_vendor = st.text_input("Enter Costume Vendor:", key="scan_vendor_input")
    scanned_size = st.selectbox("Select Costume Size:", ["XS", "S", "M", "L", "XL"], key="scan_size_input")
    scanned_qty = st.number_input("Enter Costume Quantity:", min_value=1, value=1, key="scan_qty_input")

    # When clicked, it takes the typed info and adds it to the list
    if st.button("Process Document and Add to Table", key="scan_submit_btn"):
        if scanned_name != "":
            
            found = False
            
            # Checks if this costume is already in the list
            for item in st.session_state.closet_list:
                if item["Costume Name"] == scanned_name:
                    # If found, add the new quantity to the existing size
                    if scanned_size == "XS":
                        item["XS"] += int(scanned_qty)
                    if scanned_size == "S":
                        item["S"] += int(scanned_qty)
                    if scanned_size == "M":
                        item["M"] += int(scanned_qty)
                    if scanned_size == "L":
                        item["L"] += int(scanned_qty)
                    if scanned_size == "XL":
                        item["XL"] += int(scanned_qty)
                    found = True
            
            # If the costume doesn't exist yet, make a brand new row
            if found == False:
                new_file_row = {
                    "Costume Name": scanned_name, 
                    "Vendor": scanned_vendor,
                    "Source File": uploaded_file.name, 
                    "XS": 0, "S": 0, "M": 0, "L": 0, "XL": 0
                }
                if scanned_size == "XS":
                    new_file_row["XS"] = int(scanned_qty)
                if scanned_size == "S":
                    new_file_row["S"] = int(scanned_qty)
                if scanned_size == "M":
                    new_file_row["M"] = int(scanned_qty)
                if scanned_size == "L":
                    new_file_row["L"] = int(scanned_qty)
                if scanned_size == "XL":
                    new_file_row["XL"] = int(scanned_qty)
                st.session_state.closet_list.append(new_file_row)
            
            st.balloons()
            st.rerun()

st.markdown("---")

st.markdown("### Add Costume Manually")

manual_name = st.text_input("Enter Costume Name:", key="manual_name_input")
manual_vendor = st.text_input("Enter Costume Vendor:", key="manual_vendor_input")
manual_size = st.selectbox("Select Size:", ["XS", "S", "M", "L", "XL"], key="manual_size_input")
manual_qty = st.number_input("Enter Quantity:", min_value=1, value=1, key="manual_qty_input")

if st.button("Add to Closet Table", key="manual_submit_btn"):
    if manual_name != "":
        
        found = False
        
        # Checks if this costume is already in the list
        for item in st.session_state.closet_list:
            if item["Costume Name"] == manual_name:
                if manual_size == "XS":
                    item["XS"] += int(manual_qty)
                if manual_size == "S":
                    item["S"] += int(manual_qty)
                if manual_size == "M":
                    item["M"] += int(manual_qty)
                if manual_size == "L":
                    item["L"] += int(manual_qty)
                if manual_size == "XL":
                    item["XL"] += int(manual_qty)
                found = True
        
        # If the costume doesn't exist yet, this makes a brand new row
        if found == False:
            new_manual_row = {
                "Costume Name": manual_name, 
                "Vendor": manual_vendor,
                "Source File": "Manual Entry", 
                "XS": 0, "S": 0, "M": 0, "L": 0, "XL": 0
            }
            if manual_size == "XS":
                new_manual_row["XS"] = int(manual_qty)
            if manual_size == "S":
                new_manual_row["S"] = int(manual_qty)
            if manual_size == "M":
                new_manual_row["M"] = int(manual_qty)
            if manual_size == "L":
                new_manual_row["L"] = int(manual_qty)
            if manual_size == "XL":
                new_manual_row["XL"] = int(manual_qty)
            st.session_state.closet_list.append(new_manual_row)
        # --- END SINGLE-ROW MERGING LOGIC ---
            
        st.success("Added item successfully!")
        st.rerun()

st.markdown("---")

st.markdown("### Size Table Chart")

if len(st.session_state.closet_list) == 0:
    st.info("The closet matrix is currently empty. Upload a file or add items manually.")
else:
    # Convert running list array into data grid frame rows
    display_df = pd.DataFrame(st.session_state.closet_list)
    display_df = display_df.set_index("Costume Name")
    
    # Streamlined column layout sorting order
    column_order = ["Vendor", "Source File", "XS", "S", "M", "L", "XL"]
    display_df = display_df[column_order]
    
    st.table(display_df)
