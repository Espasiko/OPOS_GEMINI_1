import asyncio
import os
import sys

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agents.agent_engine import AgentEngine

async def test_engine():
    print("🧪 Test Engine Simple...")
    engine = AgentEngine()
    
    # Test 1: Generación simple sin herramientas
    try:
        print("\n--- Test 1: Generación simple (Gemini Flash) ---")
        result = await engine.execute(
            agent_id="intent", # El agente intent suele ser simple
            inputs={"query": "Hola, ¿qué puedes hacer?"},
            model_override="gemini-flash"
        )
        print(f"Resultado: {result.get('content')[:100]}...")
    except Exception as e:
        print(f"Error Test 1: {e}")

    # Test 2: Generación DeepSeek (Sin herramientas)
    try:
        print("\n--- Test 2: DeepSeek Simple ---")
        result = await engine.execute(
            agent_id="intent",
            inputs={"query": "Analiza mi intención: quiero un caso de jubilación."},
            model_override="deepseek"
        )
        print(f"Resultado: {result.get('content')[:100]}...")
    except Exception as e:
        print(f"Error Test 2: {e}")

if __name__ == "__main__":
    asyncio.run(test_engine())
