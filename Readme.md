# API Setup and Deployment Guide

This document provides a comprehensive guide to setting up the API environment, configuring the database, and launching the FastAPI server.

## Prerequisites

Ensure the following requirements are met before proceeding:

- Python version 3.8 or higher
- Dependencies listed in [requirements.txt](src/api/requirements.txt)

## Setup Instructions

Follow these steps to prepare and deploy the API:

1. **Set Up a Virtual Environment**

   Create a virtual environment to isolate project dependencies:

   ```sh
   python -m venv venv
   ```

2. **Activate the Virtual Environment**

   Activate the virtual environment based on your operating system:

   - **Linux/macOS**:
     ```sh
     source venv/bin/activate
     ```
   - **Windows**:
     ```sh
     venv\Scripts\activate
     ```

3. **Apply Database Migrations**

   Run the following command to apply all pending database migrations:

   ```sh
   alembic upgrade head
   ```

4. **Start the FastAPI Server**

   Launch the server using the command below:

   ```sh
   uvicorn main:app
   ```

Once the server is running, the API will be available at [http://localhost:8000](http://localhost:8000).
