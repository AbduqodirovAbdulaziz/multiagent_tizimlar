"""
Symptom Agent - Simptomlarni tahlil qiluvchi agent.

Bu agent bemorning simptomlarini tahlil qiladi va
ularni kategoriyalarga ajratadi.
"""
from typing import Dict, Any, List
from .base import BaseAgent
from apps.core.constants import ACL_PERFORMATIVES


class SymptomAgent(BaseAgent):
    """
    Simptomlar agenti.
    
    Vazifalar:
    - Simptomlarni tahlil qilish
    - Simptomlarni kategoriyalarga ajratish
    - Og'irlik darajasini aniqlash
    """
    
    def __init__(self):
        super().__init__('symptom_agent')
        
        # Simptom kategoriyalari
        self.symptom_categories = {
            'respiratory': ['yo\'tal', 'nafas qisilishi', 'burun bitishi', 'tomoq og\'rig\'i'],
            'digestive': ['qorin og\'rig\'i', 'ko\'ngil aynishi', 'ichburug\'', 'qabziyat'],
            'neurological': ['bosh og\'rig\'i', 'bosh aylanishi', 'hushidan ketish'],
            'cardiovascular': ['ko\'krak og\'rig\'i', 'yurak urishi', 'nafas qisilishi'],
            'general': ['isitma', 'charchoq', 'ishtahasizlik', 'vazn yo\'qotish'],
        }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simptomlarni qayta ishlash.
        
        Args:
            input_data: {
                'symptoms': List[str],
                'patient_id': int,
                'session_id': str
            }
        
        Returns:
            {
                'categorized_symptoms': Dict,
                'severity': str,
                'recommendations': List[str]
            }
        """
        symptoms = input_data.get('symptoms', [])
        session_id = input_data.get('session_id')
        
        self.log('INFO', f"Simptomlarni tahlil qilish boshlandi", {
            'session_id': session_id,
            'symptoms_count': len(symptoms)
        })
        
        # Simptomlarni kategoriyalash
        categorized = self._categorize_symptoms(symptoms)
        
        # Og'irlik darajasini aniqlash
        severity = self._assess_severity(symptoms, categorized)
        
        # Tavsiyalar
        recommendations = self._generate_recommendations(categorized, severity)
        
        result = {
            'categorized_symptoms': categorized,
            'severity': severity,
            'recommendations': recommendations,
            'processed_symptoms': symptoms
        }
        
        self.log('INFO', f"Simptomlar tahlili yakunlandi", {
            'session_id': session_id,
            'severity': severity,
            'categories': list(categorized.keys())
        })
        
        return result
    
    def _categorize_symptoms(self, symptoms: List[str]) -> Dict[str, List[str]]:
        """Simptomlarni kategoriyalarga ajratish."""
        categorized = {}
        
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            found = False
            
            for category, keywords in self.symptom_categories.items():
                for keyword in keywords:
                    if keyword in symptom_lower:
                        if category not in categorized:
                            categorized[category] = []
                        categorized[category].append(symptom)
                        found = True
                        break
                if found:
                    break
            
            if not found:
                if 'other' not in categorized:
                    categorized['other'] = []
                categorized['other'].append(symptom)
        
        return categorized
    
    def _assess_severity(self, symptoms: List[str], categorized: Dict) -> str:
        """Og'irlik darajasini aniqlash."""
        # Oddiy qoidalar asosida
        critical_keywords = ['nafas qisilishi', 'ko\'krak og\'rig\'i', 'hushidan ketish']
        high_keywords = ['isitma', 'qon', 'og\'riq']
        
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            for keyword in critical_keywords:
                if keyword in symptom_lower:
                    return 'CRITICAL'
        
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            for keyword in high_keywords:
                if keyword in symptom_lower:
                    return 'HIGH'
        
        if len(symptoms) > 5:
            return 'MEDIUM'
        
        return 'LOW'
    
    def _generate_recommendations(self, categorized: Dict, severity: str) -> List[str]:
        """Tavsiyalar generatsiya qilish."""
        recommendations = []
        
        if severity == 'CRITICAL':
            recommendations.append("Zudlik bilan shifokorga murojaat qiling")
            recommendations.append("Tez tibbiy yordam chaqiring")
        elif severity == 'HIGH':
            recommendations.append("Imkon qadar tezroq shifokorga ko'rining")
            recommendations.append("Simptomlarni kuzatib boring")
        else:
            recommendations.append("Shifokor bilan maslahatlashing")
            recommendations.append("Ko'proq dam oling")
        
        # Kategoriya bo'yicha tavsiyalar
        if 'respiratory' in categorized:
            recommendations.append("Nafas olish mashqlarini bajaring")
        
        if 'digestive' in categorized:
            recommendations.append("Yengil ovqatlanish rejimiga o'ting")
        
        return recommendations
