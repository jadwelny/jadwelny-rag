from enum import Enum

class VectorDBEnum(Enum):
    QDRANT = "QDRANT"

class DistanceMethodEnum(Enum):
    COSINE = "consine"
    DOT = "dot"
    