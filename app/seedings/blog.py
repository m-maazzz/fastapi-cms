import os
import sys

# Ensure root path is included
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app.models.blog import Blog
from app.core.database import SessionLocal


def seed_blogs():
    db = SessionLocal()
    try:
        blogs = [
            Blog(
                title="The Rise of AI in Everyday Life",
                slug="ai-in-everyday-life",
                content="Artificial Intelligence is becoming part of our daily lives...",
                image_url="https://example.com/images/ai_blog.jpg",
                is_published=True,
                author_name="John Doe",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            Blog(
                title="Exploring Space: A New Frontier",
                slug="exploring-space-frontier",
                content="Space exploration has entered a new phase with private companies leading...",
                image_url="https://example.com/images/space_blog.jpg",
                is_published=True,
                author_name="Jane Smith",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            Blog(
                title="Why Minimalism Works",
                slug="why-minimalism-works",
                content="Minimalism helps clear mental clutter and reduces decision fatigue.",
                image_url="",  # No image
                is_published=False,
                author_name="Minimal Guru",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            Blog(
                title="Tech Layoffs in 2025",
                slug="tech-layoffs-2025",
                content="Major companies are streamlining due to economic downturn...",
                image_url="https://example.com/images/layoffs.jpg",
                is_published=False,
                author_name="Jane Smith",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            Blog(
                title="How to Work Remotely",
                slug="how-to-work-remotely",
                content="Remote work is here to stay. Here's how to do it right...",
                image_url=None,
                is_published=True,
                author_name="Remote Ninja",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
        ]

        for blog in blogs:
            db.add(blog)
        db.commit()
        print("✅ Blogs seeded successfully.")
    except IntegrityError:
        db.rollback()
        print("⚠️ Blogs already seeded or duplicate slug/email found.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_blogs()
