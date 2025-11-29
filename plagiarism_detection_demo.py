#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔬 SCRIPT DE DETECCIÓN DE PLAGIO EN FINE-TUNING
Mide: BLEU, ROUGE, Cosine Similarity, N-gram Overlap
Propósito: Educativo - entender qué es detectable

USO:
    python3 plagiarism_detection_demo.py
"""

import re
from collections import Counter
from math import log
import numpy as np

# ============================================================================
# 1. MÉTRICAS DE SIMILITUD
# ============================================================================

def extract_ngrams(text, n=2):
    """Extrae n-gramas (palabras consecutivas)"""
    words = text.lower().split()
    return [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]

def bleu_score(reference, candidate, max_n=4):
    """
    Calcula BLEU score (0-1, donde 1 = idéntico)
    Mide overlap de n-gramas entre reference y candidate
    """
    ref_words = reference.lower().split()
    cand_words = candidate.lower().split()
    
    scores = []
    for n in range(1, min(max_n + 1, len(cand_words) + 1)):
        ref_ngrams = Counter(extract_ngrams(reference, n))
        cand_ngrams = Counter(extract_ngrams(candidate, n))
        
        matches = sum((ref_ngrams & cand_ngrams).values())
        total = sum(cand_ngrams.values())
        
        if total > 0:
            scores.append(matches / total)
        else:
            scores.append(0)
    
    return sum(scores) / len(scores) if scores else 0

def ngram_overlap_percent(text1, text2, n=2):
    """
    Porcentaje de n-gramas compartidos entre dos textos
    """
    ngrams1 = set(extract_ngrams(text1.lower(), n))
    ngrams2 = set(extract_ngrams(text2.lower(), n))
    
    if not ngrams1 or not ngrams2:
        return 0
    
    overlap = len(ngrams1 & ngrams2)
    total = len(ngrams1 | ngrams2)
    
    return (overlap / total * 100) if total > 0 else 0

def cosine_similarity_simple(text1, text2):
    """
    Similitud coseno basada en frecuencia de palabras
    (Aproximación simple, sin embeddings complejos)
    Rango: 0-1, donde 1 = idéntico
    """
    words1 = text1.lower().split()
    words2 = text2.lower().split()
    
    counter1 = Counter(words1)
    counter2 = Counter(words2)
    
    all_words = set(counter1.keys()) | set(counter2.keys())
    
    vec1 = [counter1.get(w, 0) for w in all_words]
    vec2 = [counter2.get(w, 0) for w in all_words]
    
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = sum(a ** 2 for a in vec1) ** 0.5
    norm2 = sum(b ** 2 for b in vec2) ** 0.5
    
    if norm1 == 0 or norm2 == 0:
        return 0
    
    return dot_product / (norm1 * norm2)

def longest_common_substring(text1, text2):
    """Encuentra la substring más larga común entre dos textos"""
    words1 = text1.lower().split()
    words2 = text2.lower().split()
    
    m, n = len(words1), len(words2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_len = 0
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if words1[i-1] == words2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                max_len = max(max_len, dp[i][j])
    
    return max_len

# ============================================================================
# 2. PREDICCIÓN DE RIESGO
# ============================================================================

def predict_detection_risk(original, paraphrased):
    """
    Calcula riesgo de detección basado en múltiples métricas
    Retorna: (riesgo: str, score: float, detalles: dict)
    """
    metrics = {
        'bleu': bleu_score(original, paraphrased),
        'ngram_overlap_2': ngram_overlap_percent(original, paraphrased, 2),
        'ngram_overlap_3': ngram_overlap_percent(original, paraphrased, 3),
        'cosine': cosine_similarity_simple(original, paraphrased),
        'lcs_words': longest_common_substring(original, paraphrased)
    }
    
    # Scoring: promedio ponderado
    risk_score = (
        metrics['bleu'] * 0.3 +
        (metrics['ngram_overlap_2'] / 100) * 0.3 +
        metrics['cosine'] * 0.4
    )
    
    # Interpretación
    if risk_score < 0.20:
        risk = "BAJO"
        detail = "Muy diferente - baja probabilidad de detección técnica"
    elif risk_score < 0.40:
        risk = "BAJO-MEDIO"
        detail = "Bastante diferente - difícil detección automática"
    elif risk_score < 0.60:
        risk = "MEDIO"
        detail = "Similitud moderada - herramientas estándar lo detectarían"
    elif risk_score < 0.80:
        risk = "ALTO"
        detail = "Muy similar - fácil detección con BLEU/ROUGE"
    else:
        risk = "CRÍTICO"
        detail = "Casi idéntico - detección trivial"
    
    return risk, risk_score, metrics, detail

# ============================================================================
# 3. EJEMPLOS PARA DEMOSTRACIÓN
# ============================================================================

EXAMPLES = {
    "ejemplo_1_obvious": {
        "titulo": "❌ PLAGIO OBVIO (Copia exacta)",
        "original": "La Ley General de la Seguridad Social (LGSS), aprobada por Real Decreto Legislativo 8/2015, de 30 de octubre, es la norma fundamental que regula el sistema de protección social en España. La LGSS se aplica a los trabajadores por cuenta ajena y por cuenta propia.",
        "parafraseo": "La Ley General de la Seguridad Social (LGSS), aprobada por Real Decreto Legislativo 8/2015, de 30 de octubre, es la norma fundamental que regula el sistema de protección social en España. La LGSS se aplica a los trabajadores por cuenta ajena y por cuenta propia.",
    },
    
    "ejemplo_2_superficial": {
        "titulo": "⚠️ PARAFRASEO SUPERFICIAL (Cambios mínimos)",
        "original": "La Ley General de la Seguridad Social (LGSS), aprobada por Real Decreto Legislativo 8/2015, de 30 de octubre, es la norma fundamental que regula el sistema de protección social en España.",
        "parafraseo": "La Ley sobre la protección del sistema social, conocida como LGSS y aprobada mediante el Real Decreto Legislativo 8/2015, es la ley más importante para regular los temas de protección social en España.",
    },
    
    "ejemplo_3_decent": {
        "titulo": "✅ PARAFRASEO DECENTE (Reformulación moderada)",
        "original": "La LGSS se aplica a trabajadores por cuenta ajena y cuenta propia. Cubre enfermedad, maternidad, invalidez, vejez y muerte.",
        "parafraseo": "El sistema protege tanto a empleados como a autónomos. Las contingencias cubiertas incluyen riesgos de salud, eventos reproductivos, incapacidad laboral, jubilación y fallecimiento.",
    },
    
    "ejemplo_4_strong": {
        "titulo": "✅✅ TRANSFORMACIÓN PROFUNDA (Muy diferente)",
        "original": "La Seguridad Social protege a trabajadores ante enfermedad, desempleo y jubilación mediante un sistema de contribuciones.",
        "parafraseo": "Un modelo de protección social basado en aportaciones de empleados y empresas cubre contingencias laborales como problemas de salud, pérdida de empleo y fin de la vida laboral.",
    },
}

# ============================================================================
# 4. MAIN: MOSTRAR RESULTADOS
# ============================================================================

def main():
    print("\n" + "="*80)
    print("🔬 ANÁLISIS DE DETECTABILIDAD EN FINE-TUNING")
    print("="*80)
    print("\nDemostración: Cómo se detectan plagio/parafraseo en outputs de modelos IA")
    print("\n" + "-"*80)
    
    for key, example in EXAMPLES.items():
        print(f"\n{example['titulo']}")
        print("-" * 80)
        
        original = example['original']
        parafraseo = example['parafraseo']
        
        print(f"\n📝 ORIGINAL ({len(original.split())} palabras):")
        print(f"   {original[:100]}...")
        
        print(f"\n✏️ PARAFRASEO ({len(parafraseo.split())} palabras):")
        print(f"   {parafraseo[:100]}...")
        
        risk, score, metrics, detail = predict_detection_risk(original, parafraseo)
        
        print(f"\n📊 MÉTRICAS:")
        print(f"   • BLEU score:        {metrics['bleu']:.3f} (0=diferente, 1=idéntico)")
        print(f"   • N-gram 2 overlap:  {metrics['ngram_overlap_2']:.1f}%")
        print(f"   • N-gram 3 overlap:  {metrics['ngram_overlap_3']:.1f}%")
        print(f"   • Cosine similarity: {metrics['cosine']:.3f}")
        print(f"   • LCS común:         {metrics['lcs_words']} palabras")
        
        print(f"\n🚨 RIESGO DETECCIÓN: {risk}")
        print(f"   Score: {score:.2f}/1.00")
        print(f"   → {detail}")
        
        # Interpretación para herramientas reales
        print(f"\n🔍 ¿Qué herramientas lo detectarían?")
        if score < 0.20:
            print(f"   ❌ Turnitin/Copyscape:      NO")
            print(f"   ❌ BLEU/ROUGE analysis:     NO")
            print(f"   ❌ Google Scholar:          NO")
        elif score < 0.40:
            print(f"   ⚠️ Turnitin/Copyscape:      Probablemente NO")
            print(f"   ⚠️ BLEU/ROUGE analysis:     NO")
            print(f"   ❌ Google Scholar:          NO")
        elif score < 0.60:
            print(f"   ✅ Turnitin/Copyscape:      SÍ (puede flagear)")
            print(f"   ⚠️ BLEU/ROUGE analysis:     Posible")
            print(f"   ❌ Google Scholar:          Probablemente no")
        else:
            print(f"   ✅ Turnitin/Copyscape:      SÍ (definitivo)")
            print(f"   ✅ BLEU/ROUGE analysis:     SÍ (obvio)")
            print(f"   ✅ Google Scholar:          SÍ")
    
    # Tabla resumen
    print("\n" + "="*80)
    print("📊 TABLA RESUMEN: ¿CUÁNDO ES SEGURO USAR MATERIAL?")
    print("="*80)
    
    print("""
┌─────────────────────────────────────────────────────────────────────────┐
│ BLEU Score / Risk | Interpretación                  | Recomendación     │
├─────────────────────────────────────────────────────────────────────────┤
│ 0.00 - 0.20       | Muy diferente (parafraseo fuerte)| ✅ MÁS SEGURO    │
│                   | Baja detectabilidad técnica       |                   │
├─────────────────────────────────────────────────────────────────────────┤
│ 0.20 - 0.40       | Bastante diferente (reforma buena)| ⚠️  MEDIO RIESGO│
│                   | Difícil para herramientas auto    |                   │
├─────────────────────────────────────────────────────────────────────────┤
│ 0.40 - 0.60       | Moderadamente similar (paraf.sup.)| ⚠️  ALTO RIESGO │
│                   | Detectable con BLEU/ROUGE        |                   │
├─────────────────────────────────────────────────────────────────────────┤
│ 0.60 - 0.80       | Muy similar (copia light)        | ❌ MUY ALTO RIESGO│
│                   | Fácil detección automática        |                   │
├─────────────────────────────────────────────────────────────────────────┤
│ 0.80 - 1.00       | Casi idéntico (copia clara)      | ❌ CRÍTICO        │
│                   | Detección trivial                |                   │
└─────────────────────────────────────────────────────────────────────────┘
""")
    
    print("\n" + "="*80)
    print("💡 CONCLUSIONES PARA TU CASO")
    print("="*80)
    
    print("""
1. ¿Si parafraseo material academia (1%), ¿se detecta?
   → Depende de CÓMO lo parafrasees:
     • Copiar tal cual (0% cambios)           → DETECTADO 100%
     • Cambiar palabras (superficial)         → DETECTABLE (60-80% riesgo)
     • Reformular profundo (estructura nueva) → BAJO RIESGO TÉCNICO (~20%)
     • Transformación muy profunda           → CASI IMPOSIBLE (~5% riesgo)

2. ¿Pero legalmente es seguro?
   → NO. Incluso si parafrasea perfectamente, la academia puede:
      • Demostrar intención (tienes su PDF)
      • Probar similitud semántica profunda
      • Recurrir legalmente aunque técnicamente no sea detectable

3. ¿Entonces qué hacer?
   → OPCIÓN A: Usar 100% datos públicos (SEGURO)
   → OPCIÓN B: Contactar academia 5 minutos (SEGURO)
   → OPCIÓN C: Asumir riesgo (transformar profundo, mantener privado, rezar)

4. ¿Tiempo estimado?
   • Recolectar datos públicos (BOE):  ~2-3 horas
   • Contactar academias:              ~30 minutos
   • Esperar respuesta:                ~5-7 días
   • Entrenar modelo:                  ~2-4 horas (Colab)
   
   TOTAL RUTA SEGURA: ~1 semana (99% seguridad legal + técnica)
   TOTAL RUTA RIESGOSA: ~3 días (5% riesgo legal + 20% técnico)
""")
    
    print("\n" + "="*80)
    print("✅ FIN DE DEMOSTRACIÓN")
    print("="*80)
    print("\nPara más información, ver: DEMO_DETECCION_PLAGIO_FINETUNE.md")
    print("\n")

if __name__ == "__main__":
    main()
