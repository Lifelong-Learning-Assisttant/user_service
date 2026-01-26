import asyncio
import httpx
import pytest
from datetime import datetime, timedelta, timezone

BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_brute_force_protection():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        username = "test_user"
        # We assume the password is NOT "wrong_password"
        wrong_payload = {
            "username": username,
            "password": "wrong_password"
        }

        print("\nStarting brute force test...")
        
        # 1. Try 5 times with wrong password
        for i in range(1, 6):
            response = await client.post("/auth/login", data=wrong_payload)
            print(f"Attempt {i}: Status {response.status_code}, Detail: {response.json().get('detail')}")
            assert response.status_code == 401

        # 2. The 6th attempt should be blocked with 403
        response = await client.post("/auth/login", data=wrong_payload)
        print(f"Attempt 6 (should be blocked): Status {response.status_code}, Detail: {response.json().get('detail')}")
        
        assert response.status_code == 403
        assert "Account is locked" in response.json().get("detail")

if __name__ == "__main__":
    asyncio.run(test_brute_force_protection())