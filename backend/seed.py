import asyncio
from datetime import datetime, date, timedelta
from app.db.session import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole, Patient, Caregiver, FamilyMember
from app.models.service import Service
from app.models.care_request import CareRequest, CareRequestStatus
from app.models.appointment import Appointment, AppointmentState
from app.models.visit import Visit
from app.models.care_plan import CarePlan, CarePlanStatus
from app.models.vitals_meds import VitalSign, Medication, MedicationStatus
from app.models.document import Document
from app.models.billing import Invoice, Payment, InvoiceStatus

async def seed_data():
    async with AsyncSessionLocal() as db:
        print('Checking if data exists...')
        from sqlalchemy.future import select
        existing_users = await db.execute(select(User))
        if len(existing_users.scalars().all()) > 0:
            print('Data already exists. Skipping...')
            return

        print('Seeding users and profiles...')
        # 1. Admin
        admin_user = User(
            email='admin@healthcare.com',
            hashed_password=get_password_hash('admin123'),
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin_user)

        # 2. Doctor
        doc_user = User(
            email='doctor.smith@healthcare.com',
            hashed_password=get_password_hash('doctor123'),
            role=UserRole.DOCTOR,
            is_active=True
        )
        db.add(doc_user)

        # 3. Caregivers
        cg1_user = User(
            email='caregiver.sarah@healthcare.com',
            hashed_password=get_password_hash('caregiver123'),
            role=UserRole.CAREGIVER,
            is_active=True
        )
        cg2_user = User(
            email='nurse.john@healthcare.com',
            hashed_password=get_password_hash('nurse123'),
            role=UserRole.CAREGIVER,
            is_active=True
        )
        db.add_all([cg1_user, cg2_user])

        # 4. Patients
        p1_user = User(
            email='patient.alice@gmail.com',
            hashed_password=get_password_hash('patient123'),
            role=UserRole.PATIENT,
            is_active=True
        )
        p2_user = User(
            email='patient.robert@gmail.com',
            hashed_password=get_password_hash('patient123'),
            role=UserRole.PATIENT,
            is_active=True
        )
        p3_user = User(
            email='patient.eleanor@gmail.com',
            hashed_password=get_password_hash('patient123'),
            role=UserRole.PATIENT,
            is_active=True
        )
        db.add_all([p1_user, p2_user, p3_user])
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
            full_name='Alice Jenkins',
            date_of_birth='1958-04-12',
            gender='Female',
            phone='+1 (555) 234-5678',
            address='742 Evergreen Terrace, Springfield',
            blood_group='A+'
        )
        p2 = Patient(
            user_id=p2_user.id,
            full_name='Robert Sterling',
            date_of_birth='1965-09-24',
            gender='Male',
            phone='+1 (555) 876-5432',
            address='1204 Elm Street, Boston',
            blood_group='O+'
        )
        p3 = Patient(
            user_id=p3_user.id,
            full_name='Eleanor Vance',
            date_of_birth='1949-11-03',
            gender='Female',
            phone='+1 (555) 345-6789',
            address='45 Hillcrest Ave, Newton',
            blood_group='B-'
        )
        db.add_all([p1, p2, p3])

        # Caregiver Profiles
        cg1 = Caregiver(
            user_id=cg1_user.id,
            full_name='Sarah Jenkins, RN',
            qualification='BSN, Registered Nurse',
            specialization='Geriatric & Palliative Care',
            experience_years=7,
            is_verified=True
        )
        cg2 = Caregiver(
            user_id=cg2_user.id,
            full_name='John Morales, PT',
            qualification='DPT, Physical Therapist',
            specialization='Post-Surgery Physical Rehabilitation',
            experience_years=5,
            is_verified=True
        )
        db.add_all([cg1, cg2])
        await db.commit()
        await db.refresh(p1)
        await db.refresh(p2)
        await db.refresh(p3)
        await db.refresh(cg1)
        await db.refresh(cg2)

        # Services
        s1 = Service(
            name='General Nursing & Health Monitoring',
            description='Daily health checks, vitals logging, and medication administration by a licensed nurse.',
            category='Nursing',
            duration_minutes=60,
            base_price=80.0,
            required_qualification='RN / LPN',
            is_active=True
        )
        s2 = Service(
            name='Physical Therapy & Mobility Rehabilitation',
            description='Targeted exercises, gait training, and joint mobility therapy to restore independence.',
            category='Therapy',
            duration_minutes=45,
            base_price=110.0,
            required_qualification='PT / DPT',
            is_active=True
        )
        s3 = Service(
            name='Post-Operative Wound Care & Dressing',
            description='Sterile dressing change, surgical wound inspection, and infection prevention.',
            category='Nursing',
            duration_minutes=30,
            base_price=95.0,
            required_qualification='RN',
            is_active=True
        )
        s4 = Service(
            name='Elderly Daily Living & Companion Care',
            description='Meal prep, hygiene assistance, mobility support, and companionship.',
            category='Daily Care',
            duration_minutes=120,
            base_price=65.0,
            required_qualification='CNA / Caregiver',
            is_active=True
        )
        s5 = Service(
            name='Comprehensive Health & Vitals Assessment',
            description='Full biometrics, blood pressure, glucose, oxygen level, and physician progress notes.',
            category='Medical',
            duration_minutes=30,
            base_price=50.0,
            required_qualification='RN / Doctor',
            is_active=True
        )
        db.add_all([s1, s2, s3, s4, s5])
        await db.commit()
        await db.refresh(s1)
        await db.refresh(s2)
        await db.refresh(s3)
        await db.refresh(s4)
        await db.refresh(s5)

        # Care Requests
        cr1 = CareRequest(
            patient_id=p1.id,
            service_id=s1.id,
            preferred_date=datetime.now() + timedelta(days=1),
            preferred_start_time='09:00 AM',
            duration_hours=1,
            medical_requirements='Hypertension management and daily BP monitoring',
            special_instructions='Please call upon arrival at front gate',
            status=CareRequestStatus.APPROVED
        )
        cr2 = CareRequest(
            patient_id=p2.id,
            service_id=s2.id,
            preferred_date=datetime.now() + timedelta(days=2),
            preferred_start_time='02:00 PM',
            duration_hours=1,
            medical_requirements='Post knee arthroscopy rehab',
            special_instructions='Wheelchair ramp on side door',
            status=CareRequestStatus.APPROVED
        )
        cr3 = CareRequest(
            patient_id=p3.id,
            service_id=s4.id,
            preferred_date=datetime.now() + timedelta(days=3),
            preferred_start_time='10:30 AM',
            duration_hours=2,
            medical_requirements='Assistance with mobility and meal prep',
            special_instructions='Prefers morning walk if weather permits',
            status=CareRequestStatus.PENDING
        )
        db.add_all([cr1, cr2, cr3])
        await db.commit()
        await db.refresh(cr1)
        await db.refresh(cr2)
        await db.refresh(cr3)

        # Appointments
        apt1 = Appointment(
            care_request_id=cr1.id,
            patient_id=p1.id,
            caregiver_id=cg1.id,
            service_id=s1.id,
            scheduled_date=datetime.now() - timedelta(days=1),
            start_time='09:00 AM',
            end_time='10:00 AM',
            status=AppointmentState.COMPLETED,
            notes='Scheduled routine nursing check-up'
        )
        apt2 = Appointment(
            care_request_id=cr2.id,
            patient_id=p2.id,
            caregiver_id=cg2.id,
            service_id=s2.id,
            scheduled_date=datetime.now() + timedelta(days=1),
            start_time='02:00 PM',
            end_time='02:45 PM',
            status=AppointmentState.CONFIRMED,
            notes='Knee rehab physical therapy session'
        )
        apt3 = Appointment(
            care_request_id=cr1.id,
            patient_id=p1.id,
            caregiver_id=cg1.id,
            service_id=s5.id,
            scheduled_date=datetime.now(),
            start_time='11:00 AM',
            end_time='11:30 AM',
            status=AppointmentState.IN_PROGRESS,
            notes='Vitals assessment and medication refill check'
        )
        db.add_all([apt1, apt2, apt3])
        await db.commit()
        await db.refresh(apt1)
        await db.refresh(apt2)
        await db.refresh(apt3)

        # Visit Record for completed appointment
        v1 = Visit(
            appointment_id=apt1.id,
            arrival_time=datetime.now() - timedelta(days=1, hours=2),
            departure_time=datetime.now() - timedelta(days=1, hours=1),
            services_provided='Vitals recorded, Lisinopril medication confirmed, diabetic foot check performed.',
            patient_condition='Stable and alert. Blood pressure within target range.',
            notes='Patient reported slight fatigue in mornings, advised adequate hydration.',
            follow_up_recommendation='Repeat blood pressure check next week.'
        )
        db.add(v1)
        await db.commit()
        await db.refresh(v1)

        # Vitals Signs
        vt1 = VitalSign(
            patient_id=p1.id,
            visit_id=v1.id,
            temperature=98.6,
            blood_pressure='122/78',
            heart_rate=72,
            respiratory_rate=16,
            oxygen_saturation=98.5,
            blood_glucose=105.0,
            weight=68.5
        )
        vt2 = VitalSign(
            patient_id=p2.id,
            visit_id=None,
            temperature=98.4,
            blood_pressure='118/76',
            heart_rate=68,
            respiratory_rate=14,
            oxygen_saturation=99.0,
            blood_glucose=94.0,
            weight=82.0
        )
        db.add_all([vt1, vt2])

        # Medications
        m1 = Medication(
            patient_id=p1.id,
            prescribed_by=doc_user.id,
            medicine_name='Lisinopril',
            dosage='10 mg',
            frequency='Once daily in morning',
            route='Oral',
            start_date=date(2026, 1, 15),
            end_date=date(2026, 7, 15),
            instructions='Take with water with breakfast',
            status=MedicationStatus.ACTIVE
        )
        m2 = Medication(
            patient_id=p1.id,
            prescribed_by=doc_user.id,
            medicine_name='Metformin',
            dosage='500 mg',
            frequency='Twice daily with meals',
            route='Oral',
            start_date=date(2026, 2, 1),
            end_date=date(2026, 8, 1),
            instructions='For blood sugar regulation',
            status=MedicationStatus.ACTIVE
        )
        m3 = Medication(
            patient_id=p2.id,
            prescribed_by=doc_user.id,
            medicine_name='Ibuprofen',
            dosage='400 mg',
            frequency='As needed for pain',
            route='Oral',
            start_date=date(2026, 3, 1),
            end_date=date(2026, 3, 20),
            instructions='Take after food for joint pain',
            status=MedicationStatus.ACTIVE
        )
        db.add_all([m1, m2, m3])

        # Care Plans
        cp1 = CarePlan(
            patient_id=p1.id,
            doctor_id=doc_user.id,
            diagnosis='Stage 1 Essential Hypertension & Mild Type 2 Diabetes',
            goals='Maintain BP below 130/80 mmHg, Fasting Glucose below 110 mg/dL.',
            instructions='Daily morning blood pressure log, 30-minute light walking, low sodium diet.',
            required_services='General Nursing, Vitals Assessment',
            frequency='Weekly nurse visits',
            start_date=date(2026, 1, 10),
            end_date=date(2026, 6, 30),
            follow_up_date=date(2026, 4, 15),
            status=CarePlanStatus.ACTIVE
        )
        cp2 = CarePlan(
            patient_id=p2.id,
            doctor_id=doc_user.id,
            diagnosis='Post Right Knee Arthroscopic Meniscectomy',
            goals='Restore 120-degree knee flexion, unassisted walking, pain score <= 2/10.',
            instructions='Quad strengthening exercises, ice therapy 3x daily, avoid high impact loads.',
            required_services='Physical Therapy Rehabilitation',
            frequency='2x weekly PT sessions',
            start_date=date(2026, 2, 20),
            end_date=date(2026, 4, 20),
            follow_up_date=date(2026, 3, 25),
            status=CarePlanStatus.ACTIVE
        )
        db.add_all([cp1, cp2])

        # Documents
        d1 = Document(
            patient_id=p1.id,
            uploaded_by=doc_user.id,
            filename='Comprehensive_Lab_Report_Jan2026.pdf',
            file_path='uploads/sample_lab_report.pdf',
            file_type='application/pdf',
            file_size=245760,
            description='Complete blood count, lipid panel, and HbA1c lab results'
        )
        d2 = Document(
            patient_id=p2.id,
            uploaded_by=doc_user.id,
            filename='Knee_MRI_Discharge_Summary.pdf',
            file_path='uploads/sample_discharge.pdf',
            file_type='application/pdf',
            file_size=512000,
            description='Orthopedic surgical discharge summary & rehab guidelines'
        )
        db.add_all([d1, d2])

        # Invoices and Payments
        inv1 = Invoice(
            invoice_number='INV-2026-001',
            patient_id=p1.id,
            appointment_id=apt1.id,
            base_price=80.0,
            additional_charges=10.0,
            discount=5.0,
            tax=7.5,
            total=92.5,
            status=InvoiceStatus.PAID
        )
        inv2 = Invoice(
            invoice_number='INV-2026-002',
            patient_id=p2.id,
            appointment_id=apt2.id,
            base_price=110.0,
            additional_charges=0.0,
            discount=0.0,
            tax=9.9,
            total=119.9,
            status=InvoiceStatus.PENDING
        )
        db.add_all([inv1, inv2])
        await db.commit()
        await db.refresh(inv1)
        await db.refresh(inv2)

        pmt1 = Payment(
            invoice_id=inv1.id,
            amount=92.5,
            transaction_id='TXN-984712093481',
            payment_method='SANDBOX_CARD_4242',
            status='SUCCESS'
        )
        db.add(pmt1)
        await db.commit()

        print('Database successfully seeded with comprehensive demo data!')

if __name__ == '__main__':
    asyncio.run(seed_data())
