# TEMAS UTILIZADOS EN LAS 50 Q&A COPILOT VS

*Fecha: 6 de diciembre de 2025*  
*Dataset: qa_verificadas_boe_copilot_vs (50 Q&A)*

## 📋 LISTADO DE TEMAS CUBIERTOS

### ✅ TEMAS YA UTILIZADOS (23 temas diferentes):

1. **Afiliación y altas/bajas**
   - Altas y bajas de trabajadores
   - Obligación de afiliación

2. **Cálculos de prestaciones**
   - Métodos de cálculo
   - Bases reguladoras

3. **Complementos pensiones**
   - Complemento brecha de género
   - Complementos a mínimos

4. **Convenios internacionales SS**
   - Totalización períodos
   - Exportación prestaciones

5. **Entidades gestoras - INSS**
   - Competencias INSS
   - Gestión prestaciones

6. **Gestión recaudatoria - TGSS**
   - Competencias TGSS
   - Prescripción deudas

7. **IMV - Ingreso Mínimo Vital**
   - Requisitos acceso
   - Compatibilidades

8. **Infracciones y sanciones SS**
   - Tipos infracciones
   - Graduación sanciones

9. **Jubilación anticipada**
   - Jubilación parcial
   - Requisitos anticipada

10. **Maternidad y paternidad**
    - Prestación maternidad
    - Prestación paternidad

11. **Mutuas colaboradoras**
    - Gestión AT/EP
    - Adscripción empresas

12. **Prestaciones específicas**
    - Riesgo embarazo
    - Cuidado menores cáncer

13. **Prestaciones no contributivas**
    - PNC invalidez
    - Requisitos acceso

14. **Procedimiento administrativo SS**
    - Tramitación expedientes
    - Plazos resolución

15. **Régimen Especial Agrario**
    - Campo aplicación
    - Peculiaridades REA

16. **Recaudación y gestión**
    - Obligación cotización
    - Plazos de ingreso

17. **Responsabilidades empresariales**
    - Recargo prestaciones
    - Responsabilidad solidaria

18. **RETA - Autónomos**
    - Campo aplicación RETA
    - Cotización autónomos

19. **Sistema RED**
    - Transmisión electrónica datos
    - Obligatoriedad uso

20. **Incapacidad Temporal** (temas muerte/supervivencia)
21. **Incapacidad Permanente**
22. **Pensiones supervivencia**
23. **Cotización y bases**

---

## 🚫 TEMAS PENDIENTES DEL TEMARIO OFICIAL

Para evitar repeticiones en futuros datasets, estos temas AÚN NO se han utilizado:

- Prestaciones familiares específicas
- Regímenes especiales marineros/minería
- Seguridad Social Clases Pasivas
- Sistemas complementarios (planes pensiones)
- Asistencia social
- Normativa europea específica
- Procedimientos judiciales SS
- Control e inspección SS
- Estadísticas y memoria anual
- Tesorería y patrimonio SS
- Y otros del temario completo...

---

## 📊 ESTADÍSTICAS DE COBERTURA

- **Total Q&A generadas**: 50
- **Temas únicos cubiertos**: 23
- **Promedio Q&A por tema**: 2.2
- **Verificación BOE**: 100% de las Q&A
- **Score calidad**: >98% todas las Q&A
- **Formato**: Oposiciones realistas nivel C1

---

## 🎯 RECOMENDACIONES PARA FUTUROS DATASETS

1. **NO repetir** estos 23 temas para mantener variedad
2. **Priorizar** temas pendientes del temario oficial
3. **Mantener** verificación BOE API
4. **Seguir** estructura realista oposiciones
5. **Diversificar** niveles de dificultad

---

## 🚀 **PROPUESTA: ORQUESTADOR INTELIGENTE**

### **Concepto del Script Orquestador:**

En lugar de un script monolítico de 50 Q&A (que tiene limitaciones de tokens, rate limits BOE y control de calidad), se propone un **orquestador inteligente** que:

#### **Funcionamiento:**
```python
def orquestador_50_qa():
    """Ejecuta automáticamente scripts pequeños hasta completar 50"""
    
    while count_qa < 50:
        qa_restantes = 50 - count_qa
        lote_size = min(10, qa_restantes)  # Lotes de máximo 10
        
        # Elegir tema siguiente automáticamente del temario
        tema_siguiente = elegir_tema_no_usado()
        
        # Ejecutar script pequeño especializado
        ejecutar_script_lote(tema_siguiente, lote_size)
        
        # Verificar y continuar
        count_qa = contar_qa_totales()
        
    consolidar_dataset_final()
```

#### **Ventajas del Orquestador:**
- ✅ **Rotación automática** de temas del temario completo
- ✅ **No repetición** - evita temas ya usados
- ✅ **Cobertura completa** del temario oficial 36+ temas
- ✅ **Guardado incremental** - no se pierde trabajo si falla
- ✅ **Rate limiting automático** para BOE API
- ✅ **Control granular** de calidad por lotes
- ✅ **Debugging fácil** - fallo aislado por lote
- ✅ **Respeta límites** de memoria y contexto

#### **Por qué NO script único:**
- ❌ Temario completo = 50,000+ tokens (satura contexto)
- ❌ Rate limits BOE API (429 Too Many Requests)
- ❌ Difícil control de calidad en lote grande
- ❌ Si falla Q&A 40, se pierde todo el trabajo
- ❌ Alto consumo RAM/procesamiento

### **Modelo de IA utilizado:**
- **Modelo actual**: Claude Sonnet 4 (GitHub Copilot)
- **Cambio modelo UI**: Automático e inmediato en VS Code
- **Scripts Python**: Requieren configuración propia de API keys
- **Independencia**: Scripts no heredan modelo del IDE

---

*Archivo generado automáticamente el 6/12/2025*
*Proyecto: OPOS_GEMINI_1 - Sistema Q&A Verificado BOE*