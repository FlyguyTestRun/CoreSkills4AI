from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(tags=["hello"])


@router.get("/hello")
async def hello_world():
    """Simple hello endpoint for workflow testing."""
    return {
        "message": "Hello from CoreSkills4ai!",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
