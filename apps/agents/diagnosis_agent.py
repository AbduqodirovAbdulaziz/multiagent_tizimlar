"""
Diagnosis Agent - Diagnoz qo'yuvchi agent.

Bu agent simptomlar va tahlillar asosida diagnoz qo'yadi.
"""
from typing import Dict, Any, List
from .base import BaseAgent
from apps.diagnostics.models import DiseasePattern


class DiagnosisAgent(BaseAgent):
    """
    Diagnoz agenti.
    
    Vazifalar:
    - Simptomlar va tahlillar asosida diagnoz qo'yish
    - Kasallik ehtimolligini hisoblash
    - Eng mos keladigan kasalliklarni topish
    """
    
    def __init__(self):
        super().__init__('diagnosis_agent')
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Diagnoz qo'yish.
        
        Args:
            input_data: {
                'symptom_analysis': Dict,
                'analysis_results': Dict,
                'session_id': str
            }
        
        Returns:
            {
                'diagnoses': List[Dict],
                'confidence_scores': Dict,
                'recommendations': List[str]
            }
        """
        symptom_analysis = input_data.get('symptom_analysis', {})
        analysis_results = input_data.get('analysis_results', {})
        session_id = input_data.get('session_id')
        
        symptoms = symptom_analysis.get('processed_symptoms', [])
        
        self.log('INFO', f"Diagnoz qo'yish boshlandi", {
            'session_id': session_id,
            'symptoms_count': len(symptoms)
        })
        
        # Mos keladigan kasalliklarni topish
        matching_diseases = self._find_matching_diseases(symptoms)
        
        # Diagnozlar ro'yxati
        diagnoses = []
        confidence_scores = {}
        
        for disease_data in matching_diseases[:5]:  # Top 5
            disease = disease_data['disease']
            score = disease_data['score']
            
            diagnoses.append({
                'disease_id': disease.id,
                'disease_name': disease.name,
                'icd_code': disease.icd_code,
                'confidence': score,
                'severity': disease.severity,
                'description': disease.description
            })
            
            confidence_scores[disease.name] = score
        
        # Tavsiyalar
        recommendations = self._generate_recommendations(diagnoses)
        
        result = {
            'diagnoses': diagnoses,
            'confidence_scores': confidence_scores,
            'recommendations': recommendations
        }
        
        self.log('INFO', f"Diagnoz qo'yildi", {
            'session_id': session_id,
            'diagnoses_count': len(diagnoses),
            'top_diagnosis': diagnoses[0]['disease_name'] if diagnoses else None
        })
        
        return result
    
    def _find_matching_diseases(self, symptoms: List[str]) -> List[Dict]:
        """Mos keladigan kasalliklarni topish."""
        diseases = DiseasePattern.objects.filter(is_active=True)
        matches = []
        
        for disease in diseases:
            score = disease.calculate_match_score(symptoms)
            if score > 0:
                matches.append({
                    'disease': disease,
                    'score': score
                })
        
        # Score bo'yicha saralash
        matches.sort(key=lambda x: x['score'], reverse=True)
        
        return matches
    
    def _generate_recommendations(self, diagnoses: List[Dict]) -> List[str]:
        """Tavsiyalar generatsiya qilish."""
        recommendations = []
        
        if not diagnoses:
            recommendations.append("Aniq diagnoz qo'yish uchun qo'shimcha ma'lumotlar kerak")
            recommendations.append("Shifokor bilan shaxsiy maslahatlashing")
            return recommendations
        
        top_diagnosis = diagnoses[0]
        
        if top_diagnosis['confidence'] > 0.7:
            recommendations.append(f"Yuqori ehtimollik bilan {top_diagnosis['disease_name']} kasalligi aniqlandi")
            recommendations.append("Mutaxassis shifokor bilan maslahatlashing")
        elif top_diagnosis['confidence'] > 0.4:
            recommendations.append(f"O'rtacha ehtimollik bilan {top_diagnosis['disease_name']} kasalligi aniqlandi")
            recommendations.append("Qo'shimcha tahlillar o'tkazish tavsiya etiladi")
        else:
            recommendations.append("Aniq diagnoz qo'yish qiyin")
            recommendations.append("Keng qamrovli tekshiruvdan o'ting")
        
        return recommendations
