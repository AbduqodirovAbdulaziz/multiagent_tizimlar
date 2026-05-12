"""
Analysis Agent - Tahlillarni baholash agenti.

Bu agent tibbiy tahlil natijalarini baholaydi.
"""
from typing import Dict, Any, List
from .base import BaseAgent


class AnalysisAgent(BaseAgent):
    """
    Tahlil agenti.
    
    Vazifalar:
    - Tahlil natijalarini baholash
    - Normal qiymatlar bilan solishtirish
    - Anomaliyalarni aniqlash
    """
    
    def __init__(self):
        super().__init__('analysis_agent')
        
        # Normal qiymatlar (oddiy misollar)
        self.normal_ranges = {
            'temperature': (36.0, 37.5),
            'blood_pressure_systolic': (90, 140),
            'blood_pressure_diastolic': (60, 90),
            'heart_rate': (60, 100),
            'glucose': (3.9, 6.1),
        }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tahlillarni qayta ishlash.
        
        Args:
            input_data: {
                'test_results': Dict,
                'symptom_analysis': Dict,
                'session_id': str
            }
        
        Returns:
            {
                'analysis_results': Dict,
                'anomalies': List,
                'recommendations': List[str]
            }
        """
        test_results = input_data.get('test_results', {})
        symptom_analysis = input_data.get('symptom_analysis', {})
        session_id = input_data.get('session_id')
        
        self.log('INFO', f"Tahlillarni baholash boshlandi", {
            'session_id': session_id,
            'tests_count': len(test_results)
        })
        
        # Tahlillarni baholash
        analysis_results = self._analyze_tests(test_results)
        
        # Anomaliyalarni aniqlash
        anomalies = self._detect_anomalies(test_results)
        
        # Tavsiyalar
        recommendations = self._generate_recommendations(analysis_results, anomalies)
        
        result = {
            'analysis_results': analysis_results,
            'anomalies': anomalies,
            'recommendations': recommendations,
            'test_results': test_results
        }
        
        self.log('INFO', f"Tahlillar baholandi", {
            'session_id': session_id,
            'anomalies_count': len(anomalies)
        })
        
        return result
    
    def _analyze_tests(self, test_results: Dict) -> Dict:
        """Tahlillarni baholash."""
        analysis = {}
        
        for test_name, value in test_results.items():
            if test_name in self.normal_ranges:
                min_val, max_val = self.normal_ranges[test_name]
                
                if isinstance(value, (int, float)):
                    if value < min_val:
                        status = 'low'
                    elif value > max_val:
                        status = 'high'
                    else:
                        status = 'normal'
                    
                    analysis[test_name] = {
                        'value': value,
                        'status': status,
                        'normal_range': f"{min_val}-{max_val}"
                    }
        
        return analysis
    
    def _detect_anomalies(self, test_results: Dict) -> List[Dict]:
        """Anomaliyalarni aniqlash."""
        anomalies = []
        
        for test_name, value in test_results.items():
            if test_name in self.normal_ranges:
                min_val, max_val = self.normal_ranges[test_name]
                
                if isinstance(value, (int, float)):
                    if value < min_val or value > max_val:
                        anomalies.append({
                            'test': test_name,
                            'value': value,
                            'expected': f"{min_val}-{max_val}",
                            'severity': 'high' if abs(value - (min_val + max_val) / 2) > (max_val - min_val) else 'medium'
                        })
        
        return anomalies
    
    def _generate_recommendations(self, analysis_results: Dict, anomalies: List) -> List[str]:
        """Tavsiyalar generatsiya qilish."""
        recommendations = []
        
        if anomalies:
            recommendations.append("Qo'shimcha tahlillar o'tkazish tavsiya etiladi")
            recommendations.append("Mutaxassis shifokor bilan maslahatlashing")
        else:
            recommendations.append("Tahlil natijalari normal chegaralarda")
        
        return recommendations
