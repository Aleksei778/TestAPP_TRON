import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

@pytest.fixture
def test_tron_data():
    test_tron_data = {
        "address": "TNaRAoLUyYEV2uFZdZULU5H8KZ1sZo76fy",
        "offset": 1,
        "limit": 2
    }

    return test_tron_data

@pytest.mark.asyncio
async def test_get_tron_address_info(test_tron_data: dict):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/tron-info", json={"address": test_tron_data['address']})

        data = response.json()

        assert response.status_code == 200
        assert data["address"] == test_tron_data['address']
        assert "address" in data
        assert "balance" in data
        assert "bandwidth" in data
        assert "energy" in data

@pytest.mark.asyncio
async def test_get_recent_address_queries(test_tron_data: dict):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/tron-info", params={"offset": test_tron_data['offset'], "limit": test_tron_data['limit']})

        data = response.json()

        assert response.status_code == 200  
        assert len(data) == test_tron_data['limit']
        assert isinstance(data, list)

        for item in data:
            assert "address" in item
            assert "balance" in item
            assert "bandwidth" in item
            assert "energy" in item