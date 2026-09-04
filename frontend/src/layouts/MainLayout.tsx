import React, { useEffect, useState } from "react";
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
  { name: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
  { name: "Appointments", path: "/dashboard/appointments", icon: Calendar },
  { name: "Patients & EHR", path: "/dashboard/patients", icon: Users },
  { name: "Caregivers & Nurses", path: "/dashboard/caregivers", icon: HeartHandshake },
  { name: "Services Catalog", path: "/dashboard/services", icon: Layers },
  { name: "Care Plans", path: "/dashboard/care-plans", icon: Stethoscope },
  { name: "Billing & GST Invoices", path: "/dashboard/billing", icon: IndianRupee },
  { name: "Clinical Documents", path: "/dashboard/documents", icon: FileText },
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
    navigate("/");
  };

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col justify-between shrink-0">
        <div>
          <div className="h-16 flex items-center justify-between px-6 border-b border-slate-100">
            <Link to="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
              <div className="w-9 h-9 rounded-xl bg-orange-600 flex items-center justify-center text-white font-bold shadow-md shadow-orange-500/20">
                <Activity size={20} />
              </div>
              <div>
                <span className="font-bold text-slate-800 text-base leading-none block">CareFleet India</span>
                <span className="text-[10px] text-orange-600 font-semibold tracking-wider uppercase">HealthCare OS (INR)</span>
              </div>
            </Link>
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
          <Link
            to="/"
            className="w-full mb-3 py-2 px-3 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold flex items-center justify-center gap-2 transition-all cursor-pointer"
          >
            &larr; Switch / Landing Portal
          </Link>
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
            <Link
              to="/"
              className="px-3 py-1.5 rounded-xl bg-orange-50 hover:bg-orange-100 text-orange-700 font-semibold border border-orange-200 transition-all flex items-center gap-1.5"
            >
              <Calendar size={13} /> Book Visit / Portal Gateway
            </Link>
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
