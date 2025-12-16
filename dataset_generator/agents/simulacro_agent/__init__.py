"""
Agente Generador de Simulacros - OpositaIA
==========================================

Módulo para generar simulacros y tests de oposiciones
usando el RAG de Qdrant via MCP.

Uso:
    from agents.simulacro_agent import SimulacroAgent, TestGenerator
    
    agent = SimulacroAgent()
    simulacro = agent.generar_simulacro(112)
    test = agent.generar_test(80)
"""

from .simulacro_agent import SimulacroAgent
from .test_generator import TestGenerator
from .mcp_client import MCPClient, get_mcp_client

__all__ = [
    "SimulacroAgent",
    "TestGenerator", 
    "MCPClient",
    "get_mcp_client"
]

__version__ = "1.0.0"
