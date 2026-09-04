import React, { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { 
  ShieldCheck, 
  UserCheck, 
  Calendar, 
  Clock, 
  HeartHandshake, 
  Stethoscope, 
  Activity, 
  CheckCircle2, 
  ArrowRight, 
  Lock, 
  Mail, 
  Sparkles, 
  Layers, 
  Users,
  X,
  Heart,
  Award,
  PhoneCall,
  MapPin,
  Smile,
  BadgeCheck,
  Star
} from "lucide-react";
import api from "../api/axios";

export default function Landing() {
  const navigate = useNavigate();
  const [showAdminModal, setShowAdminModal] = useState(false);
  const [showBookingSection, setShowBookingSection] = useState(false);
  
  // Admin Login State
  const [adminEmail, setAdminEmail] = useState("admin@healthcare.in");
  const [adminPassword, setAdminPassword] = useState("admin123");
  const [adminLoading, setAdminLoading] = useState(false);
  const [adminError, setAdminError] = useState("");

  // Services and Caregivers for Booking Block
  const [services, setServices] = useState<any[]>([]);
  const [caregivers, setCaregivers] = useState<any[]>([]);
  const [selectedServiceId, setSelectedServiceId] = useState<string>("");
  const [selectedCaregiverId, setSelectedCaregiverId] = useState<string>("");
  const [patientName, setPatientName] = useState("Aarav Sharma");
  const [patientPhone, setPatientPhone] = useState("+91 98450 12345");
  const [patientAddress, setPatientAddress] = useState("#42, 4th Cross, Indiranagar, Bengaluru");
  const [bookingDate, setBookingDate] = useState("");
  const [bookingNotes, setBookingNotes] = useState("");
  const [bookingSuccess, setBookingSuccess] = useState<any | null>(null);
  const [bookingLoading, setBookingLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [srvRes, cgRes] = await Promise.all([
        api.get("/services/").catch(() => ({ data: [] })),
        api.get("/caregivers/").catch(() => ({ data: [] }))
      ]);
      setServices(srvRes.data || []);
      setCaregivers(cgRes.data || []);
      if (srvRes.data && srvRes.data.length > 0) {
        setSelectedServiceId(srvRes.data[0].id.toString());
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleAdminLogin = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setAdminLoading(true);
    setAdminError("");

    try {
      const formData = new URLSearchParams();
      formData.append("username", adminEmail);
      formData.append("password", adminPassword);

      const res = await api.post("/auth/login", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
      });

      localStorage.setItem("token", res.data.access_token);
      const meRes = await api.get("/auth/me");
      localStorage.setItem("user", JSON.stringify(meRes.data));

      navigate("/dashboard");
    } catch (err: any) {
      setAdminError(err?.response?.data?.detail || "Invalid credentials. Please check your email and password.");
    } finally {
      setAdminLoading(false);
    }
  };

  const handlePatientQuickLogin = async (email: string = "aarav.patient@gmail.com") => {
    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", "patient123");

      const res = await api.post("/auth/login", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
      });

      localStorage.setItem("token", res.data.access_token);
      const meRes = await api.get("/auth/me");
      localStorage.setItem("user", JSON.stringify(meRes.data));

      navigate("/dashboard/appointments");
    } catch (err) {
      console.error(err);
    }
  };

  const handleBookAppointment = async (e: React.FormEvent) => {
    e.preventDefault();
    setBookingLoading(true);

    try {
      // Authenticate as demo patient if not logged in
      if (!localStorage.getItem("token")) {
        const formData = new URLSearchParams();
        formData.append("username", "aarav.patient@gmail.com");
        formData.append("password", "patient123");
        const authRes = await api.post("/auth/login", formData, {
          headers: { "Content-Type": "application/x-www-form-urlencoded" }
        });
        localStorage.setItem("token", authRes.data.access_token);
        const me = await api.get("/auth/me");
        localStorage.setItem("user", JSON.stringify(me.data));
      }

      const selectedSrv = services.find(s => s.id.toString() === selectedServiceId) || services[0];
      const payload = {
        service_id: Number(selectedServiceId || (selectedSrv?.id ?? 1)),
        caregiver_id: selectedCaregiverId ? Number(selectedCaregiverId) : 1,
        scheduled_start: bookingDate || new Date(Date.now() + 86400000).toISOString(),
        notes: `${bookingNotes} | Patient: ${patientName} (${patientPhone}) | Addr: ${patientAddress}`
      };

      const res = await api.post("/appointments/", payload);
      setBookingSuccess({
        id: res.data.id,
        service: selectedSrv?.name || "General Nursing",
        price: selectedSrv?.base_price || 799,
        date: bookingDate || "Tomorrow 10:00 AM",
        patient: patientName
      });
    } catch (err: any) {
      alert(err?.response?.data?.detail || "Booking could not be completed. Please check date/time.");
    } finally {
      setBookingLoading(false);
    }
  };

  const selectedServiceObj = services.find(s => s.id.toString() === selectedServiceId);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between font-sans relative overflow-x-hidden selection:bg-orange-500 selection:text-white">
      {/* Warm Ambient Glow Highlights */}
      <div className="absolute -top-32 left-1/4 w-96 h-96 bg-orange-600/15 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute top-1/3 -right-20 w-80 h-80 bg-amber-500/10 rounded-full blur-[100px] pointer-events-none"></div>
      <div className="absolute bottom-10 left-10 w-96 h-96 bg-emerald-600/10 rounded-full blur-[120px] pointer-events-none"></div>

      {/* Top Friendly Header */}
      <header className="relative z-20 max-w-7xl mx-auto w-full px-6 py-5 flex items-center justify-between border-b border-slate-800/80 backdrop-blur-xl">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-2xl bg-linear-to-tr from-orange-500 to-amber-500 flex items-center justify-center text-white shadow-lg shadow-orange-500/25 ring-2 ring-orange-400/30">
            <Heart size={22} className="text-white fill-white/20 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-lg font-bold tracking-tight text-white">CareFleet India</span>
              <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 text-[10px] font-bold border border-emerald-500/20">
                Live & Verified
              </span>
            </div>
            <span className="text-xs text-slate-400 font-medium">Compassionate Home Healthcare (INR ₹)</span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => handlePatientQuickLogin("aarav.patient@gmail.com")}
            className="text-xs font-semibold text-slate-300 hover:text-white px-3.5 py-2 rounded-xl hover:bg-slate-800 transition-all cursor-pointer hidden md:flex items-center gap-1.5"
          >
            <UserCheck size={14} className="text-orange-400" /> Patient Sign In
          </button>
          <button
            onClick={() => setShowAdminModal(true)}
            className="text-xs font-bold bg-linear-to-r from-orange-600 to-amber-600 hover:from-orange-500 hover:to-amber-500 text-white px-4 py-2.5 rounded-xl transition-all shadow-md shadow-orange-600/20 cursor-pointer flex items-center gap-2"
          >
            <Lock size={13} /> Admin & Staff Login
          </button>
        </div>
      </header>

      {/* Humanized Hero Section */}
      <main className="relative z-10 max-w-7xl mx-auto w-full px-6 pt-12 pb-16 flex-1 flex flex-col items-center text-center">
        
        {/* Trust Pill */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-800/80 border border-slate-700/80 text-orange-300 text-xs font-semibold mb-6 shadow-sm">
          <span className="flex h-2 w-2 rounded-full bg-emerald-400 animate-ping"></span>
          <span>Namaste! Dedicated In-Home Clinical & Nursing Care</span>
        </div>

        {/* Empathy-First Main Headline */}
        <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white max-w-4xl leading-tight">
          Healing begins with <span className="bg-clip-text text-transparent bg-linear-to-r from-orange-400 via-amber-300 to-yellow-300">comfort, empathy & trust</span> at home.
        </h1>
        
        <p className="text-slate-300 text-sm sm:text-base max-w-2xl mt-5 leading-relaxed font-normal">
          Whether you need a dedicated nurse for an aging parent, physiotherapy after surgery, or a hospital team managing clinical records — we are by your side across India.
        </p>

        {/* Social Proof & Trust Stats */}
        <div className="flex flex-wrap items-center justify-center gap-6 mt-8 py-3 px-6 rounded-2xl bg-slate-900/60 border border-slate-800 text-xs text-slate-300">
          <div className="flex items-center gap-1.5">
            <Star size={14} className="text-amber-400 fill-amber-400" />
            <span><strong className="text-white">4.9/5</strong> Rating (10,000+ Visits)</span>
          </div>
          <span className="text-slate-700 hidden sm:inline">&bull;</span>
          <div className="flex items-center gap-1.5">
            <BadgeCheck size={14} className="text-emerald-400" />
            <span><strong className="text-white">100%</strong> Certified Nurses & Physios</span>
          </div>
          <span className="text-slate-700 hidden sm:inline">&bull;</span>
          <div className="flex items-center gap-1.5">
            <Clock size={14} className="text-blue-400" />
            <span><strong className="text-white">Instant</strong> Dispatch in INR (₹)</span>
          </div>
        </div>

        {/* Humanized Choice Gateway (Patient vs Admin) */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl mt-12 text-left">
          
          {/* Card 1: Patient / Family Care */}
          <div 
            onClick={() => {
              setShowBookingSection(true);
              setTimeout(() => {
                document.getElementById("booking-block")?.scrollIntoView({ behavior: "smooth" });
              }, 150);
            }}
            className="group relative bg-linear-to-b from-orange-950/40 via-slate-900/90 to-slate-900 border-2 border-orange-500/50 hover:border-orange-400 rounded-3xl p-8 transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl hover:shadow-orange-500/20 cursor-pointer flex flex-col justify-between overflow-hidden"
          >
            <div className="absolute top-0 right-0 w-40 h-40 bg-orange-500/10 rounded-full blur-2xl group-hover:bg-orange-500/20 transition-all"></div>
            
            <div>
              <div className="flex items-center justify-between mb-6">
                <div className="w-14 h-14 rounded-2xl bg-linear-to-tr from-orange-500 to-amber-500 flex items-center justify-center text-white shadow-lg shadow-orange-500/30 group-hover:scale-110 transition-transform">
                  <Calendar size={28} />
                </div>
                <span className="px-3 py-1 rounded-full bg-orange-500/20 text-orange-300 text-[11px] font-bold uppercase tracking-wider border border-orange-500/30">
                  Starts at ₹799
                </span>
              </div>

              <span className="text-xs font-bold text-orange-400 uppercase tracking-wider block mb-1">
                For Patients & Families
              </span>
              <h2 className="text-2xl font-bold text-white group-hover:text-amber-200 transition-colors">
                Book a Nurse or Doctor Visit
              </h2>
              <p className="text-xs text-slate-300 mt-2.5 leading-relaxed">
                Schedule a registered nurse, physiotherapist, or geriatric caregiver directly to your home. No password required to schedule.
              </p>

              <div className="mt-6 flex flex-wrap gap-2 text-[11px] text-slate-300 font-medium">
                <span className="px-2.5 py-1 rounded-lg bg-slate-800/80 border border-slate-700">✓ Home Vitals Check</span>
                <span className="px-2.5 py-1 rounded-lg bg-slate-800/80 border border-slate-700">✓ Knee Rehab & Physio</span>
                <span className="px-2.5 py-1 rounded-lg bg-slate-800/80 border border-slate-700">✓ Sterile Dressing</span>
              </div>
            </div>

            <div className="mt-8 pt-5 border-t border-slate-800 flex items-center justify-between">
              <span className="text-xs font-bold text-orange-400 flex items-center gap-1.5">
                <Sparkles size={14} /> Tap to Open Scheduling Block
              </span>
              <div className="w-10 h-10 rounded-xl bg-orange-600 group-hover:bg-amber-500 text-white flex items-center justify-center transition-all group-hover:translate-x-1 shadow-md shadow-orange-600/30">
                <ArrowRight size={18} />
              </div>
            </div>
          </div>

          {/* Card 2: Hospital & Admin Team */}
          <div 
            onClick={() => setShowAdminModal(true)}
            className="group relative bg-slate-900/80 hover:bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-3xl p-8 transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl hover:shadow-slate-800/50 cursor-pointer flex flex-col justify-between overflow-hidden"
          >
            <div className="absolute top-0 right-0 w-40 h-40 bg-blue-500/5 rounded-full blur-2xl group-hover:bg-blue-500/10 transition-all"></div>
            
            <div>
              <div className="flex items-center justify-between mb-6">
                <div className="w-14 h-14 rounded-2xl bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300 group-hover:text-white group-hover:bg-slate-700 transition-all group-hover:scale-110">
                  <ShieldCheck size={28} />
                </div>
                <span className="px-3 py-1 rounded-full bg-slate-800 text-slate-400 text-[11px] font-semibold border border-slate-700">
                  Staff Access
                </span>
              </div>

              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1">
                For Hospital & Care Team
              </span>
              <h2 className="text-2xl font-bold text-white group-hover:text-slate-200 transition-colors">
                Hospital & Admin Portal
              </h2>
              <p className="text-xs text-slate-400 mt-2.5 leading-relaxed">
                Hospital staff dispatching, electronic medical records (EHR), physician treatment plans, and 18% GST invoice billing.
              </p>

              <div className="mt-6 flex flex-wrap gap-2 text-[11px] text-slate-400 font-medium">
                <span className="px-2.5 py-1 rounded-lg bg-slate-800/60 border border-slate-800">✓ Doctor Telemetry</span>
                <span className="px-2.5 py-1 rounded-lg bg-slate-800/60 border border-slate-800">✓ Caregiver Rosters</span>
                <span className="px-2.5 py-1 rounded-lg bg-slate-800/60 border border-slate-800">✓ Invoices (INR ₹)</span>
              </div>
            </div>

            <div className="mt-8 pt-5 border-t border-slate-800/80 flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 flex items-center gap-1.5">
                <Lock size={13} className="text-orange-400" /> Enter ID & Password
              </span>
              <div className="w-10 h-10 rounded-xl bg-slate-800 group-hover:bg-slate-700 text-white flex items-center justify-center transition-all group-hover:translate-x-1">
                <ArrowRight size={18} />
              </div>
            </div>
          </div>
        </div>

        {/* Friendly Simulator Persona Bar */}
        <div className="mt-8 p-4 rounded-2xl bg-slate-900/60 border border-slate-800/80 max-w-4xl w-full flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2 text-slate-400">
            <Smile size={16} className="text-orange-400 shrink-0" />
            <span className="font-semibold text-white">1-Click Test Accounts:</span>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={() => { setAdminEmail("admin@healthcare.in"); setAdminPassword("admin123"); setShowAdminModal(true); }}
              className="px-3 py-1.5 rounded-xl bg-indigo-500/15 hover:bg-indigo-500/25 text-indigo-300 border border-indigo-500/30 font-semibold cursor-pointer transition-all"
            >
              🛡️ Admin (`admin@healthcare.in`)
            </button>
            <button
              onClick={() => { setAdminEmail("dr.rajesh@healthcare.in"); setAdminPassword("doctor123"); setShowAdminModal(true); }}
              className="px-3 py-1.5 rounded-xl bg-emerald-500/15 hover:bg-emerald-500/25 text-emerald-300 border border-emerald-500/30 font-semibold cursor-pointer transition-all"
            >
              🩺 Dr. Rajesh (MD)
            </button>
            <button
              onClick={() => { setAdminEmail("anjali.nurse@healthcare.in"); setAdminPassword("caregiver123"); setShowAdminModal(true); }}
              className="px-3 py-1.5 rounded-xl bg-amber-500/15 hover:bg-amber-500/25 text-amber-300 border border-amber-500/30 font-semibold cursor-pointer transition-all"
            >
              👩‍⚕️ Sister Anjali (RN)
            </button>
            <button
              onClick={() => handlePatientQuickLogin("aarav.patient@gmail.com")}
              className="px-3 py-1.5 rounded-xl bg-orange-500/15 hover:bg-orange-500/25 text-orange-300 border border-orange-500/30 font-semibold cursor-pointer transition-all"
            >
              🧑 Aarav Sharma (Patient)
            </button>
          </div>
        </div>
      </main>

      {/* Interactive Appointment Scheduling Block (Smooth Animated Block) */}
      {(showBookingSection || true) && (
        <section id="booking-block" className="relative z-10 max-w-5xl mx-auto w-full px-6 py-12 border-t border-white/10 animate-fade-in">
          <div className="bg-slate-800/90 rounded-3xl p-8 border border-orange-500/30 shadow-2xl shadow-black/50 backdrop-blur-xl">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 pb-6 border-b border-slate-700">
              <div>
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-xl bg-orange-600 flex items-center justify-center text-white font-bold">
                    <Calendar size={18} />
                  </div>
                  <h2 className="text-2xl font-bold text-white">Instant Home Healthcare Scheduling (INR ₹)</h2>
                </div>
                <p className="text-xs text-slate-400 mt-1">Book certified nursing, physiotherapy, and diagnostic assessment at your doorstep.</p>
              </div>

              <div className="px-3 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-bold flex items-center gap-1.5">
                <CheckCircle2 size={16} /> Verified Staff Dispatch Ready
              </div>
            </div>

            {/* Booking Success View */}
            {bookingSuccess ? (
              <div className="py-12 text-center animate-scale-in">
                <div className="w-16 h-16 rounded-3xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center justify-center mx-auto mb-4">
                  <CheckCircle2 size={36} />
                </div>
                <h3 className="text-2xl font-bold text-white">Home Visit Booked Successfully!</h3>
                <p className="text-sm text-slate-300 mt-2 max-w-md mx-auto">
                  Booking <strong>#{bookingSuccess.id}</strong> for <strong>{bookingSuccess.service}</strong> (₹{bookingSuccess.price}) has been confirmed for <strong>{bookingSuccess.patient}</strong>.
                </p>
                <div className="flex justify-center gap-3 mt-6">
                  <button
                    onClick={() => { setBookingSuccess(null); }}
                    className="px-5 py-2.5 bg-slate-700 hover:bg-slate-600 text-white rounded-xl text-xs font-semibold cursor-pointer"
                  >
                    + Book Another Visit
                  </button>
                  <button
                    onClick={() => handlePatientQuickLogin("aarav.patient@gmail.com")}
                    className="px-5 py-2.5 bg-orange-600 hover:bg-orange-700 text-white rounded-xl text-xs font-bold shadow-lg shadow-orange-600/30 cursor-pointer flex items-center gap-1.5"
                  >
                    View in Patient Portal <ArrowRight size={14} />
                  </button>
                </div>
              </div>
            ) : (
              <form onSubmit={handleBookAppointment} className="mt-6 space-y-6">
                {/* Step 1: Service Cards */}
                <div>
                  <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                    <Layers size={14} className="text-orange-400" /> 1. Select Clinical Service in Rupees (₹)
                  </label>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                    {services.map((s) => (
                      <div
                        key={s.id}
                        onClick={() => setSelectedServiceId(s.id.toString())}
                        className={`p-4 rounded-2xl border transition-all cursor-pointer flex flex-col justify-between text-left ${
                          selectedServiceId === s.id.toString()
                            ? "bg-orange-600/20 border-orange-500 shadow-md shadow-orange-500/20 ring-2 ring-orange-500"
                            : "bg-slate-700/50 hover:bg-slate-700 border-slate-600 text-slate-300"
                        }`}
                      >
                        <div>
                          <div className="flex justify-between items-start mb-2">
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-white/10 text-orange-300">
                              {s.category}
                            </span>
                            <span className="text-sm font-extrabold text-white">₹{s.base_price}</span>
                          </div>
                          <div className="text-xs font-bold text-white">{s.name}</div>
                          <div className="text-[10px] text-slate-400 mt-1 line-clamp-2">{s.description}</div>
                        </div>
                        <div className="text-[10px] text-slate-400 mt-3 flex items-center gap-1 font-mono">
                          <Clock size={12} /> {s.duration_minutes} mins
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Step 2 & 3: Details & Time */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-slate-700">
                  <div>
                    <label className="block text-xs font-bold text-slate-300 mb-1.5">2. Preferred Staff / Nurse</label>
                    <select
                      value={selectedCaregiverId}
                      onChange={(e) => setSelectedCaregiverId(e.target.value)}
                      className="w-full px-3 py-2.5 rounded-xl bg-slate-900 border border-slate-600 text-white text-xs focus:border-orange-500 focus:outline-hidden"
                    >
                      <option value="">-- Auto-Dispatch Available Staff --</option>
                      {caregivers.map((cg) => (
                        <option key={cg.id} value={cg.id}>
                          {cg.full_name} ({cg.specialization})
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-300 mb-1.5">3. Preferred Date & Time</label>
                    <input
                      type="datetime-local"
                      required
                      value={bookingDate}
                      onChange={(e) => setBookingDate(e.target.value)}
                      className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-600 text-white text-xs focus:border-orange-500 focus:outline-hidden"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-300 mb-1.5">4. Patient Full Name</label>
                    <input
                      type="text"
                      required
                      value={patientName}
                      onChange={(e) => setPatientName(e.target.value)}
                      className="w-full px-3 py-2.5 rounded-xl bg-slate-900 border border-slate-600 text-white text-xs focus:border-orange-500 focus:outline-hidden"
                      placeholder="e.g. Aarav Sharma"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-slate-300 mb-1.5">Mobile Number (+91)</label>
                    <input
                      type="tel"
                      required
                      value={patientPhone}
                      onChange={(e) => setPatientPhone(e.target.value)}
                      className="w-full px-3 py-2.5 rounded-xl bg-slate-900 border border-slate-600 text-white text-xs focus:border-orange-500 focus:outline-hidden"
                      placeholder="+91 98450 12345"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-300 mb-1.5">Home Address & Landmark</label>
                    <input
                      type="text"
                      required
                      value={patientAddress}
                      onChange={(e) => setPatientAddress(e.target.value)}
                      className="w-full px-3 py-2.5 rounded-xl bg-slate-900 border border-slate-600 text-white text-xs focus:border-orange-500 focus:outline-hidden"
                      placeholder="Flat, Apartment, Street, City"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-300 mb-1.5">Special Medical Notes / Symptoms</label>
                  <textarea
                    rows={2}
                    value={bookingNotes}
                    onChange={(e) => setBookingNotes(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-600 text-white text-xs focus:border-orange-500 focus:outline-hidden"
                    placeholder="e.g. Fasting sugar test, gate code 4022, post-surgery knee rehab..."
                  />
                </div>

                {/* Submit Action */}
                <div className="flex flex-col sm:flex-row justify-between items-center gap-4 pt-4 border-t border-slate-700">
                  <div className="text-xs text-slate-400">
                    Estimated Fee: <strong className="text-lg text-white font-bold ml-1">₹{selectedServiceObj?.base_price || 799}</strong> (Pay via UPI / Card upon confirmation)
                  </div>

                  <button
                    type="submit"
                    disabled={bookingLoading}
                    className="w-full sm:w-auto px-8 py-3.5 bg-linear-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-bold rounded-xl text-sm shadow-xl shadow-orange-500/20 transition-all duration-300 hover:scale-105 cursor-pointer disabled:opacity-50 flex items-center justify-center gap-2"
                  >
                    <CheckCircle2 size={18} />
                    {bookingLoading ? "Confirming Booking..." : `Confirm & Book Home Visit (₹${selectedServiceObj?.base_price || 799})`}
                  </button>
                </div>
              </form>
            )}
          </div>
        </section>
      )}

      {/* Admin Login Modal Dialog */}
      {showAdminModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50 backdrop-blur-md animate-fade-in">
          <div className="bg-slate-900 rounded-3xl p-8 max-w-md w-full border border-slate-700 shadow-2xl animate-scale-in relative text-left">
            <button
              onClick={() => setShowAdminModal(false)}
              className="absolute top-6 right-6 p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors cursor-pointer"
            >
              <X size={20} />
            </button>

            <div className="w-12 h-12 rounded-2xl bg-orange-600/20 border border-orange-500/30 flex items-center justify-center text-orange-400 mb-4 shadow-md">
              <Lock size={24} />
            </div>

            <h3 className="text-2xl font-bold text-white">Admin & Staff Sign In</h3>
            <p className="text-xs text-slate-400 mt-1 mb-6">Enter administrative credentials or pick a simulator account.</p>

            {adminError && (
              <div className="p-3 mb-4 rounded-xl bg-rose-500/20 border border-rose-500/30 text-rose-300 text-xs font-semibold">
                {adminError}
              </div>
            )}

            <form onSubmit={handleAdminLogin} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Staff / Admin Email ID</label>
                <div className="relative">
                  <Mail size={16} className="absolute left-3.5 top-3 text-slate-500" />
                  <input
                    type="email"
                    required
                    value={adminEmail}
                    onChange={(e) => setAdminEmail(e.target.value)}
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-800 border border-slate-700 text-white text-xs focus:border-orange-500 focus:outline-hidden"
                    placeholder="admin@healthcare.in"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Password</label>
                <div className="relative">
                  <Lock size={16} className="absolute left-3.5 top-3 text-slate-500" />
                  <input
                    type="password"
                    required
                    value={adminPassword}
                    onChange={(e) => setAdminPassword(e.target.value)}
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-800 border border-slate-700 text-white text-xs focus:border-orange-500 focus:outline-hidden"
                    placeholder="••••••••"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={adminLoading}
                className="w-full py-3 bg-orange-600 hover:bg-orange-700 text-white font-bold rounded-xl text-xs shadow-lg shadow-orange-600/30 transition-all cursor-pointer disabled:opacity-50 flex items-center justify-center gap-2"
              >
                <ShieldCheck size={16} />
                {adminLoading ? "Authenticating..." : "Unlock Admin Workspace"}
              </button>
            </form>

            {/* Quick Persona Switcher in modal */}
            <div className="mt-6 pt-4 border-t border-slate-800">
              <span className="text-[10px] uppercase font-bold text-slate-400 block mb-2">1-Click Quick Fill:</span>
              <div className="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  onClick={() => { setAdminEmail("admin@healthcare.in"); setAdminPassword("admin123"); }}
                  className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-[11px] font-bold text-indigo-300 text-center cursor-pointer"
                >
                  Admin
                </button>
                <button
                  type="button"
                  onClick={() => { setAdminEmail("dr.rajesh@healthcare.in"); setAdminPassword("doctor123"); }}
                  className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-[11px] font-bold text-emerald-300 text-center cursor-pointer"
                >
                  Dr. Rajesh
                </button>
                <button
                  type="button"
                  onClick={() => { setAdminEmail("anjali.nurse@healthcare.in"); setAdminPassword("caregiver123"); }}
                  className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-[11px] font-bold text-amber-300 text-center cursor-pointer"
                >
                  Sister Anjali
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="relative z-10 max-w-7xl mx-auto w-full px-6 py-6 border-t border-white/10 text-center text-xs text-slate-500">
        CareFleet India &bull; Home Healthcare Clinical Management &bull; Built with FastAPI & React (INR ₹)
      </footer>
    </div>
  );
}
