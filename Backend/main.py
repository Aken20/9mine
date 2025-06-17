import uvicorn
import dotenv
from models import Candidate, User
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException, status, File, UploadFile, Form
import uvicorn
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
import sys
import uuid
import pymongo
import mongodb_init
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
import os
from passlib.hash import bcrypt
from bson.objectid import ObjectId
from fastapi import Depends
from auth import JWTHandler, get_current_user
import random
import string
from update_cv_paths import resolve_cv_path

dotenv.load_dotenv()

MONGO_URL = os.getenv("ME_CONFIG_MONGODB_URL")
MONGO_USERNAME = os.getenv("ME_CONFIG_MONGODB_USERNAME")
MONGO_PASSWORD = os.getenv("ME_CONFIG_MONGODB_PASSWORD")

MONGO_CLIENT = MongoClient(MONGO_URL)
MONGO_DB = MONGO_CLIENT["admin"]

app = FastAPI()

# File paths will be handled as simple strings in the Candidate model

# Mount static files directory for CV access
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media")
os.makedirs(static_dir, exist_ok=True)

# Mount both at /static and /api/static to handle different routing scenarios
app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.mount("/api/static", StaticFiles(directory=static_dir), name="api_static")

from add_canidates import add_candidate

@app.get("/api/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.get("/api/mongo")
async def mongo():
    try:
        MONGO_DB.command("ping")
        return {"status": "ok", "data": {"message": "MongoDB is running"}}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def mongo_to_dict(mongo_obj):
    # Convert the ObjectId to string for serialization
    mongo_dict = dict(mongo_obj)
    mongo_dict["_id"] = str(mongo_dict["_id"])  # Convert ObjectId to string
    return mongo_dict

@app.post("/api/mongo/get_candidate")
async def get_candidate(request: dict):
    try:
        # Check token and validate
        token = request.get("token")
        
        # Try to decode the token to check validity and get user_type
        try:
            payload = JWTHandler().decode_token(token)
            user_type = payload.get("user_type", "regular")
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        # For student tokens, don't check against users collection, just validate the token
        if user_type != "student":
            # For regular users, check if they exist in the database
            if not MONGO_DB["users"].find_one({"access_token": token}):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
                
        add_candidate(MONGO_DB)
        print(request, 'get_candidate')
        specialization = request.get("specialization")

        # Validate that candidate_id is provided
        if not specialization:
            candidate = MONGO_DB["candidates"].find({})

        # Fetch the candidate from MongoDB
        else:
            candidate = MONGO_DB["candidates"].find({"specialization": specialization})

        # Check if the candidate exists
        if not candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")

        return {"status": "ok", "data": [mongo_to_dict(c) for c in candidate]}
    except HTTPException as e:
        # Handle validation errors or missing candidate ID
        return {"status": "error", "error": e.detail}
    except Exception as e:
        # Handle unexpected errors
        return {"status": "error", "error": str(e)}

@app.post("/api/create_candidate")
async def create_candidate(
    data: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        request = Candidate.parse_raw(data)
        if not request:
            print("No candidate data provided")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Candidate data is required")

        # Validate the candidate data using the Candidate Pydantic model
        candidate_obj = Candidate(**request.dict())
        if MONGO_DB["candidates"].find_one({"name": candidate_obj.name}):
            print("Candidate already exists")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Candidate already exists")
        # Insert the candidate data into MongoDB
        # print("Inserting candidate data:", candidate_obj.dict())
        cv_path = ''.join(["/app/media/", file.filename])
        print(f"Uploading CV to: {cv_path}")
        with open(cv_path, "wb") as f:
            f.write(file.file.read())
        if not cv_path:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CV file not found")
        candidate_obj.CVPath = cv_path
        MONGO_DB["candidates"].insert_one(candidate_obj.dict())

        return {"status": "ok", "data": candidate_obj.dict()}
    except HTTPException as e:
        # Handle validation errors or missing candidate data
        return {"status": "error", "error": e.detail}
    except Exception as e:
        # Handle unexpected errors
        return {"status": "error", "error": str(e)}

# No file upload endpoint needed - files will be handled as paths only

@app.post("/api/mongo/search_candidate")
async def search_candidate(request: dict):
    try:
        query = request.get("query")
        token = request.get("token")
        
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        # Try to decode the token to check validity and get user_type
        try:
            payload = JWTHandler().decode_token(token)
            user_type = payload.get("user_type", "regular")
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            
        # For student tokens, don't check in users collection
        if user_type != "student":
            # For regular users, verify in database
            user = MONGO_DB["users"].find_one({"access_token": token})
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
                
            # Check expiry if applicable
            if "expires_at" in user and user["expires_at"] < datetime.now():
                MONGO_DB["users"].delete_one({"access_token": token})
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account expired")
        print(request, 'search_candidate')
        search_query = request.get("query")
        # Validate that query is provided
        if not search_query:
            return get_candidate(request)
        # Fetch the candidate from MongoDB
        l = []
        for i in MONGO_DB["candidates"].find({"$or": [{"name": {"$regex": search_query}}, {"email": {"$regex": search_query}}, {"phone": {"$regex": search_query}}, {"nationality": {"$regex": search_query}}, {"education": {"$regex": search_query}}, {"specialization": {"$regex": search_query}}]}):
            l.append(mongo_to_dict(i))
        if not l:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
        return {"status": "ok", "data": l}
    except HTTPException as e:
        # Handle validation errors or missing candidate ID
        return {"status": "error", "error": e.detail}
    except Exception as e:
        # Handle unexpected errors
        return {"status": "error", "error": str(e)}

@app.post("/api/mongo/download_cv")
async def download_cv(request: dict):
    try:
        token = request.get("token")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            
        # Try to decode the token to check validity and get user_type
        try:
            payload = JWTHandler().decode_token(token)
            user_type = payload.get("user_type", "regular")
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            
        # For student tokens, don't check in users collection
        if user_type != "student":
            # For regular users, verify in database
            user = MONGO_DB["users"].find_one({"access_token": token})
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
                
            # Check expiry if applicable
            if "expires_at" in user and user["expires_at"] < datetime.now():
                MONGO_DB["users"].delete_one({"access_token": token})
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account expired")
        # print(request, 'download_cv')
        # print(request.get("id"))
        candidate_id = request.get("id")
        # Validate that candidate_id is provided
        if not candidate_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Candidate ID is required")
        # Fetch the candidate from MongoDB
        candidate = MONGO_DB["candidates"].find_one({"_id": ObjectId(candidate_id)})
        # Check if the candidate exists
        # print(candidate)
        if not candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
        # Get CV file path
        cv_path = candidate.get("CVPath")
        
        # Check if CV path exists in the candidate record
        if not cv_path:
            return {"status": "error", "error": "No CV path available for this candidate"}
        
        # Use the helper function to resolve the file path
        cv_file_path = resolve_cv_path(cv_path, candidate.get("name"))
        
        if not cv_file_path:
            print(f"CV file not found for candidate: {candidate.get('name')}")
            return {"status": "error", "error": "CV file not found in any of the expected locations"}
        
        # Return the file directly as a streaming response with appropriate headers
        from fastapi.responses import FileResponse
        
        print(f"Serving file: {cv_file_path}")
        
        # Use FileResponse with headers for browser PDF preview
        return FileResponse(
            path=cv_file_path,
            filename=os.path.basename(cv_file_path),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename=\"CV_{candidate.get('name', 'candidate')}.pdf\"",
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "SAMEORIGIN",
                "Access-Control-Allow-Origin": "*",  # Allow embedding in any site
                "Cache-Control": "max-age=3600"  # Cache for 1 hour
            }
        )
    except HTTPException as e:
        # Handle validation errors or missing candidate ID
        return {"status": "error", "error": e.detail}
    except Exception as e:
        # Handle unexpected errors
        return {"status": "error", "error": str(e)}


@app.post("/api/upload_cv")
async def upload_cv(token: str = Form(...), cv: UploadFile = File(...)):
    try:
        # token = request.get("token")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            
        # Try to decode the token to check validity and get user_type
        try:
            payload = JWTHandler().decode_token(token)
            user_type = payload.get("user_type", "student")
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            
        # For student tokens, don't check in users collection
        if user_type != "student":
            print("Invalid user type", user_type)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            # For regular users, verify in database
        user = MONGO_DB["users"].find_one({"access_token": token})
        if not user:
            print("Invalid credentials")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            
        # Check expiry if applicable
        if "expires_at" in user and user["expires_at"] < datetime.now():
            MONGO_DB["users"].delete_one({"access_token": token})
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account expired")
        # add the uploaded cv to the mounted directory
        cv_path = ''.join(["/app/media/", cv.filename])
        print(f"Uploading CV to: {cv_path}")
        with open(cv_path, "wb") as f:
            f.write(cv.file.read())
        if not cv_path:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CV file not found")
        MONGO_DB["users"].update_one({"_id": user["_id"]}, {"$set": {"CVPath": cv_path}})
        print(f"Updated CV path for user: {user.get('username')}")
        return {"status": "ok", "data": {"cv_path": cv_path}}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.post("/api/generate_visitor_account")
async def generate_visitor_account(request: dict):
    try:
        # generate a random username and password of 8 characters
        username = request.get("username")
        days = request.get("days")
        expires_at = datetime.now() + timedelta(days=days)
        # print(username, 'username')
        if not username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is required")
        if MONGO_DB["users"].find_one({"username": username}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        _type = "visitor"
        MONGO_DB["users"].insert_one({"username": username, "password": bcrypt.hash(password), "_type": _type, "access_token": None, "expires_at": expires_at})
        return {"status": "ok", "data": {"user": {"username": username, "password": password, "expires_at": expires_at}}}
    except HTTPException as e:
        # Handle validation errors or missing user data
        return {"status": "error", "error": e.detail}
    except Exception as e:
        # Handle unexpected errors
        return {"status": "error", "error": str(e)}

@app.post("/api/login")
async def login(request: dict):
    try:
        username = request.get("username")
        password = request.get("password")
        user = MONGO_DB["users"].find_one({"username": username})
        
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        # Check expiry if it exists
        if "expires_at" in user and user["expires_at"] < datetime.now():
            MONGO_DB["users"].delete_one({"username": username})
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account has expired")
            
        if not bcrypt.verify(password, user["password"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        # Determine user type (default to "regular" if not specified)
        user_type = user.get("_type", "regular")
        
        # Create token with user type
        Token = JWTHandler().encode_token(username, user_type=user_type)
        MONGO_DB["users"].update_one({"username": username}, {"$set": {"access_token": Token}})
        
        return {"status": "ok", "data": {"token": Token, "user_type": user_type}}
    except HTTPException as e:
        # Handle validation errors or missing user data
        return {"status": "error", "error": e.detail}
    except Exception as e:
        # Handle unexpected errors
        return {"status": "error", "error": str(e)}

@app.post("/api/is_logged_in")
async def is_logged_in(request: dict):
    try:
        token = request.get("token")
        if not token:
            return {"status": "error", "error": "No token provided"}
            
        # First validate the token structure and signature
        try:
            payload = JWTHandler().decode_token(token)
            username = payload["sub"]
            user_type = payload.get("user_type", "regular")
        except Exception:
            return {"status": "error", "error": "Invalid token"}
        
        # Then find the user in database
        user = MONGO_DB["users"].find_one({"access_token": token})
        
        # If token is valid but not found in database
        if not user:
            # For student tokens (from student portal), we want to keep them valid
            # even if they're not in regular users collection
            if user_type == "student":
                return {"status": "ok", "data": {"is_logged_in": True, "user_type": "student"}}
            return {"status": "error", "error": "User not found"}
        
        # Check expiry if applicable
        if "expires_at" in user and user["expires_at"] < datetime.now():
            MONGO_DB["users"].delete_one({"access_token": token})
            return {"status": "error", "error": "Account expired"}
        
        return {"status": "ok", "data": {"is_logged_in": True, "user_type": user.get("_type", "regular")}}
    except HTTPException as e:
        # Handle validation errors or missing user data
        return {"status": "error", "error": e.detail}
    except Exception as e:
        # Handle unexpected errors
        return {"status": "error", "error": str(e)}

@app.post("/api/logout")
async def logout(request: dict):
    try:
        token = request.get("token")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            
        # Try to decode the token to check validity and get user_type
        try:
            payload = JWTHandler().decode_token(token)
            user_type = payload.get("user_type", "regular")
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        # For student tokens, just return success without modifying database
        # This is because student tokens are managed separately in the student portal
        if user_type == "student":
            return {"status": "ok", "data": {"token": None}}
            
        # For regular users
        user = MONGO_DB["users"].find_one({"access_token": token})
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            
        # Check expiry if applicable
        if "expires_at" in user and user["expires_at"] < datetime.now():
            MONGO_DB["users"].delete_one({"access_token": token})
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account expired")
            
        MONGO_DB["users"].update_one({"access_token": token}, {"$set": {"access_token": None}})
        return {"status": "ok", "data": {"token": None}}
    except HTTPException as e:
        return {"status": "error", "error": e.detail}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.post("/api/student/login")
async def student_login(request: dict):
    try:
        username = request.get("username")
        password = request.get("password")
        
        # Validate that username and password are provided
        if not username or not password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username and password are required")
        
        # Here you would typically validate against 42 Intra credentials or your student database
        # For this implementation, we'll create a JWT token with user_type="student"
        
        # Generate a token specifically marked as a student token
        token = JWTHandler().encode_token(username, user_type="student")
        
        # We don't store student tokens in the regular users collection
        # They are handled separately by the student portal authentication system
        MONGO_DB["users"].insert_one({"username": username, "access_token": token, "_type": "student"})
        print("Student logged in successfully")
        return {"status": "ok", "data": {"token": token, "user_type": "student"}}
    except HTTPException as e:
        return {"status": "error", "error": e.detail}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.post("/api/student/logout")
async def student_logout(request: dict):
    try:
        token = request.get("token")
        if not token:
            return {"status": "ok", "data": {"token": None}}
            
        # For student tokens, we don't need to update any database
        # We just need to validate that it's a student token
        try:
            payload = JWTHandler().decode_token(token)
            user_type = payload.get("user_type", "")
            
            if user_type != "student":
                return {"status": "error", "error": "Not a student token"}
                
        except Exception:
            return {"status": "error", "error": "Invalid token"}
            
        # Just return success - the frontend will handle removing the token cookie
        return {"status": "ok", "data": {"token": None}}
    except Exception as e:
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)