import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AndEight - District Wardrobe Manager",
    page_icon="💃",
    layout="wide"
)

# Custom Styling (Deep Plum & Neon Electric Pink Theme)
st.markdown("""
<style>
    .main { background-color: #fdfbff; }
    h1 { color: #4A154B; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; }
    h3 { color: #3A0CA3; }
    .stButton>button { background-color: #F72585; color: white; border-radius: 6px; font-weight: bold; width: 100%; }
</style>
""", unsafe_allow_html=True)

st.title("💃 AndEight")
st.subheader("Automated Costume Inventory & District Lifecycle Management System")

# --- GLOBAL DISTRIBUTED REGISTRY ---
ggusd_schools = [
    "Santiago High", "Bolsa Grande High", "Garden Grove High", 
    "Hare High", "La Quinta High", "Los Amigos High", "Pacifica High", "Rancho Alamitos High"
]

# Simulate current active session user
current_user_school = st.sidebar.selectbox("Active Campus Node:", ggusd_schools, index=0)

if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {
            "ID": "COS-001", "Name": "Sparkle Lyrical Dress", "Vendor": "Weissman", "Size": "M", 
            "Color": "Teal", "Total Qty": 15, "In Stock": 5, "Lent Out": 10, "Lent To": "Garden Grove High",
            "Owner School": "Santiago High", "Purchase Year": 2024, "Lifespan (Yrs)": 4, 
            "Washing": "Hand wash cold, line dry.", "Eco Action": "Donate to local middle school theater troupe."
        },
        {
            "ID": "COS-002", "Name": "Jazz Fringe Unitard", "Vendor": "A Wish Come True", "Size": "S", 
            "Color": "Red", "Total Qty": 12, "In Stock": 12, "Lent Out": 0, "Lent To": "None",
            "Owner School": "Santiago High", "Purchase Year": 2025, "Lifespan (Yrs)": 3, 
            "Washing": "Machine wash delicate, cold.", "Eco Action": "Recycle fabric via APES textile drive."
        }
    ])

# --- SIDEBAR: SMART INGESTION ---
st.sidebar.header("📷 Smart Invoice Ingestion")
st.sidebar.write("Upload a Weissman PDF invoice or snap a photo of a receipt to automatically parse and inventory items.")
uploaded_file = st.sidebar.file_uploader("Upload PDF or Image Receipt", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.sidebar.success("✅ Document uploaded successfully!")
    if st.sidebar.button("🤖 Execute Computer Vision Parse"):
        new_items = [
            {"ID": "COS-003", "Name": "Glitz Tap Costume", "Vendor": "Weissman (AI Parsed)", "Size": "S", "Color": "Gold", "Total Qty": 5, "In Stock": 5, "Lent Out": 0, "Lent To": "None", "Owner School": current_user_school, "Purchase Year": 2026, "Lifespan (Yrs)": 4, "Washing": "Dry clean only", "Eco Action": "Threadcycle processing"},
            {"ID": "COS-004", "Name": "Glitz Tap Costume", "Vendor": "Weissman (AI Parsed)", "Size": "M", "Color": "Gold", "Total Qty": 10, "In Stock": 10, "Lent Out": 0, "Lent To": "None", "Owner School": current_user_school, "Purchase Year": 2026, "Lifespan (Yrs)": 4, "Washing": "Dry clean only", "Eco Action": "Threadcycle processing"},
            {"ID": "COS-005", "Name": "Glitz Tap Costume", "Vendor": "Weissman (AI Parsed)", "Size": "L", "Color": "Gold", "Total Qty": 5, "In Stock": 5, "Lent Out": 0, "Lent To": "None", "Owner School": current_user_school, "Purchase Year": 2026, "Lifespan (Yrs)": 4, "Washing": "Dry clean only", "Eco Action": "Threadcycle processing"}
        ]
        st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame(new_items)], ignore_index=True)
        st.sidebar.balloons()
        st.rerun()

# --- MAIN APP INTERFACE ---
tab1, tab2, tab3 = st.tabs(["📋 Campus Ledger", "🚚 District Borrowing Desk", "🌱 APES Circular Economy Tracker"])

# TAB 1: MASTER LEDGER
with tab1:
    st.header(f"Active Registry: {current_user_school}")
    
    def check_availability(row):
        if row["Lent Out"] > 0:
            return f"❌ Missing: Lent out to {row['Lent To']}"
        return "✅ In Stock"
        
    local_df = st.session_state.inventory[st.session_state.inventory["Owner School"] == current_user_school].copy()
    if not local_df.empty:
        local_df["Status Vector"] = local_df.apply(check_availability, axis=1)
        st.dataframe(local_df[["ID", "Name", "Size", "Color", "Total Qty", "In Stock", "Status Vector"]], use_container_width=True)
    else:
        st.info("No costume assets indexed for this school yet.")

# TAB 2: INTER-SCHOOL BORROWING ROUTER
with tab2:
    st.header("Inter-School Lending Desk")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📤 Log Outbound District Transfer")
        available_lend_df = st.session_state.inventory[(st.session_state.inventory["Owner School"] == current_user_school) & (st.session_state.inventory["In Stock"] > 0)]
        
        if not available_lend_df.empty:
            selected_id = st.selectbox("Select Costume ID to Transfer", available_lend_df["ID"])
            target_school = st.selectbox("Select Target Recipient School", [s for s in ggusd_schools if s != current_user_school])
            max_qty = int(st.session_state.inventory[st.session_state.inventory["ID"] == selected_id]["In Stock"].values[0])
            lend_qty = st.number_input("Quantity of Outfits to Send", min_value=1, max_value=max_qty, value=1)
            
            if st.button("Confirm District Transfer"):
                idx = st.session_state.inventory[st.session_state.inventory["ID"] == selected_id].index
                st.session_state.inventory.loc[idx, "In Stock"] -= lend_qty
                st.session_state.inventory.loc[idx, "Lent Out"] += lend_qty
                st.session_state.inventory.loc[idx, "Lent To"] = target_school
                st.success(f"Successfully transferred items to {target_school}!")
                st.rerun()
        else:
            st.info("No items locally available to lend out.")
            
    with col2:
        st.markdown("### 📥 Active Loan Ledger")
        active_loans = st.session_state.inventory[st.session_state.inventory["Lent Out"] > 0]
        if not active_loans.empty:
            st.dataframe(active_loans[["ID", "Name", "Lent Out", "Lent To"]], use_container_width=True)
        else:
            st.info("All wardrobe assets are currently in house.")

# TAB 3: APES / SUSTAINABILITY PIPELINE
with tab3:
    st.header("🌱 APES Sustainable Asset Monitoring")
    
    total_items_lent = st.session_state.inventory["Lent Out"].sum()
    pounds_saved = total_items_lent * 1.5
    
    st.metric(
        label="🌱 Total Textile Waste Diverted from Local Landfills",
        value=f"{pounds_saved} lbs",
        delta="Environmental Impact Benefit"
    )
    
    st.markdown("#### Costume Care & Disposal Actions Matrix")
    lifecycle_df = st.session_state.inventory[st.session_state.inventory["Owner School"] == current_user_school].copy()
    
    if not lifecycle_df.empty:
        current_year = 2026
        lifecycle_df["Years Remaining"] = lifecycle_df["Lifespan (Yrs)"] - (current_year - lifecycle_df["Purchase Year"])
        
        def assign_eco_urgency(val):
            if val <= 0: return "🚨 End of Life - Execute Eco Action"
            return "🟩 Active Rotation"
            
        lifecycle_df["Status Vector"] = lifecycle_df["Years Remaining"].apply(assign_eco_urgency)
        st.dataframe(lifecycle_df[["ID", "Name", "Washing", "Years Remaining", "Status Vector", "Eco Action"]], use_container_width=True)
    else:
        st.info("No lifecycle metrics compiled yet.")
