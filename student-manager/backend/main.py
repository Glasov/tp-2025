"""
Student Manager API - Backend
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import students, courses, grades, reports

app = FastAPI(
    title="Student Manager API",
    description="API для управления студентами и оценками",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Подключаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продуктиве указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(grades.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {
        "message": "Student Manager API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "student-manager"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)