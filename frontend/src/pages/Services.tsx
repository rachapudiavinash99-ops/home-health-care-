import React, { useEffect, useState } from "react";
import api from "../api/axios";
import { Layers, Clock, Plus, IndianRupee, CalendarCheck, CheckCircle2 } from "lucide-react";

export default function Services() {
  const [services, setServices] = useState<any[]>([]);
  const [caregivers, setCaregivers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showBookModal, setShowBookModal] = useState(false);
  const [selectedService, setSelectedService] = useState<any | null>(null);
  const [currentUser, setCurrentUser] = useState<any>(null);

  const [newService, setNewService] = useState({
    name: "",
    description: "",
    category: "NURSING",
    base_price: "",
    duration_minutes: "60"
  });

  const [bookingData, setBookingData] = useState({
    scheduled_start: "",
    caregiver_id: "",
    notes: ""
  });

  useEffect(() => {
    const userStr = localStorage.getItem("user");
    if (userStr) {
      setCurrentUser(JSON.parse(userStr));
    }
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [srvRes, cgRes] = await Promise.all([
        api.get("/services/"),
        api.get("/caregivers/").catch(() => ({ data: [] }))
      ]);
      setServices(srvRes.data || []);
      setCaregivers(cgRes.data || []);
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
      setShowAddModal(false);
      setNewService({ name: "", description: "", category: "NURSING", base_price: "", duration_minutes: "60" });
      fetchData();
      alert("Clinical service created successfully!");
    } catch (err: any) {
      alert(err?.response?.data?.detail || "Failed to create service");
    }
  };

  const openBookModal = (s: any) => {
    setSelectedService(s);
    setShowBookModal(true);
  };

  const handleBookServiceSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        service_id: selectedService.id,
        caregiver_id: Number(bookingData.caregiver_id || (caregivers[0]?.id ?? 1)),
        scheduled_start: bookingData.scheduled_start || new Date().toISOString(),
        notes: bookingData.notes || ("Booked " + selectedService.name)
      };
      await api.post("/appointments/", payload);
      setShowBookModal(false);
      setBookingData({ scheduled_start: "", caregiver_id: "", notes: "" });
      alert("Booking confirmed for " + selectedService.name + " (₹" + selectedService.base_price + ")! Check Appointments page.");
    } catch (err: any) {
      alert(err?.response?.data?.detail || "Booking failed");
    }
  };

  const isPatient = currentUser?.role === "PATIENT";

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Clinical Home Services Catalog (INR ₹)</h1>
          <p className="text-xs text-slate-500 mt-1">Book certified home nursing, physiotherapy, and elderly companion care in India.</p>
        </div>
        {!isPatient && (
          <button
            onClick={() => setShowAddModal(true)}
            className="px-4 py-2.5 bg-orange-600 hover:bg-orange-700 text-white font-medium rounded-xl text-xs flex items-center gap-2 shadow-sm transition-all cursor-pointer"
          >
            <Plus size={16} /> Add Clinical Service
          </button>
        )}
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
                <p className="text-xs text-slate-500 mt-2 line-clamp-3">{s.description}</p>
              </div>

              <div className="mt-6 pt-4 border-t border-slate-100">
                <div className="flex items-center justify-between text-xs text-slate-400 mb-3">
                  <span className="flex items-center gap-1"><Clock size={14} /> {s.duration_minutes} Mins</span>
                  <span className="text-emerald-600 font-medium">&bull; Certified Staff</span>
                </div>

                <button
                  onClick={() => openBookModal(s)}
                  className="w-full py-2.5 bg-orange-50 hover:bg-orange-600 hover:text-white text-orange-700 font-bold rounded-xl text-xs flex items-center justify-center gap-2 transition-all cursor-pointer"
                >
                  <CalendarCheck size={14} /> Book This Service (₹{s.base_price})
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Book Service Modal */}
      {showBookModal && selectedService && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-50 backdrop-blur-xs">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full shadow-2xl border border-slate-100">
            <h3 className="text-lg font-bold text-slate-800 mb-1">Book: {selectedService.name}</h3>
            <p className="text-xs text-slate-500 mb-4">Fee: <strong>₹{selectedService.base_price}</strong> ({selectedService.duration_minutes} Mins)</p>

            <form onSubmit={handleBookServiceSubmit} className="space-y-3 text-sm">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Preferred Staff / Nurse</label>
                <select
                  value={bookingData.caregiver_id}
                  onChange={(e) => setBookingData({ ...bookingData, caregiver_id: e.target.value })}
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

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Visit Date & Time</label>
                <input
                  type="datetime-local"
                  required
                  value={bookingData.scheduled_start}
                  onChange={(e) => setBookingData({ ...bookingData, scheduled_start: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Special Notes / Address</label>
                <textarea
                  rows={2}
                  value={bookingData.notes}
                  onChange={(e) => setBookingData({ ...bookingData, notes: e.target.value })}
                  placeholder="Address landmark, patient condition notes..."
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t">
                <button
                  type="button"
                  onClick={() => setShowBookModal(false)}
                  className="px-4 py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-100 cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-lg text-xs font-semibold bg-orange-600 hover:bg-orange-700 text-white shadow-sm cursor-pointer flex items-center gap-1.5"
                >
                  <CheckCircle2 size={14} /> Confirm Booking (₹{selectedService.base_price})
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Service Modal */}
      {showAddModal && (
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
                  onClick={() => setShowAddModal(false)}
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
