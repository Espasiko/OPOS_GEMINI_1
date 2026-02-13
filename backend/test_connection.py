
import httpx
import asyncio
import os
import json

async def test_conn():
    url = "https://electroyhogarpelotazo.tienda/v1/chat/completions"
    data = {
        "model": "salamandra-7b-instruct",
        "messages": [{"role": "user", "content": "Hola"}],
        "stream": True,
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    print(f"Testing connection to: {url}")
    print("Using verify=False, timeout=300")
    
    try:
        async with httpx.AsyncClient(timeout=300.0, verify=False) as client:
            async with client.stream("POST", url, json=data) as response:
                print(f"Status: {response.status_code}")
                async for line in response.aiter_lines():
                    print(f"Received: {line[:100]}")
                    break
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_conn())
