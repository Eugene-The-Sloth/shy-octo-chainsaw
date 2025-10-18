"""
In-memory database configuration for testing the Mergington High School API
"""

from argon2 import PasswordHasher

# (Collections are defined as InMemoryCollection instances below)

class InMemoryCollection:
    def __init__(self):
        self.data = {}

    def find(self, query=None):
        # Very small query matcher: supports matching by _id or schedule_details.days/$in
        results = []
        for k, v in self.data.items():
            doc = {"_id": k, **v}
            if not query:
                results.append(doc)
                continue

            # Support simple _id lookup
            if isinstance(query, dict) and "_id" in query:
                if query["_id"] == k:
                    results.append(doc)
                continue

            # Support schedule_details.days $in matching
            match = True
            for key, cond in (query or {}).items():
                if key == "schedule_details.days" and isinstance(cond, dict) and "$in" in cond:
                    days = v.get("schedule_details", {}).get("days", [])
                    if not any(d in days for d in cond["$in"]):
                        match = False
                        break
            if match:
                results.append(doc)

        return results


    def find_one(self, query):
        # Support finding by _id
        if isinstance(query, dict):
            if "_id" in query:
                if query["_id"] in self.data:
                    return {"_id": query["_id"], **self.data[query["_id"]]}
                return None

            # Support a subset of queries by delegating to find()
            found = self.find(query)
            return found[0] if found else None
        return None


    def insert_one(self, document):
        id = document["_id"]
        del document["_id"]
        self.data[id] = document


    def count_documents(self, query=None):
        return len(self.data)


    def aggregate(self, pipeline):
        # Simple implementation for days aggregation
        if len(pipeline) == 3:  # Assuming the days pipeline
            days = set()
            for activity in self.data.values():
                if "schedule_details" in activity:
                    days.update(activity["schedule_details"]["days"])
            return [{"_id": day} for day in sorted(days)]
        return []


    def update_one(self, filter_doc, update_doc):
        """Support minimal update operations used by routers: $push and $pull on participants"""
        # Find the document
        _id = filter_doc.get("_id")
        if _id not in self.data:
            class DummyResult:
                modified_count = 0
            return DummyResult()

        doc = self.data[_id]
        # Handle $push
        if "$push" in update_doc:
            for field, val in update_doc["$push"].items():
                if field == "participants":
                    if "participants" not in doc:
                        doc["participants"] = []
                    doc["participants"].append(val)

        # Handle $pull
        if "$pull" in update_doc:
            for field, val in update_doc["$pull"].items():
                if field == "participants" and "participants" in doc:
                    try:
                        doc["participants"].remove(val)
                    except ValueError:
                        pass

        self.data[_id] = doc

        class Result:
            def __init__(self):
                self.modified_count = 1

        return Result()

# Use in-memory collections
activities_collection = InMemoryCollection()
teachers_collection = InMemoryCollection()

# Methods
def hash_password(password):
    """Hash password using Argon2"""
    ph = PasswordHasher()
    return ph.hash(password)

def init_database():
    """Initialize database if empty"""

    # Initialize activities if empty
    if activities_collection.count_documents({}) == 0:
        for name, details in initial_activities.items():
            activities_collection.insert_one({"_id": name, **details})

    # Initialize teacher accounts if empty
    if teachers_collection.count_documents({}) == 0:
        for teacher in initial_teachers:
            teachers_collection.insert_one({"_id": teacher["username"], **teacher})

# Initial database if empty
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Mondays and Fridays, 3:15 PM - 4:45 PM",
        "schedule_details": {
            "days": ["Monday", "Friday"],
            "start_time": "15:15",
            "end_time": "16:45"
        },
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 7:00 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "07:00",
            "end_time": "08:00"
        },
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Manga Club": {
        "description": "Explore the fantastic stories of the most interesting characters from Japanese Manga (graphic novels).",
        "schedule": "Tuesdays, 7:00 PM - 8:00 PM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "19:00",
            "end_time": "20:00"
        },
        "max_participants": 15,
        "participants": []
    },
    "Morning Fitness": {
        "description": "Early morning physical training and exercises",
        "schedule": "Mondays, Wednesdays, Fridays, 6:30 AM - 7:45 AM",
        "schedule_details": {
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "06:30",
            "end_time": "07:45"
        },
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and compete in basketball tournaments",
        "schedule": "Wednesdays and Fridays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Wednesday", "Friday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art techniques and create masterpieces",
        "schedule": "Thursdays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Thursday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Monday", "Wednesday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and prepare for math competitions",
        "schedule": "Tuesdays, 7:15 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "07:15",
            "end_time": "08:00"
        },
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Friday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "amelia@mergington.edu"]
    },
    "Weekend Robotics Workshop": {
        "description": "Build and program robots in our state-of-the-art workshop",
        "schedule": "Saturdays, 10:00 AM - 2:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "10:00",
            "end_time": "14:00"
        },
        "max_participants": 15,
        "participants": ["ethan@mergington.edu", "oliver@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Weekend science competition preparation for regional and state events",
        "schedule": "Saturdays, 1:00 PM - 4:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "13:00",
            "end_time": "16:00"
        },
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Sunday Chess Tournament": {
        "description": "Weekly tournament for serious chess players with rankings",
        "schedule": "Sundays, 2:00 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Sunday"],
            "start_time": "14:00",
            "end_time": "17:00"
        },
        "max_participants": 16,
        "participants": ["william@mergington.edu", "jacob@mergington.edu"]
    }
}

initial_teachers = [
    {
        "username": "mrodriguez",
        "display_name": "Ms. Rodriguez",
        "password": hash_password("art123"),
        "role": "teacher"
     },
    {
        "username": "mchen",
        "display_name": "Mr. Chen",
        "password": hash_password("chess456"),
        "role": "teacher"
    },
    {
        "username": "principal",
        "display_name": "Principal Martinez",
        "password": hash_password("admin789"),
        "role": "admin"
    }
]
