"""
MongoDB initialization module for the 42 Student Portal backend.
This module handles initial setup and connection to MongoDB.
"""

import os
import dotenv
from pymongo import MongoClient

# Load environment variables
dotenv.load_dotenv()

def initialize_mongodb():
    """Initialize MongoDB connection and return client and database."""
    mongo_url = os.getenv("ME_CONFIG_MONGODB_URL")
    mongo_username = os.getenv("ME_CONFIG_MONGODB_USERNAME")
    mongo_password = os.getenv("ME_CONFIG_MONGODB_PASSWORD")
    
    # Connect to MongoDB
    mongo_client = MongoClient(mongo_url)
    mongo_db = mongo_client["admin"]
    
    # Test connection
    try:
        mongo_db.command("ping")
        print("MongoDB connection successful")
    except Exception as e:
        print(f"MongoDB connection failed: {str(e)}")
    
    return mongo_client, mongo_db

# Initialize MongoDB when module is imported
mongo_client, mongo_db = initialize_mongodb()
