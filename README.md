# Petstore Management System 🐾

A comprehensive Streamlit web application providing a user-friendly interface for managing pets, store orders, and users through the Swagger Petstore API.

## Overview

This application is a frontend for the **Swagger Petstore REST API** running on `http://localhost:8080/api/v3`. It provides an intuitive UI for performing CRUD operations across three main domains:

- **🐶 Pets**: Add, view, update, and delete pets. Search by status, tags, or ID.
- **🏪 Store**: Manage store inventory and pet orders.
- **👥 Users**: Create, update, delete, and authenticate users.

## Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **pip** - Python package manager (comes with Python)
- **Backend API** - The Swagger Petstore API must be running on `http://localhost:8080`

## Installation

### 1. Clone or Download the Project

```bash
cd example-app
```

### 2. Create a Virtual Environment (Recommended)

On **Windows (PowerShell)**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

On **macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- **Streamlit** - The web framework
- **Requests** - For making HTTP calls to the backend API

## Running the Application

### 1. Ensure Backend API is Running

Make sure your Swagger Petstore API is accessible at `http://localhost:8080/api/v3`

### 2. Start the Streamlit App

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:3000` (or another port if 3000 is in use).

## Features

### 🐶 Pet Management
- **View Pets**: Search by status (available, pending, sold), tags, or pet ID
- **Add Pet**: Create new pets with details like name, category, tags, and photo URLs
- **Update Pet**: Modify existing pet information
- **Delete Pet**: Remove pets from the system

### 🏪 Store Management
- **Inventory**: View real-time pet inventory by status
- **Orders**: Create, retrieve, and delete pet orders with status tracking

### 👥 User Management
- **Find Users**: Search users by username
- **Create/Update Users**: Add new users or modify existing user details
- **Delete Users**: Remove users from the system
- **Authentication**: Login and logout functionality

## API Endpoints Supported

The application integrates with the following Swagger Petstore API endpoints:

### Pet Endpoints
- `GET /pet/findByStatus` - Find pets by status
- `GET /pet/findByTags` - Find pets by tags
- `GET /pet/{petId}` - Get pet by ID
- `POST /pet` - Add a new pet
- `PUT /pet` - Update an existing pet
- `DELETE /pet/{petId}` - Delete a pet

### Store Endpoints
- `GET /store/inventory` - Get store inventory
- `POST /store/order` - Place a new order
- `GET /store/order/{orderId}` - Get order by ID
- `DELETE /store/order/{orderId}` - Delete an order

### User Endpoints
- `GET /user/{username}` - Get user by username
- `POST /user` - Create a new user
- `POST /user/createWithList` - Create multiple users (via API)
- `GET /user/login` - Login user
- `GET /user/logout` - Logout user
- `PUT /user/{username}` - Update user
- `DELETE /user/{username}` - Delete user

## Configuration

The API base URL is configured in `app.py`:

```python
API_BASE_URL = "http://localhost:8080/api/v3"
```

To change the backend API URL, edit this variable in the file.

## Project Structure

```
example-app/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── openapi.json        # OpenAPI specification for the backend API
├── README.md          # This file
└── LICENSE            # Project license
```

## Troubleshooting

### "Connection refused" or "Cannot connect to backend"
- **Check**: Ensure the backend API is running on `http://localhost:8080`
- **Test**: Try accessing `http://localhost:8080/api/v3/store/inventory` in your browser

### "ModuleNotFoundError" when starting the app
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

### Streamlit port already in use
- **Solution**: Run on a different port: `streamlit run app.py --server.port 3001`

## Development

### Adding New Features
1. Identify the API endpoint in `openapi.json`
2. Add UI components in the appropriate tab/subtab
3. Use the `make_request()` helper function to call the API
4. Handle success and error responses

### Testing the App
1. Ensure the backend API is running
2. Test each tab and operation thoroughly
3. Verify error handling with invalid inputs

## API Documentation

For detailed information about the Swagger Petstore API, refer to:
- **OpenAPI Specification**: See `openapi.json` in this project
- **Swagger UI**: Visit `http://localhost:8080` (if available)
- **Official Petstore Docs**: https://swagger.io

## License

This project is licensed under the Apache 2.0 License. See the LICENSE file for details.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify the backend API is responding correctly
3. Review the application logs in the Streamlit terminal output
