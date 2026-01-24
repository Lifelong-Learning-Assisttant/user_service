import asyncio
import sys
import os
import json
from sqlalchemy import select

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import async_session
from app.models.user import User
from app.core.security import get_password_hash

async def bulk_create_users(file_path):
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
        print("Error: JSON file must contain a list of users.")
        return

    async with async_session() as session:
        for user_info in users_data:
            username = user_info.get("username")
            password = user_info.get("password")
            role = user_info.get("role", "user")

            if not username or not password:
                print(f"Skipping invalid user data: {user_info}")
                continue

            # Check if user exists
            result = await session.execute(select(User).where(User.username == username))
            existing_user = result.scalars().first()
            
            if existing_user:
                print(f"User '{username}' already exists. Skipping.")
                continue

            # Create new user
            new_user = User(
                username=username,
                hashed_password=get_password_hash(password),
                role=role,
                is_active=True
            )
            session.add(new_user)
            print(f"Prepared user '{username}' with role '{role}'.")

        await session.commit()
        print("Bulk user creation completed successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bulk_create_users.py <path_to_json_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    asyncio.run(bulk_create_users(file_path))