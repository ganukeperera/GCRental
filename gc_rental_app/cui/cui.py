"""CUI"""

from abc import ABC, abstractmethod

class CUI(ABC):
    """Interface used to generalized CUI"""
    
    @abstractmethod
    def show_menu(self):
        """Abstract method created for showing the menu"""