import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="LQ Dance Closet",
    page_icon="💃",
    layout="centered"
)

# Custom Styling (La Quinta High Theme / Elegant Plum)
st.markdown("""
<style>
    .main { background-color: #fdfbff; }
    h1 { color: #4A154B; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; text-align: center; }
    h3 { color: #3A0CA3; }
    .stButton>button { background-color: #F72585; color: white; border-radius: 6px; font-weight: bold; width: 100%; }
</style>
""", unsafe_allow_html=True)

st.title("💃 LQ Dance Closet")
st.markdown("<p style='text-align: center; color: gray;'>La Quinta High School Performing Arts Wardrobe Portal</p>", unsafe_allow_html=True)

# --- CORE BACKEND TRACKING DATA ---
if 'raw_data' not in st.session_state:
    st.session_state.raw_data = [
        {"Costume Name": "Lovesong Lyrical Dress", "Size": "S", "Qty": 1},
        {"Costume Name": "Lovesong Lyrical Dress", "Size": "M", "Qty": 2},
        {"Costume Name": "Lovesong Lyrical Dress", "Size": "L", "Qty": 1},
        {"Costume Name": "Mesh Sleeve Low Back Leotard", "Size": "XS", "Qty": 1},
        {"Costume Name": "Mesh Sleeve Low Back Leotard", "Size": "S", "Qty": 3},
        {"Costume Name": "Mesh Sleeve Low Back Leotard", "Size": "M", "Qty": 5},
        {"Costume Name": "Mesh Sleeve Low Back Leotard", "Size": "L", "Qty": 1},
    ]

# --- INVOICE UPLOADER ---
st.markdown("### 📷 Smart Invoice Ingestion")
uploaded_file = st.file_uploader("Upload Weissman PDF or snap a receipt photo", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.success("✅ Receipt Document Uploaded!")
    if st.button("🤖 Run AI Invoice Scan"):
        # Simulated parsing that logs items cleanly by design and size
        st.session_state.raw_data.extend([
            {"Costume Name": "Glitz Tap Costume (AI)", "Size": "S", "Qty": 2},
            {"Costume Name": "Glitz Tap Costume (AI)", "Size": "M", "Qty": 4},
            {"Costume Name": "Glitz Tap Costume (AI)", "Size": "L", "Qty": 2}
        ])
        st.balloons()
        st.rerun()

st.markdown("---")

# --- MANUAL INVENTORY FORM ---
st.markdown("### 📝 Quick Add Costume Manually")
with st.form("manual_add", clear_on_submit=True):
    c_name = st.text_input("Costume Name")
    c_size = st.selectbox("Select Size", ["XS", "S", "M", "L", "XL"])
    c_qty = st.number_input("Quantity", min_value=1, value=1)
    
    submit_button = st.form_submit_button("Add to Closet")
    
    if submit_button and c_name:
        st.session_state.raw_data.append({
            "Costume Name": c_name,
            "Size": c_size,
            "Qty": int(c_qty)
        })
        st.rerun()

st.markdown("---")

# --- CUSTOM MATRIX TABLE CHART ENGINE ---
st.markdown("### 📊 Dynamic Size Matrix Table Chart")
st.markdown("<p style='font-size: 13px; color: gray; margin-top:-15px;'>Quantities mapped inside the grid with specific sizes along the bottom.</p>", unsafe_allow_html=True)

df = pd.DataFrame(st.session_state.raw_data)

# Create an indexed pivot table chart configuration matrix
pivot_df = df.pivot_table(
    index='Costume Name', 
    columns='Size', 
    values='Qty', 
    aggfunc='sum'
).fillna(0).astype(int)

# Force the standardized sizes along the bottom layout column order
desired_order = [s for s in ["XS", "S", "M", "L", "XL"] if s in pivot_df.columns]
pivot_df = pivot_df[desired_order]

# Display the custom matrix chart grid layout directly
st.table(pivot_df)
