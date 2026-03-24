# Comparativa: Jorge Cuesta vs. Estándar DM (Diego de Miguel)

Tras analizar los casos reales de DM (Enero, Febrero, Ejercicios 18 y 19), he identificado por qué el caso de Jorge Cuesta te parece "simple". Aquí tienes el diagnóstico del GAP de sofisticación:

## 1. La Estructura de Personajes (El "Putojorge" es un llanero solitario)
| Característica | Jorge Cuesta (V14 actual) | Casos Reales DM (Enero/Feb/18/19) |
| :--- | :--- | :--- |
| **Número de Actores** | **1 protagonista** + mención a empresa. | **Min. 4-6 personajes** con nombres propios y parentescos. |
| **Entrelazamiento** | Lineal. Jorge quiere jubilarse y se jubila. | **Red**. María Ángeles y José Alberto (compañeros), Sergio y Alba (socios administradores), Carmelo (hijo conviviente), Javier (marido sin actividad). |
| **Conflictos Cruzados** | Ninguno. Solo cálculos. | **Múltiples**. Impago de empresa + accidente de trabajo + embargo de garaje personal + incapacidad de un primo. |

## 2. La Complejidad de las Preguntas (El "Salto de Régimen")
| Niveles de Trampa | Jorge Cuesta (V14 actual) | Estándar DM |
| :--- | :--- | :--- |
| **Focalización** | 100% Jubilación. | **Híbrido**. Empieza con Encuadramiento (¿RETA o General?), salta a Recaudación (¿Providencia o Reclamación?) y acaba en Jubilación Activa. |
| **Cambio de Rumbo** | Narrativa estática. | **Narrativa evolutiva**. "En junio Alicia empieza reducción de jornada... en noviembre tiene un parto... luego IT...". |
| **Trampa de Parentesco** | Ausente. | **Crítica**. "Contrata a su hijo Jacinto de 34 años con discapacidad" (Lógica de exclusión de desempleo). |

## 3. Elementos "DM" Ausentes en Jorge Cuesta
1. **La Empresa no es un decorado:** En los casos de DM, la empresa tiene problemas (impagos, concursos, cambios de estatutos). En Jorge Cuesta, la empresa solo es "Desengaño 21 SL".
2. **Datos de "Relleno Inteligente":** DM añade datos que no sirven para nada o que son distractores puros (ej. "nació en Villacastín, a 40km", "tickets de compra justificados"). Jorge Cuesta es demasiado directo.
3. **El "Vuelco" de los 15 días:** DM siempre pregunta por plazos de notificación vs emisión (Trampa C11/C12 de nuestro catálogo).

## 4. Conclusión del Análisis
El "Putojorge" es un **Cálculo Matemático Perfecto**, pero una **Narrativa Pedagógica Pobre**. 
- **Fallo:** El `CaseSchemaBuilder` solo inyecta el tema principal (JubilaciónS12). 
- **Solución:** Necesitamos que el Builder elija **3 temas MINIMO, HASTA 8 PUEDE LLEGAR** (Encuadramiento + Recaudación + Jubilación) y cree una **Red de Personajes** (Jefe, Empleado, Familiar) antes de pasarle el testigo al Redactor.

**¿Quieres que modifique el `CaseSchemaBuilder` para que obligatoriamente mezcle 3 personajes y 2 temas secundarios en cada caso?**
