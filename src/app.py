"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

from .repository import ActivityRepository
from .service import ActivityService

app = FastAPI(
    title="Mergington High School API",
    description="API for viewing and signing up for extracurricular activities",
)

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(Path(__file__).parent, "static")),
    name="static",
)

repository = ActivityRepository()
service = ActivityService(repository)


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/activities")
def get_activities():
    return repository.get_all()


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    try:
        message = service.signup(activity_name, email)
        return {"message": message}
    except ValueError as error:
        detail = str(error)
        if detail == "Activity not found":
            raise HTTPException(status_code=404, detail=detail)
        raise HTTPException(status_code=400, detail=detail)


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    try:
        message = service.unregister(activity_name, email)
        return {"message": message}
    except ValueError as error:
        detail = str(error)
        if detail == "Activity not found":
            raise HTTPException(status_code=404, detail=detail)
        raise HTTPException(status_code=400, detail=detail)
