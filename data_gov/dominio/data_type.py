from enum import Enum


class DataType(Enum):
    STRUCTURED = 'Estructurados'
    SEMISTRUCTURED = 'Semiestructurados'
    UNSTRUCTURED = 'No estructurados'
    UNDEFINED = 'Indefinidos'


    # Other ver si se pasa como str o CategoryType, así funciona en ambos casos
    # Redefinir en cada Enum
    def __eq__(self, other):
        if isinstance(other, str):
            return str(self.name) == str(other)
        if isinstance(other, DataType):
            return other == self
        return False
