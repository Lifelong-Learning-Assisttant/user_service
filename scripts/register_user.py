import asyncio
import sys
import os
from sqlalchemy import select

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import async_session
from app.models.user import User
from app.core.security import get_password_hash

async def register_user(username, password, role="user"):
    async with async_session() as session:
        # Check if user exists
        result = await session.execute(select(User).where(User.username == username))
        existing_user = result.scalars().first()
        
        if existing_user:
            print(f"Error: User '{username}' already exists.")
            return

        # Create new user
        new_user = User(
            username=username,
            hashed_password=get_password_hash(password),
            role=role,
            is_active=True
        )
        session.add(new_user)
        await session.commit()
        print(f"User '{username}' registered successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python register_user.py <username> <password> [role]")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    role = sys.argv[3] if len(sys.argv) == 4 else "user"
    
    asyncio.run(register_user(username, password, role))