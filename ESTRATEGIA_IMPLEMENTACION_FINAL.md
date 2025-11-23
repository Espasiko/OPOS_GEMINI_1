# 🎯 ESTRATEGIA DE IMPLEMENTACIÓN FINAL - OPOSITAIA

**Fecha**: 23 Noviembre 2025  
**Complemento de**: PROPUESTAS_IDEAS_DESARROLLO.md  
**Estado**: Plan definitivo consolidado

---

## 📊 SISTEMA DE MONITORIZACIÓN DE TOKENS (CRÍTICO)

### Por qué es CRÍTICO:
- ⚠️ **Groq free tier**: 14,400 req/día (si pasas → error 429, NO cobro)
- ⚠️ **Mistral OCR**: €10 disponibles (si gastas todo → sin OCR)
- ⚠️ **Sin monitorización**: No sabes cuánto usas hasta que falla

### Implementación Completa:

```python
# backend/middleware/token_tracker.py
from datetime import datetime, timedelta
from typing import Dict, List
import asyncio
from collections import defaultdict

class TokenTracker:
    """Sistema completo de monitorización de tokens"""
    
    def __init__(self):
        self.usage_cache = defaultdict(list)  # Cache en memoria
        self.alerts_sent = set()  # Evitar spam de alertas
        
        # Límites por provider
        self.limits = {
            "groq": {
                "daily_requests": 14400,
                "per_minute": 30,
                "cost_per_1k_tokens": 0.0,  # GRATIS
                "warning_threshold": 0.80,  # Alerta al 80%
                "critical_threshold": 0.95  # Crítico al 95%
            },
            "mistral": {
                "budget_total": 10.0,  # €10 disponibles
                "cost_per_1k_tokens": 0.002,  # Ejemplo
                "warning_threshold": 0.80,
                "critical_threshold": 0.95
            },
            "gemini": {
                "daily_requests": 1500,  # Free tier
                "cost_per_1k_tokens": 0.0,
                "warning_threshold": 0.80,
                "critical_threshold": 0.95
            }
        }
    
    async def track_usage(
        self,
        user_id: str,
        feature: str,  # "chat", "flashcards", "mindmap", "summary", etc.
        provider: str,  # "groq", "mistral", "gemini"
        model: str,
        tokens_input: int,
        tokens_output: int,
        cost: float = 0.0,
        metadata: Dict = None
    ):
        """Registra cada uso de tokens con contexto completo"""
        
        usage_record = {
            "timestamp": datetime.now(),
            "user_id": user_id,
            "feature": feature,
            "provider": provider,
            "model": model,
            "tokens_input": tokens_input,
            "tokens_output": tokens_output,
            "tokens_total": tokens_input + tokens_output,
            "cost": cost,
            "metadata": metadata or {}
        }
        
        # Guardar en cache (en producción: PostgreSQL/Redis)
        self.usage_cache[provider].append(usage_record)
        
        # Verificar límites inmediatamente
        await self.check_limits(provider)
        
        # Limpiar cache antiguo (> 24h)
        await self.cleanup_old_records()
    
    async def check_limits(self, provider: str):
        """Verifica límites y envía alertas si es necesario"""
        
        if provider not in self.limits:
            return
        
        limit_config = self.limits[provider]
        usage_today = await self.get_daily_usage(provider)
        
        # GROQ: Verificar requests diarios
        if provider == "groq":
            requests_today = usage_today["total_requests"]
            max_requests = limit_config["daily_requests"]
            usage_percent = requests_today / max_requests
            
            if usage_percent >= limit_config["critical_threshold"]:
                await self.send_alert(
                    level="CRITICAL",
                    provider=provider,
                    message=f"🚨 GROQ CRÍTICO: {requests_today}/{max_requests} requests ({usage_percent:.1%})"
                )
            elif usage_percent >= limit_config["warning_threshold"]:
                await self.send_alert(
                    level="WARNING",
                    provider=provider,
                    message=f"⚠️ Groq: {requests_today}/{max_requests} requests ({usage_percent:.1%})"
                )
        
        # MISTRAL: Verificar presupuesto
        elif provider == "mistral":
            cost_today = usage_today["total_cost"]
            budget = limit_config["budget_total"]
            usage_percent = cost_today / budget
            
            if usage_percent >= limit_config["critical_threshold"]:
                await self.send_alert(
                    level="CRITICAL",
                    provider=provider,
                    message=f"🚨 MISTRAL CRÍTICO: €{cost_today:.2f}/€{budget} ({usage_percent:.1%})"
                )
            elif usage_percent >= limit_config["warning_threshold"]:
                await self.send_alert(
                    level="WARNING",
                    provider=provider,
                    message=f"⚠️ Mistral: €{cost_today:.2f}/€{budget} ({usage_percent:.1%})"
                )
    
    async def get_daily_usage(self, provider: str) -> Dict:
        """Obtiene uso del día actual"""
        today = datetime.now().date()
        records = [
            r for r in self.usage_cache[provider]
            if r["timestamp"].date() == today
        ]
        
        return {
            "total_requests": len(records),
            "total_tokens": sum(r["tokens_total"] for r in records),
            "total_cost": sum(r["cost"] for r in records),
            "by_feature": self._group_by_feature(records),
            "by_user": self._group_by_user(records),
            "by_model": self._group_by_model(records)
        }
    
    async def get_usage_report(
        self,
        period: str = "daily",  # "daily", "weekly", "monthly"
        provider: str = None
    ) -> Dict:
        """Genera reporte completo de uso"""
        
        if period == "daily":
            start_date = datetime.now() - timedelta(days=1)
        elif period == "weekly":
            start_date = datetime.now() - timedelta(days=7)
        elif period == "monthly":
            start_date = datetime.now() - timedelta(days=30)
        
        providers = [provider] if provider else self.usage_cache.keys()
        
        report = {}
        for prov in providers:
            records = [
                r for r in self.usage_cache[prov]
                if r["timestamp"] >= start_date
            ]
            
            report[prov] = {
                "total_requests": len(records),
                "total_tokens": sum(r["tokens_total"] for r in records),
                "total_cost": sum(r["cost"] for r in records),
                "by_feature": self._group_by_feature(records),
                "by_user": self._group_by_user(records),
                "by_model": self._group_by_model(records),
                "by_day": self._group_by_day(records)
            }
        
        return report
    
    async def send_alert(self, level: str, provider: str, message: str):
        """Envía alerta (email, Slack, Discord, etc.)"""
        alert_key = f"{provider}_{level}_{datetime.now().date()}"
        
        # Evitar spam (1 alerta por día por nivel)
        if alert_key in self.alerts_sent:
            return
        
        self.alerts_sent.add(alert_key)
        
        # Aquí implementar envío real (email, Slack, etc.)
        print(f"[{level}] {message}")
        
        # TODO: Enviar email
        # await send_email(to="admin@opositaia.com", subject=f"[{level}] {provider}", body=message)
        
        # TODO: Enviar a Slack/Discord
        # await send_slack_message(message)
    
    def _group_by_feature(self, records: List[Dict]) -> Dict:
        """Agrupa por feature"""
        grouped = defaultdict(lambda: {"requests": 0, "tokens": 0, "cost": 0.0})
        for r in records:
            grouped[r["feature"]]["requests"] += 1
            grouped[r["feature"]]["tokens"] += r["tokens_total"]
            grouped[r["feature"]]["cost"] += r["cost"]
        return dict(grouped)
    
    def _group_by_user(self, records: List[Dict]) -> Dict:
        """Agrupa por usuario"""
        grouped = defaultdict(lambda: {"requests": 0, "tokens": 0, "cost": 0.0})
        for r in records:
            grouped[r["user_id"]]["requests"] += 1
            grouped[r["user_id"]]["tokens"] += r["tokens_total"]
            grouped[r["user_id"]]["cost"] += r["cost"]
        return dict(grouped)
    
    def _group_by_model(self, records: List[Dict]) -> Dict:
        """Agrupa por modelo"""
        grouped = defaultdict(lambda: {"requests": 0, "tokens": 0, "cost": 0.0})
        for r in records:
            grouped[r["model"]]["requests"] += 1
            grouped[r["model"]]["tokens"] += r["tokens_total"]
            grouped[r["model"]]["cost"] += r["cost"]
        return dict(grouped)
    
    def _group_by_day(self, records: List[Dict]) -> Dict:
        """Agrupa por día"""
        grouped = defaultdict(lambda: {"requests": 0, "tokens": 0, "cost": 0.0})
        for r in records:
            day = r["timestamp"].date().isoformat()
            grouped[day]["requests"] += 1
            grouped[day]["tokens"] += r["tokens_total"]
            grouped[day]["cost"] += r["cost"]
        return dict(grouped)
    
    async def cleanup_old_records(self):
        """Limpia registros antiguos (> 30 días)"""
        cutoff = datetime.now() - timedelta(days=30)
        for provider in self.usage_cache:
            self.usage_cache[provider] = [
                r for r in self.usage_cache[provider]
                if r["timestamp"] >= cutoff
            ]

# Instancia global
tracker = TokenTracker()
```

### Uso en cada endpoint:

```python
# backend/routers/chat.py
from middleware.token_tracker import tracker

@app.post("/api/chat")
async def chat(message: str, user_id: str):
    # Llamar a Groq
    response = await groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": message}]
    )
    
    # TRACK INMEDIATAMENTE
    await tracker.track_usage(
        user_id=user_id,
        feature="chat",
        provider="groq",
        model=response.model,
        tokens_input=response.usage.prompt_tokens,
        tokens_output=response.usage.completion_tokens,
        cost=0.0,  # Groq es gratis
        metadata={"endpoint": "/api/chat"}
    )
    
    return response.choices[0].message.content

@app.post("/api/flashcards")
async def generate_flashcards(topic: str, user_id: str):
    response = await groq_client.chat.completions.create(...)
    
    await tracker.track_usage(
        user_id=user_id,
        feature="flashcards",  # ← Diferente feature
        provider="groq",
        model=response.model,
        tokens_input=response.usage.prompt_tokens,
        tokens_output=response.usage.completion_tokens,
        cost=0.0
    )
    
    return response

@app.post("/api/ocr")
async def extract_pdf_text(pdf_file: bytes, user_id: str):
    # Verificar presupuesto ANTES de usar Mistral
    usage = await tracker.get_daily_usage("mistral")
    if usage["total_cost"] >= 9.5:  # Límite de seguridad
        raise HTTPException(
            status_code=429,
            detail="Presupuesto Mistral OCR agotado por hoy"
        )
    
    response = await mistral_client.ocr.extract(file=pdf_file)
    
    await tracker.track_usage(
        user_id=user_id,
        feature="ocr",
        provider="mistral",
        model="pixtral-12b",
        tokens_input=0,
        tokens_output=len(response.text.split()),
        cost=0.10,  # Estimar coste
        metadata={"file_size": len(pdf_file)}
    )
    
    return response.text
```

### Dashboard de Monitorización:

```python
# backend/routers/admin.py
@app.get("/api/admin/usage-dashboard")
async def usage_dashboard(period: str = "daily"):
    """Dashboard de uso para admin"""
    report = await tracker.get_usage_report(period=period)
    
    return {
        "period": period,
        "providers": report,
        "alerts": {
            "groq": await tracker.check_limits("groq"),
            "mistral": await tracker.check_limits("mistral")
        },
        "recommendations": generate_recommendations(report)
    }

def generate_recommendations(report: Dict) -> List[str]:
    """Genera recomendaciones basadas en uso"""
    recommendations = []
    
    # Groq
    if "groq" in report:
        groq_usage = report["groq"]["total_requests"]
        if groq_usage > 10000:
            recommendations.append(
                "⚠️ Uso alto de Groq (>10K req/día). Considera implementar caché."
            )
    
    # Mistral
    if "mistral" in report:
        mistral_cost = report["mistral"]["total_cost"]
        if mistral_cost > 8.0:
            recommendations.append(
                "🚨 Presupuesto Mistral casi agotado (€{:.2f}/€10). Limitar uso de OCR.".format(mistral_cost)
            )
    
    return recommendations
```

---

