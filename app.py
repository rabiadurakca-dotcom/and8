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
    
    # SAFETY CHECK: Only show the image preview if the file is NOT a PDF document
    if uploaded_file.name.endswith(".pdf") == False:
        st.image(uploaded_file, caption="Uploaded Document Preview", width=200)
    else:
        st.info(f"📄 Processing document metadata for: {uploaded_file.name}")
    
    # Simple input text boxes so you can enter the real details from your file
    scanned_name = st.text_input("Enter Costume Name:")
    scanned_vendor = st.text_input("Enter Costume Vendor:")
    scanned_size = st.selectbox("Select Costume Size:", ["XS", "S", "M", "L", "XL"])
    scanned_qty = st.number_input("Enter Costume Quantity:", min_value=1, value=1)

    # When clicked, take the typed info and add it to our list
    if st.button("Process Document and Add to Table"):
        if scanned_name != "":
            # Create a dictionary row using the file name and typed information
            new_file_row = {
                "Costume Name": scanned_name, 
                "Vendor": scanned_vendor,
                "Source File": uploaded_file.name, 
                "XS": 0, "S": 0, "M": 0, "L": 0, "XL": 0
            }
            
            # Put the quantity into the right size slot
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
                
            # Add to our main storage list
            st.session_state.closet_list.append(new_file_row)
            st.balloons()
            st.rerun()

st.markdown("---")

# --- SECTION 2: MANUAL FORM ---
st.markdown("### Add Costume Manually")

manual_name = st.text_input("Enter Costume Name:")
manual_vendor = st.text_input("Enter Costume Vendor:")
manual_size = st.selectbox("Select Size:", ["XS", "S", "M", "L", "XL"])
manual_qty = st.number_input("Enter Quantity:", min_value=1, value=1)

if st.button("Add to Closet Table"):
    if manual_name != "":
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
        st.success("Added item successfully!")
        st.rerun()

st.markdown("---")

# --- SECTION 3: DISPLAY THE TABLE ---
st.markdown("### Size Table Chart")

if len(st.session_state.closet_list) == 0:
    st.info("The closet matrix is currently empty. Upload a file or add items manually.")
else:
    # Turn our basic list of rows into a data grid table to display on screen
    display_df = pd.DataFrame(st.session_state.closet_list)
    display_df = display_df.set_index("Costume Name")
    
    # Order the columns nicely (including your vendor tracking column)
    column_order = ["Vendor", "Source File", "XS", "S", "M", "L", "XL"]
    display_df = display_df[column_order]
    
    st.table(display_df)
