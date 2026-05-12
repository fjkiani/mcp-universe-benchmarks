"""Patient management routes"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from database.session import get_db
from database.models import Patient, Organization
from middleware.auth import get_current_user
from services.audit_service import log_audit
from uuid import UUID
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/v1/patients", tags=["Patients"])


class PatientCreate(BaseModel):
    firstName: str
    lastName: str
    dob: str  # YYYY-MM-DD
    phone: str
    email: Optional[EmailStr] = None
    insurance: Optional[dict] = None


class PatientUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    insurance: Optional[dict] = None


class PatientResponse(BaseModel):
    id: str
    mrn: str
    fhir_resource: dict
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


def create_fhir_patient(patient_data: dict, mrn: str) -> dict:
    """Create FHIR Patient resource"""
    return {
        "resourceType": "Patient",
        "id": mrn,
        "identifier": [{
            "system": "http://hospital.example.org/patients",
            "value": mrn
        }],
        "active": True,
        "name": [{
            "use": "official",
            "family": patient_data.get("lastName", ""),
            "given": [patient_data.get("firstName", "")]
        }],
        "telecom": [
            {
                "system": "phone",
                "value": patient_data.get("phone", ""),
                "use": "mobile"
            }
        ],
        "birthDate": patient_data.get("dob", ""),
        "address": []
    }


@router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient_data: PatientCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new patient"""
    # Generate MRN
    mrn = f"MRN-{str(uuid.uuid4())[:8].upper()}"
    
    # Create FHIR resource
    patient_dict = patient_data.dict()
    fhir_resource = create_fhir_patient(patient_dict, mrn)
    
    # Add email if provided
    if patient_data.email:
        fhir_resource["telecom"].append({
            "system": "email",
            "value": patient_data.email
        })
    
    # Create patient record
    patient = Patient(
        organization_id=current_user.organization_id,
        mrn=mrn,
        fhir_resource=fhir_resource
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    
    # Audit log
    log_audit(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        action="patient.created",
        resource_type="Patient",
        resource_id=patient.id,
        patient_id=patient.id,
        details={"mrn": mrn}
    )
    
    return patient


@router.get("", response_model=List[PatientResponse])
async def list_patients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List patients with optional search"""
    query = db.query(Patient).filter(
        Patient.organization_id == current_user.organization_id,
        Patient.deleted_at.is_(None)
    )
    
    # Search by name or MRN
    if search:
        query = query.filter(
            (Patient.mrn.ilike(f"%{search}%")) |
            (Patient.fhir_resource['name'][0]['family'].astext.ilike(f"%{search}%")) |
            (Patient.fhir_resource['name'][0]['given'][0].astext.ilike(f"%{search}%"))
        )
    
    patients = query.order_by(Patient.created_at.desc()).offset(skip).limit(limit).all()
    return patients


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a patient by ID"""
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.organization_id == current_user.organization_id,
        Patient.deleted_at.is_(None)
    ).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Audit log
    log_audit(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        action="patient.viewed",
        resource_type="Patient",
        resource_id=patient.id,
        patient_id=patient.id
    )
    
    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: UUID,
    patient_data: PatientUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update a patient"""
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.organization_id == current_user.organization_id,
        Patient.deleted_at.is_(None)
    ).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Update FHIR resource
    fhir = patient.fhir_resource.copy()
    update_dict = patient_data.dict(exclude_unset=True)
    
    if "firstName" in update_dict:
        fhir["name"][0]["given"][0] = update_dict["firstName"]
    if "lastName" in update_dict:
        fhir["name"][0]["family"] = update_dict["lastName"]
    if "phone" in update_dict:
        for telecom in fhir.get("telecom", []):
            if telecom.get("system") == "phone":
                telecom["value"] = update_dict["phone"]
                break
    if "email" in update_dict:
        # Update or add email
        email_found = False
        for telecom in fhir.get("telecom", []):
            if telecom.get("system") == "email":
                telecom["value"] = update_dict["email"]
                email_found = True
                break
        if not email_found:
            fhir.setdefault("telecom", []).append({
                "system": "email",
                "value": update_dict["email"]
            })
    
    patient.fhir_resource = fhir
    patient.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(patient)
    
    # Audit log
    log_audit(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        action="patient.updated",
        resource_type="Patient",
        resource_id=patient.id,
        patient_id=patient.id,
        details={"updated_fields": list(update_dict.keys())}
    )
    
    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
    patient_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Soft delete a patient"""
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.organization_id == current_user.organization_id,
        Patient.deleted_at.is_(None)
    ).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Soft delete
    patient.deleted_at = datetime.utcnow()
    db.commit()
    
    # Audit log
    log_audit(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        action="patient.deleted",
        resource_type="Patient",
        resource_id=patient.id,
        patient_id=patient.id
    )
    
    return None

