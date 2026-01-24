import asyncio
import sys
import os
import json
from sqlalchemy import select, delete

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import async_session
from app.models.user import User
from app.models.settings import UserSetting
from app.models.session import ChatSession
from app.models.quiz import QuizResult

async def bulk_delete_users(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    try:
        with open(file_path, 'r') as f:
            users_data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return

    if not isinstance(users_data, list):
        print("Error: JSON file must contain a list of objects.")
        return

    async with async_session() as session:
        for user_info in users_data:
            username = user_info.get("username")
            if not username:
                print(f"Skipping invalid data (no username): {user_info}")
                continue

            # Check if user exists
            result = await session.execute(select(User).where(User.username == username))
            user = result.scalars().first()
            
            if not user:
                print(f"User '{username}' not found. Skipping.")
                continue

            # Delete related data
            await session.execute(delete(UserSetting).where(UserSetting.user_id == user.id))
            await session.execute(delete(ChatSession).where(ChatSession.user_id == user.id))
            await session.execute(delete(QuizResult).where(QuizResult.user_id == user.id))
            
            # Delete user
            await session.delete(user)
            print(f"Deleted user '{username}' and all associated data.")

        await session.commit()
        print("Bulk user deletion completed successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bulk_delete_users.py <path_to_json_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    asyncio.run(bulk_delete_users(file_path))