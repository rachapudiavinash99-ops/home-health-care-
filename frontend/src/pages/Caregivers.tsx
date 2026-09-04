import React, { useEffect, useState } from "react";
import api from "../api/axios";
import { HeartHandshake, ShieldCheck, Award, Briefcase } from "lucide-react";

export default function Caregivers() {
  const [caregivers, setCaregivers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCaregivers();
  }, []);

  const fetchCaregivers = async () => {
    setLoading(true);
    try {
      const res = await api.get("/caregivers/").catch(async () => {
        const me = await api.get("/caregivers/me").catch(() => null);
        return { data: me?.data ? [me.data] : [] };
      });
      setCaregivers(res.data || []);
    } catch (err) {
      console.error("Error fetching caregivers:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <h1 className="text-2xl font-bold text-slate-800">Caregiver & Nursing Staff</h1>
        <p className="text-xs text-slate-500 mt-1">Verified nurses, therapists, and certified health aides.</p>
      </div>

      {loading ? (
        <div className="p-8 text-center text-slate-400 text-sm">Loading caregiver roster...</div>
      ) : caregivers.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-100">
          <HeartHandshake size={36} className="mx-auto text-slate-300 mb-2" />
          <p className="text-sm text-slate-500 font-medium">No caregivers found.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {caregivers.map((cg) => (
            <div key={cg.id} className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 hover:shadow-md transition-shadow flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className="p-3 rounded-xl bg-amber-50 text-amber-700">
                    <HeartHandshake size={24} />
                  </div>
                  {cg.is_verified && (
                    <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1">
                      <ShieldCheck size={14} /> Verified Staff
                    </span>
                  )}
                </div>

                <h3 className="text-lg font-bold text-slate-800">{cg.full_name}</h3>
                <p className="text-xs font-semibold text-blue-600 mt-0.5">{cg.qualification}</p>

                <div className="mt-4 space-y-2 text-xs text-slate-600">
                  <div className="flex items-center gap-2 p-2 rounded-lg bg-slate-50">
                    <Award size={14} className="text-amber-600" />
                    <span>Specialization: <strong>{cg.specialization}</strong></span>
                  </div>
                  <div className="flex items-center gap-2 p-2 rounded-lg bg-slate-50">
                    <Briefcase size={14} className="text-blue-600" />
                    <span>Experience: <strong>{cg.experience_years} Years</strong></span>
                  </div>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs">
                <span className="text-slate-400">Staff ID: #{cg.id}</span>
                <span className="font-medium text-emerald-600">&bull; Available for Dispatch</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
