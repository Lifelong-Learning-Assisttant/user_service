import asyncio
import sys
import os
from sqlalchemy import select

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import async_session
from app.models.user import User

async def list_users():
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        
        print("\n--- Registered Users ---")
        if not users:
            print("No users found.")
        else:
            for user in users:
                status = "Active" if user.is_active else "Inactive"
                print(f"ID: {user.id} | Username: {user.username} | Role: {user.role} | Status: {status} | Created: {user.created_at}")
        print("------------------------\n")

if __name__ == "__main__":
    asyncio.run(list_users())