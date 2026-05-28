from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from datetime import date
from src.core.pattern import Pattern
from src.core.scheduler import Scheduler
from src.core.git_engine import GitEngine
import json
import os

app = FastAPI(title="GitHubWall")

current_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")


class PatternRequest(BaseModel):
    data: List[List[int]]
    name: str = "custom"


class ExecuteRequest(BaseModel):
    repo: str
    pattern: PatternRequest
    start_date: str
    end_date: str


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/patterns")
async def list_patterns():
    patterns_dir = os.path.join(os.path.dirname(current_dir), "patterns")
    patterns = []
    if os.path.isdir(patterns_dir):
        for filename in os.listdir(patterns_dir):
            if filename.endswith(".json"):
                patterns.append(filename[:-5])
    return {"patterns": patterns}


@app.get("/api/patterns/{name}")
async def get_pattern(name: str):
    patterns_dir = os.path.join(os.path.dirname(current_dir), "patterns")
    file_path = os.path.join(patterns_dir, f"{name}.json")
    if not os.path.isfile(file_path):
        return {"error": f"Pattern '{name}' not found"}
    with open(file_path, "r") as f:
        return json.load(f)


@app.post("/api/preview")
async def preview_pattern(pattern: PatternRequest):
    try:
        p = Pattern(name=pattern.name, data=pattern.data)
        return {"valid": True, "width": p.width, "height": p.height}
    except ValueError as e:
        return {"valid": False, "error": str(e)}


@app.post("/api/execute")
async def execute(request: ExecuteRequest):
    try:
        pattern = Pattern(name=request.pattern.name, data=request.pattern.data)
        start = date.fromisoformat(request.start_date)
        end = date.fromisoformat(request.end_date)

        scheduler = Scheduler(start, end)
        schedule = scheduler.generate_schedule(pattern)

        engine = GitEngine(request.repo)
        engine.init_repo()

        for commit_date in schedule:
            engine.create_commit(commit_date)

        return {"success": True, "commits": len(schedule), "repo": request.repo}
    except Exception as e:
        return {"success": False, "error": str(e)}


def run_web(host: str = "0.0.0.0", port: int = 8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)
