"""
Coordinator Agent - Barcha agentlarni muvofiqlashtiruvchi agent.

Bu agent diagnostika jarayonini boshqaradi va barcha agentlarni
ketma-ket chaqiradi.
"""
from typing import Dict, Any
from .base import BaseAgent
from .symptom_agent import SymptomAgent
from .analysis_agent import AnalysisAgent
from .diagnosis_agent import DiagnosisAgent
from .treatment_agent import TreatmentAgent
from apps.diagnostics.models import DiagnosticSession, DiagnosticResult, DiseasePattern
from apps.core.exceptions import AgentException


class CoordinatorAgent(BaseAgent):
    """
    Koordinator agent.
    
    Vazifalar:
    - Diagnostika jarayonini boshqarish
    - Agentlarni ketma-ket chaqirish
    - Natijalarni yig'ish va saqlash
    - Xatolarni boshqarish
    """
    
    def __init__(self):
        super().__init__('coordinator_agent')
        
        # Agentlarni initsializatsiya qilish
        self.symptom_agent = SymptomAgent()
        self.analysis_agent = AnalysisAgent()
        self.diagnosis_agent = DiagnosisAgent()
        self.treatment_agent = TreatmentAgent()
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Diagnostika jarayonini boshqarish.
        
        Args:
            input_data: {
                'session_id': str,
                'patient_id': int,
                'symptoms': List[str],
                'test_results': Dict (optional)
            }
        
        Returns:
            {
                'session_id': str,
                'status': str,
                'results': Dict
            }
        """
        session_id = input_data.get('session_id')
        
        self.log('INFO', f"Diagnostika jarayoni boshlandi", {
            'session_id': session_id
        })
        
        try:
            # Session olish
            session = DiagnosticSession.objects.get(session_id=session_id)
            session.mark_as_in_progress()
            
            # 1. Simptomlarni tahlil qilish
            self.log('INFO', "1/4: Simptomlar tahlili", {'session_id': session_id})
            symptom_result = self.symptom_agent.execute({
                'symptoms': input_data.get('symptoms', []),
                'patient_id': input_data.get('patient_id'),
                'session_id': session_id
            })
            self._update_session_state(session, 'symptom_agent', 'completed')
            
            # 2. Tahlillarni baholash
            self.log('INFO', "2/4: Tahlillar baholash", {'session_id': session_id})
            analysis_result = self.analysis_agent.execute({
                'test_results': input_data.get('test_results', {}),
                'symptom_analysis': symptom_result,
                'session_id': session_id
            })
            self._update_session_state(session, 'analysis_agent', 'completed')
            
            # 3. Diagnoz qo'yish
            self.log('INFO', "3/4: Diagnoz qo'yish", {'session_id': session_id})
            diagnosis_result = self.diagnosis_agent.execute({
                'symptom_analysis': symptom_result,
                'analysis_results': analysis_result,
                'session_id': session_id
            })
            self._update_session_state(session, 'diagnosis_agent', 'completed')
            
            # 4. Davolash rejasini yaratish
            self.log('INFO', "4/4: Davolash rejasi", {'session_id': session_id})
            treatment_result = self.treatment_agent.execute({
                'diagnoses': diagnosis_result.get('diagnoses', []),
                'symptom_analysis': symptom_result,
                'session_id': session_id
            })
            self._update_session_state(session, 'treatment_agent', 'completed')
            
            # Natijalarni saqlash
            self._save_results(session, diagnosis_result, treatment_result)
            
            # Sessionni yakunlash
            session.mark_as_completed()
            
            result = {
                'session_id': session_id,
                'status': 'completed',
                'results': {
                    'symptom_analysis': symptom_result,
                    'analysis': analysis_result,
                    'diagnosis': diagnosis_result,
                    'treatment': treatment_result
                }
            }
            
            self.log('INFO', f"Diagnostika jarayoni yakunlandi", {
                'session_id': session_id,
                'diagnoses_count': len(diagnosis_result.get('diagnoses', []))
            })
            
            return result
            
        except DiagnosticSession.DoesNotExist:
            error_msg = f"Session topilmadi: {session_id}"
            self.log('ERROR', error_msg, {'session_id': session_id})
            raise AgentException(error_msg)
            
        except Exception as e:
            error_msg = f"Diagnostika xatosi: {str(e)}"
            self.log('ERROR', error_msg, {
                'session_id': session_id,
                'error': str(e)
            })
            
            try:
                session = DiagnosticSession.objects.get(session_id=session_id)
                session.mark_as_failed(error_msg)
            except:
                pass
            
            raise AgentException(error_msg)
    
    def _update_session_state(self, session: DiagnosticSession, agent_name: str, state: str):
        """Session agent holatini yangilash."""
        session.agent_states[agent_name] = state
        session.save(update_fields=['agent_states'])
    
    def _save_results(self, session: DiagnosticSession, diagnosis_result: Dict, treatment_result: Dict):
        """Natijalarni bazaga saqlash."""
        diagnoses = diagnosis_result.get('diagnoses', [])
        
        for diagnosis_data in diagnoses:
            try:
                disease = DiseasePattern.objects.get(id=diagnosis_data['disease_id'])
                
                DiagnosticResult.objects.create(
                    session=session,
                    disease=disease,
                    confidence_score=diagnosis_data['confidence'],
                    recommended_tests=disease.recommended_tests,
                    treatment_plan=treatment_result.get('treatment_plan', ''),
                    agent_recommendations={
                        'symptom_recommendations': diagnosis_result.get('recommendations', []),
                        'treatment_recommendations': treatment_result.get('lifestyle_recommendations', []),
                        'medications': treatment_result.get('medications', []),
                        'follow_up': treatment_result.get('follow_up', '')
                    }
                )
            except DiseasePattern.DoesNotExist:
                self.log('WARNING', f"Kasallik topilmadi: {diagnosis_data['disease_id']}")
                continue
