from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any
from core.launcher import launch_test

app = FastAPI()
TESTS = {}

class LoadTestRequest(BaseModel):
    test_type: str
    config: Dict[str, Any]
    runner_type: str = "local"
    data: dict | list | str | None = None

@app.post("/run")
def run_load_test(req: LoadTestRequest, background_tasks: BackgroundTasks):
    import uuid
    test_id = str(uuid.uuid4())
    # background (non-blocking) execution
    background_tasks.add_task(
        launch_test, req.test_type, req.config, req.runner_type, req.data, test_id, TESTS
    )
    return {"test_id": test_id, "status": "started"}

@app.get("/status/{test_id}")
def test_status(test_id: str):
    return TESTS.get(test_id, {"status": "unknown"})