import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { 
  Users, 
  Calendar, 
  HeartHandshake, 
  IndianRupee, 
  Clock, 
  ArrowUpRight,
  Layers,
  CalendarPlus,
  ShieldCheck
} from "lucide-react";
import api from "../api/axios";

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalPatients: 0,
    activeAppointments: 0,
    totalCaregivers: 0,
    pendingInvoices: 0
  });
  const [recentAppointments, setRecentAppointments] = useState<any[]>([]);
  const [services, setServices] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentUser, setCurrentUser] = useState<any>(null);

  useEffect(() => {
    const userStr = localStorage.getItem("user");
    if (userStr) {
      setCurrentUser(JSON.parse(userStr));
    }
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const [pRes, aRes, cgRes, invRes, srvRes] = await Promise.all([
        api.get("/patients/").catch(() => ({ data: [] })),
        api.get("/appointments/").catch(() => ({ data: [] })),
        api.get("/caregivers/").catch(() => ({ data: [] })),
        api.get("/billing/invoices").catch(() => ({ data: [] })),
        api.get("/services/").catch(() => ({ data: [] }))
      ]);

      const patients = pRes.data || [];
      const appointments = aRes.data || [];
      const caregivers = cgRes.data || [];
      const invoices = invRes.data || [];

      setStats({
        totalPatients: patients.length,
        activeAppointments: appointments.filter((a: any) => a.status === "CONFIRMED" || a.status === "IN_PROGRESS").length,
        totalCaregivers: caregivers.length,
        pendingInvoices: invoices.filter((i: any) => i.status === "PENDING").length
      });

      setRecentAppointments(appointments.slice(0, 5));
      setServices(srvRes.data || []);
    } catch (err) {
      console.error("Failed to load dashboard:", err);
    } finally {
      setLoading(false);
    }
  };

  const isPatient = currentUser?.role === "PATIENT";

  const statCards = [
    { title: isPatient ? "My Active Bookings" : "Active Visits", value: stats.activeAppointments, icon: Calendar, color: "text-amber-600 bg-amber-50", link: "/appointments" },
    { title: "Available Nurses & Physios", value: stats.totalCaregivers, icon: HeartHandshake, color: "text-emerald-600 bg-emerald-50", link: "/caregivers" },
    { title: "Clinical Offerings (₹)", value: services.length, icon: Layers, color: "text-blue-600 bg-blue-50", link: "/services" },
    { title: isPatient ? "My Pending Invoices" : "Pending Invoices (₹)", value: stats.pendingInvoices, icon: IndianRupee, color: "text-purple-600 bg-purple-50", link: "/billing" }
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-linear-to-r from-orange-600 to-amber-600 rounded-3xl p-6 text-white shadow-xl shadow-orange-500/10 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <span className="text-[11px] font-bold bg-white/20 px-3 py-1 rounded-full uppercase tracking-wider">
            {isPatient ? "Patient Health Portal" : "India Clinical Operations"}
          </span>
          <h1 className="text-2xl font-bold mt-2">
            {isPatient ? "Welcome, " + (currentUser?.full_name || "Patient") : "Home Healthcare Command Center"}
          </h1>
          <p className="text-xs text-orange-100 mt-1">
            {isPatient 
              ? "Book verified nursing, physiotherapy, and check your electronic health records in INR (₹)."
              : "EHR Management, Caregiver Telemetry & UPI Billing (INR ₹)."}
          </p>
        </div>
        <div className="flex gap-2">
          <Link
            to="/appointments"
            className="px-4 py-2 bg-white text-orange-700 hover:bg-orange-50 font-bold rounded-xl text-xs transition-all shadow-sm flex items-center gap-1.5"
          >
            <CalendarPlus size={14} /> {isPatient ? "Book Home Visit" : "Manage Schedule"} <ArrowUpRight size={14} />
          </Link>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((card) => {
          const Icon = card.icon;
          return (
            <Link
              key={card.title}
              to={card.link}
              className="bg-white rounded-2xl p-5 border border-slate-100 shadow-sm hover:shadow-md transition-shadow flex items-center justify-between"
            >
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{card.title}</p>
                <h3 className="text-2xl font-bold text-slate-800 mt-1">{loading ? "..." : card.value}</h3>
              </div>
              <div className={"p-3.5 rounded-2xl " + card.color}>
                <Icon size={22} />
              </div>
            </Link>
          );
        })}
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Schedule / Visits */}
        <div className="lg:col-span-2 bg-white rounded-3xl p-6 border border-slate-100 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-bold text-slate-800 flex items-center gap-2">
              <Calendar size={18} className="text-orange-600" /> {isPatient ? "My Booked Visits" : "Recent Appointments"}
            </h2>
            <Link to="/appointments" className="text-xs font-bold text-orange-600 hover:underline">
              {isPatient ? "+ Book Visit" : "View all"}
            </Link>
          </div>

          {loading ? (
            <div className="p-8 text-center text-slate-400 text-xs">Loading appointments...</div>
          ) : recentAppointments.length === 0 ? (
            <div className="p-8 text-center text-slate-400 text-xs">
              No appointments scheduled.
              {isPatient && (
                <div className="mt-2">
                  <Link to="/appointments" className="text-orange-600 font-bold hover:underline">Click here to book a home visit.</Link>
                </div>
              )}
            </div>
          ) : (
            <div className="divide-y divide-slate-100">
              {recentAppointments.map((appt) => (
                <div key={appt.id} className="py-3.5 flex items-center justify-between first:pt-0 last:pb-0">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-orange-50 text-orange-700 flex items-center justify-center font-bold text-xs">
                      #{appt.id}
                    </div>
                    <div>
                      <div className="text-xs font-bold text-slate-800">
                        {isPatient ? "Home Healthcare Visit #" + appt.id : "Patient ID: #" + appt.patient_id}
                      </div>
                      <div className="text-[11px] text-slate-400 flex items-center gap-1 mt-0.5">
                        <Clock size={12} /> {new Date(appt.scheduled_date || appt.scheduled_start).toLocaleString()}
                      </div>
                    </div>
                  </div>
                  <span className={"px-2.5 py-1 text-[11px] font-semibold rounded-full " + (
                    appt.status === "COMPLETED" ? "bg-emerald-50 text-emerald-700" :
                    appt.status === "IN_PROGRESS" ? "bg-amber-50 text-amber-700" : "bg-blue-50 text-blue-700"
                  )}>
                    {appt.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Clinical Services Catalog in INR */}
        <div className="bg-white rounded-3xl p-6 border border-slate-100 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-bold text-slate-800 flex items-center gap-2">
              <Layers size={18} className="text-orange-600" /> Book Services (INR ₹)
            </h2>
            <Link to="/services" className="text-xs font-bold text-orange-600 hover:underline">
              All Services
            </Link>
          </div>

          {loading ? (
            <div className="p-8 text-center text-slate-400 text-xs">Loading services...</div>
          ) : (
            <div className="space-y-3">
              {services.slice(0, 5).map((s) => (
                <Link 
                  key={s.id} 
                  to="/services"
                  className="p-3 rounded-2xl bg-slate-50 hover:bg-orange-50/50 border border-slate-100 flex items-center justify-between transition-colors block"
                >
                  <div>
                    <h4 className="text-xs font-bold text-slate-800">{s.name}</h4>
                    <p className="text-[10px] text-slate-500 mt-0.5">{s.duration_minutes} mins &bull; Certified Nurse</p>
                  </div>
                  <span className="text-xs font-bold text-orange-600">₹{s.base_price}</span>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
