import streamlit as st
import pandas as pd

st.title("La Quinta Dance Closet")
st.write("La Quinta High School Performing Arts Wardrobe Portal")

# 1. INITIALIZE STORAGE (AP CSP Concept: Creating a List of Dictionaries)
if 'closet_list' not in st.session_state:
    st.session_state.closet_list = []
    
st.markdown("### Automated Scan")
uploaded_file = st.file_uploader("Upload a receipt photo or pdf", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    file_key = f"processed_{uploaded_file.name}"
    
    if file_key not in st.session_state:
        items_to_add = []
        
        try:
            # 2. STRING EXTRACTION (Extract text from the file)
            file_text = ""
            if uploaded_file.type == "application/pdf":
                import pypdf
                reader = pypdf.PdfReader(uploaded_file)
                for page in reader.pages:
                    if page.extract_text():
                        file_text += page.extract_text() + "\n"
            else:
                file_text = uploaded_file.name

            # 3. LINE-BY-LINE SELECTION & ITERATION (AP CSP Concept: Algorithms & Traversal)
            lines = file_text.split("\n")
            for line in lines:
                clean_line = line.strip()
                
                # Skip empty lines
                if clean_line == "":
                    continue
                
                # Split line into an array of words
                words = clean_line.split()
                
                # Sequencing flags to detect data attributes
                detected_size = ""
                detected_qty = 0
                
                # Nested Loop to inspect individual words (AP CSP Grid/Array Traversal)
                for word in words:
                    # Look for standard size labels
                    if word == "XS" or word == "S" or word == "M" or word == "L" or word == "XL":
                        detected_size = word
                    
                    # Look for numerical tokens (Quantity)
                    elif word.isdigit():
                        detected_qty = int(word)
                
                # 4. CONDITIONAL SELECTION (AP CSP Concept: Selection/Boolean Logic)
                if detected_size != "" and detected_qty > 0:
                    
                    # Algorithm to strip keywords and isolate the costume name
                    clean_name = clean_line
                    for word in words:
                        if word == detected_size or word.isdigit() or len(word) <= 2:
                            clean_name = clean_name.replace(word, "")
                    
                    clean_name = clean_name.strip(",.- _'\"")
                    
                    if clean_name != "":
                        # Append the temporary structure to our list
                        items_to_add.append({
                            "Name": clean_name,
                            "Vendor": "Scanned Vendor",
                            "Size": detected_size,
                            "Qty": detected_qty
                        })

            # Failsafe fallback array item if no matching text structure is found
            if len(items_to_add) == 0:
                fallback_name = uploaded_file.name.split(".")[0]
                items_to_add.append({"Name": fallback_name, "Vendor": "Receipt File", "Size": "M", "Qty": 1})

        except Exception:
            items_to_add = [{"Name": uploaded_file.name, "Vendor": "Imported", "Size": "M", "Qty": 1}]
            
        # 5. DATA AGGREGATION & MERGING (AP CSP Concept: Managing Complexity)
        for incoming in items_to_add:
            found = False
            
            # Linear Search Algorithm through existing inventory list
            for item in st.session_state.closet_list:
                name1 = incoming["Name"].lower()
                name2 = item["Costume Name"].lower()
                
                # Text matching checks if one name is nested within another
                if name1 in name2 or name2 in name1:
                    item[incoming["Size"]] = item[incoming["Size"]] + incoming["Qty"]
                    found = True
                    break
                        
            # Create a brand new record if it's unique
            if found == False:
                new_row = {
                    "Costume Name": incoming["Name"], "Vendor": incoming["Vendor"], "Source File": uploaded_file.name,
                    "XS": 0, "S": 0, "M": 0, "L": 0, "XL": 0
                }
                new_row[incoming["Size"]] = incoming["Qty"]
                st.session_state.closet_list.append(new_row)
        
        st.session_state[file_key] = True
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
        for item in st.session_state.closet_list:
            if manual_name.lower() in item["Costume Name"].lower() or item["Costume Name"].lower() in manual_name.lower():
                item[manual_size] = item[manual_size] + int(manual_qty)
                if len(manual_name) > len(item["Costume Name"]):
                    item["Costume Name"] = manual_name
                found = True
                break
        
        if found == False:
            new_manual_row = {
                "Costume Name": manual_name, "Vendor": manual_vendor, "Source File": "Manual Entry",
                "XS": 0, "S": 0, "M": 0, "L": 0, "XL": 0
            }
            new_manual_row[manual_size] = int(manual_qty)
            st.session_state.closet_list.append(new_manual_row)
            
        st.success("Added item successfully!")
        st.rerun()

st.markdown("---")
st.markdown("### Size Table Chart")

if len(st.session_state.closet_list) == 0:
    st.info("The closet matrix is currently empty. Upload a file or add items manually.")
else:
    display_df = pd.DataFrame(st.session_state.closet_list)
    display_df = display_df.set_index("Costume Name")
    column_order = ["Vendor", "Source File", "XS", "S", "M", "L", "XL"]
    st.table(display_df[column_order])
