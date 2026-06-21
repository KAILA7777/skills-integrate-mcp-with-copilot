import json
from pathlib import Path
from typing import Dict, Optional

from .models import Activity, ActivityStore

DEFAULT_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    }
}


class ActivityRepository:
    def __init__(self, data_path: Optional[Path] = None):
        self.data_file = (
            Path(data_path)
            if data_path
            else Path(__file__).parent / "data" / "activities.json"
        )
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self._activities = self._load_activities()

    def _load_activities(self) -> Dict[str, Activity]:
        if not self.data_file.exists():
            self._write_activities(DEFAULT_ACTIVITIES)

        try:
            raw_data = json.loads(self.data_file.read_text(encoding="utf-8"))
            activity_store = ActivityStore.parse_obj(raw_data)
            return {name: activity for name, activity in activity_store.root.items()}
        except (json.JSONDecodeError, ValueError):
            self._write_activities(DEFAULT_ACTIVITIES)
            return {name: Activity.parse_obj(payload) for name, payload in DEFAULT_ACTIVITIES.items()}

    def _write_activities(self, activities: Dict[str, dict]) -> None:
        self.data_file.write_text(json.dumps(activities, indent=2, ensure_ascii=False), encoding="utf-8")

    def get_all(self) -> Dict[str, Activity]:
        return self._activities

    def get(self, activity_name: str) -> Optional[Activity]:
        return self._activities.get(activity_name)

    def save(self) -> None:
        self._write_activities({name: activity.dict() for name, activity in self._activities.items()})
