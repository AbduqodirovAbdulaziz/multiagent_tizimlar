"""
Treatment Agent - Davolash rejasini taklif qiluvchi agent.

Bu agent diagnoz asosida davolash rejasini taklif qiladi.
"""
from typing import Dict, Any, List
from .base import BaseAgent
from apps.diagnostics.models import DiseasePattern


class TreatmentAgent(BaseAgent):
    """
    Davolash agenti.
    
    Vazifalar:
    - Davolash rejasini taklif qilish
    - Dori-darmonlarni tavsiya qilish
    - Parhez va hayot tarzini tavsiya qilish
    """
    
    def __init__(self):
        super().__init__('treatment_agent')
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Davolash rejasini yaratish.
        
        Args:
            input_data: {
                'diagnoses': List[Dict],
                'symptom_analysis': Dict,
                'session_id': str
            }
        
        Returns:
            {
                'treatment_plan': str,
                'medications': List[str],
                'lifestyle_recommendations': List[str],
                'follow_up': str
            }
        """
        diagnoses = input_data.get('diagnoses', [])
        symptom_analysis = input_data.get('symptom_analysis', {})
        session_id = input_data.get('session_id')
        
        self.log('INFO', f"Davolash rejasini yaratish boshlandi", {
            'session_id': session_id,
            'diagnoses_count': len(diagnoses)
        })
        
        if not diagnoses:
            return {
                'treatment_plan': 'Diagnoz aniqlanmadi, davolash rejasi tayyorlanmadi',
                'medications': [],
                'lifestyle_recommendations': ['Shifokor bilan maslahatlashing'],
                'follow_up': 'Shifokorga murojaat qiling'
            }
        
        # Asosiy diagnoz
        primary_diagnosis = diagnoses[0]
        
        # Davolash rejasini olish
        treatment_plan = self._create_treatment_plan(primary_diagnosis)
        
        # Dori-darmonlar
        medications = self._recommend_medications(primary_diagnosis)
        
        # Hayot tarzi tavsiylari
        lifestyle_recommendations = self._recommend_lifestyle(primary_diagnosis, symptom_analysis)
        
        # Kuzatuv
        follow_up = self._create_follow_up_plan(primary_diagnosis)
        
        result = {
            'treatment_plan': treatment_plan,
            'medications': medications,
            'lifestyle_recommendations': lifestyle_recommendations,
            'follow_up': follow_up
        }
        
        self.log('INFO', f"Davolash rejasi yaratildi", {
            'session_id': session_id,
            'primary_diagnosis': primary_diagnosis['disease_name']
        })
        
        return result
    
    def _create_treatment_plan(self, diagnosis: Dict) -> str:
        """Davolash rejasini yaratish."""
        disease_id = diagnosis.get('disease_id')
        
        try:
            disease = DiseasePattern.objects.get(id=disease_id)
            if disease.treatment_options:
                return disease.treatment_options
        except DiseasePattern.DoesNotExist:
            pass
        
        # Default plan
        return f"""
Davolash rejasi: {diagnosis['disease_name']}

1. Shifokor bilan maslahatlashing
2. Tavsiya etilgan dori-darmonlarni qabul qiling
3. Parhez va hayot tarziga rioya qiling
4. Muntazam kuzatuvdan o'ting

DIQQAT: Bu avtomatik tizim tavsiyasi. Albatta shifokor bilan maslahatlashing!
        """.strip()
    
    def _recommend_medications(self, diagnosis: Dict) -> List[str]:
        """Dori-darmonlarni tavsiya qilish."""
        # Bu yerda haqiqiy tibbiy ma'lumotlar bo'lishi kerak
        # Hozircha umumiy tavsiyalar
        
        severity = diagnosis.get('severity', 'MEDIUM')
        
        medications = [
            "DIQQAT: Dori-darmonlarni faqat shifokor retsepti bilan qabul qiling!",
        ]
        
        if severity in ['HIGH', 'CRITICAL']:
            medications.append("Zudlik bilan shifokorga murojaat qiling")
        else:
            medications.append("Shifokor bilan maslahatlashib, kerakli dorilarni belgilang")
        
        return medications
    
    def _recommend_lifestyle(self, diagnosis: Dict, symptom_analysis: Dict) -> List[str]:
        """Hayot tarzi tavsiyalari."""
        recommendations = [
            "Ko'proq dam oling va uxlang",
            "Sog'lom ovqatlaning",
            "Stressdan qoching",
            "Jismoniy faollikni me'yorida saqlang",
        ]
        
        severity = symptom_analysis.get('severity', 'LOW')
        
        if severity in ['HIGH', 'CRITICAL']:
            recommendations.insert(0, "To'liq dam olish rejimiga o'ting")
        
        categorized = symptom_analysis.get('categorized_symptoms', {})
        
        if 'respiratory' in categorized:
            recommendations.append("Toza havoda ko'proq vaqt o'tkazing")
            recommendations.append("Nafas olish mashqlarini bajaring")
        
        if 'digestive' in categorized:
            recommendations.append("Yengil va sog'lom ovqatlanish rejimiga o'ting")
            recommendations.append("Ko'p suv iching")
        
        return recommendations
    
    def _create_follow_up_plan(self, diagnosis: Dict) -> str:
        """Kuzatuv rejasini yaratish."""
        confidence = diagnosis.get('confidence', 0)
        severity = diagnosis.get('severity', 'MEDIUM')
        
        if severity == 'CRITICAL':
            return "Zudlik bilan shifokorga murojaat qiling va doimiy nazoratda bo'ling"
        elif severity == 'HIGH':
            return "1 hafta ichida shifokorga ko'rining va holatni kuzatib boring"
        elif confidence < 0.5:
            return "2 hafta ichida qo'shimcha tekshiruvlardan o'ting"
        else:
            return "1 oy ichida nazorat tekshiruvidan o'ting"
