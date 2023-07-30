from enum import Enum


class DataSourceStatus(Enum):
    ACTIVE = 'Activo'
    PAUSED = 'Pausado'
    INACTIVE = 'Inactivo'

    # Other ver si se pasa como str o CategoryType, así funciona en ambos casos
    # Redefinir en cada Enum
    def __eq__(self, other):
        if isinstance(other, str):
            return str(self.name) == str(other)
        if isinstance(other, DataSourceStatus):
            return other == self
        return False
