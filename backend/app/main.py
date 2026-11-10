from fastapi import FastAPI
from app.routers.courses import router as courses_router
from fastapi.middleware.cors import CORSMiddleware
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router
from app.routers.topic import router as topics_router
from app.routers.learning_material import router as learning_materials_router
from app.routers.learner_profile import router as learner_profile_router
from app.routers.learning_progress import router as learning_progress_router
from app.routers import quiz
from app.routers import quiz_attempt
from app.routers import topic_mastery
from app.routers import course_enrollment
from app.routers import dashboard
from app.routers import recommendation
from app.routers import learning_path

app = FastAPI(title="Personalized AI Learning System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(courses_router)
app.include_router(topics_router)
app.include_router(learning_materials_router)
app.include_router(learner_profile_router)
app.include_router(learning_progress_router)
app.include_router(quiz.router)
app.include_router(quiz_attempt.router)
app.include_router(topic_mastery.router)
app.include_router(course_enrollment.router)
app.include_router(dashboard.router)
app.include_router(recommendation.router)
app.include_router(learning_path.router)

@app.get("/")
def root():
    return {"message": "Personalized AI Learning System API is running"}
