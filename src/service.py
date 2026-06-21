from typing import Dict

from .repository import ActivityRepository
from .models import Activity


class ActivityService:
    def __init__(self, repository: ActivityRepository):
        self.repository = repository

    def list_activities(self) -> Dict[str, Activity]:
        return self.repository.get_all()

    def signup(self, activity_name: str, email: str) -> str:
        activity = self.repository.get(activity_name)
        if activity is None:
            raise ValueError("Activity not found")

        if email in activity.participants:
            raise ValueError("Student is already signed up")

        activity.participants.append(email)
        self.repository.save()
        return f"Signed up {email} for {activity_name}"

    def unregister(self, activity_name: str, email: str) -> str:
        activity = self.repository.get(activity_name)
        if activity is None:
            raise ValueError("Activity not found")

        if email not in activity.participants:
            raise ValueError("Student is not signed up for this activity")

        activity.participants.remove(email)
        self.repository.save()
        return f"Unregistered {email} from {activity_name}"
