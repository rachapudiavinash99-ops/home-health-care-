import asyncio
import os
from datetime import datetime, date, timedelta
from app.db.session import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole, Patient, Caregiver
from app.models.service import Service
from app.models.care_request import CareRequest, CareRequestStatus
from app.models.appointment import Appointment, AppointmentState
from app.models.visit import Visit
from app.models.care_plan import CarePlan, CarePlanStatus
from app.models.vitals_meds import VitalSign, Medication, MedicationStatus
from app.models.document import Document
from app.models.billing import Invoice, Payment, InvoiceStatus

async def reseed():
    async with AsyncSessionLocal() as db:
        print("Cleaning previous records for Indian localization...")
        from sqlalchemy import text
        for table in ["payments", "invoices", "documents", "care_plans", "medications", "vital_signs", "visits", "appointments", "care_requests", "services", "caregivers", "patients", "users"]:
            try:
                await db.execute(text(f"DELETE FROM {table}"))
            except Exception as e:
                pass
        await db.commit()

        print("Seeding Indian healthcare personas...")
        # 1. Admin
        admin_user = User(
            email="admin@healthcare.in",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            is_active=True
        )
        # Also keep admin@healthcare.com alias for convenience
        admin_user_alias = User(
            email="admin@healthcare.com",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            is_active=True
        )
        # 2. Doctor
        doc_user = User(
            email="dr.rajesh@healthcare.in",
            hashed_password=get_password_hash("doctor123"),
            role=UserRole.DOCTOR,
            is_active=True
        )
        # 3. Caregivers
        cg1_user = User(
            email="anjali.nurse@healthcare.in",
            hashed_password=get_password_hash("caregiver123"),
            role=UserRole.CAREGIVER,
            is_active=True
        )
        cg2_user = User(
            email="amit.physio@healthcare.in",
            hashed_password=get_password_hash("physio123"),
            role=UserRole.CAREGIVER,
            is_active=True
        )
        # 4. Patients
        p1_user = User(
            email="aarav.patient@gmail.com",
            hashed_password=get_password_hash("patient123"),
            role=UserRole.PATIENT,
            is_active=True
        )
        p2_user = User(
            email="sunita.devi@gmail.com",
            hashed_password=get_password_hash("patient123"),
            role=UserRole.PATIENT,
            is_active=True
        )
        p3_user = User(
            email="ramesh.gupta@gmail.com",
            hashed_password=get_password_hash("patient123"),
            role=UserRole.PATIENT,
            is_active=True
        )

        db.add_all([admin_user, admin_user_alias, doc_user, cg1_user, cg2_user, p1_user, p2_user, p3_user])
        await db.commit()
        await db.refresh(admin_user)
        await db.refresh(doc_user)
        await db.refresh(cg1_user)
        await db.refresh(cg2_user)
        await db.refresh(p1_user)
        await db.refresh(p2_user)
        await db.refresh(p3_user)

        # Patient Profiles
        p1 = Patient(
            user_id=p1_user.id,
            full_name="Aarav Sharma",
            date_of_birth="1962-08-15",
            gender="Male",
            phone="+91 98450 12345",
            address="#42, 4th Cross, Indiranagar, Bengaluru, Karnataka 560038",
            blood_group="B+"
        )
        p2 = Patient(
            user_id=p2_user.id,
            full_name="Sunita Devi",
            date_of_birth="1958-03-22",
            gender="Female",
            phone="+91 98110 54321",
            address="Flat 302, Palm Meadows, Whitefield, Bengaluru, Karnataka 560066",
            blood_group="O+"
        )
        p3 = Patient(
            user_id=p3_user.id,
            full_name="Ramesh Gupta",
            date_of_birth="1948-11-09",
            gender="Male",
            phone="+91 98200 98765",
            address="B-12, Sector 15, Rohini, New Delhi 110085",
            blood_group="AB+"
        )
        db.add_all([p1, p2, p3])

        # Caregiver Profiles
        cg1 = Caregiver(
            user_id=cg1_user.id,
            full_name="Sister Anjali Verma",
            qualification="B.Sc Nursing, INC Registered Nurse (RN/RM)",
            specialization="Geriatric Care, ICU Telemetry & Post-Op Recovery",
            experience_years=8,
            is_verified=True
        )
        cg2 = Caregiver(
            user_id=cg2_user.id,
            full_name="Dr. Amit Patel, MPT",
            qualification="MPT (Orthopedics), IAP Certified",
            specialization="Neuro & Post-Joint Replacement Rehabilitation",
            experience_years=6,
            is_verified=True
        )
        db.add_all([cg1, cg2])
        await db.commit()
        await db.refresh(p1)
        await db.refresh(p2)
        await db.refresh(p3)
        await db.refresh(cg1)
        await db.refresh(cg2)

        # Indian Services in INR (₹)
        s1 = Service(
            name="General Nursing & Health Monitoring",
            description="Daily vitals recording, BP & blood sugar check, medication administration and diabetic foot care by registered nurse.",
            category="NURSING",
            duration_minutes=60,
            base_price=799.0,
            required_qualification="B.Sc Nursing / GNM",
            is_active=True
        )
        s2 = Service(
            name="Physiotherapy & Mobility Rehabilitation",
            description="Specialized joint mobilization, stroke rehabilitation, gait training and pain management by licensed physiotherapist.",
            category="THERAPY",
            duration_minutes=45,
            base_price=1299.0,
            required_qualification="BPT / MPT",
            is_active=True
        )
        s3 = Service(
            name="Post-Operative Wound Care & Sterile Dressing",
            description="Aseptic surgical wound dressing, stitch/staple removal check, and infection prevention at home.",
            category="NURSING",
            duration_minutes=30,
            base_price=999.0,
            required_qualification="Registered Nurse (RN)",
            is_active=True
        )
        s4 = Service(
            name="Elderly Attendant & Companion Care",
            description="Assistance with daily living activities (ADL), mobility support, feeding, hygiene, and companionship.",
            category="PERSONAL_CARE",
            duration_minutes=120,
            base_price=1499.0,
            required_qualification="Certified Attendant",
            is_active=True
        )
        s5 = Service(
            name="Comprehensive Vitals & ECG Health Assessment",
            description="12-Lead ECG check, SpO2, blood glucose profiling, lipid assessment and doctor consultation report.",
            category="SPECIALIZED",
            duration_minutes=30,
            base_price=599.0,
            required_qualification="Clinical Nurse / Doctor",
            is_active=True
        )
        s6 = Service(
            name="ICU at Home & Tracheostomy Nursing",
            description="24x7 intensive nursing supervision, ventilator/oxygen concentrator monitoring, and airway management.",
            category="SPECIALIZED",
            duration_minutes=360,
            base_price=2999.0,
            required_qualification="Critical Care Nurse",
            is_active=True
        )
        db.add_all([s1, s2, s3, s4, s5, s6])
        await db.commit()
        await db.refresh(s1)
        await db.refresh(s2)
        await db.refresh(s3)
        await db.refresh(s4)
        await db.refresh(s5)
        await db.refresh(s6)

        # Care Requests
        cr1 = CareRequest(
            patient_id=p1.id,
            service_id=s1.id,
            preferred_date=datetime.now() + timedelta(days=1),
            preferred_start_time="09:00 AM",
            duration_hours=1,
            medical_requirements="Hypertension management and fasting blood sugar test",
            special_instructions="Building has security gate; please enter code 4022",
            status=CareRequestStatus.APPROVED
        )
        cr2 = CareRequest(
            patient_id=p2.id,
            service_id=s2.id,
            preferred_date=datetime.now() + timedelta(days=2),
            preferred_start_time="03:00 PM",
            duration_hours=1,
            medical_requirements="Post total knee replacement (TKR) rehabilitation",
            special_instructions="Lift available in block B",
            status=CareRequestStatus.APPROVED
        )
        db.add_all([cr1, cr2])
        await db.commit()
        await db.refresh(cr1)
        await db.refresh(cr2)

        # Appointments
        apt1 = Appointment(
            care_request_id=cr1.id,
            patient_id=p1.id,
            caregiver_id=cg1.id,
            service_id=s1.id,
            scheduled_date=datetime.now() - timedelta(days=1),
            start_time="09:00 AM",
            end_time="10:00 AM",
            status=AppointmentState.COMPLETED,
            notes="Routine home nursing visit and BP monitoring"
        )
        apt2 = Appointment(
            care_request_id=cr2.id,
            patient_id=p2.id,
            caregiver_id=cg2.id,
            service_id=s2.id,
            scheduled_date=datetime.now() + timedelta(days=1),
            start_time="03:00 PM",
            end_time="03:45 PM",
            status=AppointmentState.CONFIRMED,
            notes="Knee mobilization and quadriceps strengthening therapy"
        )
        apt3 = Appointment(
            care_request_id=cr1.id,
            patient_id=p1.id,
            caregiver_id=cg1.id,
            service_id=s5.id,
            scheduled_date=datetime.now(),
            start_time="11:30 AM",
            end_time="12:00 PM",
            status=AppointmentState.IN_PROGRESS,
            notes="Monthly ECG check and diabetes medicine titration review"
        )
        db.add_all([apt1, apt2, apt3])
        await db.commit()
        await db.refresh(apt1)
        await db.refresh(apt2)
        await db.refresh(apt3)

        # Visit Record
        v1 = Visit(
            appointment_id=apt1.id,
            arrival_time=datetime.now() - timedelta(days=1, hours=2),
            departure_time=datetime.now() - timedelta(days=1, hours=1),
            services_provided="Vitals recorded: BP 124/82 mmHg, RBS 112 mg/dL. Telmisartan medicine adherence checked.",
            patient_condition="Stable and active. No edema or dizziness reported.",
            notes="Advised low-salt Indian diet and 20-min morning walking.",
            follow_up_recommendation="Repeat fasting blood glucose and lipid panel in 15 days."
        )
        db.add(v1)
        await db.commit()
        await db.refresh(v1)

        # Vital Signs
        vt1 = VitalSign(
            patient_id=p1.id,
            visit_id=v1.id,
            temperature=98.4,
            blood_pressure="124/82",
            heart_rate=74,
            respiratory_rate=16,
            oxygen_saturation=99.0,
            blood_glucose=112.0,
            weight=72.0
        )
        vt2 = VitalSign(
            patient_id=p2.id,
            visit_id=None,
            temperature=98.6,
            blood_pressure="118/76",
            heart_rate=70,
            respiratory_rate=15,
            oxygen_saturation=98.5,
            blood_glucose=98.0,
            weight=65.0
        )
        db.add_all([vt1, vt2])

        # Medications (Common Indian Pharmaceutical Brands)
        m1 = Medication(
            patient_id=p1.id,
            prescribed_by=doc_user.id,
            medicine_name="Telmisartan (Telma 40)",
            dosage="40 mg",
            frequency="Once daily before breakfast",
            route="Oral",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            instructions="Take with warm water every morning",
            status=MedicationStatus.ACTIVE
        )
        m2 = Medication(
            patient_id=p1.id,
            prescribed_by=doc_user.id,
            medicine_name="Metformin (Glycomet 500 SR)",
            dosage="500 mg",
            frequency="Twice daily after meals",
            route="Oral",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            instructions="Take after lunch and dinner",
            status=MedicationStatus.ACTIVE
        )
        m3 = Medication(
            patient_id=p2.id,
            prescribed_by=doc_user.id,
            medicine_name="Calcium & Vitamin D3 (Shelcal 500)",
            dosage="500 mg + 250 IU",
            frequency="Once daily after dinner",
            route="Oral",
            start_date=date(2026, 2, 1),
            end_date=date(2026, 8, 1),
            instructions="For bone healing and joint health",
            status=MedicationStatus.ACTIVE
        )
        db.add_all([m1, m2, m3])

        # Care Plans
        cp1 = CarePlan(
            patient_id=p1.id,
            doctor_id=doc_user.id,
            diagnosis="Essential Hypertension & Type 2 Diabetes Mellitus (HbA1c: 6.8%)",
            goals="Target BP <= 125/80 mmHg, Fasting Blood Glucose < 110 mg/dL, regular kidney profile.",
            instructions="Weekly home nursing BP check, Telmisartan 40mg adherence, 30 min daily brisk walk, low GI diet.",
            required_services="General Nursing & Health Monitoring",
            frequency="Weekly Visits",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 6, 30),
            follow_up_date=date(2026, 4, 15),
            status=CarePlanStatus.ACTIVE
        )
        cp2 = CarePlan(
            patient_id=p2.id,
            doctor_id=doc_user.id,
            diagnosis="Post Total Knee Arthroplasty (Right TKR) - 4 Weeks Post-Op",
            goals="Achieve 115-degree knee flexion, independent stair climbing, normal quadriceps strength.",
            instructions="Daily physiotherapist-led isometric quads, knee bend exercises, cryotherapy 3x daily.",
            required_services="Physiotherapy & Mobility Rehabilitation",
            frequency="3x Weekly Sessions",
            start_date=date(2026, 2, 15),
            end_date=date(2026, 4, 30),
            follow_up_date=date(2026, 3, 30),
            status=CarePlanStatus.ACTIVE
        )
        db.add_all([cp1, cp2])

        # Documents
        d1 = Document(
            patient_id=p1.id,
            uploaded_by=doc_user.id,
            filename="Aarav_Sharma_HbA1c_Lipid_Panel_Report.pdf",
            file_path="uploads/aarav_sharma_lab_report.pdf",
            file_type="application/pdf",
            file_size=245760,
            description="Diagnostic Lab Report - Blood Glucose, Lipid Profile, Serum Creatinine"
        )
        d2 = Document(
            patient_id=p2.id,
            uploaded_by=doc_user.id,
            filename="Sunita_Devi_TKR_Discharge_Summary_Manipal.pdf",
            file_path="uploads/sunita_devi_discharge.pdf",
            file_type="application/pdf",
            file_size=512000,
            description="Hospital Discharge Summary & Post-Op Physical Therapy Protocol"
        )
        db.add_all([d1, d2])

        # Invoices and Payments in INR (₹)
        inv1 = Invoice(
            invoice_number="INV-2026-001",
            patient_id=p1.id,
            appointment_id=apt1.id,
            base_price=799.0,
            additional_charges=50.0,
            discount=50.0,
            tax=143.82,  # 18% GST
            total=942.82,
            status=InvoiceStatus.PAID
        )
        inv2 = Invoice(
            invoice_number="INV-2026-002",
            patient_id=p2.id,
            appointment_id=apt2.id,
            base_price=1299.0,
            additional_charges=0.0,
            discount=0.0,
            tax=233.82,  # 18% GST
            total=1532.82,
            status=InvoiceStatus.PENDING
        )
        db.add_all([inv1, inv2])
        await db.commit()
        await db.refresh(inv1)
        await db.refresh(inv2)

        pmt1 = Payment(
            invoice_id=inv1.id,
            amount=942.82,
            transaction_id="UPI-984712093481@okhdfcbank",
            payment_method="UPI_GPAY_SANDBOX",
            status="SUCCESS"
        )
        db.add(pmt1)
        await db.commit()

        print("Indian localization database re-seeded successfully!")

if __name__ == "__main__":
    asyncio.run(reseed())
