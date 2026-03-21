from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import generate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
print("Hello")
app.include_router(generate.router)