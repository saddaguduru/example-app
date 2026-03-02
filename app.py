"""
Streamlit Frontend for Swagger Petstore API
A user-friendly interface for managing pets, store orders, and users
"""

import streamlit as st
import requests
import json
from typing import Optional, Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8080/api/v3"

# Page configuration
st.set_page_config(
    page_title="Petstore Management",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
        padding: 10px 24px;
    }
    </style>
    """, unsafe_allow_html=True)

# Session state initialization
if 'api_token' not in st.session_state:
    st.session_state.api_token = None

# Helper functions
def make_request(method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> tuple[bool, Any]:
    """Make an API request and return success status and response"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if method.upper() == "GET":
            response = requests.get(url, params=params, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, params=params, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, params=params, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, params=params, headers=headers)
        else:
            return False, "Invalid HTTP method"
        
        if response.status_code in [200, 201]:
            try:
                return True, response.json()
            except:
                return True, response.text
        else:
            return False, {"error": f"API Error {response.status_code}", "message": response.text}
    except Exception as e:
        return False, {"error": str(e)}

# Main App
st.title("🐾 Petstore Management System")
st.markdown("A comprehensive interface for managing pets, store orders, and users")

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["🐶 Pets", "🏪 Store", "👥 Users"])

# ==================== PETS TAB ====================
with tab1:
    st.header("Pet Management")
    
    pet_subtab1, pet_subtab2, pet_subtab3, pet_subtab4 = st.tabs(
        ["View Pets", "Add Pet", "Update Pet", "Manage Results"]
    )
    
    # View Pets Tab
    with pet_subtab1:
        st.subheader("Find Pets")
        col1, col2 = st.columns(2)
        
        with col1:
            search_type = st.radio("Search by:", ["Status", "Tags", "ID"])
        
        if search_type == "Status":
            status = st.selectbox("Select Status:", ["available", "pending", "sold"])
            if st.button("Find Pets by Status", key="find_pets_status"):
                success, result = make_request("GET", "/pet/findByStatus", params={"status": status})
                if success:
                    st.success(f"Found {len(result)} pets")
                    if result:
                        st.dataframe(result)
                        st.json(result)
                else:
                    st.error(f"Error: {result}")
        
        elif search_type == "Tags":
            tags_input = st.text_input("Enter tags (comma-separated):")
            if st.button("Find Pets by Tags", key="find_pets_tags"):
                if tags_input:
                    tags = [tag.strip() for tag in tags_input.split(",")]
                    success, result = make_request("GET", "/pet/findByTags", params={"tags": tags})
                    if success:
                        st.success(f"Found {len(result)} pets")
                        if result:
                            st.dataframe(result)
                            st.json(result)
                    else:
                        st.error(f"Error: {result}")
                else:
                    st.warning("Please enter at least one tag")
        
        elif search_type == "ID":
            pet_id = st.number_input("Pet ID:", min_value=1, step=1)
            if st.button("Get Pet by ID", key="get_pet_id"):
                success, result = make_request("GET", f"/pet/{pet_id}")
                if success:
                    st.success("Pet found!")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Name:** {result.get('name', 'N/A')}")
                        st.write(f"**Status:** {result.get('status', 'N/A')}")
                        if result.get('category'):
                            st.write(f"**Category:** {result['category'].get('name', 'N/A')}")
                    with col2:
                        st.write(f"**ID:** {result.get('id', 'N/A')}")
                        if result.get('tags'):
                            st.write(f"**Tags:** {', '.join([t.get('name', '') for t in result['tags']])}")
                    st.json(result)
                else:
                    st.error(f"Error: {result}")
    
    # Add Pet Tab
    with pet_subtab2:
        st.subheader("Add New Pet")
        with st.form("add_pet_form"):
            col1, col2 = st.columns(2)
            with col1:
                pet_name = st.text_input("Pet Name *", placeholder="e.g., Buddy")
                pet_status = st.selectbox("Status *", ["available", "pending", "sold"])
            with col2:
                pet_id = st.number_input("Pet ID (optional):", min_value=0, value=0)
                category_name = st.text_input("Category (optional):", placeholder="e.g., Dogs")
            
            tags_input = st.text_input("Tags (comma-separated, optional):", placeholder="e.g., friendly, playful")
            photo_urls = st.text_area("Photo URLs (one per line, optional):")
            
            submitted = st.form_submit_button("Add Pet", type="primary")
            if submitted:
                if not pet_name:
                    st.error("Pet name is required")
                else:
                    pet_data = {
                        "name": pet_name,
                        "status": pet_status,
                        "photoUrls": [url.strip() for url in photo_urls.split("\n") if url.strip()] or ["https://via.placeholder.com/150"],
                    }
                    
                    if pet_id > 0:
                        pet_data["id"] = pet_id
                    
                    if category_name:
                        pet_data["category"] = {"name": category_name}
                    
                    if tags_input:
                        pet_data["tags"] = [{"name": tag.strip()} for tag in tags_input.split(",")]
                    
                    success, result = make_request("POST", "/pet", data=pet_data)
                    if success:
                        st.success("✅ Pet added successfully!")
                        st.json(result)
                    else:
                        st.error(f"Error: {result}")
    
    # Update Pet Tab
    with pet_subtab3:
        st.subheader("Update Pet")
        pet_id = st.number_input("Pet ID to update:", min_value=1, step=1, key="update_pet_id")
        
        with st.form("update_pet_form"):
            col1, col2 = st.columns(2)
            with col1:
                pet_name = st.text_input("Pet Name:", placeholder="e.g., Buddy")
                pet_status = st.selectbox("Status:", ["available", "pending", "sold"])
            with col2:
                category_name = st.text_input("Category:", placeholder="e.g., Dogs")
            
            tags_input = st.text_input("Tags (comma-separated):", placeholder="e.g., friendly, playful")
            photo_urls = st.text_area("Photo URLs (one per line):")
            
            submitted = st.form_submit_button("Update Pet", type="primary")
            if submitted:
                pet_data = {
                    "id": pet_id,
                    "name": pet_name or "Updated Pet",
                    "status": pet_status,
                    "photoUrls": [url.strip() for url in photo_urls.split("\n") if url.strip()] or ["https://via.placeholder.com/150"],
                }
                
                if category_name:
                    pet_data["category"] = {"name": category_name}
                
                if tags_input:
                    pet_data["tags"] = [{"name": tag.strip()} for tag in tags_input.split(",")]
                
                success, result = make_request("PUT", "/pet", data=pet_data)
                if success:
                    st.success("✅ Pet updated successfully!")
                    st.json(result)
                else:
                    st.error(f"Error: {result}")
        
        st.divider()
        st.subheader("Delete Pet")
        delete_pet_id = st.number_input("Pet ID to delete:", min_value=1, step=1, key="delete_pet_id")
        if st.button("🗑️ Delete Pet", key="delete_pet_btn", type="secondary"):
            success, result = make_request("DELETE", f"/pet/{delete_pet_id}")
            if success:
                st.success("✅ Pet deleted successfully!")
                st.json(result)
            else:
                st.error(f"Error: {result}")
    
    # Results Tab
    with pet_subtab4:
        st.subheader("View Raw API Response")
        st.info("Use 'View Pets' or other tabs to generate responses. They will appear here.")

# ==================== STORE TAB ====================
with tab2:
    st.header("Store Management")
    
    store_subtab1, store_subtab2 = st.tabs(["Inventory", "Orders"])
    
    # Inventory Tab
    with store_subtab1:
        st.subheader("Store Inventory")
        if st.button("Refresh Inventory", key="refresh_inventory"):
            success, result = make_request("GET", "/store/inventory")
            if success:
                st.success("Inventory loaded successfully")
                # Convert to a more readable format
                inventory_list = [{"Status": k, "Count": v} for k, v in result.items()]
                st.dataframe(inventory_list)
                st.json(result)
            else:
                st.error(f"Error: {result}")
    
    # Orders Tab
    with store_subtab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Place New Order")
            with st.form("place_order_form"):
                order_pet_id = st.number_input("Pet ID:", min_value=1, step=1)
                order_quantity = st.number_input("Quantity:", min_value=1, step=1, value=1)
                order_status = st.selectbox("Status:", ["placed", "approved", "delivered"])
                order_complete = st.checkbox("Mark as complete", value=False)
                
                submitted = st.form_submit_button("Place Order", type="primary")
                if submitted:
                    order_data = {
                        "petId": order_pet_id,
                        "quantity": order_quantity,
                        "status": order_status,
                        "complete": order_complete
                    }
                    success, result = make_request("POST", "/store/order", data=order_data)
                    if success:
                        st.success("✅ Order placed successfully!")
                        st.json(result)
                    else:
                        st.error(f"Error: {result}")
        
        with col2:
            st.subheader("View/Delete Order")
            order_id = st.number_input("Order ID:", min_value=1, step=1, key="view_order_id")
            
            if st.button("Get Order", key="get_order_btn"):
                success, result = make_request("GET", f"/store/order/{order_id}")
                if success:
                    st.success("Order found!")
                    st.json(result)
                else:
                    st.error(f"Error: {result}")
            
            if st.button("Delete Order", key="delete_order_btn", type="secondary"):
                success, result = make_request("DELETE", f"/store/order/{order_id}")
                if success:
                    st.success("✅ Order deleted successfully!")
                    st.json(result)
                else:
                    st.error(f"Error: {result}")

# ==================== USERS TAB ====================
with tab3:
    st.header("User Management")
    
    user_subtab1, user_subtab2, user_subtab3 = st.tabs(["View Users", "Add/Update User", "Authentication"])
    
    # View Users Tab
    with user_subtab1:
        st.subheader("Find User")
        username = st.text_input("Enter username:", placeholder="e.g., user1")
        if st.button("Find User", key="find_user_btn"):
            if username:
                success, result = make_request("GET", f"/user/{username}")
                if success:
                    st.success("User found!")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Username:** {result.get('username', 'N/A')}")
                        st.write(f"**Email:** {result.get('email', 'N/A')}")
                        st.write(f"**First Name:** {result.get('firstName', 'N/A')}")
                    with col2:
                        st.write(f"**Last Name:** {result.get('lastName', 'N/A')}")
                        st.write(f"**Phone:** {result.get('phone', 'N/A')}")
                        st.write(f"**Status:** {result.get('userStatus', 'N/A')}")
                    st.json(result)
                else:
                    st.error(f"Error: {result}")
            else:
                st.warning("Please enter a username")
    
    # Add/Update User Tab
    with user_subtab2:
        st.subheader("Create or Update User")
        with st.form("user_form"):
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username *", placeholder="e.g., john_doe")
                first_name = st.text_input("First Name", placeholder="e.g., John")
                email = st.text_input("Email", placeholder="e.g., john@email.com")
            with col2:
                password = st.text_input("Password", type="password", placeholder="Enter password")
                last_name = st.text_input("Last Name", placeholder="e.g., Doe")
                phone = st.text_input("Phone", placeholder="e.g., 555-1234")
            
            user_status = st.number_input("User Status (1=active, 0=inactive):", min_value=0, max_value=1, value=1)
            operation = st.selectbox("Operation:", ["Create New User", "Update Existing User"])
            
            submitted = st.form_submit_button("Submit", type="primary")
            if submitted:
                if not username:
                    st.error("Username is required")
                else:
                    user_data = {
                        "username": username,
                        "password": password or "default123",
                        "firstName": first_name,
                        "lastName": last_name,
                        "email": email,
                        "phone": phone,
                        "userStatus": user_status
                    }
                    
                    if operation == "Create New User":
                        success, result = make_request("POST", "/user", data=user_data)
                    else:
                        success, result = make_request("PUT", f"/user/{username}", data=user_data)
                    
                    if success:
                        st.success(f"✅ User {operation.lower()} successfully!")
                        st.json(result)
                    else:
                        st.error(f"Error: {result}")
        
        st.divider()
        st.subheader("Delete User")
        delete_username = st.text_input("Username to delete:", placeholder="e.g., john_doe", key="delete_user_input")
        if st.button("🗑️ Delete User", key="delete_user_btn", type="secondary"):
            if delete_username:
                success, result = make_request("DELETE", f"/user/{delete_username}")
                if success:
                    st.success("✅ User deleted successfully!")
                else:
                    st.error(f"Error: {result}")
            else:
                st.warning("Please enter a username")
    
    # Authentication Tab
    with user_subtab3:
        st.subheader("User Authentication")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Login")
            login_username = st.text_input("Username:", placeholder="e.g., user1", key="login_user")
            login_password = st.text_input("Password:", type="password", placeholder="Enter password", key="login_pass")
            if st.button("Login", key="login_btn", type="primary"):
                if login_username and login_password:
                    success, result = make_request(
                        "GET", 
                        "/user/login", 
                        params={"username": login_username, "password": login_password}
                    )
                    if success:
                        st.success("✅ Login successful!")
                        st.session_state.api_token = result
                        st.write(f"Token: {result}")
                    else:
                        st.error(f"Login failed: {result}")
                else:
                    st.warning("Please enter username and password")
        
        with col2:
            st.write("### Logout")
            if st.button("Logout", key="logout_btn"):
                success, result = make_request("GET", "/user/logout")
                if success:
                    st.success("✅ Logged out successfully!")
                    st.session_state.api_token = None
                else:
                    st.error(f"Logout failed: {result}")

# ==================== FOOTER ====================
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <small>Petstore Management System | Powered by Streamlit</small>
    <br>
    <small>API Base URL: http://localhost:8080</small>
</div>
""", unsafe_allow_html=True)
