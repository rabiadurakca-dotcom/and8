import streamlit as st
import pandas as pd

# Set up the webpage title
st.title("💃 LQ Dance Closet")
st.write("La Quinta High School Performing Arts Wardrobe Portal")

# Initialize an empty list to store our dance costumes if it doesn't exist yet
if 'closet_list' not in st.session_state:
    st.session_state.closet_list = []

# --- SECTION 1: UPLOAD RECEIPT ---
st.markdown("### 📷 Smart Invoice Ingestion")
uploaded_file = st.file_uploader("Upload a receipt photo or PDF", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.success("Receipt Document Uploaded Successfully!")
    
    # When the user clicks the scan button, simulate reading the receipt data
    if st.button("Run AI Invoice Scan"):
        
        # 1. Add the data for the Lovesong Lyrical Dress from the receipt
        st.session_state.closet_list.append({"Item": "Lovesong Lyrical Dress", "XS": 0, "S": 1, "M": 2, "L": 1, "XL": 0})
        
        # 2. Add the data for the Mesh Sleeve Leotard from the receipt
        st.session_state.closet_list.append({"Item": "Mesh Sleeve Low Back Leotard", "XS": 1, "S": 3, "M": 5, "L": 1, "XL": 0})
        
        st.balloons()
        st.rerun()

st.markdown("---")

# --- SECTION 2: MANUAL FORM ---
st.markdown("### 📝 Quick Add Costume Manually")

# Create simple input boxes for the user
manual_name = st.text_input("Enter Costume Name:")
manual_size = st.selectbox("Select Size:", ["XS", "S", "M", "L", "XL"])
manual_qty = st.number_input("Enter Quantity:", min_value=1, value=1)

if st.button("Add to Closet"):
    if manual_name != "":
        # Create a blank row structure for sizes
        new_row = {"Item": manual_name, "XS": 0, "S": 0, "M": 0, "L": 0, "XL": 0}
        
        # Look at what size was picked and put the quantity into that specific spot
        if manual_size == "XS":
            new_row["XS"] = int(manual_qty)
        elif manual_size == "S":
            new_row["S"] = int(manual_qty)
        elif manual_size == "M":
            new_row["M"] = int(manual_qty)
        elif manual_size == "L":
            new_row["L"] = int(manual_qty)
        elif manual_size == "XL":
            new_row["XL"] = int(manual_qty)
            
        # Append the new row to our running closet list registry
        st.session_state.closet_list.append(new_row)
        st.success("Added item successfully!")
        st.rerun()

st.markdown("---")

# --- SECTION 3: DISPLAY CHART MATRIX ---
st.markdown("### 📊 Size Matrix Table Chart")

# If there is nothing in the list, tell the user
if len(st.session_state.closet_list) == 0:
    st.info("The closet matrix is currently empty. Upload a receipt or add items manually.")
else:
    # Convert our simple list of dictionaries into a clean data frame grid layout
    display_dataframe = pd.DataFrame(st.session_state.closet_list)
    
    # Set the row indexes to be the costume names so it looks like a clean spreadsheet chart grid
    display_dataframe = display_dataframe.set_index("Item")
    
    # Render the final organized data table onto the webpage screen
    st.table(display_dataframe)
