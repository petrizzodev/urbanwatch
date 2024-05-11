from typing import Annotated, List

from fastapi import APIRouter, Depends

from schemas.incident import Incident as IncidentSchema, IncidentType, IncidentInDB
from schemas.user import User
from services.incident import get_all_incidents, get_incidents_by_type, get_incidents_by_username, create_incident, update_incident, delete_incident_by_id
from core.security import get_current_active_user


incident_router = APIRouter(prefix='/v1')


@incident_router.get('/incident', tags=['incident'], status_code=200)
def get_incidents(current_user: Annotated[User, Depends(get_current_active_user)]) -> List[IncidentInDB]:
    return get_all_incidents()


@incident_router.get('/incident/me', tags=['incident'], status_code=200)
def get_incidents(current_user: Annotated[User, Depends(get_current_active_user)]) -> List[IncidentInDB]:
    return get_incidents_by_username(current_user.username)


@incident_router.get('/incident/{type}', tags=['incident'], status_code=200)
def get_incidents(type:IncidentType, current_user: Annotated[User, Depends(get_current_active_user)]) -> List[IncidentInDB]:
    return get_incidents_by_type(type)


@incident_router.post('/incident', tags=['incident'], status_code=201)
def post_incident(incident: IncidentSchema, current_user: Annotated[User, Depends(get_current_active_user)]) -> IncidentInDB:
    return create_incident(incident, current_user.username)


@incident_router.put('/incident/{incident_id}', tags=['incident'], status_code=200)
def put_incident(incident_id: str, incident: IncidentSchema, current_user: Annotated[User, Depends(get_current_active_user)]) -> IncidentInDB:
    return update_incident(incident_id, incident, current_user)


@incident_router.delete('/incident/{incident_id}', tags=['incident'], status_code=200)
def delete_incident(incident_id: str, current_user: Annotated[User, Depends(get_current_active_user)]) -> bool:
    return delete_incident_by_id(incident_id, current_user)