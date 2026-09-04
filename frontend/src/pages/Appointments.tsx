import React, { useEffect, useState } from "react";
import api from "../api/axios";
import { Calendar, Clock, User, Plus, HeartHandshake, CheckCircle2, ShieldCheck, AlertCircle } from "lucide-react";

export default function Appointments() {
  const [appointments, setAppointments] = useState<any[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [caregivers, setCaregivers] = useState<any[]>([]);
  const [services, setServices] = useState<any[]>([]);
  const [filter, setFilter] = useState("ALL");
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [currentUser, setCurrentUser] = useState<any>(null);

  const [newAppt, setNewAppt] = useState({
    patient_id: "",
    caregiver_id: "",
    service_id: "",
    scheduled_start: "",
    scheduled_end: "",
    notes: ""
  });

  useEffect(() => {
    const userStr = localStorage.getItem("user");
    if (userStr) {
      setCurrentUser(JSON.parse(userStr));
    }
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
      
      // Default service selection
      if (srvRes.data && srvRes.data.length > 0 && !newAppt.service_id) {
        setNewAppt(prev => ({ ...prev, service_id: srvRes.data[0].id.toString() }));
      }
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
      const selectedService = services.find(s => s.id.toString() === newAppt.service_id) || services[0];
      const payload = {
        patient_id: currentUser?.role === "PATIENT" ? undefined : Number(newAppt.patient_id || (patients[0]?.id ?? 1)),
        caregiver_id: Number(newAppt.caregiver_id || (caregivers[0]?.id ?? 1)),
        service_id: Number(newAppt.service_id || (selectedService?.id ?? 1)),
        scheduled_start: newAppt.scheduled_start || new Date().toISOString(),
        scheduled_end: newAppt.scheduled_end || new Date(Date.now() + 3600000).toISOString(),
        notes: newAppt.notes || "Home healthcare visit booked"
      };
      await api.post("/appointments/", payload);
      setShowModal(false);
      setNewAppt({
        patient_id: "",
        caregiver_id: "",
        service_id: services[0]?.id?.toString() || "",
        scheduled_start: "",
        scheduled_end: "",
        notes: ""
      });
      loadData();
      alert("Appointment successfully booked!");
    } catch (err: any) {
      alert(err?.response?.data?.detail || "Failed to create appointment");
    }
  };

  const isPatient = currentUser?.role === "PATIENT";

  const filtered = appointments.filter(a => {
    if (filter === "ALL") return true;
    return a.status === filter;
  });

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold text-slate-800">
              {isPatient ? "My Home Care Appointments" : "Clinical Visits & Appointments"}
            </h1>
            {isPatient && (
              <span className="px-2.5 py-0.5 rounded-full bg-orange-100 text-orange-700 text-xs font-bold">
                Patient Portal
              </span>
            )}
          </div>
          <p className="text-xs text-slate-500 mt-1">
            {isPatient 
              ? "Book a verified nurse or physiotherapist to visit your home in India." 
              : "Nurse dispatch schedules, visit verification, and care tracking in India."}
          </p>
        </div>

        {isPatient && (
          <button
            onClick={() => setShowModal(true)}
            className="px-4 py-2.5 bg-orange-600 hover:bg-orange-700 text-white font-semibold rounded-xl text-xs flex items-center gap-2 shadow-sm transition-all cursor-pointer"
          >
            <Plus size={16} /> Book Home Visit Now (₹)
          </button>
        )}
      </div>

      {/* Patient info box */}
      {isPatient && (
        <div className="p-4 rounded-2xl bg-orange-50/70 border border-orange-200 text-xs text-orange-800 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldCheck size={18} className="text-orange-600" />
            <span>Booking for <strong>{currentUser?.full_name || "Patient"}</strong> (Verified Patient Account). Certified caregiver will visit at your home address.</span>
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="px-3 py-1.5 bg-orange-600 hover:bg-orange-700 text-white font-bold rounded-lg text-xs transition-colors shrink-0"
          >
            + New Booking
          </button>
        </div>
      )}

      {/* Status Filter Tabs */}
      <div className="flex gap-2 border-b border-slate-200 pb-2">
        {["ALL", "CONFIRMED", "IN_PROGRESS", "COMPLETED", "CANCELLED"].map((s) => (
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
          <p className="text-sm text-slate-500 font-medium">No appointments found.</p>
          {isPatient && (
            <button
              onClick={() => setShowModal(true)}
              className="mt-3 px-4 py-2 bg-orange-600 text-white rounded-xl text-xs font-semibold hover:bg-orange-700"
            >
              Book Your First Home Visit
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((appt) => (
            <div key={appt.id} className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5 flex flex-col justify-between hover:shadow-md transition-shadow">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className={"px-2.5 py-1 text-xs font-semibold rounded-full " + (
                    appt.status === "COMPLETED" ? "bg-emerald-50 text-emerald-700 border border-emerald-200" :
                    appt.status === "CONFIRMED" ? "bg-blue-50 text-blue-700 border border-blue-200" :
                    appt.status === "IN_PROGRESS" ? "bg-amber-50 text-amber-700 border border-amber-200" :
                    "bg-slate-100 text-slate-600"
                  )}>
                    {appt.status}
                  </span>
                  <span className="text-xs font-mono text-slate-400">Booking #{appt.id}</span>
                </div>

                <div className="space-y-2 text-xs text-slate-600">
                  <div className="flex items-center gap-2">
                    <User size={14} className="text-orange-600" />
                    <span className="font-medium text-slate-800">
                      {isPatient ? "Patient: You (Patient #" + appt.patient_id + ")" : "Patient ID: #" + appt.patient_id}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <HeartHandshake size={14} className="text-emerald-600" />
                    <span>Assigned Caregiver / Nurse: #{appt.caregiver_id}</span>
                  </div>
                  <div className="flex items-center gap-2 text-slate-500">
                    <Clock size={14} />
                    <span>{new Date(appt.scheduled_date || appt.scheduled_start).toLocaleString()}</span>
                  </div>
                  {appt.notes && (
                    <div className="mt-2 p-2 rounded-lg bg-slate-50 border border-slate-100 text-slate-600 italic">
                      "{appt.notes}"
                    </div>
                  )}
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-end gap-2 text-xs">
                {appt.status === "CONFIRMED" && (
                  <>
                    {!isPatient && (
                      <button
                        onClick={() => handleUpdateStatus(appt.id, "IN_PROGRESS")}
                        className="px-2.5 py-1 bg-amber-50 text-amber-700 font-semibold rounded-lg hover:bg-amber-100 cursor-pointer"
                      >
                        Start Visit
                      </button>
                    )}
                    <button
                      onClick={() => handleUpdateStatus(appt.id, "CANCELLED")}
                      className="px-2.5 py-1 bg-rose-50 text-rose-700 font-semibold rounded-lg hover:bg-rose-100 cursor-pointer"
                    >
                      Cancel Visit
                    </button>
                  </>
                )}
                {appt.status === "IN_PROGRESS" && !isPatient && (
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

      {/* Booking Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-50 backdrop-blur-xs">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full shadow-2xl border border-slate-100">
            <div className="flex items-center justify-between mb-1">
              <h3 className="text-lg font-bold text-slate-800">
                {isPatient ? "Book Home Healthcare Visit" : "Schedule New Appointment"}
              </h3>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-orange-100 text-orange-700">INR (₹)</span>
            </div>
            <p className="text-xs text-slate-500 mb-4">
              {isPatient 
                ? "Select clinical service and date. A certified nurse/physio will visit your location."
                : "Assign certified caregiver and service to a patient."}
            </p>

            <form onSubmit={handleCreateAppointment} className="space-y-3.5 text-sm">
              {/* If Admin/Doctor, show patient select. If Patient, show locked badge */}
              {isPatient ? (
                <div className="p-3 rounded-xl bg-orange-50/70 border border-orange-200 text-xs">
                  <span className="text-slate-500 block text-[10px] uppercase font-bold">Booking For Patient:</span>
                  <span className="font-bold text-slate-800">{currentUser?.full_name || "Aarav Sharma"}</span>
                  <span className="text-slate-400 ml-1">({currentUser?.email})</span>
                </div>
              ) : (
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
              )}

              {/* Service Selection */}
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Clinical Service (Rupees ₹)</label>
                <select
                  value={newAppt.service_id}
                  onChange={(e) => setNewAppt({ ...newAppt, service_id: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs font-medium"
                >
                  {services.map((s) => (
                    <option key={s.id} value={s.id}>
                      {s.name} — ₹{s.base_price} ({s.duration_minutes} mins)
                    </option>
                  ))}
                </select>
              </div>

              {/* Caregiver Selection */}
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Preferred Staff / Nurse</label>
                <select
                  value={newAppt.caregiver_id}
                  onChange={(e) => setNewAppt({ ...newAppt, caregiver_id: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                >
                  <option value="">-- Auto-Dispatch Available Staff --</option>
                  {caregivers.map((cg) => (
                    <option key={cg.id} value={cg.id}>
                      {cg.full_name} ({cg.specialization})
                    </option>
                  ))}
                </select>
              </div>

              {/* Date & Time */}
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Visit Date & Time</label>
                  <input
                    type="datetime-local"
                    required
                    value={newAppt.scheduled_start}
                    onChange={(e) => setNewAppt({ ...newAppt, scheduled_start: e.target.value })}
                    className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Estimated End Time</label>
                  <input
                    type="datetime-local"
                    required
                    value={newAppt.scheduled_end}
                    onChange={(e) => setNewAppt({ ...newAppt, scheduled_end: e.target.value })}
                    className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                  />
                </div>
              </div>

              {/* Notes */}
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">
                  {isPatient ? "Special Medical Instructions / Address Landmark" : "Clinical Notes"}
                </label>
                <textarea
                  rows={2}
                  value={newAppt.notes}
                  onChange={(e) => setNewAppt({ ...newAppt, notes: e.target.value })}
                  placeholder="e.g. Fasting blood sugar test, please arrive before 9 AM; gate code 4022..."
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
                  className="px-4 py-2 rounded-lg text-xs font-semibold bg-orange-600 hover:bg-orange-700 text-white shadow-sm cursor-pointer flex items-center gap-1.5"
                >
                  <CheckCircle2 size={14} /> {isPatient ? "Confirm & Book Visit (₹)" : "Confirm Schedule"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
