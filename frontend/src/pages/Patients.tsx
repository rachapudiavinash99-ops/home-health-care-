import React, { useEffect, useState } from "react";
import api from "../api/axios";
import { Users, Heart, Pill, Stethoscope, ChevronRight, X } from "lucide-react";

export default function Patients() {
  const [patients, setPatients] = useState<any[]>([]);
  const [selectedPatient, setSelectedPatient] = useState<any | null>(null);
  const [vitals, setVitals] = useState<any[]>([]);
  const [medications, setMedications] = useState<any[]>([]);
  const [carePlans, setCarePlans] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [drawerLoading, setDrawerLoading] = useState(false);

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    setLoading(true);
    try {
      const res = await api.get("/patients/").catch(async () => {
        const me = await api.get("/patients/me").catch(() => null);
        return { data: me?.data ? [me.data] : [] };
      });
      setPatients(res.data || []);
    } catch (err) {
      console.error("Error fetching patients:", err);
    } finally {
      setLoading(false);
    }
  };

  const openPatientEHR = async (p: any) => {
    setSelectedPatient(p);
    setDrawerLoading(true);
    try {
      const [vRes, mRes, cpRes] = await Promise.all([
        api.get("/vitals/patient/" + p.id).catch(() => ({ data: [] })),
        api.get("/medications/patient/" + p.id).catch(() => ({ data: [] })),
        api.get("/care-plans/patient/" + p.id).catch(() => ({ data: [] }))
      ]);
      setVitals(vRes.data || []);
      setMedications(mRes.data || []);
      setCarePlans(cpRes.data || []);
    } catch (err) {
      console.error("Error fetching EHR details:", err);
    } finally {
      setDrawerLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <h1 className="text-2xl font-bold text-slate-800">Patient Directory & Clinical EHR</h1>
        <p className="text-xs text-slate-500 mt-1">Comprehensive patient records, real-time vitals, medication administration, and care pathways.</p>
      </div>

      {loading ? (
        <div className="p-8 text-center text-slate-400 text-sm">Loading patient records...</div>
      ) : patients.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-100">
          <Users size={36} className="mx-auto text-slate-300 mb-2" />
          <p className="text-sm text-slate-500 font-medium">No patient records found.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {patients.map((p) => (
            <div key={p.id} className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 hover:shadow-md transition-shadow flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-xs font-mono font-semibold px-2.5 py-1 rounded-full bg-blue-50 text-blue-700">
                    Patient #{p.id}
                  </span>
                  <span className="text-xs text-slate-400 font-medium">DOB: {p.date_of_birth}</span>
                </div>

                <h3 className="text-lg font-bold text-slate-800">{p.full_name}</h3>
                <p className="text-xs text-slate-500 mt-1">{p.address}</p>

                <div className="mt-4 p-3 rounded-xl bg-slate-50 border border-slate-100 text-xs">
                  <span className="font-semibold text-slate-700 block mb-1">Emergency Contact:</span>
                  <div className="text-slate-600">{p.emergency_contact_name} ({p.emergency_contact_phone})</div>
                </div>
              </div>

              <button
                onClick={() => openPatientEHR(p)}
                className="mt-6 w-full py-2.5 bg-blue-50 hover:bg-blue-600 hover:text-white text-blue-700 font-semibold rounded-xl text-xs flex items-center justify-center gap-1.5 transition-all cursor-pointer"
              >
                Open Full EHR Chart <ChevronRight size={14} />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* EHR Slide-out Drawer */}
      {selectedPatient && (
        <div className="fixed inset-0 bg-black/40 flex justify-end z-50 backdrop-blur-xs">
          <div className="bg-white w-full max-w-xl h-full shadow-2xl p-6 overflow-y-auto flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between pb-4 border-b border-slate-100">
                <div>
                  <h2 className="text-lg font-bold text-slate-800">{selectedPatient.full_name}</h2>
                  <p className="text-xs text-slate-400 font-mono">EHR Chart Record #{selectedPatient.id}</p>
                </div>
                <button
                  onClick={() => setSelectedPatient(null)}
                  className="p-2 rounded-xl text-slate-400 hover:bg-slate-100 cursor-pointer"
                >
                  <X size={20} />
                </button>
              </div>

              {drawerLoading ? (
                <div className="py-12 text-center text-slate-400 text-xs">Loading clinical records...</div>
              ) : (
                <div className="space-y-6 mt-6">
                  {/* Vitals */}
                  <div>
                    <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-3 flex items-center gap-1.5 text-rose-600">
                      <Heart size={16} /> Latest Vital Signs
                    </h4>
                    {vitals.length === 0 ? (
                      <div className="p-4 rounded-xl bg-slate-50 text-slate-400 text-xs">No vitals logged.</div>
                    ) : (
                      <div className="space-y-2">
                        {vitals.map((v) => (
                          <div key={v.id} className="p-3 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between text-xs">
                            <div>
                              <div className="font-bold text-slate-800">
                                BP: {v.blood_pressure_systolic}/{v.blood_pressure_diastolic} mmHg | HR: {v.heart_rate} bpm
                              </div>
                              <div className="text-[10px] text-slate-400 mt-0.5">SpO2: {v.oxygen_saturation}% | Temp: {v.temperature}°F</div>
                            </div>
                            <span className="text-[10px] font-mono text-slate-400">{new Date(v.recorded_at).toLocaleDateString()}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Active Medications */}
                  <div>
                    <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-3 flex items-center gap-1.5 text-blue-600">
                      <Pill size={16} /> Active Medications
                    </h4>
                    {medications.length === 0 ? (
                      <div className="p-4 rounded-xl bg-slate-50 text-slate-400 text-xs">No active medications prescribed.</div>
                    ) : (
                      <div className="space-y-2">
                        {medications.map((m) => (
                          <div key={m.id} className="p-3 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between text-xs">
                            <div>
                              <span className="font-bold text-slate-800">{m.name}</span>
                              <span className="text-slate-500 ml-1.5">({m.dosage})</span>
                              <div className="text-[10px] text-slate-400 mt-0.5">{m.instructions} &bull; {m.frequency}</div>
                            </div>
                            <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700">
                              {m.status}
                            </span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Care Plans */}
                  <div>
                    <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-3 flex items-center gap-1.5 text-emerald-600">
                      <Stethoscope size={16} /> Physician Care Plans
                    </h4>
                    {carePlans.length === 0 ? (
                      <div className="p-4 rounded-xl bg-slate-50 text-slate-400 text-xs">No care plans on file.</div>
                    ) : (
                      <div className="space-y-2">
                        {carePlans.map((cp) => (
                          <div key={cp.id} className="p-3 rounded-xl bg-slate-50 border border-slate-100 text-xs">
                            <div className="flex items-center justify-between font-bold text-slate-800 mb-1">
                              <span>{cp.diagnosis}</span>
                              <span className="text-[10px] font-semibold text-emerald-600">{cp.status}</span>
                            </div>
                            <p className="text-slate-600 text-[11px] mb-1"><strong>Goals:</strong> {cp.goals}</p>
                            <p className="text-slate-500 text-[10px]"><strong>Regimen:</strong> {cp.instructions}</p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>

            <div className="pt-4 border-t border-slate-100">
              <button
                onClick={() => setSelectedPatient(null)}
                className="w-full py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold rounded-xl text-xs transition-colors cursor-pointer"
              >
                Close EHR Drawer
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
