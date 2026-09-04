# Indian Localization updater
import os
print("Initialized Indian updater")

mainlayout_src = """import React, { useEffect, useState } from "react";
import { Outlet, Link, useLocation, useNavigate } from "react-router-dom";
import { 
  LayoutDashboard, 
  Calendar, 
  Users, 
  HeartHandshake, 
  Stethoscope, 
  FileText, 
  IndianRupee, 
  LogOut, 
  Activity,
  Layers
} from "lucide-react";
import api from "../api/axios";

const navItems = [
  { name: "Dashboard", path: "/", icon: LayoutDashboard },
  { name: "Appointments", path: "/appointments", icon: Calendar },
  { name: "Patients & EHR", path: "/patients", icon: Users },
  { name: "Caregivers & Nurses", path: "/caregivers", icon: HeartHandshake },
  { name: "Services Catalog", path: "/services", icon: Layers },
  { name: "Care Plans", path: "/care-plans", icon: Stethoscope },
  { name: "Billing & GST Invoices", path: "/billing", icon: IndianRupee },
  { name: "Clinical Documents", path: "/documents", icon: FileText },
];

export default function MainLayout() {
  const location = useLocation();
  const navigate = useNavigate();
  const [currentUser, setCurrentUser] = useState<any>(null);

  useEffect(() => {
    const userStr = localStorage.getItem("user");
    if (!userStr && !localStorage.getItem("token")) {
      switchPersona("admin@healthcare.in", "admin123");
    } else if (userStr) {
      setCurrentUser(JSON.parse(userStr));
    }
  }, []);

  const switchPersona = async (email: string, pass: string) => {
    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", pass);
      const res = await api.post("/auth/login", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
      });
      localStorage.setItem("token", res.data.access_token);
      
      const meRes = await api.get("/auth/me");
      localStorage.setItem("user", JSON.stringify(meRes.data));
      setCurrentUser(meRes.data);
      window.location.reload();
    } catch (err) {
      console.error("Failed to switch persona:", err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col justify-between shrink-0">
        <div>
          <div className="h-16 flex items-center gap-3 px-6 border-b border-slate-100">
            <div className="w-9 h-9 rounded-xl bg-orange-600 flex items-center justify-center text-white font-bold shadow-md shadow-orange-500/20">
              <Activity size={20} />
            </div>
            <div>
              <span className="font-bold text-slate-800 text-base leading-none block">CareFleet India</span>
              <span className="text-[10px] text-orange-600 font-semibold tracking-wider uppercase">HealthCare OS (INR)</span>
            </div>
          </div>

          <div className="p-4">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider px-3 mb-2 block">Healthcare Modules</span>
            <nav className="space-y-1">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.path;
                return (
                  <Link
                    key={item.name}
                    to={item.path}
                    className={"flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-medium transition-all " + (
                      isActive
                        ? "bg-orange-600 text-white shadow-sm shadow-orange-500/30"
                        : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                    )}
                  >
                    <Icon size={16} />
                    <span>{item.name}</span>
                  </Link>
                );
              })}
            </nav>
          </div>
        </div>

        {/* User Footer */}
        <div className="p-4 border-t border-slate-100 bg-slate-50/50">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5 min-w-0">
              <div className="w-8 h-8 rounded-full bg-orange-100 text-orange-700 flex items-center justify-center font-bold text-xs uppercase">
                {currentUser?.full_name ? currentUser.full_name.charAt(0) : "U"}
              </div>
              <div className="min-w-0">
                <div className="text-xs font-semibold text-slate-800 truncate">{currentUser?.full_name || "Admin User"}</div>
                <div className="text-[10px] font-bold text-orange-600 uppercase">{currentUser?.role || "Admin"} (IN)</div>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors cursor-pointer"
              title="Logout"
            >
              <LogOut size={16} />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top Header / Indian Persona Switcher */}
        <header className="h-16 bg-white border-b border-slate-200 px-6 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-slate-400">1-Click Persona:</span>
            <div className="flex gap-1.5 bg-slate-100 p-1 rounded-xl">
              <button
                onClick={() => switchPersona("admin@healthcare.in", "admin123")}
                className={"px-2.5 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer " + (
                  currentUser?.role === "ADMIN" ? "bg-white text-orange-600 shadow-xs" : "text-slate-600 hover:text-slate-900"
                )}
              >
                Admin
              </button>
              <button
                onClick={() => switchPersona("dr.rajesh@healthcare.in", "doctor123")}
                className={"px-2.5 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer " + (
                  currentUser?.role === "DOCTOR" ? "bg-white text-orange-600 shadow-xs" : "text-slate-600 hover:text-slate-900"
                )}
              >
                Dr. Rajesh (MD)
              </button>
              <button
                onClick={() => switchPersona("anjali.nurse@healthcare.in", "caregiver123")}
                className={"px-2.5 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer " + (
                  currentUser?.role === "CAREGIVER" ? "bg-white text-orange-600 shadow-xs" : "text-slate-600 hover:text-slate-900"
                )}
              >
                Sister Anjali (RN)
              </button>
              <button
                onClick={() => switchPersona("aarav.patient@gmail.com", "patient123")}
                className={"px-2.5 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer " + (
                  currentUser?.role === "PATIENT" ? "bg-white text-orange-600 shadow-xs" : "text-slate-600 hover:text-slate-900"
                )}
              >
                Aarav Sharma
              </button>
            </div>
          </div>

          <div className="flex items-center gap-3 text-xs">
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 font-semibold border border-emerald-200">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              India Region (INR ₹)
            </span>
          </div>
        </header>

        {/* Dynamic Page Outlet */}
        <main className="flex-1 overflow-y-auto p-6 bg-slate-50">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
"""
open("frontend/src/layouts/MainLayout.tsx", "w", encoding="utf-8").write(mainlayout_src)
print("Updated MainLayout")

login_src = """import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Activity, ShieldCheck, UserCheck } from "lucide-react";
import api from "../api/axios";

const demoAccounts = [
  { role: "Hospital Administrator", email: "admin@healthcare.in", pass: "admin123", color: "bg-indigo-50 border-indigo-200 text-indigo-700" },
  { role: "Dr. Rajesh Sharma (MD)", email: "dr.rajesh@healthcare.in", pass: "doctor123", color: "bg-emerald-50 border-emerald-200 text-emerald-700" },
  { role: "Sister Anjali Verma (RN)", email: "anjali.nurse@healthcare.in", pass: "caregiver123", color: "bg-amber-50 border-amber-200 text-amber-700" },
  { role: "Aarav Sharma (Patient)", email: "aarav.patient@gmail.com", pass: "patient123", color: "bg-blue-50 border-blue-200 text-blue-700" }
];

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("admin@healthcare.in");
  const [password, setPassword] = useState("admin123");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const res = await api.post("/auth/login", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
      });

      localStorage.setItem("token", res.data.access_token);

      const meRes = await api.get("/auth/me");
      localStorage.setItem("user", JSON.stringify(meRes.data));

      navigate("/");
    } catch (err: any) {
      console.error(err);
      setError(err?.response?.data?.detail || "Authentication failed");
    } finally {
      setLoading(false);
    }
  };

  const handleQuickLogin = (accEmail: string, accPass: string) => {
    setEmail(accEmail);
    setPassword(accPass);
    setTimeout(() => {
      handleLogin();
    }, 50);
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <div className="w-12 h-12 rounded-2xl bg-orange-600 flex items-center justify-center text-white mx-auto mb-3 shadow-lg shadow-orange-500/20">
            <Activity size={26} />
          </div>
          <h1 className="text-2xl font-bold text-slate-800">CareFleet India</h1>
          <p className="text-xs text-slate-500 mt-1">Home Healthcare Management & Clinical EHR (INR ₹ Edition)</p>
        </div>

        <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-xl shadow-slate-200/50 mb-6">
          <h2 className="text-lg font-bold text-slate-800 mb-1">Sign in</h2>
          <p className="text-xs text-slate-500 mb-6">Select an Indian persona or enter credentials.</p>

          {error && (
            <div className="p-3 mb-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs font-medium">
              {error}
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Email ID</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:outline-hidden focus:border-orange-600 text-xs transition-colors"
                placeholder="name@healthcare.in"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Password</label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:outline-hidden focus:border-orange-600 text-xs transition-colors"
                placeholder="••••••••"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-orange-600 hover:bg-orange-700 text-white font-semibold rounded-xl text-xs shadow-md shadow-orange-500/20 transition-all flex items-center justify-center gap-2 disabled:opacity-50 cursor-pointer"
            >
              <ShieldCheck size={16} />
              {loading ? "Authenticating..." : "Sign In (India)"}
            </button>
          </form>
        </div>

        {/* 1-Click Quick Indian Demo Switchers */}
        <div className="bg-white rounded-2xl p-5 border border-slate-100 shadow-xs">
          <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
            <UserCheck size={14} /> Quick Persona Sign-In (India)
          </div>
          <div className="grid grid-cols-2 gap-2">
            {demoAccounts.map((acc) => (
              <button
                key={acc.role}
                type="button"
                onClick={() => handleQuickLogin(acc.email, acc.pass)}
                className={"p-2.5 rounded-xl border text-left text-xs transition-all hover:shadow-xs cursor-pointer " + acc.color}
              >
                <div className="font-bold leading-tight">{acc.role}</div>
                <div className="text-[10px] opacity-75 mt-0.5 truncate">{acc.email}</div>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
"""
open("frontend/src/pages/Login.tsx", "w", encoding="utf-8").write(login_src)

dashboard_src = """import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { 
  Users, 
  Calendar, 
  HeartHandshake, 
  IndianRupee, 
  Clock, 
  ArrowUpRight,
  Layers
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

  useEffect(() => {
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
        activeAppointments: appointments.filter((a: any) => a.status === "SCHEDULED" || a.status === "IN_PROGRESS").length,
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

  const statCards = [
    { title: "Registered Patients", value: stats.totalPatients, icon: Users, color: "text-blue-600 bg-blue-50", link: "/patients" },
    { title: "Active Visits", value: stats.activeAppointments, icon: Calendar, color: "text-amber-600 bg-amber-50", link: "/appointments" },
    { title: "Nursing Staff & Physios", value: stats.totalCaregivers, icon: HeartHandshake, color: "text-emerald-600 bg-emerald-50", link: "/caregivers" },
    { title: "Pending Invoices (₹)", value: stats.pendingInvoices, icon: IndianRupee, color: "text-purple-600 bg-purple-50", link: "/billing" }
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-linear-to-r from-orange-600 to-amber-600 rounded-3xl p-6 text-white shadow-xl shadow-orange-500/10 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <span className="text-[11px] font-bold bg-white/20 px-3 py-1 rounded-full uppercase tracking-wider">India Clinical Operations</span>
          <h1 className="text-2xl font-bold mt-2">Home Healthcare Command Center</h1>
          <p className="text-xs text-orange-100 mt-1">EHR Management, Caregiver Telemetry & UPI Billing (INR ₹).</p>
        </div>
        <div className="flex gap-2">
          <Link
            to="/appointments"
            className="px-4 py-2 bg-white text-orange-700 hover:bg-orange-50 font-bold rounded-xl text-xs transition-all shadow-sm flex items-center gap-1.5"
          >
            Manage Schedule <ArrowUpRight size={14} />
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
        {/* Recent Schedule */}
        <div className="lg:col-span-2 bg-white rounded-3xl p-6 border border-slate-100 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-bold text-slate-800 flex items-center gap-2">
              <Calendar size={18} className="text-orange-600" /> Recent Appointments
            </h2>
            <Link to="/appointments" className="text-xs font-bold text-orange-600 hover:underline">
              View all
            </Link>
          </div>

          {loading ? (
            <div className="p-8 text-center text-slate-400 text-xs">Loading appointments...</div>
          ) : recentAppointments.length === 0 ? (
            <div className="p-8 text-center text-slate-400 text-xs">No appointments scheduled.</div>
          ) : (
            <div className="divide-y divide-slate-100">
              {recentAppointments.map((appt) => (
                <div key={appt.id} className="py-3.5 flex items-center justify-between first:pt-0 last:pb-0">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center text-slate-600 font-bold text-xs">
                      #{appt.id}
                    </div>
                    <div>
                      <div className="text-xs font-bold text-slate-800">Patient ID: #{appt.patient_id}</div>
                      <div className="text-[11px] text-slate-400 flex items-center gap-1 mt-0.5">
                        <Clock size={12} /> {new Date(appt.scheduled_start).toLocaleString()}
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
              <Layers size={18} className="text-orange-600" /> Services Catalog (INR ₹)
            </h2>
            <Link to="/services" className="text-xs font-bold text-orange-600 hover:underline">
              Catalog
            </Link>
          </div>

          {loading ? (
            <div className="p-8 text-center text-slate-400 text-xs">Loading services...</div>
          ) : (
            <div className="space-y-3">
              {services.slice(0, 5).map((s) => (
                <div key={s.id} className="p-3 rounded-2xl bg-slate-50 border border-slate-100 flex items-center justify-between">
                  <div>
                    <h4 className="text-xs font-bold text-slate-800">{s.name}</h4>
                    <p className="text-[10px] text-slate-500 mt-0.5">{s.duration_minutes} mins</p>
                  </div>
                  <span className="text-xs font-bold text-orange-600">₹{s.base_price}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
"""
open("frontend/src/pages/Dashboard.tsx", "w", encoding="utf-8").write(dashboard_src)
print("Updated Login and Dashboard")

billing_src = """import React, { useEffect, useState } from "react";
import api from "../api/axios";
import { IndianRupee, CheckCircle2, Clock, ShieldCheck, QrCode } from "lucide-react";

export default function Billing() {
  const [invoices, setInvoices] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [payingId, setPayingId] = useState<number | null>(null);

  useEffect(() => {
    fetchInvoices();
  }, []);

  const fetchInvoices = async () => {
    setLoading(true);
    try {
      const res = await api.get("/billing/invoices").catch(async () => {
        return { data: [] };
      });
      setInvoices(res.data || []);
    } catch (err) {
      console.error("Error fetching invoices:", err);
    } finally {
      setLoading(false);
    }
  };

  const handlePayInvoice = async (invoice: any) => {
    setPayingId(invoice.id);
    try {
      await api.post("/billing/payments", {
        invoice_id: invoice.id,
        amount: invoice.total,
        payment_method: "UPI_GPAY_SANDBOX"
      });
      alert("Payment of ₹" + invoice.total?.toFixed(2) + " completed via UPI / RuPay!");
      fetchInvoices();
    } catch (err: any) {
      alert(err?.response?.data?.detail || "Payment failed.");
    } finally {
      setPayingId(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">GST Invoices & Billing (INR ₹)</h1>
          <p className="text-xs text-slate-500 mt-1">18% GST Compliant Healthcare Invoices, UPI, RuPay & NetBanking.</p>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-semibold">
          <ShieldCheck size={16} /> UPI & Razorpay Sandbox Active
        </div>
      </div>

      {loading ? (
        <div className="p-8 text-center text-slate-400 text-sm">Loading invoices...</div>
      ) : invoices.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-100">
          <IndianRupee size={36} className="mx-auto text-slate-300 mb-2" />
          <p className="text-sm text-slate-500 font-medium">No invoices found.</p>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-slate-100 text-slate-400 text-xs font-semibold uppercase bg-slate-50/50">
                  <th className="p-4">Invoice #</th>
                  <th className="p-4">Patient ID</th>
                  <th className="p-4">Base Fee (₹)</th>
                  <th className="p-4">GST (18%)</th>
                  <th className="p-4">Total Amount (₹)</th>
                  <th className="p-4">Payment Status</th>
                  <th className="p-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-xs">
                {invoices.map((inv) => (
                  <tr key={inv.id} className="hover:bg-slate-50/70 transition-colors">
                    <td className="p-4 font-mono font-bold text-slate-800">{inv.invoice_number}</td>
                    <td className="p-4 text-slate-600 font-mono">#{inv.patient_id}</td>
                    <td className="p-4 text-slate-700 font-medium">₹{inv.base_price?.toFixed(2)}</td>
                    <td className="p-4 text-slate-500">₹{inv.tax?.toFixed(2)}</td>
                    <td className="p-4 font-bold text-slate-900 text-sm">₹{inv.total?.toFixed(2)}</td>
                    <td className="p-4">
                      {inv.status === "PAID" ? (
                        <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200 flex items-center gap-1 w-fit">
                          <CheckCircle2 size={12} /> PAID
                        </span>
                      ) : (
                        <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-amber-100 text-amber-800 border border-amber-200 flex items-center gap-1 w-fit">
                          <Clock size={12} /> PENDING
                        </span>
                      )}
                    </td>
                    <td className="p-4 text-right">
                      {inv.status === "PENDING" ? (
                        <button
                          disabled={payingId === inv.id}
                          onClick={() => handlePayInvoice(inv)}
                          className="px-3 py-1.5 bg-orange-600 hover:bg-orange-700 text-white font-semibold rounded-lg shadow-sm transition-all flex items-center gap-1.5 ml-auto text-xs disabled:opacity-50 cursor-pointer"
                        >
                          <QrCode size={14} /> {payingId === inv.id ? "Processing..." : "Pay via UPI (₹)"}
                        </button>
                      ) : (
                        <span className="text-emerald-600 font-medium text-xs">Settled (UPI)</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
"""
open("frontend/src/pages/Billing.tsx", "w", encoding="utf-8").write(billing_src)

services_src = """import React, { useEffect, useState } from "react";
import api from "../api/axios";
import { Layers, Clock, Plus } from "lucide-react";

export default function Services() {
  const [services, setServices] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [newService, setNewService] = useState({
    name: "",
    description: "",
    category: "NURSING",
    base_price: "",
    duration_minutes: "60"
  });

  useEffect(() => {
    fetchServices();
  }, []);

  const fetchServices = async () => {
    setLoading(true);
    try {
      const res = await api.get("/services/");
      setServices(res.data || []);
    } catch (err) {
      console.error("Error fetching services:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateService = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post("/services/", {
        name: newService.name,
        description: newService.description,
        category: newService.category,
        base_price: parseFloat(newService.base_price),
        duration_minutes: parseInt(newService.duration_minutes)
      });
      setShowModal(false);
      setNewService({ name: "", description: "", category: "NURSING", base_price: "", duration_minutes: "60" });
      fetchServices();
    } catch (err: any) {
      alert(err?.response?.data?.detail || "Failed to create service");
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Clinical Home Services (INR ₹)</h1>
          <p className="text-xs text-slate-500 mt-1">Certified home nursing, physiotherapy, and medical care rates in Indian Rupees.</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2.5 bg-orange-600 hover:bg-orange-700 text-white font-medium rounded-xl text-xs flex items-center gap-2 shadow-sm transition-all cursor-pointer"
        >
          <Plus size={16} /> Add Clinical Service
        </button>
      </div>

      {loading ? (
        <div className="p-8 text-center text-slate-400 text-sm">Loading services...</div>
      ) : services.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-100">
          <Layers size={36} className="mx-auto text-slate-300 mb-2" />
          <p className="text-sm text-slate-500 font-medium">No services found.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {services.map((s) => (
            <div key={s.id} className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 flex flex-col justify-between hover:shadow-md transition-shadow">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-orange-50 text-orange-700 border border-orange-200">
                    {s.category}
                  </span>
                  <span className="text-sm font-bold text-slate-900">₹{s.base_price?.toFixed(2)}</span>
                </div>

                <h3 className="text-base font-bold text-slate-800">{s.name}</h3>
                <p className="text-xs text-slate-500 mt-2">{s.description}</p>
              </div>

              <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-400">
                <span className="flex items-center gap-1"><Clock size={14} /> {s.duration_minutes} Mins</span>
                <span className="text-emerald-600 font-medium">&bull; Active in India</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {showModal && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-50 backdrop-blur-xs">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full shadow-2xl border border-slate-100">
            <h3 className="text-lg font-bold text-slate-800 mb-1">Add Clinical Service</h3>
            <p className="text-xs text-slate-500 mb-4">Define service name, duration, and price in INR (₹).</p>

            <form onSubmit={handleCreateService} className="space-y-3 text-sm">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Service Name</label>
                <input
                  type="text"
                  required
                  value={newService.name}
                  onChange={(e) => setNewService({ ...newService, name: e.target.value })}
                  placeholder="e.g. IV Infusion & Cannulation"
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Category</label>
                <select
                  value={newService.category}
                  onChange={(e) => setNewService({ ...newService, category: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                >
                  <option value="NURSING">Nursing</option>
                  <option value="THERAPY">Physiotherapy</option>
                  <option value="PERSONAL_CARE">Attendant Care</option>
                  <option value="SPECIALIZED">Specialized / ICU</option>
                </select>
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Fee in Rupees (₹)</label>
                  <input
                    type="number"
                    step="1"
                    required
                    value={newService.base_price}
                    onChange={(e) => setNewService({ ...newService, base_price: e.target.value })}
                    placeholder="799"
                    className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Duration (Mins)</label>
                  <input
                    type="number"
                    required
                    value={newService.duration_minutes}
                    onChange={(e) => setNewService({ ...newService, duration_minutes: e.target.value })}
                    placeholder="60"
                    className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Description</label>
                <textarea
                  rows={2}
                  required
                  value={newService.description}
                  onChange={(e) => setNewService({ ...newService, description: e.target.value })}
                  placeholder="Clinical protocol details..."
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-100 cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-lg text-xs font-semibold bg-orange-600 hover:bg-orange-700 text-white shadow-sm cursor-pointer"
                >
                  Save Service (INR)
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
"""
open("frontend/src/pages/Services.tsx", "w", encoding="utf-8").write(services_src)

appt_src = """import React, { useEffect, useState } from "react";
import api from "../api/axios";
import { Calendar, Clock, User, Plus, HeartHandshake } from "lucide-react";

export default function Appointments() {
  const [appointments, setAppointments] = useState<any[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [caregivers, setCaregivers] = useState<any[]>([]);
  const [services, setServices] = useState<any[]>([]);
  const [filter, setFilter] = useState("ALL");
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  const [newAppt, setNewAppt] = useState({
    patient_id: "",
    caregiver_id: "",
    service_id: "",
    scheduled_start: "",
    scheduled_end: "",
    notes: ""
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [apptRes, patRes, cgRes, srvRes] = await Promise.all([
        api.get("/appointments/").catch(() => ({ data: [] })),
        api.get("/patients/").catch(() => ({ data: [] })),
        api.get("/caregivers/").catch(() => ({ data: [] })),
        api.get("/services/").catch(() => ({ data: [] }))
      ]);
      setAppointments(apptRes.data || []);
      setPatients(patRes.data || []);
      setCaregivers(cgRes.data || []);
      setServices(srvRes.data || []);
    } catch (err) {
      console.error("Error fetching appointments data:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateStatus = async (id: number, status: string) => {
    try {
      await api.patch("/appointments/" + id + "/status", { status });
      loadData();
    } catch (err: any) {
      alert(err?.response?.data?.detail || "Failed to update status");
    }
  };

  const handleCreateAppointment = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        patient_id: Number(newAppt.patient_id || (patients[0]?.id ?? 1)),
        caregiver_id: Number(newAppt.caregiver_id || (caregivers[0]?.id ?? 1)),
        service_id: Number(newAppt.service_id || (services[0]?.id ?? 1)),
        scheduled_start: newAppt.scheduled_start || new Date().toISOString(),
        scheduled_end: newAppt.scheduled_end || new Date(Date.now() + 3600000).toISOString(),
        notes: newAppt.notes
      };
      await api.post("/appointments/", payload);
      setShowModal(false);
      loadData();
    } catch (err: any) {
      alert(err?.response?.data?.detail || "Failed to create appointment");
    }
  };

  const filtered = appointments.filter(a => {
    if (filter === "ALL") return true;
    return a.status === filter;
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Home Care Visits & Appointments</h1>
          <p className="text-xs text-slate-500 mt-1">Nurse dispatch schedules, visit verification, and care tracking in India.</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2.5 bg-orange-600 hover:bg-orange-700 text-white font-medium rounded-xl text-xs flex items-center gap-2 shadow-sm transition-all cursor-pointer"
        >
          <Plus size={16} /> Schedule Visit
        </button>
      </div>

      <div className="flex gap-2 border-b border-slate-200 pb-2">
        {["ALL", "SCHEDULED", "IN_PROGRESS", "COMPLETED", "CANCELLED"].map((s) => (
          <button
            key={s}
            onClick={() => setFilter(s)}
            className={"px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer " + (filter === s ? "bg-orange-600 text-white" : "bg-slate-100 text-slate-600 hover:bg-slate-200")}
          >
            {s.replace("_", " ")}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="p-8 text-center text-slate-400 text-sm">Loading visits schedule...</div>
      ) : filtered.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-100">
          <Calendar size={36} className="mx-auto text-slate-300 mb-2" />
          <p className="text-sm text-slate-500 font-medium">No appointments match this filter.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((appt) => (
            <div key={appt.id} className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5 flex flex-col justify-between hover:shadow-md transition-shadow">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className={"px-2.5 py-1 text-xs font-semibold rounded-full " + (
                    appt.status === "COMPLETED" ? "bg-emerald-50 text-emerald-700 border border-emerald-200" :
                    appt.status === "SCHEDULED" ? "bg-blue-50 text-blue-700 border border-blue-200" :
                    appt.status === "IN_PROGRESS" ? "bg-amber-50 text-amber-700 border border-amber-200" :
                    "bg-slate-100 text-slate-600"
                  )}>
                    {appt.status}
                  </span>
                  <span className="text-xs font-mono text-slate-400">Visit #{appt.id}</span>
                </div>

                <div className="space-y-2 text-xs text-slate-600">
                  <div className="flex items-center gap-2">
                    <User size={14} className="text-orange-600" />
                    <span className="font-medium text-slate-800">Patient ID: #{appt.patient_id}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <HeartHandshake size={14} className="text-emerald-600" />
                    <span>Staff ID: #{appt.caregiver_id}</span>
                  </div>
                  <div className="flex items-center gap-2 text-slate-500">
                    <Clock size={14} />
                    <span>{new Date(appt.scheduled_start).toLocaleString()}</span>
                  </div>
                  {appt.notes && (
                    <div className="mt-2 p-2 rounded-lg bg-slate-50 border border-slate-100 text-slate-600 italic">
                      "{appt.notes}"
                    </div>
                  )}
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-end gap-2 text-xs">
                {appt.status === "SCHEDULED" && (
                  <>
                    <button
                      onClick={() => handleUpdateStatus(appt.id, "IN_PROGRESS")}
                      className="px-2.5 py-1 bg-amber-50 text-amber-700 font-semibold rounded-lg hover:bg-amber-100 cursor-pointer"
                    >
                      Start Visit
                    </button>
                    <button
                      onClick={() => handleUpdateStatus(appt.id, "CANCELLED")}
                      className="px-2.5 py-1 bg-rose-50 text-rose-700 font-semibold rounded-lg hover:bg-rose-100 cursor-pointer"
                    >
                      Cancel
                    </button>
                  </>
                )}
                {appt.status === "IN_PROGRESS" && (
                  <button
                    onClick={() => handleUpdateStatus(appt.id, "COMPLETED")}
                    className="px-2.5 py-1 bg-emerald-600 text-white font-semibold rounded-lg hover:bg-emerald-700 cursor-pointer"
                  >
                    Complete Visit
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {showModal && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-50 backdrop-blur-xs">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full shadow-2xl border border-slate-100">
            <h3 className="text-lg font-bold text-slate-800 mb-1">Schedule Home Visit</h3>
            <p className="text-xs text-slate-500 mb-4">Assign certified nurse/physiotherapist to patient.</p>

            <form onSubmit={handleCreateAppointment} className="space-y-3 text-sm">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Patient</label>
                <select
                  value={newAppt.patient_id}
                  onChange={(e) => setNewAppt({ ...newAppt, patient_id: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                >
                  {patients.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.full_name} ({p.phone})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Caregiver / Nurse</label>
                <select
                  value={newAppt.caregiver_id}
                  onChange={(e) => setNewAppt({ ...newAppt, caregiver_id: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                >
                  {caregivers.map((cg) => (
                    <option key={cg.id} value={cg.id}>
                      {cg.full_name} ({cg.specialization})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Clinical Service (INR ₹)</label>
                <select
                  value={newAppt.service_id}
                  onChange={(e) => setNewAppt({ ...newAppt, service_id: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                >
                  {services.map((s) => (
                    <option key={s.id} value={s.id}>
                      {s.name} (₹{s.base_price})
                    </option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Start Time</label>
                  <input
                    type="datetime-local"
                    required
                    value={newAppt.scheduled_start}
                    onChange={(e) => setNewAppt({ ...newAppt, scheduled_start: e.target.value })}
                    className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">End Time</label>
                  <input
                    type="datetime-local"
                    required
                    value={newAppt.scheduled_end}
                    onChange={(e) => setNewAppt({ ...newAppt, scheduled_end: e.target.value })}
                    className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Clinical Notes / Address Landmark</label>
                <textarea
                  rows={2}
                  value={newAppt.notes}
                  onChange={(e) => setNewAppt({ ...newAppt, notes: e.target.value })}
                  placeholder="Gate code, landmark, clinical notes..."
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-100 cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-lg text-xs font-semibold bg-orange-600 hover:bg-orange-700 text-white shadow-sm cursor-pointer"
                >
                  Confirm Appointment
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
"""
open("frontend/src/pages/Appointments.tsx", "w", encoding="utf-8").write(appt_src)
print("Updated Billing, Services, and Appointments!")
