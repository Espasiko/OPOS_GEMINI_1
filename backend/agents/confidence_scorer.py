"""
Confidence Scorer - Heurísticas de calidad
"""
import logging
from typing import Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ConfidenceScore:
    """Score de confianza del caso"""
    overall: float  # 0-1
    breakdown: Dict[str, float]
    level: str  # ALTA/MEDIA/BAJA
    issues: list


class ConfidenceScorer:
    """
    Calcula confidence score basado en heurísticas
    NO incluye velocity (requiere feedback de usuarios)
    """
    
    @staticmethod
    def calculate_confidence(caso: Dict[str, Any]) -> ConfidenceScore:
        """
        Calcula confidence score del caso
        
        Args:
            caso: Caso práctico generado
        
        Returns:
            ConfidenceScore con desglose
        """
        scores = {
            'estructura': ConfidenceScorer._score_estructura(caso),
            'citas_legales': ConfidenceScorer._score_citas(caso),
            'calculos': ConfidenceScorer._score_calculos(caso),
            'logica': ConfidenceScorer._score_logica(caso),
            'claridad': ConfidenceScorer._score_claridad(caso)
        }
        
        issues = []
        
        # Weighted average
        confidence = (
            scores['estructura'] * 0.20 +
            scores['citas_legales'] * 0.25 +
            scores['calculos'] * 0.25 +
            scores['logica'] * 0.20 +
            scores['claridad'] * 0.10
        )
        
        # Determinar nivel
        if confidence >= 0.85:
            level = 'ALTA'
        elif confidence >= 0.70:
            level = 'MEDIA'
            issues.append("Confidence media - revisar antes de usar")
        else:
            level = 'BAJA'
            issues.append("Confidence baja - NO usar sin validación manual")
        
        # Identificar issues específicos
        for key, score in scores.items():
            if score < 0.7:
                issues.append(f"{key}: score bajo ({score:.2f})")
        
        logger.info(f"Confidence calculated: {confidence:.2f} ({level})")
        
        return ConfidenceScore(
            overall=confidence,
            breakdown=scores,
            level=level,
            issues=issues
        )
    
    @staticmethod
    def _score_estructura(caso: Dict[str, Any]) -> float:
        """Score basado en estructura del caso"""
        score = 0.0
        checks = 0
        
        # Campos requeridos
        required = ['enunciado', 'pregunta', 'opciones', 'respuesta_correcta', 'explicacion']
        for field in required:
            checks += 1
            if field in caso and caso[field]:
                score += 1.0
        
        # Opciones completas
        checks += 1
        if 'opciones' in caso and isinstance(caso['opciones'], dict):
            if set(caso['opciones'].keys()) == {'A', 'B', 'C', 'D'}:
                score += 1.0
        
        return score / checks if checks > 0 else 0.0
    
    @staticmethod
    def _score_citas(caso: Dict[str, Any]) -> float:
        """Score basado en citas legales"""
        explicacion = caso.get('explicacion', '')
        
        # Buscar patrones de citas
        tiene_articulo = 'art' in explicacion.lower() or 'artículo' in explicacion.lower()
        tiene_ley = any(ley in explicacion.upper() for ley in ['LGSS', 'TRLGSS', 'RD'])
        tiene_numero = any(char.isdigit() for char in explicacion)
        
        score = sum([tiene_articulo, tiene_ley, tiene_numero]) / 3.0
        
        return score
    
    @staticmethod
    def _score_calculos(caso: Dict[str, Any]) -> float:
        """Score basado en precisión de cálculos"""
        # Si hay metadata con cálculo usado (calculadora SS)
        if 'metadata' in caso and 'calculo_usado' in caso['metadata']:
            # Calculadora SS siempre es 100% precisa
            return 1.0
        
        # Si el caso tiene cálculos en la explicación, verificar
        explicacion = caso.get('explicacion', '').lower()
        
        # Buscar patrones de cálculos
        tiene_division = '/' in explicacion or '÷' in explicacion
        tiene_multiplicacion = '×' in explicacion or '*' in explicacion
        tiene_porcentaje = '%' in explicacion
        tiene_numeros = any(char.isdigit() for char in explicacion)
        
        if tiene_division and tiene_multiplicacion and tiene_porcentaje:
            return 1.0  # Cálculo completo mostrado
        elif tiene_numeros and (tiene_division or tiene_multiplicacion):
            return 0.8  # Cálculo parcial
        
        # Sin cálculo verificable
        return 0.7  # Neutral
    
    @staticmethod
    def _score_logica(caso: Dict[str, Any]) -> float:
        """Score basado en lógica legal"""
        explicacion = caso.get('explicacion', '').lower()
        
        # Heurísticas de buena explicación
        tiene_porque = 'porque' in explicacion or 'ya que' in explicacion
        tiene_por_tanto = 'por tanto' in explicacion or 'por lo tanto' in explicacion
        no_vago = not any(vago in explicacion for vago in ['quizás', 'probablemente', 'puede que', 'tal vez'])
        longitud_ok = len(explicacion) > 100  # Al menos 100 caracteres
        
        score = sum([tiene_porque, tiene_por_tanto, no_vago, longitud_ok]) / 4.0
        
        return score
    
    @staticmethod
    def _score_claridad(caso: Dict[str, Any]) -> float:
        """Score basado en claridad del enunciado"""
        enunciado = caso.get('enunciado', '')
        pregunta = caso.get('pregunta', '')
        
        # Heurísticas
        longitud_ok = 100 <= len(enunciado) <= 500
        tiene_pregunta = '¿' in pregunta
        no_ambiguo = not any(amb in enunciado.lower() for amb in ['tal vez', 'posiblemente', 'quizás'])
        
        score = sum([longitud_ok, tiene_pregunta, no_ambiguo]) / 3.0
        
        return score
