import React, { useEffect, useState } from "react";
import api from "../api/axios";
import { Stethoscope, CheckCircle2, Plus } from "lucide-react";

export default function CarePlans() {
  const [carePlans, setCarePlans] = useState<any[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [newPlan, setNewPlan] = useState({
    patient_id: "",
    diagnosis: "",
    goals: "",
    instructions: "",
    required_services: "Nursing & Health Monitoring",
    frequency: "Weekly",
    start_date: "2026-03-01"
  });

  useEffect(() => {
    fetchCarePlans();
  }, []);

  const fetchCarePlans = async () => {
    setLoading(true);
    try {
      const [cpRes, pRes] = await Promise.all([
        api.get("/care-plans/").catch(() => ({ data: [] })),
        api.get("/patients/").catch(() => ({ data: [] }))
      ]);
      setCarePlans(cpRes.data || []);
      setPatients(pRes.data || []);
    } catch (err) {
      console.error("Error fetching care plans:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCarePlan = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post("/care-plans/", {
        patient_id: Number(newPlan.patient_id || (patients[0]?.id ?? 1)),
        diagnosis: newPlan.diagnosis,
        goals: newPlan.goals,
        instructions: newPlan.instructions,
        required_services: newPlan.required_services,
        frequency: newPlan.frequency,
        start_date: newPlan.start_date
      });
      setShowModal(false);
      fetchCarePlans();
    } catch (err: any) {
      alert(err?.response?.data?.detail || "Failed to create care plan");
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Physician Care Plans</h1>
          <p className="text-xs text-slate-500 mt-1">Clinical diagnosis, therapeutic goals, and prescribed treatment pathways.</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl text-xs flex items-center gap-2 shadow-sm transition-all cursor-pointer"
        >
          <Plus size={16} /> Create Care Plan
        </button>
      </div>

      {loading ? (
        <div className="p-8 text-center text-slate-400 text-sm">Loading care plans...</div>
      ) : carePlans.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-100">
          <Stethoscope size={36} className="mx-auto text-slate-300 mb-2" />
          <p className="text-sm text-slate-500 font-medium">No care plans recorded.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {carePlans.map((cp) => (
            <div key={cp.id} className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 flex flex-col justify-between hover:shadow-md transition-shadow">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1">
                    <CheckCircle2 size={12} /> {cp.status}
                  </span>
                  <span className="text-xs font-mono text-slate-400">Patient ID: #{cp.patient_id}</span>
                </div>

                <h3 className="text-lg font-bold text-slate-800">{cp.diagnosis}</h3>

                <div className="mt-4 space-y-2.5 text-xs text-slate-600">
                  <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                    <span className="font-bold text-slate-700 block mb-1">Therapeutic Goals:</span>
                    <span>{cp.goals}</span>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                    <span className="font-bold text-slate-700 block mb-1">Instructions:</span>
                    <span>{cp.instructions}</span>
                  </div>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                <span>Frequency: <strong>{cp.frequency}</strong></span>
                <span>Start: {cp.start_date}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {showModal && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-50 backdrop-blur-xs">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full shadow-2xl border border-slate-100">
            <h3 className="text-lg font-bold text-slate-800 mb-1">Create Patient Care Plan</h3>
            <p className="text-xs text-slate-500 mb-4">Prescribe medical regimen and treatment goals.</p>

            <form onSubmit={handleCreateCarePlan} className="space-y-3 text-sm">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Patient</label>
                <select
                  value={newPlan.patient_id}
                  onChange={(e) => setNewPlan({ ...newPlan, patient_id: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                >
                  {patients.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.full_name} (ID: {p.id})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Primary Diagnosis</label>
                <input
                  type="text"
                  required
                  value={newPlan.diagnosis}
                  onChange={(e) => setNewPlan({ ...newPlan, diagnosis: e.target.value })}
                  placeholder="e.g. Type 2 Diabetes Management"
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Goals</label>
                <textarea
                  rows={2}
                  required
                  value={newPlan.goals}
                  onChange={(e) => setNewPlan({ ...newPlan, goals: e.target.value })}
                  placeholder="Expected health milestones..."
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Instructions & Regimen</label>
                <textarea
                  rows={2}
                  required
                  value={newPlan.instructions}
                  onChange={(e) => setNewPlan({ ...newPlan, instructions: e.target.value })}
                  placeholder="Medication timing, therapy guidelines..."
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                />
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Frequency</label>
                  <input
                    type="text"
                    value={newPlan.frequency}
                    onChange={(e) => setNewPlan({ ...newPlan, frequency: e.target.value })}
                    className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Start Date</label>
                  <input
                    type="date"
                    required
                    value={newPlan.start_date}
                    onChange={(e) => setNewPlan({ ...newPlan, start_date: e.target.value })}
                    className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                  />
                </div>
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
                  className="px-4 py-2 rounded-lg text-xs font-semibold bg-blue-600 hover:bg-blue-700 text-white shadow-sm cursor-pointer"
                >
                  Save Care Plan
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
