"""
Diagnostics services - Business logic layer.
"""
from typing import List, Dict, Optional
from django.db import transaction
from apps.core.utils import generate_session_id
from .models import DiagnosticSession, DiagnosticResult, DiseasePattern
from apps.patients.models import Patient


class DiagnosticService:
    """
    Diagnostika business logic servisi.
    
    Bu servis diagnostika sessiyalarini boshqaradi va
    agent'lar bilan integratsiyani ta'minlaydi.
    """
    
    @staticmethod
    @transaction.atomic
    def create_session(patient: Patient, symptoms: List[str]) -> DiagnosticSession:
        """
        Yangi diagnostika sessiyasini yaratish.
        
        Args:
            patient: Bemor obyekti
            symptoms: Simptomlar ro'yxati
        
        Returns:
            DiagnosticSession obyekti
        """
        session = DiagnosticSession.objects.create(
            session_id=generate_session_id(),
            patient=patient,
            symptoms=symptoms,
            status='PENDING',
            agent_states={
                'symptom_agent': 'pending',
                'analysis_agent': 'pending',
                'diagnosis_agent': 'pending',
                'treatment_agent': 'pending',
            }
        )
        
        return session
    
    @staticmethod
    def update_agent_state(session: DiagnosticSession, agent_name: str, state: str):
        """
        Agent holatini yangilash.
        
        Args:
            session: DiagnosticSession obyekti
            agent_name: Agent nomi
            state: Yangi holat
        """
        session.agent_states[agent_name] = state
        session.save(update_fields=['agent_states'])
    
    @staticmethod
    @transaction.atomic
    def add_result(
        session: DiagnosticSession,
        disease: DiseasePattern,
        confidence_score: float,
        recommended_tests: List[str],
        treatment_plan: str,
        agent_recommendations: Dict
    ) -> DiagnosticResult:
        """
        Diagnostika natijasini qo'shish.
        
        Args:
            session: DiagnosticSession obyekti
            disease: DiseasePattern obyekti
            confidence_score: Ishonch darajasi
            recommended_tests: Tavsiya etilgan tahlillar
            treatment_plan: Davolash rejasi
            agent_recommendations: Agent tavsiyalari
        
        Returns:
            DiagnosticResult obyekti
        """
        result = DiagnosticResult.objects.create(
            session=session,
            disease=disease,
            confidence_score=confidence_score,
            recommended_tests=recommended_tests,
            treatment_plan=treatment_plan,
            agent_recommendations=agent_recommendations
        )
        
        return result
    
    @staticmethod
    def find_matching_diseases(symptoms: List[str], min_score: float = 0.3) -> List[Dict]:
        """
        Simptomlar bo'yicha mos keladigan kasalliklarni topish.
        
        Args:
            symptoms: Simptomlar ro'yxati
            min_score: Minimal mos kelish darajasi
        
        Returns:
            Kasalliklar va ularning mos kelish darajasi
        """
        diseases = DiseasePattern.objects.filter(is_active=True)
        matches = []
        
        for disease in diseases:
            score = disease.calculate_match_score(symptoms)
            if score >= min_score:
                matches.append({
                    'disease': disease,
                    'score': score
                })
        
        # Mos kelish darajasi bo'yicha saralash
        matches.sort(key=lambda x: x['score'], reverse=True)
        
        return matches
    
    @staticmethod
    def get_session_statistics(session: DiagnosticSession) -> Dict:
        """
        Sessiya statistikasini olish.
        
        Args:
            session: DiagnosticSession obyekti
        
        Returns:
            Statistika dictionary
        """
        from django.db.models import Avg
        
        results = session.results.all()
        
        avg_confidence = results.aggregate(Avg('confidence_score'))['confidence_score__avg'] or 0
        
        return {
            'total_results': results.count(),
            'avg_confidence': avg_confidence,
            'top_disease': results.first().disease.name if results.exists() else None,
            'duration': session.get_duration(),
            'agent_states': session.agent_states,
        }
