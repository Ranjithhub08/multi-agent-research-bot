import os
import sys

# Change directory to backend-python and run the app
if __name__ == "__main__":
    print("🚀 Starting Autonomous Research Grid Backend...")
    # Add backend-python to sys.path
    sys.path.append(os.path.join(os.getcwd(), "backend"))
    
    import uvicorn
    # Use the app from backend/app/main.py
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
