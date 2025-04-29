from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from supabase import create_client, Client
from fastapi.staticfiles import StaticFiles

SUPABASE_URL = "https://fsjcyqjddjwyzekkpyfj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZzamN5cWpkZGp3eXpla2tweWZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM1MTYxMzcsImV4cCI6MjA1OTA5MjEzN30.oJHx5REchPMvCVQ3h8Qe0CuVkKs6Oc_6Am2YO4yHoDg"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/auth", response_class=HTMLResponse)
async def handle_auth(
    request: Request,
    action: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    if action == "register":
        try:
            response = supabase.auth.sign_up({"email": email, "password": password})
            if response.user:
                message = f"✅ Зарегистрирован: {email}"
            else:
                message = "❌ Ошибка регистрации"
        except Exception as e:
            message = f"❌ Ошибка: {e}"
    elif action == "login":
        try:
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if response.session:
                message = f"✅ Вход выполнен: {email}"
            else:
                message = "❌ Неверный логин или пароль"
        except Exception as e:
            message = f"❌ Ошибка входа: {e}"
    else:
        message = "❌ Неизвестное действие"

    return templates.TemplateResponse("result.html", {"request": request, "message": message})
