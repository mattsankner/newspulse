from fastapi import FastAPI #core application class 
from fastapi.middleware.cors import CORSMiddleware #middleware for cross-origin resource sharing
"""
run:
    uvicorn main:app --reload
Visit http://127.0.0.1:8000/docs for Swagger
Visit http://127.0.0.1:8000/redoc for ReDoc
"""

#create fastapi app instance
app = FastAPI(
    title="Political Content Analyzer",
    description="An application that analyzes political content from X",
    version="0.1.0"
)

# Add CORS middleware: browser security feature that allows or restricts web pages to access your resources
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Which domains can talk to you: allow Angular default port
    allow_credentials=True,                   #allow credentials: cookies/auth headers
    allow_methods=["*"],                      #allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],                      #allow all headers
)

@app.get("/")
async def root(): #async for concurrent operations -> FastAPI runs it in its event loop
    return {"message": "Welcome to Political Content Analyzer API"} #returns any serializable python object




