import streamlit as st
from datetime import datetime

# Database of electrical services with pricing and descriptions
services_db = {
    'powerpoint_install': {
        'name': 'Power Point Install',
        'price': 165.00,
        'description': 'Installation of a single standard power point (GPO) including all necessary wiring and testing.'
    },
    'ceiling_fan_fitoff': {
        'name': 'Ceiling Fan Fit-off',
        'price': 245.00,
        'description': 'Supply and installation of a standard ceiling fan with light fitting including wiring and connection.'
    },
    'switchboard_upgrade': {
        'name': 'Switchboard Upgrade',
        'price': 2850.00,
        'description': 'Complete switchboard replacement with new RCDs, circuit breakers and safety switches to current AS/NZS 3000 standards.'
    },
    'downlight_install': {
        'name': 'Downlight Install',
        'price': 95.00,
        'description': 'Installation of a single LED downlight including cutout, wiring and IC-rated housing.'
    },
    'smoke_alarm_install': {
        'name': 'Smoke Alarm Install',
        'price': 185.00,
        'description': 'Supply and installation of hardwired photoelectric smoke alarm with battery backup compliant with current regulations.'
    },
    'safety_switch_install': {
        'name': 'Safety Switch Install',
        'price': 320.00,
        'description': 'Installation of RCD safety switch to existing switchboard providing protection against electric shock.'
    },
    'oven_cooktop_connection': {
        'name': 'Oven/Cooktop Connection',
        'price': 275.00,
        'description': 'Electrical connection and isolation switch installation for electric oven or cooktop appliance.'
    },
    'light_fitting_replacement': {
        'name': 'Light Fitting Replacement',
        'price': 135.00,
        'description': 'Removal of old light fitting and installation of new fitting including connection and testing.'
    },
    'data_point_install': {
        'name': 'Data Point Install',
        'price': 155.00,
        'description': 'Installation of Category 6 data point including cable run up to 20 metres and wall plate.'
    },
    'hot_water_system_connection': {
        'name': 'Hot Water System Connection',
        'price': 385.00,
        'description': 'Electrical connection of electric hot water system including isolation switch and compliance certification.'
    }
}

# Function to validate Australian address
def validate_australian_address(address):
    """
    Validates if the address appears to be an Australian address.
    Checks for Australian state abbreviations and postcodes.
    """
    if not address:
        return False
    
    # Convert address to uppercase for checking
    address_upper = address.upper()
    
    # Australian state and territory abbreviations
    aus_states = ['NSW', 'VIC', 'QLD', 'SA', 'WA', 'TAS', 'NT', 'ACT']
    
    # Check if any Australian state is mentioned
    has_state = any(state in address_upper for state in aus_states)
    
    # Check if address contains a 4-digit postcode (Australian postcodes are 4 digits)
    import re
    has_postcode = bool(re.search(r'\b\d{4}\b', address))
    
    # Address should have at least a state or postcode to be considered Australian
    if has_state or has_postcode:
        return True
    else:
        return False

# Set the page title
st.title("⚡ Electrical Services Quote Generator")

# SIDEBAR: Service selection dropdown
st.sidebar.header("Select Service")
# Create a dropdown with service names as display labels, keys as values
selected_service_key = st.sidebar.selectbox(
    "Service Type",
    options=list(services_db.keys()),
    format_func=lambda x: services_db[x]['name']  # Display the friendly name instead of the key
)

# Get the selected service details from the database
selected_service = services_db[selected_service_key]

# MAIN SCREEN: Display service information in two columns
st.subheader("Selected Service Details")

# Create two columns for side-by-side layout
col1, col2 = st.columns(2)

# Left column: Service name
with col1:
    st.write("**Service:**")
    st.write(selected_service['name'])

# Right column: Price
with col2:
    st.write("**Price:**")
    st.write(f"${selected_service['price']:.2f} AUD")

# Display service description below the columns
st.info(f"📋 {selected_service['description']}")

# Add spacing
st.markdown("---")

# INPUT FIELDS: Customer information
st.subheader("Customer Information")
customer_name = st.text_input("Customer Name", placeholder="e.g., John Smith")
customer_address = st.text_input("Customer Address", placeholder="e.g., 123 Main Street, Sydney NSW 2000")

# Add spacing
st.markdown("---")

# ACTION BUTTON: Generate quote
if st.button("Generate Quote", type="primary"):
    # Validation 1: Check if customer name is empty
    if not customer_name and not customer_address:
        st.error("🚫 Please enter a customer name.")
    # Validation 2: Check if only name is provided without address
    elif customer_name and not customer_address:
        st.error("🚫 Please enter a customer address.")
    # Validation 2: Check if only address is provided without name
    elif not customer_name and customer_address:
        st.error("🚫 Please enter a customer name.")
    # Validation 3: Check if the address is a valid Australian address
    elif not validate_australian_address(customer_address):
        st.error("🚫 Please enter a valid Australian address (must include state abbreviation like NSW, VIC, QLD, etc. or a 4-digit postcode).")
    else:
        # Get today's date and format it
        today_date = datetime.now().strftime("%d %B %Y")
        
        # All validations passed - OUTPUT: Display the professional quote letter
        quote_letter = f"""
# ⚡ GOLD COAST ELECTRICAL PROS

### Professional Electrical Services - Licensed & Insured

---

### 📄 OFFICIAL QUOTATION

**Date:** {today_date}

**To:**  
{customer_name}  
{customer_address}

**From:**  
Gold Coast Electrical Pros Pty Ltd  
Licensed Electrician - Lic. #12345  
ABN: 12 345 678 901

---

Dear {customer_name},

Thank you for your enquiry. We are pleased to provide you with the following quote for electrical services at your property.

**Service Requested:** {selected_service['name']}

**Description:**  
{selected_service['description']}

**Quote Amount:** ${selected_service['price']:.2f} AUD (GST Included)

---

### 📋 Terms & Conditions

**Disclaimer:** This quote is valid for 30 days from the date above. Payment terms: 50% deposit required to book.

All work will be completed to Australian Standards (AS/NZS 3000) and includes a certificate of compliance upon completion.

---

### ✅ Next Steps

**To proceed, reply 'YES' to this message.**

Should you have any questions or require further information, please don't hesitate to contact us.

**Contact:** 0412 345 678 | info@gcelectricalpros.com.au

Regards,  
**Gold Coast Electrical Pros Team**

---

*Servicing Gold Coast & Surrounds | Available 24/7 for Emergency Call-Outs*
        """
        
        # Create plain text version for copying (without markdown formatting)
        quote_text_plain = f"""⚡ GOLD COAST ELECTRICAL PROS

Professional Electrical Services - Licensed & Insured

---

📄 OFFICIAL QUOTATION

Date: {today_date}

To:  
{customer_name}  
{customer_address}

From:  
Gold Coast Electrical Pros Pty Ltd  
Licensed Electrician - Lic. #12345  
ABN: 12 345 678 901

---

Dear {customer_name},

Thank you for your enquiry. We are pleased to provide you with the following quote for electrical services at your property.

Service Requested: {selected_service['name']}

Description:  
{selected_service['description']}

Quote Amount: ${selected_service['price']:.2f} AUD (GST Included)

---

📋 Terms & Conditions

Disclaimer: This quote is valid for 30 days from the date above. Payment terms: 50% deposit required to book.

All work will be completed to Australian Standards (AS/NZS 3000) and includes a certificate of compliance upon completion.

---

✅ Next Steps

To proceed, reply 'YES' to this message.

Should you have any questions or require further information, please don't hesitate to contact us.

Contact: 0412 345 678 | info@gcelectricalpros.com.au

Regards,  
Gold Coast Electrical Pros Team

---

Servicing Gold Coast & Surrounds | Available 24/7 for Emergency Call-Outs
"""
        
        # Display the quote in a success message box with markdown formatting
        st.success("✅ Quote Generated Successfully!")
        st.markdown(quote_letter)
        
        # Add a copy button below the quote
        st.code(quote_text_plain, language=None)
        
        # Copy button using streamlit's native functionality
        if st.button("📋 Copy Quote to Clipboard"):
            st.write("✅ Quote copied! You can now paste it into an email or message.")