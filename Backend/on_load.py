#!/usr/bin/env python3
from pymongo import MongoClient
import os
import glob
from bson import ObjectId
import sys

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["candidate_db"]  # Replace with your actual database name
collection = db["candidates"]

# Path to the CV files
cv_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media", "CVs To Share June 2024")

# Get all PDF files
cv_files = glob.glob(os.path.join(cv_dir, "*.pdf"))

print(f"Found {len(cv_files)} CV files in {cv_dir}")

# Update count
updated = 0
not_found = 0

# Get all candidates
candidates = list(collection.find())
print(f"Found {len(candidates)} candidates in database")

# Process each candidate
for candidate in candidates:
    name = candidate.get("name", "").strip()
    if not name:
        continue
    
    # Try to find a matching CV file
    found = False
    for cv_path in cv_files:
        filename = os.path.basename(cv_path)
        # Check various filename patterns
        if (name.lower() in filename.lower() or 
            name.lower().replace(" ", "_") in filename.lower() or
            name.split()[0].lower() in filename.lower()):
            
            # Update the candidate record with the container path
            container_path = f"/app/media/CVs To Share June 2024/{filename}"
            collection.update_one(
                {"_id": candidate["_id"]},
                {"$set": {"CVPath": container_path}}
            )
            print(f"Updated {name} with CV path: {container_path}")
            updated += 1
            found = True
            break
    
    if not found:
        print(f"No CV found for candidate: {name}")
        not_found += 1

print(f"\nSummary:\n  - Updated {updated} candidate records\n  - Could not find CVs for {not_found} candidates")