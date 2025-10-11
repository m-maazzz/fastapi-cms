from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.models.event import Event  # Adjust import as needed
from app.core.database import SessionLocal
from sqlalchemy.exc import IntegrityError

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def seed_events():
    db = SessionLocal()
    try:
        events = [
            Event(
                title="Annual Tech Conference",
                slug="annual-tech-conference",
                description="A conference for tech enthusiasts.",
                event_date=datetime.now() + timedelta(days=30),
                location="San Francisco, CA",
                image_url="https://example.com/images/tech_conf.jpg",
                is_published=True,
                organizer_name="Tech Org"
            ),
            Event(
                title="Music Festival 2025",
                slug="music-festival-2025",
                description="Join us for a weekend of live music.",
                event_date=datetime.now() + timedelta(days=60),
                location="Austin, TX",
                image_url="https://example.com/images/music_festival.jpg",
                is_published=False,
                organizer_name="Music Inc."
            )
        ]
        for event in events:
            db.add(event)
        db.commit()
        print("Events seeded successfully.")
    except IntegrityError:
        db.rollback()
        print("Events already seeded or duplicate found.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_events()
