from enum import Enum

from pydantic import BaseModel, constr


class IncidentState(str, Enum):
    REPORTED = 'reported'
    IN_REVIEW = 'in_review'
    RESOLVED = 'resolved'


class IncidentType(str, Enum):
    EMERGENCIAS_MEDICAS = 'emergencias_medicas'
    ACCIDENTES_DE_TRAFICO = 'accidentes_de_trafico'
    CRIMEN_Y_SEGURIDAD = 'crimen_y_seguridad'
    PROBLEMAS_DE_INFRAESTRUCTURA = 'problemas_de_infraestructura'
    PROBLEMAS_AMBIENTALES = 'problemas_ambientales'
    PROBLEMAS_DE_TRAFICO_Y_TRANSPORTE = 'problemas_de_trafico_y_transporte'
    PROBLEMAS_DE_SALUD_PUBLICA = 'problemas_de_salud_publica'
    INCIDENTES_NATURALES = 'incidentes_naturales'


class Incident(BaseModel):
    type: IncidentType
    description: constr(max_length=255)
    detail: constr(max_length=255)
    address: str
    evidence: str
    state: IncidentState

class IncidentInDB(Incident):
    user_username: str
    class Config:
        orm_mode = True