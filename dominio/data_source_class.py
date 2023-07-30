from enum import Enum


class DataSourceClass(Enum):
    SERVIDOR_BD = 'Servidor BD'
    SISTEMA_FICHEROS = 'Sistema de ficheros'
    API = 'API'
    SERVICIO_STREAMING = 'Servicio de streaming'
    SISTEMA_TRANSFERENCIA_FICHEROS = 'Sistema de transferencia de ficheros'
    NOT_A_DIGITAL_SOURCE = 'Fuente no digital'

    # Other ver si se pasa como str o CategoryType, así funciona en ambos casos
    # Redefinir en cada Enum
    def __eq__(self, other):
        if isinstance(other, str):
            return str(self.name) == str(other)
        if isinstance(other, DataSourceClass):
            return other == self
        return False
