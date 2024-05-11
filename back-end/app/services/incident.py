from typing import List

from fastapi import HTTPException

from core.db import SessionLocal
from models.incident import Incident as IncidentModel
from schemas.incident import Incident as IncidentSchema, IncidentInDB, IncidentType


def validate_authorization(incident_user, username, user_role):
    if not (user_role or incident_user == username):
        raise HTTPException(status_code=403, detail='You do not have permission to update this incident')


def get_all_incidents() -> List[IncidentInDB]:
    try:
        db = SessionLocal()
        return db.query(IncidentModel).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error fetching all incidents') from e
    finally:
        db.close()


def get_incidents_by_type(type: IncidentType) -> List[IncidentInDB]:
    try:
        db = SessionLocal()
        incidents = db.query(IncidentModel).filter(IncidentModel.type == type).all()
        if not incidents:
            raise HTTPException(status_code=404, detail='No results found')
        return incidents
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error fetching incidents by type') from e
    finally:
        db.close()


def get_incidents_by_username(username: str) -> List[IncidentInDB]:
    try:
        db = SessionLocal()
        incidents = db.query(IncidentModel).filter(IncidentModel.user_username == username).all()
        if not incidents:
            raise HTTPException(status_code=404, detail='No results found')
        return incidents
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error fetching incidents by user') from e
    finally:
        db.close()


def create_incident(incident_data: IncidentSchema, current_user) -> IncidentInDB:
    try:
        db = SessionLocal()
        new_incident = IncidentModel(**incident_data.model_dump())
        if current_user:
            new_incident.user_username = current_user
        else:
            raise HTTPException(status_code=500, detail='To create an incident, you need to be authenticated.') from e    
        db.add(new_incident)
        db.commit()
        db.refresh(new_incident)
        return new_incident
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error creating incident') from e
    finally:
        db.close()


def update_incident(incident_id: str, incident_data: IncidentSchema, current_user) -> IncidentInDB:
    db = SessionLocal()
    db_incident = db.query(IncidentModel).filter(IncidentModel.id == incident_id).first()
    if not db_incident:
        raise HTTPException(status_code=404, detail='Incident not found')
    validate_authorization(db_incident.user_username, current_user.username, current_user.is_admin)        
    try:
        db_incident.type = incident_data.type
        db_incident.description = incident_data.description
        db_incident.detail = incident_data.detail
        db_incident.address = incident_data.address
        db_incident.evidence = incident_data.evidence
        db_incident.state = incident_data.state
        db.commit()
        return db_incident
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error updating incident') from e
    finally:
        db.close()


def delete_incident_by_id(incident_id: str, current_user) -> bool:
    db = SessionLocal()
    incident = db.query(IncidentModel).filter(IncidentModel.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail='Incident not found')
    validate_authorization(incident.user_username, current_user.username, current_user.is_admin)        
    try:
        db.delete(incident)
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error deleting incident') from e
    finally:
        db.close()