import streamlit as st
from datetime import datetime
import pandas as pd
import os
import urllib.parse

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

# CSV Database file path
CSV_FILE = 'quotes_database.csv'

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

# Function to initialize CSV database
def init_database():
    """
    Creates the CSV file if it doesn't exist.
    This ensures the app won't crash when trying to read quotes on first run.
    """
    if not os.path.exists(CSV_FILE):
        # Create a new CSV with column headers
        df = pd.DataFrame(columns=['Date', 'Time', 'Customer_Name', 'Customer_Email', 'Customer_Address', 'Service', 'Price', 'Status'])
        df.to_csv(CSV_FILE, index=False)
        
# Function to save quote to CSV
def save_quote(customer_name, customer_email, customer_address, service_name, price):
    """
    Appends a new quote record to the CSV database.
    Each quote gets a timestamp and default status of 'Sent'.
    """
    # Get current date and time
    now = datetime.now()
    date_str = now.strftime("%d/%m/%Y")
    time_str = now.strftime("%H:%M:%S")
    
    # Create new quote record
    new_quote = {
        'Date': date_str,
        'Time': time_str,
        'Customer_Name': customer_name,
        'Customer_Email': customer_email if customer_email else '',
        'Customer_Address': customer_address,
        'Service': service_name,
        'Price': price,
        'Status': 'Sent'
    }
    
    # Read existing data
    df = pd.read_csv(CSV_FILE)
    
    # Append new quote using pd.concat
    df = pd.concat([df, pd.DataFrame([new_quote])], ignore_index=True)
    
    # Save back to CSV
    df.to_csv(CSV_FILE, index=False)

# Function to load all quotes from CSV
def load_quotes():
    """
    Reads all quotes from the CSV database.
    Returns a pandas DataFrame for easy display and filtering.
    """
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=['Date', 'Time', 'Customer_Name', 'Customer_Email', 'Customer_Address', 'Service', 'Price', 'Status'])

# Function to update quote status in CSV
def update_quote_status(row_index, new_status):
    """
    Updates the status of a specific quote in the CSV database.
    Uses the row index to identify which quote to update.
    """
    # Read existing data
    df = pd.read_csv(CSV_FILE)
    
    # Update the status for the specified row
    df.at[row_index, 'Status'] = new_status
    
    # Save back to CSV
    df.to_csv(CSV_FILE, index=False)

# Function to create mailto link (for desktop email apps)
def create_mailto_link(customer_email, customer_name, service_name, price, description, today_date):
    """
    Creates a mailto URL that opens the user's default email client.
    Pre-fills the recipient, subject, and body with quote details.
    """
    
    # Email subject line
    subject = f"Electrical Services Quotation - {service_name}"
    
    # Email body with Australian formatting
    body = f"""G'day {customer_name},

Thank you for your enquiry with Gold Coast Electrical Pros.

We are pleased to provide you with the following quotation for electrical services at your property.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUOTATION DETAILS

Date: {today_date}

Service Requested: {service_name}

Description: {description}

Quoted Amount: ${price:.2f} AUD (GST Included)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TERMS & CONDITIONS

- This quotation is valid for 30 days from the date above
- Payment terms: 50% deposit required to book
- All work will be completed to Australian Standards (AS/NZS 3000)
- Certificate of compliance provided upon completion

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXT STEPS

To proceed with this quotation, simply reply 'YES' to this email or give us a call on 0412 345 678.

Should you have any questions or require further information, please don't hesitate to contact us.

Cheers,
Gold Coast Electrical Pros Team

Phone: 0412 345 678
Email: info@gcelectricalpros.com.au
Licence: #12345 | ABN: 12 345 678 901

Servicing Gold Coast & Surrounds | Available 24/7 for Emergency Call-Outs
"""
    
    # URL encode the subject and body
    subject_encoded = urllib.parse.quote(subject)
    body_encoded = urllib.parse.quote(body)
    
    # Build the complete mailto URL
    mailto_url = f"mailto:{customer_email}?subject={subject_encoded}&body={body_encoded}"
    
    return mailto_url

# Function to create Gmail direct link (for web-based Gmail)
def create_gmail_link(customer_email, customer_name, service_name, price, description, today_date):
    """
    Creates a direct Gmail compose link that opens in browser with pre-filled content.
    This works perfectly with web-based Gmail and bypasses mailto limitations.
    """
    subject = f"Electrical Services Quotation - {service_name}"
    
    # Email body text
    body = f"""G'day {customer_name},

Thank you for your enquiry with Gold Coast Electrical Pros.

We are pleased to provide you with the following quotation for electrical services at your property.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUOTATION DETAILS

Date: {today_date}

Service Requested: {service_name}

Description: {description}

Quoted Amount: ${price:.2f} AUD (GST Included)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TERMS & CONDITIONS

- This quotation is valid for 30 days from the date above
- Payment terms: 50% deposit required to book
- All work will be completed to Australian Standards (AS/NZS 3000)
- Certificate of compliance provided upon completion

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXT STEPS

To proceed with this quotation, simply reply 'YES' to this email or give us a call on 0412 345 678.

Should you have any questions or require further information, please don't hesitate to contact us.

Cheers,
Gold Coast Electrical Pros Team

Phone: 0412 345 678
Email: info@gcelectricalpros.com.au
Licence: #12345 | ABN: 12 345 678 901

Servicing Gold Coast & Surrounds | Available 24/7 for Emergency Call-Outs
"""
    
    # URL encode the subject and body
    subject_encoded = urllib.parse.quote(subject)
    body_encoded = urllib.parse.quote(body)
    
    # Gmail compose URL format
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={customer_email}&su={subject_encoded}&body={body_encoded}"
    
    return gmail_url

# Initialize the database on app start
init_database()

# Set the page title
st.title("⚡ Electrical Services Quote Generator")

# CREATE TABBED NAVIGATION
tab1, tab2 = st.tabs(["📝 Generate Quote", "📊 Quote History"])

# TAB 1: GENERATE QUOTE
with tab1:
    # SIDEBAR: Service selection dropdown
    st.sidebar.header("Select Service")
    selected_service_key = st.sidebar.selectbox(
        "Service Type",
        options=list(services_db.keys()),
        format_func=lambda x: services_db[x]['name']
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
    customer_email = st.text_input("Customer Email (Optional)", placeholder="e.g., john.smith@email.com")
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
        # Validation 3: Check if only address is provided without name
        elif not customer_name and customer_address:
            st.error("🚫 Please enter a customer name.")
        # Validation 4: Check if the address is a valid Australian address
        elif not validate_australian_address(customer_address):
            st.error("🚫 Please enter a valid Australian address (must include state abbreviation like NSW, VIC, QLD, etc. or a 4-digit postcode).")
        else:
            # Get today's date and format it
            today_date = datetime.now().strftime("%d %B %Y")
            
            # All validations passed - OUTPUT: Display the professional quote letter
            quote_letter = f"""⚡ GOLD COAST ELECTRICAL PROS
Professional Electrical Services - Licensed & Insured

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 OFFICIAL QUOTATION

Date: {today_date}

To:  
{customer_name}  
{customer_address}

From:  
Gold Coast Electrical Pros Pty Ltd  
Licensed Electrician - Lic. #12345  
ABN: 12 345 678 901

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Dear {customer_name},

Thank you for your enquiry. We are pleased to provide you with the following 
quotation for electrical services at your property.

Service Requested: {selected_service['name']}

Description:  
{selected_service['description']}

Quoted Amount: ${selected_service['price']:.2f} AUD (GST Included)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 TERMS & CONDITIONS

Disclaimer: This quotation is valid for 30 days from the date above. 
Payment terms: 50% deposit required to book.

All work will be completed to Australian Standards (AS/NZS 3000) and includes 
a certificate of compliance upon completion.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ NEXT STEPS

To proceed, reply 'YES' to this message.

Should you have any questions or require further information, please don't 
hesitate to contact us.

Contact: 0412 345 678 | info@gcelectricalpros.com.au

Regards,  
Gold Coast Electrical Pros Team

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Servicing Gold Coast & Surrounds | Available 24/7 for Emergency Call-Outs
"""
            
            # Display the quote in a success message
            st.success("✅ Quote Generated Successfully!")
            
            # Use st.code to display the quote with a built-in copy button
            st.code(quote_letter, language=None)
            
            # SAVE QUOTE TO DATABASE
            save_quote(
                customer_name=customer_name,
                customer_email=customer_email,
                customer_address=customer_address,
                service_name=selected_service['name'],
                price=selected_service['price']
            )
            
            st.info("💾 Quote saved to database for tracking.")
            
            # EMAIL BUTTON FUNCTIONALITY
            # Only show email buttons if customer provided an email address
            if customer_email and customer_email.strip():
                st.markdown("---")
                st.subheader("📧 Send Quote via Email")
                
                # Create three columns for different email options
                email_col1, email_col2, email_col3 = st.columns(3)
                
                # OPTION 1: Gmail Direct Link (Best for Chrome/web users)
                with email_col1:
                    st.write("**🌐 Gmail**")
                    st.caption("*(Recommended)*")
                    
                    # Create Gmail direct link
                    gmail_link = create_gmail_link(
                        customer_email=customer_email,
                        customer_name=customer_name,
                        service_name=selected_service['name'],
                        price=selected_service['price'],
                        description=selected_service['description'],
                        today_date=today_date
                    )
                    
                    # Gmail button
                    st.markdown(
                        f"""
                        <a href="{gmail_link}" target="_blank">
                            <button style="
                                background-color: #ea4335;
                                color: white;
                                padding: 12px 24px;
                                font-size: 16px;
                                border: none;
                                border-radius: 5px;
                                cursor: pointer;
                                font-weight: bold;
                                width: 100%;
                                margin-top: 10px;
                            ">
                                📧 Open Gmail
                            </button>
                        </a>
                        """,
                        unsafe_allow_html=True
                    )
                    st.caption("✅ Opens Gmail with pre-filled quote")
                
                # OPTION 2: Desktop Email App (Outlook, Apple Mail, etc.)
                with email_col2:
                    st.write("**💻 Desktop App**")
                    st.caption("*(Outlook/Apple Mail)*")
                    
                    # Create mailto link for desktop apps
                    mailto_link = create_mailto_link(
                        customer_email=customer_email,
                        customer_name=customer_name,
                        service_name=selected_service['name'],
                        price=selected_service['price'],
                        description=selected_service['description'],
                        today_date=today_date
                    )
                    
                    # Desktop app button
                    st.markdown(
                        f"""
                        <a href="{mailto_link}">
                            <button style="
                                background-color: #0066cc;
                                color: white;
                                padding: 12px 24px;
                                font-size: 16px;
                                border: none;
                                border-radius: 5px;
                                cursor: pointer;
                                font-weight: bold;
                                width: 100%;
                                margin-top: 10px;
                            ">
                                📧 Email App
                            </button>
                        </a>
                        """,
                        unsafe_allow_html=True
                    )
                    st.caption("✅ For desktop email apps")
                
                # OPTION 3: Copy to Clipboard (Manual paste)
                with email_col3:
                    st.write("**📋 Copy Text**")
                    st.caption("*(Manual paste)*")
                    
                    # Create copyable email text
                    email_content = f"""To: {customer_email}
Subject: Electrical Services Quotation - {selected_service['name']}

G'day {customer_name},

Thank you for your enquiry with Gold Coast Electrical Pros.

We are pleased to provide you with the following quotation for electrical services at your property.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUOTATION DETAILS

Date: {today_date}
Service Requested: {selected_service['name']}
Description: {selected_service['description']}
Quoted Amount: ${selected_service['price']:.2f} AUD (GST Included)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TERMS & CONDITIONS

- This quotation is valid for 30 days from the date above
- Payment terms: 50% deposit required to book
- All work will be completed to Australian Standards (AS/NZS 3000)
- Certificate of compliance provided upon completion

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXT STEPS

To proceed with this quotation, simply reply 'YES' to this email or give us a call on 0412 345 678.

Cheers,
Gold Coast Electrical Pros Team

Phone: 0412 345 678
Email: info@gcelectricalpros.com.au
Licence: #12345 | ABN: 12 345 678 901
"""
                    
                    # Copy button (shows content in expandable section)
                    with st.expander("📄 View Email"):
                        st.code(email_content, language=None)
                    
                    st.caption("✅ Copy and paste into any email")
                
                # Help text
                st.info("💡 **For Gmail users:** Click the red '📧 Open Gmail' button - it will open Gmail in a new tab with the quote already filled in!")
            else:
                # Show helpful message if no email was provided
                st.warning("💡 **Tip:** Add a customer email address above to enable the 'Send Email' buttons!")

# TAB 2: QUOTE HISTORY
with tab2:
    st.header("📊 Quote History & Tracking")
    
    # Load all quotes from database
    quotes_df = load_quotes()
    
    # Check if there are any quotes in the database
    if quotes_df.empty:
        st.info("📭 No quotes generated yet. Go to the 'Generate Quote' tab to create your first quote!")
    else:
        # SEARCH FUNCTIONALITY
        st.subheader("🔍 Search Quotes")
        search_term = st.text_input("Search by Customer Name", placeholder="Type customer name to filter...")
        
        # Filter the dataframe based on search term
        if search_term:
            filtered_df = quotes_df[quotes_df['Customer_Name'].str.contains(search_term, case=False, na=False)]
        else:
            filtered_df = quotes_df
        
        # Display results count
        st.write(f"**Showing {len(filtered_df)} of {len(quotes_df)} quotes**")
        
        # Add spacing
        st.markdown("---")
        
        # DISPLAY QUOTE HISTORY TABLE WITH STATUS UPDATE
        st.subheader("All Quotes")
        
        # Create a container for each quote row with status update capability
        for idx, row in filtered_df.iterrows():
            # Create expandable section for each quote
            with st.expander(f"📋 {row['Date']} - {row['Customer_Name']} - {row['Service']} - ${row['Price']:.2f}", expanded=False):
                # Display quote details
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Customer:** {row['Customer_Name']}")
                    st.write(f"**Email:** {row['Customer_Email'] if row['Customer_Email'] else 'Not provided'}")
                    st.write(f"**Address:** {row['Customer_Address']}")
                    st.write(f"**Service:** {row['Service']}")
                    st.write(f"**Price:** ${row['Price']:.2f} AUD")
                    st.write(f"**Date/Time:** {row['Date']} at {row['Time']}")
                
                with col2:
                    st.write("**Current Status:**")
                    
                    # Color-code the status badge
                    status_color = {
                        'Sent': '🟡',
                        'Approved': '🔵',
                        'Won': '🟢',
                        'Lost': '🔴'
                    }
                    
                    current_status = row['Status']
                    status_emoji = status_color.get(current_status, '⚪')
                    
                    st.markdown(f"### {status_emoji} {current_status}")
                    
                    # Status update dropdown
                    st.write("**Update Status:**")
                    new_status = st.selectbox(
                        "Change to:",
                        options=['Sent', 'Approved', 'Won', 'Lost'],
                        index=['Sent', 'Approved', 'Won', 'Lost'].index(current_status),
                        key=f"status_{idx}"
                    )
                    
                    # Update button
                    if st.button("💾 Update", key=f"update_{idx}"):
                        if new_status != current_status:
                            update_quote_status(idx, new_status)
                            st.success(f"✅ Status updated to '{new_status}'")
                            st.rerun()
                        else:
                            st.info("ℹ️ Status unchanged")
        
        # SUMMARY STATISTICS
        st.markdown("---")
        st.subheader("📈 Summary Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Quotes", len(quotes_df))
        
        with col2:
            total_value = quotes_df['Price'].sum()
            st.metric("Total Value", f"${total_value:,.2f}")
        
        with col3:
            active_count = len(quotes_df[quotes_df['Status'].isin(['Sent', 'Approved'])])
            st.metric("Active Quotes", active_count)
        
        with col4:
            won_count = len(quotes_df[quotes_df['Status'] == 'Won'])
            st.metric("Won Jobs", won_count)
        
        # Additional analytics row
        col5, col6, col7, col8 = st.columns(4)
        
        with col5:
            sent_count = len(quotes_df[quotes_df['Status'] == 'Sent'])
            st.metric("🟡 Sent", sent_count)
        
        with col6:
            approved_count = len(quotes_df[quotes_df['Status'] == 'Approved'])
            st.metric("🔵 Approved", approved_count)
        
        with col7:
            won_value = quotes_df[quotes_df['Status'] == 'Won']['Price'].sum()
            st.metric("🟢 Won Value", f"${won_value:,.2f}")
        
        with col8:
            lost_count = len(quotes_df[quotes_df['Status'] == 'Lost'])
            st.metric("🔴 Lost", lost_count)
        
        # Win rate calculation
        if len(quotes_df) > 0:
            closed_quotes = len(quotes_df[quotes_df['Status'].isin(['Won', 'Lost'])])
            if closed_quotes > 0:
                win_rate = (won_count / closed_quotes) * 100
                st.markdown("---")
                st.metric("🎯 Win Rate (Won / Closed)", f"{win_rate:.1f}%")
