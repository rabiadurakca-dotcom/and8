import streamlit as st
import pandas as pd

# 1. Set up the web page titles
st.title("💃 LQ Dance Closet")
st.write("La Quinta High School Performing Arts Wardrobe Portal")

# 2. Create an empty list to hold our costume data if it doesn't exist yet
if 'closet_list' not in st.session_state:
    st.session_state.closet_list = []

# --- SECTION 1: UPLOAD ANY IMAGE ---
st.markdown("### 📷 Automated Scan")

# Create a file uploader box
uploaded_file = st.file_uploader("Upload a receipt photo or pdf", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    
    # Show the actual image that was uploaded right on the screen
    st.image(uploaded_file, caption="Uploaded Document Preview", width=200)
    
    # Simple input text boxes so you can enter the real details from your file
    scanned_name = st.text_input("Enter Costume Name from File:")
    scanned_size = st.selectbox("Select Costume Size:", ["XS", "S", "M", "L", "XL"])
    scanned_qty = st.number_input("Enter Costume Quantity:", min_value=1, value=1)

    # When clicked, take the typed info and add it to our list
    if st.button("Process Document and Add to Table"):
        if scanned_name != "":
            # Create a dictionary row using the file name and typed information
            new_file_row = {
                "Costume Name": scanned_name, 
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
st.markdown("### 📝 Quick Add Costume Manually")

manual_name = st.text_input("Enter Costume Name Manually:")
manual_size = st.selectbox("Select Size Manually:", ["XS", "S", "M", "L", "XL"])
manual_qty = st.number_input("Enter Quantity Manually:", min_value=1, value=1)

if st.button("Add to Closet Table"):
    if manual_name != "":
        new_manual_row = {
            "Costume Name": manual_name, 
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
st.markdown("### 📊 Size Matrix Table Chart")

if len(st.session_state.closet_list) == 0:
    st.info("The closet matrix is currently empty. Upload a file or add items manually.")
else:
    # Turn our basic list of rows into a data grid table to display on screen
    display_df = pd.DataFrame(st.session_state.closet_list)
    display_df = display_df.set_index("Costume Name")
    
    # Order the columns nicely
    column_order = ["Source File", "XS", "S", "M", "L", "XL"]
    display_df = display_df[column_order]
    
    st.table(display_df)
