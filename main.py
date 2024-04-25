from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse  # Add FileResponse import

app = FastAPI()

# A simple "database" to store user credentials (for demonstration purposes)
users_db = {
    "fazle": "123456"
}

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    # Check if the provided credentials are correct
    if username in users_db and users_db[username] == password:
        # If the credentials are correct, redirect to the index page
        response = RedirectResponse(url="/index.html")
        response.set_cookie(key="username", value=username)  # Store username in a cookie for demonstration
        return response
    else:
        # If the credentials are incorrect, raise an HTTPException with status code 401 (Unauthorized)
        raise HTTPException(status_code=401, detail="Incorrect username or password")

@app.get("/index.html", response_class=HTMLResponse)
async def index(request: Request):
    username = request.cookies.get("username", "Guest")
    return f"Welcome, {username}! This is the index page."

# Serve static files
@app.get("/{filename}")
async def get_static_file(filename: str):
    return FileResponse(filename)
