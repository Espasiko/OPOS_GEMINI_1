#!/usr/bin/env python3
"""
🔍 VERIFICADOR DE ARQUITECTURA - OpositaIA
Verifica que todos los componentes estén correctamente configurados
"""

import os
import sys
import asyncio
import json
import httpx
from pathlib import Path
from typing import Dict, List, Tuple

class ArchitectureVerifier:
    """Verifica la arquitectura completa del proyecto"""
    
    def __init__(self):
        self.results: Dict[str, Dict] = {}
        self.project_root = Path(__file__).parent
    
    async def run_all_checks(self):
        """Ejecuta todos los chequeos"""
        print("=" * 80)
        print("🏗️  VERIFICADOR DE ARQUITECTURA - OpositaIA")
        print("=" * 80)
        print()
        
        # 1. File System
        await self.check_filesystem()
        
        # 2. Dependencies
        await self.check_dependencies()
        
        # 3. Services
        await self.check_services()
        
        # 4. Configuration
        await self.check_configuration()
        
        # 5. Generate Report
        self.generate_report()
    
    async def check_filesystem(self):
        """Verifica estructura de archivos"""
        print("📁 VERIFICANDO ESTRUCTURA DE ARCHIVOS...")
        print("-" * 80)
        
        required_dirs = {
            "backend": "Backend FastAPI",
            "frontend": "Frontend React",
            "mcp-server": "MCP Server",
            "docs": "Documentación"
        }
        
        backend_subdirs = {
            "routers": "Routers",
            "agents": "Agentes IA",
            "database": "Base de datos",
            "calculators": "Calculadoras"
        }
        
        results = {"directories": {}, "files": {}}
        
        # Check main directories
        for dir_name, description in required_dirs.items():
            path = self.project_root / dir_name
            exists = path.exists()
            status = "✅" if exists else "❌"
            print(f"  {status} {description:30} {str(path)}")
            results["directories"][dir_name] = exists
        
        # Check backend structure
        print("\n  Backend Structure:")
        for subdir, description in backend_subdirs.items():
            path = self.project_root / "backend" / subdir
            exists = path.exists()
            status = "✅" if exists else "❌"
            print(f"    {status} {description:25}")
            results["directories"][f"backend/{subdir}"] = exists
        
        # Check critical files
        print("\n  Critical Files:")
        critical_files = {
            "backend/main.py": "Backend entry point",
            "backend/requirements.txt": "Python dependencies",
            "frontend/App.tsx": "React entry point",
            "frontend/package.json": "Node dependencies",
            ".env.backend": "Backend config",
            "docker-compose.yml": "Docker orchestration"
        }
        
        for file_path, description in critical_files.items():
            full_path = self.project_root / file_path
            exists = full_path.exists()
            status = "✅" if exists else "❌"
            print(f"    {status} {description:30} {file_path}")
            results["files"][file_path] = exists
        
        self.results["filesystem"] = results
        print()
    
    async def check_dependencies(self):
        """Verifica dependencias instaladas"""
        print("📦 VERIFICANDO DEPENDENCIAS...")
        print("-" * 80)
        
        results = {
            "python_packages": {},
            "node_packages": {}
        }
        
        # Python packages
        print("  Python packages:")
        python_packages = [
            "fastapi", "pydantic", "sqlalchemy", "qdrant_client",
            "httpx", "python-dotenv", "groq", "google-generativeai",
            "openai", "sentence_transformers", "nltk"
        ]
        
        for package in python_packages:
            try:
                __import__(package)
                print(f"    ✅ {package:30}")
                results["python_packages"][package] = True
            except ImportError:
                print(f"    ❌ {package:30} - NOT INSTALLED")
                results["python_packages"][package] = False
        
        # Node packages (check package.json)
        print("\n  Node packages (frontend):")
        frontend_pkg = self.project_root / "frontend" / "package.json"
        if frontend_pkg.exists():
            with open(frontend_pkg) as f:
                pkg_data = json.load(f)
                deps = {**pkg_data.get("dependencies", {}), **pkg_data.get("devDependencies", {})}
                for dep_name in ["react", "typescript", "vite", "axios"]:
                    if dep_name in deps:
                        print(f"    ✅ {dep_name:30} {deps[dep_name]}")
                        results["node_packages"][dep_name] = True
                    else:
                        print(f"    ❌ {dep_name:30} - NOT FOUND")
                        results["node_packages"][dep_name] = False
        
        self.results["dependencies"] = results
        print()
    
    async def check_services(self):
        """Verifica servicios en ejecución"""
        print("🚀 VERIFICANDO SERVICIOS EN EJECUCIÓN...")
        print("-" * 80)
        
        results = {}
        
        services = [
            ("http://localhost:8000", "Backend FastAPI", "GET", "/docs"),
            ("http://localhost:6333", "Qdrant Vector DB", "GET", "/health"),
            ("http://localhost:5173", "Frontend React", "GET", "/"),
            ("http://localhost:3000", "MCP Server", "GET", "/status"),
            ("http://localhost:8080", "Mistral Local (VPS)", "GET", "/v1/models"),
            ("http://localhost:5432", "PostgreSQL", "POST", "")
        ]
        
        async with httpx.AsyncClient(timeout=2.0) as client:
            for base_url, name, method, path in services:
                try:
                    if method == "GET":
                        response = await client.get(f"{base_url}{path}")
                        status = response.status_code in [200, 404]
                        status_code = response.status_code
                    else:
                        # Skip POST for now
                        status = None
                        status_code = "SKIPPED"
                    
                    if status is None:
                        symbol = "⏭️ "
                    elif status:
                        symbol = "✅"
                    else:
                        symbol = "❌"
                    
                    print(f"  {symbol} {name:30} [{base_url}] → {status_code}")
                    results[name] = status
                
                except httpx.ConnectError:
                    print(f"  ❌ {name:30} [{base_url}] → CONNECTION REFUSED")
                    results[name] = False
                except Exception as e:
                    print(f"  ❌ {name:30} [{base_url}] → {str(e)[:30]}")
                    results[name] = False
        
        self.results["services"] = results
        print()
    
    async def check_configuration(self):
        """Verifica configuración"""
        print("⚙️  VERIFICANDO CONFIGURACIÓN...")
        print("-" * 80)
        
        results = {
            "env_vars": {},
            "config_files": {}
        }
        
        # Environment variables
        print("  Environment variables:")
        env_vars = [
            "QDRANT_URL",
            "QDRANT_API_KEY",
            "GROQ_API_KEY",
            "GEMINI_API_KEY",
            "DEEPSEEK_API_KEY",
            "DATABASE_URL",
            "EMBEDDING_MODEL"
        ]
        
        for var in env_vars:
            value = os.getenv(var)
            if value:
                masked = value[:10] + "..." if len(value) > 10 else value
                print(f"    ✅ {var:30} = {masked}")
                results["env_vars"][var] = True
            else:
                print(f"    ⚠️  {var:30} - NOT SET")
                results["env_vars"][var] = False
        
        # Config files
        print("\n  Config files:")
        config_files = {
            ".env.backend": "Backend config",
            "docker-compose.yml": "Docker config",
            "vite.config.ts": "Vite config"
        }
        
        for file_name, description in config_files.items():
            path = self.project_root / file_name
            exists = path.exists()
            status = "✅" if exists else "⚠️ "
            print(f"    {status} {description:30} {file_name}")
            results["config_files"][file_name] = exists
        
        self.results["configuration"] = results
        print()
    
    def generate_report(self):
        """Genera reporte final"""
        print("=" * 80)
        print("📊 REPORTE FINAL")
        print("=" * 80)
        print()
        
        # Filesystem check
        fs = self.results["filesystem"]
        fs_ok = all(fs["directories"].values()) and all(fs["files"].values())
        print(f"📁 Filesystem:           {'✅ OK' if fs_ok else '❌ NEEDS FIX'}")
        if not fs_ok:
            missing = [k for k, v in {**fs["directories"], **fs["files"]}.items() if not v]
            print(f"   Missing: {', '.join(missing[:3])}")
        
        # Dependencies check
        deps = self.results["dependencies"]
        py_ok = sum(deps["python_packages"].values()) >= 8
        node_ok = sum(deps["node_packages"].values()) >= 3
        print(f"📦 Python Dependencies:  {'✅ OK' if py_ok else '❌ NEEDS FIX'}")
        print(f"📦 Node Dependencies:    {'✅ OK' if node_ok else '❌ NEEDS FIX'}")
        
        # Services check
        services = self.results["services"]
        running = sum(1 for v in services.values() if v is True)
        total = len([v for v in services.values() if v is not None])
        print(f"🚀 Services Running:     {running}/{total} active")
        if running == 0:
            print(f"   ⚠️  No services running. Start them manually:")
            print(f"       Terminal 1: cd backend && python3 main.py")
            print(f"       Terminal 2: cd frontend && npm run dev")
        
        # Configuration check
        config = self.results["configuration"]
        env_ok = sum(config["env_vars"].values()) >= 5
        config_ok = all(config["config_files"].values())
        print(f"⚙️  Configuration:        {'✅ OK' if env_ok and config_ok else '⚠️  INCOMPLETE'}")
        
        print()
        print("=" * 80)
        print("🎯 NEXT STEPS")
        print("=" * 80)
        print()
        
        if running == 0:
            print("1. Start Backend:")
            print("   $ cd backend")
            print("   $ python3 main.py")
            print()
            print("2. Start Frontend (new terminal):")
            print("   $ cd frontend")
            print("   $ npm run dev")
            print()
            print("3. Test the system:")
            print("   $ python3 test_architecture.py --test chat")
            print("   $ python3 test_architecture.py --test rag")
            print("   $ python3 test_architecture.py --test case-gen")
        else:
            print("✅ System appears to be running!")
            print()
            print("Available endpoints:")
            print("  - Backend:  http://localhost:8000/docs")
            print("  - Frontend: http://localhost:5173")
            print("  - Qdrant:   http://localhost:6333")
        
        print()

async def main():
    """Función principal"""
    verifier = ArchitectureVerifier()
    await verifier.run_all_checks()

if __name__ == "__main__":
    asyncio.run(main())
