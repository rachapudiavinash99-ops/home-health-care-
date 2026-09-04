import React, { useState } from "react";
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
