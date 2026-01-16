import asyncio
import sys
import os
from sqlalchemy import select, delete

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import async_session
from app.models.user import User
from app.models.settings import UserSetting
from app.models.session import ChatSession
from app.models.quiz import QuizResult

async def delete_user(username):
    async with async_session() as session:
        # Check if user exists
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        
        if not user:
            print(f"Error: User '{username}' not found.")
            return

        # Delete related data (cascade delete should work if configured, but let's be explicit)
        await session.execute(delete(UserSetting).where(UserSetting.user_id == user.id))
        await session.execute(delete(ChatSession).where(ChatSession.user_id == user.id))
        await session.execute(delete(QuizResult).where(QuizResult.user_id == user.id))
        
        # Delete user
        await session.delete(user)
        await session.commit()
        print(f"User '{username}' and all associated data deleted successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python delete_user.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    
    asyncio.run(delete_user(username))