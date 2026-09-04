import asyncio
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

async def populate_rich_indian_data():
    async with AsyncSessionLocal() as db:
        print("Clearing tables for rich dataset...")
        from sqlalchemy import text
        for table in ["payments", "invoices", "documents", "care_plans", "medications", "vital_signs", "visits", "appointments", "care_requests", "services", "caregivers", "patients", "users"]:
            try:
                await db.execute(text(f"DELETE FROM {table}"))
            except Exception:
                pass
        await db.commit()

        print("1. Creating Users & Personas...")
        # Admins
        u_admin1 = User(email="admin@healthcare.in", hashed_password=get_password_hash("admin123"), role=UserRole.ADMIN, is_active=True)
        u_admin2 = User(email="admin@healthcare.com", hashed_password=get_password_hash("admin123"), role=UserRole.ADMIN, is_active=True)
        
        # Doctors
        u_doc1 = User(email="dr.rajesh@healthcare.in", hashed_password=get_password_hash("doctor123"), role=UserRole.DOCTOR, is_active=True)
        u_doc2 = User(email="dr.priya@healthcare.in", hashed_password=get_password_hash("doctor123"), role=UserRole.DOCTOR, is_active=True)
        
        # Caregivers & Nurses
        u_cg1 = User(email="anjali.nurse@healthcare.in", hashed_password=get_password_hash("caregiver123"), role=UserRole.CAREGIVER, is_active=True)
        u_cg2 = User(email="amit.physio@healthcare.in", hashed_password=get_password_hash("caregiver123"), role=UserRole.CAREGIVER, is_active=True)
        u_cg3 = User(email="deepa.nurse@healthcare.in", hashed_password=get_password_hash("caregiver123"), role=UserRole.CAREGIVER, is_active=True)
        u_cg4 = User(email="rajesh.attendant@healthcare.in", hashed_password=get_password_hash("caregiver123"), role=UserRole.CAREGIVER, is_active=True)
        u_cg5 = User(email="priya.therapist@healthcare.in", hashed_password=get_password_hash("caregiver123"), role=UserRole.CAREGIVER, is_active=True)

        # Patients
        u_p1 = User(email="aarav.patient@gmail.com", hashed_password=get_password_hash("patient123"), role=UserRole.PATIENT, is_active=True)
        u_p2 = User(email="sunita.devi@gmail.com", hashed_password=get_password_hash("patient123"), role=UserRole.PATIENT, is_active=True)
        u_p3 = User(email="ramesh.gupta@gmail.com", hashed_password=get_password_hash("patient123"), role=UserRole.PATIENT, is_active=True)
        u_p4 = User(email="meenakshi.s@gmail.com", hashed_password=get_password_hash("patient123"), role=UserRole.PATIENT, is_active=True)
        u_p5 = User(email="vikram.malhotra@gmail.com", hashed_password=get_password_hash("patient123"), role=UserRole.PATIENT, is_active=True)
        u_p6 = User(email="ananya.deshmukh@gmail.com", hashed_password=get_password_hash("patient123"), role=UserRole.PATIENT, is_active=True)

        db.add_all([u_admin1, u_admin2, u_doc1, u_doc2, u_cg1, u_cg2, u_cg3, u_cg4, u_cg5, u_p1, u_p2, u_p3, u_p4, u_p5, u_p6])
        await db.commit()
        for u in [u_admin1, u_doc1, u_cg1, u_cg2, u_cg3, u_cg4, u_cg5, u_p1, u_p2, u_p3, u_p4, u_p5, u_p6]:
            await db.refresh(u)

        print("2. Creating Patient Profiles...")
        p1 = Patient(user_id=u_p1.id, full_name="Aarav Sharma", date_of_birth="1962-08-15", gender="Male", phone="+91 98450 12345", address="#42, 4th Cross, Indiranagar, Bengaluru, Karnataka 560038", blood_group="B+")
        p2 = Patient(user_id=u_p2.id, full_name="Sunita Devi", date_of_birth="1958-03-22", gender="Female", phone="+91 98110 54321", address="Flat 302, Palm Meadows, Whitefield, Bengaluru, Karnataka 560066", blood_group="O+")
        p3 = Patient(user_id=u_p3.id, full_name="Ramesh Gupta", date_of_birth="1948-11-09", gender="Male", phone="+91 98200 98765", address="B-12, Sector 15, Rohini, New Delhi 110085", blood_group="AB+")
        p4 = Patient(user_id=u_p4.id, full_name="Dr. Meenakshi Sundaram", date_of_birth="1954-06-18", gender="Female", phone="+91 94440 23456", address="Plot 18, Anna Nagar West, Chennai, Tamil Nadu 600040", blood_group="A+")
        p5 = Patient(user_id=u_p5.id, full_name="Vikram Malhotra", date_of_birth="1970-01-30", gender="Male", phone="+91 99880 34567", address="701, Sea View Towers, Worli, Mumbai, Maharashtra 400018", blood_group="O-")
        p6 = Patient(user_id=u_p6.id, full_name="Ananya Deshmukh", date_of_birth="1982-09-14", gender="Female", phone="+91 97650 45678", address="Row House 4, Koregaon Park, Pune, Maharashtra 411001", blood_group="A-")

        db.add_all([p1, p2, p3, p4, p5, p6])
        await db.commit()
        for p in [p1, p2, p3, p4, p5, p6]:
            await db.refresh(p)

        print("3. Creating Caregiver & Nursing Roster...")
        cg1 = Caregiver(user_id=u_cg1.id, full_name="Sister Anjali Verma", qualification="B.Sc Nursing, INC Registered Nurse (RN/RM)", specialization="Geriatric & Critical Care Nursing", experience_years=8, is_verified=True)
        cg2 = Caregiver(user_id=u_cg2.id, full_name="Dr. Amit Patel, MPT", qualification="MPT (Orthopedics), IAP Certified", specialization="Neuro & Joint Replacement Physiotherapy", experience_years=6, is_verified=True)
        cg3 = Caregiver(user_id=u_cg3.id, full_name="Sister Deepa Nair", qualification="GNM, Critical Care Certified", specialization="ICU at Home & Tracheostomy Management", experience_years=10, is_verified=True)
        cg4 = Caregiver(user_id=u_cg4.id, full_name="Rajesh Kannan", qualification="Certified Home Health Attendant (NSDC)", specialization="Elderly Assistance, Mobility & Dementia Care", experience_years=5, is_verified=True)
        cg5 = Caregiver(user_id=u_cg5.id, full_name="Priya Swaminathan, BOT", qualification="Bachelor of Occupational Therapy (BOT)", specialization="Post-Stroke Fine Motor Rehab & Ergonomics", experience_years=4, is_verified=True)

        db.add_all([cg1, cg2, cg3, cg4, cg5])
        await db.commit()
        for cg in [cg1, cg2, cg3, cg4, cg5]:
            await db.refresh(cg)

        print("4. Creating Clinical Services Catalog in INR (INR)...")
        s1 = Service(name="General Nursing & Health Monitoring", description="Daily vitals logging, BP & blood sugar test, medication administration, and diabetic foot check.", category="NURSING", duration_minutes=60, base_price=799.0, required_qualification="B.Sc Nursing / GNM", is_active=True)
        s2 = Service(name="Physiotherapy & Mobility Rehabilitation", description="Targeted joint mobilization, stroke rehabilitation, gait training, and pain management by licensed physiotherapist.", category="THERAPY", duration_minutes=45, base_price=1299.0, required_qualification="BPT / MPT", is_active=True)
        s3 = Service(name="Post-Operative Wound Care & Sterile Dressing", description="Aseptic surgical wound dressing, stitch/staple check, drain care, and infection prevention at home.", category="NURSING", duration_minutes=30, base_price=999.0, required_qualification="Registered Nurse (RN)", is_active=True)
        s4 = Service(name="Elderly Attendant & Companion Care", description="Assistance with daily living activities (ADL), mobility support, feeding, hygiene, and companionship.", category="PERSONAL_CARE", duration_minutes=120, base_price=1499.0, required_qualification="Certified Attendant", is_active=True)
        s5 = Service(name="Comprehensive Vitals & 12-Lead ECG Assessment", description="12-Lead ECG screening, SpO2, blood glucose profiling, lipid assessment, and doctor consultation report.", category="SPECIALIZED", duration_minutes=30, base_price=599.0, required_qualification="Clinical Nurse / Doctor", is_active=True)
        s6 = Service(name="ICU at Home & Tracheostomy Nursing", description="24x7 intensive nursing supervision, ventilator/oxygen concentrator monitoring, and airway suctioning.", category="SPECIALIZED", duration_minutes=360, base_price=2999.0, required_qualification="Critical Care Nurse", is_active=True)
        s7 = Service(name="Mother & Newborn Postnatal Care", description="Post-delivery lactation support, infant bathing, umbilical cord care, and maternal recovery monitoring.", category="NURSING", duration_minutes=90, base_price=1199.0, required_qualification="Midwife / RN", is_active=True)
        s8 = Service(name="Catheter & Ryle Tube Insertion / Care", description="Sterile urinary catheterization (Foley/Silicone), nasogastric tube insertion, and feeding management.", category="NURSING", duration_minutes=45, base_price=899.0, required_qualification="Registered Nurse", is_active=True)

        db.add_all([s1, s2, s3, s4, s5, s6, s7, s8])
        await db.commit()
        for s in [s1, s2, s3, s4, s5, s6, s7, s8]:
            await db.refresh(s)

        print("5. Creating Care Requests & Appointments across all status categories...")
        # Care requests
        cr1 = CareRequest(patient_id=p1.id, service_id=s1.id, preferred_date=datetime.now() - timedelta(days=1), preferred_start_time="09:00 AM", duration_hours=1, medical_requirements="Hypertension & blood sugar monitoring", special_instructions="Gate code 4022", status=CareRequestStatus.APPROVED)
        cr2 = CareRequest(patient_id=p2.id, service_id=s2.id, preferred_date=datetime.now() + timedelta(days=1), preferred_start_time="03:00 PM", duration_hours=1, medical_requirements="Post Total Knee Replacement therapy", special_instructions="Lift in Block B", status=CareRequestStatus.APPROVED)
        cr3 = CareRequest(patient_id=p3.id, service_id=s6.id, preferred_date=datetime.now(), preferred_start_time="08:00 AM", duration_hours=6, medical_requirements="Tracheostomy suction & oxygen support", special_instructions="Oxygen cylinder available at home", status=CareRequestStatus.APPROVED)
        cr4 = CareRequest(patient_id=p4.id, service_id=s3.id, preferred_date=datetime.now() - timedelta(days=2), preferred_start_time="11:00 AM", duration_hours=1, medical_requirements="Abdominal surgical dressing change", special_instructions="Sterile kit provided", status=CareRequestStatus.APPROVED)
        cr5 = CareRequest(patient_id=p5.id, service_id=s5.id, preferred_date=datetime.now() + timedelta(days=3), preferred_start_time="10:00 AM", duration_hours=1, medical_requirements="Cardiac post-stent ECG follow-up", special_instructions="Doctor prescription attached", status=CareRequestStatus.APPROVED)
        cr6 = CareRequest(patient_id=p6.id, service_id=s4.id, preferred_date=datetime.now() + timedelta(days=2), preferred_start_time="02:00 PM", duration_hours=2, medical_requirements="Elderly companion & mobility assistance", special_instructions="Wheelchair assistance required", status=CareRequestStatus.PENDING)

        db.add_all([cr1, cr2, cr3, cr4, cr5, cr6])
        await db.commit()
        for cr in [cr1, cr2, cr3, cr4, cr5, cr6]:
            await db.refresh(cr)

        # Appointments across ALL categories (CONFIRMED, IN_PROGRESS, COMPLETED, CANCELLED)
        apt1 = Appointment(care_request_id=cr1.id, patient_id=p1.id, caregiver_id=cg1.id, service_id=s1.id, scheduled_date=datetime.now() - timedelta(days=1), start_time="09:00 AM", end_time="10:00 AM", status=AppointmentState.COMPLETED, notes="Nursing vitals check completed successfully. BP 124/82.")
        apt2 = Appointment(care_request_id=cr2.id, patient_id=p2.id, caregiver_id=cg2.id, service_id=s2.id, scheduled_date=datetime.now() + timedelta(days=1), start_time="03:00 PM", end_time="03:45 PM", status=AppointmentState.CONFIRMED, notes="Knee mobilization and gait rehabilitation session.")
        apt3 = Appointment(care_request_id=cr3.id, patient_id=p3.id, caregiver_id=cg3.id, service_id=s6.id, scheduled_date=datetime.now(), start_time="08:00 AM", end_time="02:00 PM", status=AppointmentState.IN_PROGRESS, notes="Critical care nurse currently on duty. SpO2 98%.")
        apt4 = Appointment(care_request_id=cr4.id, patient_id=p4.id, caregiver_id=cg1.id, service_id=s3.id, scheduled_date=datetime.now() - timedelta(days=2), start_time="11:00 AM", end_time="11:30 AM", status=AppointmentState.COMPLETED, notes="Surgical incision clean and dry. No erythema.")
        apt5 = Appointment(care_request_id=cr5.id, patient_id=p5.id, caregiver_id=cg1.id, service_id=s5.id, scheduled_date=datetime.now() + timedelta(days=3), start_time="10:00 AM", end_time="10:30 AM", status=AppointmentState.CONFIRMED, notes="Scheduled home 12-lead ECG and lipid panel screening.")
        apt6 = Appointment(care_request_id=cr1.id, patient_id=p1.id, caregiver_id=cg2.id, service_id=s2.id, scheduled_date=datetime.now() - timedelta(days=4), start_time="04:00 PM", end_time="04:45 PM", status=AppointmentState.CANCELLED, notes="Patient rescheduled due to out-of-town travel.")
        apt7 = Appointment(care_request_id=cr2.id, patient_id=p6.id, caregiver_id=cg4.id, service_id=s4.id, scheduled_date=datetime.now() + timedelta(days=2), start_time="02:00 PM", end_time="04:00 PM", status=AppointmentState.CONFIRMED, notes="Attendant companion care for evening park walk.")

        db.add_all([apt1, apt2, apt3, apt4, apt5, apt6, apt7])
        await db.commit()

        print("6. Creating Detailed EHR Records (Vitals, Medications, Care Plans, Documents)...")
        # Vitals
        v1 = VitalSign(patient_id=p1.id, visit_id=None, temperature=98.4, blood_pressure="124/82", heart_rate=74, respiratory_rate=16, oxygen_saturation=99.0, blood_glucose=112.0, weight=72.0)
        v2 = VitalSign(patient_id=p2.id, visit_id=None, temperature=98.6, blood_pressure="118/76", heart_rate=70, respiratory_rate=15, oxygen_saturation=98.5, blood_glucose=98.0, weight=65.0)
        v3 = VitalSign(patient_id=p3.id, visit_id=None, temperature=99.1, blood_pressure="138/88", heart_rate=82, respiratory_rate=18, oxygen_saturation=96.0, blood_glucose=145.0, weight=68.0)
        v4 = VitalSign(patient_id=p4.id, visit_id=None, temperature=98.2, blood_pressure="120/78", heart_rate=68, respiratory_rate=14, oxygen_saturation=99.5, blood_glucose=102.0, weight=58.0)
        v5 = VitalSign(patient_id=p5.id, visit_id=None, temperature=98.6, blood_pressure="126/80", heart_rate=72, respiratory_rate=16, oxygen_saturation=98.0, blood_glucose=118.0, weight=80.0)
        v6 = VitalSign(patient_id=p6.id, visit_id=None, temperature=98.4, blood_pressure="116/74", heart_rate=76, respiratory_rate=15, oxygen_saturation=99.0, blood_glucose=92.0, weight=54.0)
        db.add_all([v1, v2, v3, v4, v5, v6])

        # Medications
        m1 = Medication(patient_id=p1.id, prescribed_by=u_doc1.id, medicine_name="Telmisartan (Telma 40)", dosage="40 mg", frequency="Once daily before breakfast", route="Oral", start_date=date(2026, 1, 1), end_date=date(2026, 12, 31), instructions="Take with warm water every morning", status=MedicationStatus.ACTIVE)
        m2 = Medication(patient_id=p1.id, prescribed_by=u_doc1.id, medicine_name="Metformin (Glycomet 500 SR)", dosage="500 mg", frequency="Twice daily after meals", route="Oral", start_date=date(2026, 1, 1), end_date=date(2026, 12, 31), instructions="Take after lunch and dinner for blood sugar", status=MedicationStatus.ACTIVE)
        m3 = Medication(patient_id=p2.id, prescribed_by=u_doc2.id, medicine_name="Calcium + Vit D3 (Shelcal 500)", dosage="500 mg + 250 IU", frequency="Once daily after dinner", route="Oral", start_date=date(2026, 2, 1), end_date=date(2026, 8, 1), instructions="For bone healing and joint recovery", status=MedicationStatus.ACTIVE)
        m4 = Medication(patient_id=p2.id, prescribed_by=u_doc2.id, medicine_name="Paracetamol (Dolo 650)", dosage="650 mg", frequency="SOS for knee pain", route="Oral", start_date=date(2026, 2, 15), end_date=date(2026, 3, 30), instructions="Max 3 tablets daily if pain score > 4", status=MedicationStatus.ACTIVE)
        m5 = Medication(patient_id=p3.id, prescribed_by=u_doc1.id, medicine_name="Levosalbutamol Respules", dosage="0.63 mg", frequency="3x daily via nebulizer", route="Inhalation", start_date=date(2026, 1, 10), end_date=date(2026, 6, 10), instructions="Nebulize with 2ml normal saline", status=MedicationStatus.ACTIVE)
        m6 = Medication(patient_id=p4.id, prescribed_by=u_doc2.id, medicine_name="Thyroxine (Thyronorm 50)", dosage="50 mcg", frequency="Once daily on empty stomach", route="Oral", start_date=date(2026, 1, 1), end_date=date(2026, 12, 31), instructions="Take 45 mins before tea/breakfast", status=MedicationStatus.ACTIVE)
        m7 = Medication(patient_id=p5.id, prescribed_by=u_doc1.id, medicine_name="Aspirin + Atorvastatin (Ecosprin AV 75/20)", dosage="75 mg / 20 mg", frequency="Once daily after dinner", route="Oral", start_date=date(2026, 1, 15), end_date=date(2026, 12, 31), instructions="Post cardiac stent maintenance therapy", status=MedicationStatus.ACTIVE)
        m8 = Medication(patient_id=p6.id, prescribed_by=u_doc2.id, medicine_name="Iron & Folic Acid (Autrin)", dosage="1 capsule", frequency="Once daily after lunch", route="Oral", start_date=date(2026, 2, 1), end_date=date(2026, 5, 1), instructions="For hemoglobin improvement", status=MedicationStatus.ACTIVE)
        db.add_all([m1, m2, m3, m4, m5, m6, m7, m8])

        # Physician Care Plans
        cp1 = CarePlan(patient_id=p1.id, doctor_id=u_doc1.id, diagnosis="Essential Hypertension & Type 2 Diabetes Mellitus", goals="Target BP <= 125/80 mmHg, Fasting Blood Glucose < 110 mg/dL, HbA1c < 6.5%.", instructions="Weekly home nursing BP check, Telmisartan 40mg adherence, 30 min daily brisk walk, low sodium diet.", required_services="General Nursing & Health Monitoring", frequency="Weekly Nurse Visits", start_date=date(2026, 1, 1), end_date=date(2026, 6, 30), follow_up_date=date(2026, 4, 15), status=CarePlanStatus.ACTIVE)
        cp2 = CarePlan(patient_id=p2.id, doctor_id=u_doc2.id, diagnosis="Post Total Knee Arthroplasty (Right TKR) - Week 4 Rehab", goals="Achieve 115-degree knee flexion, independent stair climbing, full quadriceps activation.", instructions="Daily physiotherapist-led isometric quads, passive knee bends, ice therapy 3x daily.", required_services="Physiotherapy & Mobility Rehabilitation", frequency="3x Weekly Sessions", start_date=date(2026, 2, 15), end_date=date(2026, 4, 30), follow_up_date=date(2026, 3, 30), status=CarePlanStatus.ACTIVE)
        cp3 = CarePlan(patient_id=p3.id, doctor_id=u_doc1.id, diagnosis="COPD with Chronic Tracheostomy Care", goals="Maintain SpO2 > 95%, clear airway secretions, prevent pulmonary infections.", instructions="Routine 4-hourly suctioning, nebulization, sterile inner cannula cleaning 2x daily.", required_services="ICU at Home & Tracheostomy Nursing", frequency="Daily 6-Hour Shift", start_date=date(2026, 1, 10), end_date=date(2026, 7, 10), follow_up_date=date(2026, 4, 1), status=CarePlanStatus.ACTIVE)
        cp4 = CarePlan(patient_id=p4.id, doctor_id=u_doc2.id, diagnosis="Post Laparoscopic Cholecystectomy Wound Healing", goals="Complete primary surgical wound healing without seroma or infection.", instructions="Aseptic dressing changes on alternate days, avoid lifting heavy objects > 5kg.", required_services="Post-Operative Wound Care", frequency="Alternate Days (Mon/Wed/Fri)", start_date=date(2026, 3, 1), end_date=date(2026, 3, 20), follow_up_date=date(2026, 3, 15), status=CarePlanStatus.ACTIVE)
        cp5 = CarePlan(patient_id=p5.id, doctor_id=u_doc1.id, diagnosis="Coronary Artery Disease - Post PTCA Stenting (LAD)", goals="Resting HR 60-75 bpm, LDL < 70 mg/dL, cardiac functional capacity Class I.", instructions="Daily BP log, low saturated fat diet, supervised light aerobic cardiac rehab.", required_services="Comprehensive Vitals & ECG Assessment", frequency="Bi-Weekly Checks", start_date=date(2026, 1, 20), end_date=date(2026, 7, 20), follow_up_date=date(2026, 4, 20), status=CarePlanStatus.ACTIVE)
        db.add_all([cp1, cp2, cp3, cp4, cp5])

        # Clinical Documents
        d1 = Document(patient_id=p1.id, uploaded_by=u_doc1.id, filename="Aarav_Sharma_HbA1c_Lipid_Panel_Report.pdf", file_path="uploads/aarav_sharma_lab_report.pdf", file_type="application/pdf", file_size=245760, description="Comprehensive Diagnostic Lab Panel - Fasting Sugar, HbA1c (6.8%), Lipid Profile")
        d2 = Document(patient_id=p2.id, uploaded_by=u_doc2.id, filename="Sunita_Devi_TKR_Discharge_Summary_Manipal.pdf", file_path="uploads/sunita_devi_discharge.pdf", file_type="application/pdf", file_size=512000, description="Hospital Surgical Discharge Summary & Post-Op Physical Therapy Protocol")
        d3 = Document(patient_id=p3.id, uploaded_by=u_doc1.id, filename="Ramesh_Gupta_Pulmonary_Function_Test.pdf", file_path="uploads/aarav_sharma_lab_report.pdf", file_type="application/pdf", file_size=314572, description="Spirometry Report & Arterial Blood Gas (ABG) Analysis")
        d4 = Document(patient_id=p4.id, uploaded_by=u_doc2.id, filename="Meenakshi_Sundaram_Thyroid_Panel.pdf", file_path="uploads/sunita_devi_discharge.pdf", file_type="application/pdf", file_size=188416, description="Serum TSH, Free T3/T4 Lab Report & Liver Function Test")
        d5 = Document(patient_id=p5.id, uploaded_by=u_doc1.id, filename="Vikram_Malhotra_Post_Angiogram_Report.pdf", file_path="uploads/aarav_sharma_lab_report.pdf", file_type="application/pdf", file_size=429056, description="Coronary Angiography Report & 2D-Echocardiogram (EF: 55%)")
        db.add_all([d1, d2, d3, d4, d5])

        # Invoices and Payments in INR (INR)
        inv1 = Invoice(invoice_number="INV-2026-001", patient_id=p1.id, appointment_id=1, base_price=799.0, additional_charges=50.0, discount=50.0, tax=143.82, total=942.82, status=InvoiceStatus.PAID)
        inv2 = Invoice(invoice_number="INV-2026-002", patient_id=p2.id, appointment_id=2, base_price=1299.0, additional_charges=0.0, discount=0.0, tax=233.82, total=1532.82, status=InvoiceStatus.PENDING)
        inv3 = Invoice(invoice_number="INV-2026-003", patient_id=p3.id, appointment_id=3, base_price=2999.0, additional_charges=200.0, discount=100.0, tax=557.82, total=3656.82, status=InvoiceStatus.PENDING)
        inv4 = Invoice(invoice_number="INV-2026-004", patient_id=p4.id, appointment_id=4, base_price=999.0, additional_charges=0.0, discount=0.0, tax=179.82, total=1178.82, status=InvoiceStatus.PAID)
        inv5 = Invoice(invoice_number="INV-2026-005", patient_id=p5.id, appointment_id=5, base_price=599.0, additional_charges=0.0, discount=0.0, tax=107.82, total=706.82, status=InvoiceStatus.PENDING)

        db.add_all([inv1, inv2, inv3, inv4, inv5])
        await db.commit()
        await db.refresh(inv1)
        await db.refresh(inv4)

        pmt1 = Payment(invoice_id=inv1.id, amount=942.82, transaction_id="UPI-984712093481@okhdfcbank", payment_method="UPI_GPAY_SANDBOX", status="SUCCESS")
        pmt2 = Payment(invoice_id=inv4.id, amount=1178.82, transaction_id="RUPAY-549102938172", payment_method="RUPAY_CARD_SANDBOX", status="SUCCESS")
        db.add_all([pmt1, pmt2])
        await db.commit()

        print("Rich Indian Healthcare dataset seeded successfully across all tables!")

if __name__ == "__main__":
    asyncio.run(populate_rich_indian_data())
