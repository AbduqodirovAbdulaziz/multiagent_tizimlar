"""
Base agent class - Barcha agentlar uchun bazaviy sinf.

Bu modul BDI (Belief-Desire-Intention) arxitekturasini amalga oshiradi.
"""
import logging
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from django.utils import timezone
from apps.core.models import ACLMessage, AgentLog
from apps.core.constants import ACL_PERFORMATIVES
from apps.core.utils import generate_message_id, calculate_expiry_time
from apps.core.exceptions import AgentException
from .models import AgentState


logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Bazaviy agent sinfi (BDI arxitektura).
    
    BDI Model:
    - Belief (E'tiqod): Agent bilim bazasi
    - Desire (Istak): Maqsadlar
    - Intention (Niyat): Rejalar va harakatlar
    """
    
    def __init__(self, agent_name: str):
        """
        Agent initsializatsiyasi.
        
        Args:
            agent_name: Agent nomi
        """
        self.agent_name = agent_name
        self.beliefs = {}  # Agent bilim bazasi
        self.desires = []  # Maqsadlar
        self.intentions = []  # Rejalar
        
        # Agent holatini yaratish yoki olish
        self.state, _ = AgentState.objects.get_or_create(
            agent_name=agent_name,
            defaults={'state': 'IDLE'}
        )
    
    def log(self, level: str, message: str, extra_data: Optional[Dict] = None):
        """
        Agent faoliyatini log qilish.
        
        Args:
            level: Log darajasi (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            message: Log xabari
            extra_data: Qo'shimcha ma'lumotlar
        """
        AgentLog.objects.create(
            agent_name=self.agent_name,
            level=level,
            message=message,
            extra_data=extra_data or {}
        )
        
        # Python logger'ga ham yozish
        log_method = getattr(logger, level.lower(), logger.info)
        log_method(f"[{self.agent_name}] {message}")
    
    def update_state(self, state: str, current_task: str = ''):
        """
        Agent holatini yangilash.
        
        Args:
            state: Yangi holat
            current_task: Hozirgi vazifa
        """
        self.state.state = state
        self.state.current_task = current_task
        self.state.save()
        
        self.log('INFO', f"Holat o'zgartirildi: {state}", {'task': current_task})
    
    def send_message(
        self,
        receiver: str,
        performative: str,
        content: Dict[str, Any],
        in_reply_to: Optional[str] = None
    ) -> ACLMessage:
        """
        Boshqa agentga xabar yuborish (FIPA-ACL).
        
        Args:
            receiver: Qabul qiluvchi agent nomi
            performative: Xabar turi (INFORM, REQUEST, etc.)
            content: Xabar mazmuni
            in_reply_to: Javob berilayotgan xabar ID
        
        Returns:
            ACLMessage obyekti
        """
        message_id = generate_message_id(self.agent_name, receiver)
        expires_at = calculate_expiry_time(3600)  # 1 soat
        
        message = ACLMessage.objects.create(
            message_id=message_id,
            performative=performative,
            sender=self.agent_name,
            receiver=receiver,
            content=content,
            in_reply_to=in_reply_to,
            expires_at=expires_at
        )
        
        self.log('DEBUG', f"Xabar yuborildi: {receiver}", {
            'message_id': message_id,
            'performative': performative
        })
        
        return message
    
    def receive_messages(self, mark_as_read: bool = True) -> list:
        """
        Agentga kelgan xabarlarni olish.
        
        Args:
            mark_as_read: Xabarlarni o'qilgan deb belgilash
        
        Returns:
            ACLMessage obyektlari ro'yxati
        """
        messages = ACLMessage.objects.filter(
            receiver=self.agent_name,
            is_processed=False
        ).order_by('created_at')
        
        if mark_as_read:
            for message in messages:
                message.mark_as_read()
        
        return list(messages)
    
    def update_beliefs(self, new_beliefs: Dict[str, Any]):
        """
        Agent bilim bazasini yangilash (BDI - Belief).
        
        Args:
            new_beliefs: Yangi bilimlar
        """
        self.beliefs.update(new_beliefs)
        self.log('DEBUG', "Bilimlar yangilandi", {'beliefs': list(new_beliefs.keys())})
    
    def add_desire(self, goal: str):
        """
        Yangi maqsad qo'shish (BDI - Desire).
        
        Args:
            goal: Maqsad tavsifi
        """
        if goal not in self.desires:
            self.desires.append(goal)
            self.log('DEBUG', f"Yangi maqsad qo'shildi: {goal}")
    
    def add_intention(self, plan: str):
        """
        Yangi reja qo'shish (BDI - Intention).
        
        Args:
            plan: Reja tavsifi
        """
        if plan not in self.intentions:
            self.intentions.append(plan)
            self.log('DEBUG', f"Yangi reja qo'shildi: {plan}")
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Asosiy qayta ishlash metodi (har bir agent o'zini amalga oshiradi).
        
        Args:
            input_data: Kirish ma'lumotlari
        
        Returns:
            Natija dictionary
        """
        pass
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Agent vazifasini bajarish (wrapper method).
        
        Args:
            input_data: Kirish ma'lumotlari
        
        Returns:
            Natija dictionary
        """
        try:
            self.update_state('PROCESSING', f"Processing: {input_data.get('task', 'unknown')}")
            self.log('INFO', "Vazifa boshlandi", {'input': input_data})
            
            result = self.process(input_data)
            
            self.update_state('COMPLETED')
            self.log('INFO', "Vazifa yakunlandi", {'result': result})
            
            return result
            
        except Exception as e:
            self.update_state('FAILED', str(e))
            self.log('ERROR', f"Xatolik: {str(e)}", {'error': str(e)})
            raise AgentException(f"{self.agent_name} xatolik: {str(e)}")
