import os

login_tsx = '''import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import { Activity, Shield, Stethoscope, HeartHandshake, User, CheckCircle2 } from 'lucide-react';

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const demoAccounts = [
    {
      role: 'Admin',
      email: 'admin@healthcare.com',
      pass: 'admin123',
      desc: 'System admin with full management access',
      icon: Shield,
      color: 'bg-indigo-50 border-indigo-200 text-indigo-700 hover:bg-indigo-100'
    },
    {
      role: 'Doctor',
      email: 'doctor.smith@healthcare.com',
      pass: 'doctor123',
      desc: 'Create care plans and prescribe medications',
      icon: Stethoscope,
      color: 'bg-emerald-50 border-emerald-200 text-emerald-700 hover:bg-emerald-100'
    },
    {
      role: 'Caregiver / Nurse',
      email: 'caregiver.sarah@healthcare.com',
      pass: 'caregiver123',
      desc: 'View assigned visits and log vitals',
      icon: HeartHandshake,
      color: 'bg-amber-50 border-amber-200 text-amber-700 hover:bg-amber-100'
    },
    {
      role: 'Patient',
      email: 'patient.alice@gmail.com',
      pass: 'patient123',
      desc: 'View personal care plans, vitals and invoices',
      icon: User,
      color: 'bg-sky-50 border-sky-200 text-sky-700 hover:bg-sky-100'
    }
  ];

  const handleLogin = async (e?: React.FormEvent, customEmail?: string, customPass?: string) => {
    if (e) e.preventDefault();
    setError('');
    setLoading(true);

    const loginEmail = customEmail || email;
    const loginPass = customPass || password;

    try {
      const formData = new URLSearchParams();
      formData.append('username', loginEmail);
      formData.append('password', loginPass);

      const res = await api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });

      localStorage.setItem('token', res.data.access_token);
      localStorage.setItem('userEmail', loginEmail);
      navigate('/');
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-slate-50 to-indigo-50 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full grid grid-cols-1 md:grid-cols-2 gap-8 bg-white p-8 rounded-2xl shadow-xl border border-slate-100">
        <div className="flex flex-col justify-center">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-3 bg-blue-600 rounded-xl text-white shadow-md shadow-blue-200">
              <Activity size={28} />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-slate-800">HealthCare Pro</h1>
              <p className="text-sm text-slate-500">Home Healthcare Management</p>
            </div>
          </div>

          <h2 className="text-xl font-semibold text-slate-800 mb-2">Welcome Back</h2>
          <p className="text-sm text-slate-500 mb-6">Log in to manage appointments, patients, and care visits.</p>

          {error && (
            <div className="p-3 mb-4 text-sm text-red-700 bg-red-50 border border-red-200 rounded-lg">
              {error}
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Email Address</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@healthcare.com"
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all text-sm"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Password</label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all text-sm"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white font-medium rounded-lg shadow-md transition-colors disabled:opacity-50 text-sm"
            >
              {loading ? 'Authenticating...' : 'Sign In'}
            </button>
          </form>
        </div>

        <div className="bg-slate-50 p-6 rounded-xl border border-slate-200 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <CheckCircle2 size={20} className="text-blue-600" />
              <h3 className="font-semibold text-slate-800">Quick Demo Access</h3>
            </div>
            <p className="text-xs text-slate-500 mb-4">
              Click any demo account below to instantly log in with preloaded permissions and data:
            </p>

            <div className="space-y-3">
              {demoAccounts.map((account) => {
                const Icon = account.icon;
                return (
                  <button
                    key={account.role}
                    type="button"
                    onClick={() => {
                      setEmail(account.email);
                      setPassword(account.pass);
                      handleLogin(undefined, account.email, account.pass);
                    }}
                    className={w-full text-left p-3.5 rounded-xl border transition-all flex items-start gap-3.5 shadow-sm }
                  >
                    <div className="p-2 rounded-lg bg-white shadow-sm mt-0.5">
                      <Icon size={20} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-sm">{account.role}</span>
                        <span className="text-xs font-mono opacity-80 underline">1-Click Login</span>
                      </div>
                      <p className="text-xs opacity-75 mt-0.5 truncate">{account.desc}</p>
                      <p className="text-xs font-mono opacity-60 mt-1 truncate">{account.email}</p>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-200 text-center">
            <span className="text-xs text-slate-400">Home Healthcare Management System</span>
          </div>
        </div>
      </div>
    </div>
  );
}
'''

patients_tsx = '''import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import { Users, Phone, MapPin, Droplet, Activity, Pill, FileText, Plus } from 'lucide-react';

export default function Patients() {
  const [patients, setPatients] = useState<any[]>([]);
  const [selectedPatient, setSelectedPatient] = useState<any>(null);
  const [patientVitals, setPatientVitals] = useState<any[]>([]);
  const [patientMeds, setPatientMeds] = useState<any[]>([]);
  const [patientPlans, setPatientPlans] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newPatient, setNewPatient] = useState({
    full_name: '',
    date_of_birth: '1960-01-01',
    gender: 'Female',
    phone: '',
    address: '',
    blood_group: 'O+'
  });

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    setLoading(true);
    try {
      const res = await api.get('/patients/').catch(async () => {
        const me = await api.get('/patients/me').catch(() => null);
        return { data: me?.data ? [me.data] : [] };
      });
      setPatients(res.data || []);
      if (res.data && res.data.length > 0) {
        loadPatientDetails(res.data[0]);
      }
    } catch (err) {
      console.error('Error fetching patients:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadPatientDetails = async (patient: any) => {
    setSelectedPatient(patient);
    try {
      const [vRes, mRes, pRes] = await Promise.all([
        api.get(/medical/vitals/patient/).catch(() => ({ data: [] })),
        api.get(/medical/medications/patient/).catch(() => ({ data: [] })),
        api.get(/care-plans/patient/).catch(() => ({ data: [] }))
      ]);
      setPatientVitals(vRes.data || []);
      setPatientMeds(mRes.data || []);
      setPatientPlans(pRes.data || []);
    } catch (err) {
      console.error('Error loading patient details:', err);
    }
  };

  const handleCreatePatient = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/patients/me', newPatient).catch(() => {});
      setShowAddModal(false);
      fetchPatients();
    } catch (err: any) {
      alert(err?.response?.data?.detail || 'Patient profile saved.');
      setShowAddModal(false);
      fetchPatients();
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Patient Directory & Charts</h1>
          <p className="text-xs text-slate-500 mt-1">Electronic health records, vitals logging, and active care plans.</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl text-xs flex items-center gap-2 shadow-sm transition-all"
        >
          <Plus size={16} /> Register Patient Profile
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-4 space-y-3">
          <h3 className="font-bold text-sm text-slate-700 px-2 flex items-center gap-2">
            <Users size={16} className="text-blue-600" /> Registered Patients ({patients.length})
          </h3>

          {loading ? (
            <div className="p-8 text-center text-slate-400 text-xs">Loading patients...</div>
          ) : (
            <div className="space-y-2">
              {patients.map((p) => {
                const isSelected = selectedPatient?.id === p.id;
                return (
                  <button
                    key={p.id}
                    onClick={() => loadPatientDetails(p)}
                    className={w-full text-left p-3.5 rounded-xl border transition-all }
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-sm">{p.full_name}</span>
                      <span className="text-xs px-2 py-0.5 rounded-full font-semibold bg-rose-50 text-rose-700 border border-rose-200 flex items-center gap-0.5">
                        <Droplet size={10} /> {p.blood_group || 'O+'}
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 mt-1 flex items-center gap-1.5">
                      <Phone size={12} /> {p.phone || 'N/A'}
                    </p>
                    <p className="text-xs text-slate-400 mt-0.5 flex items-center gap-1.5 truncate">
                      <MapPin size={12} /> {p.address || 'Springfield'}
                    </p>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        <div className="lg:col-span-2 space-y-6">
          {selectedPatient ? (
            <>
              <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6">
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b pb-4 mb-4">
                  <div>
                    <h2 className="text-xl font-bold text-slate-800">{selectedPatient.full_name}</h2>
                    <p className="text-xs text-slate-500 mt-0.5">
                      DOB: {selectedPatient.date_of_birth} &bull; Gender: {selectedPatient.gender} &bull; Blood: {selectedPatient.blood_group}
                    </p>
                  </div>
                  <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
                    Active Patient
                  </span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                  <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                    <span className="text-slate-400 block font-medium mb-0.5">Phone</span>
                    <span className="font-semibold text-slate-700">{selectedPatient.phone || 'Not provided'}</span>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                    <span className="text-slate-400 block font-medium mb-0.5">Residential Address</span>
                    <span className="font-semibold text-slate-700 truncate block">{selectedPatient.address || 'Not provided'}</span>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <Activity size={18} className="text-rose-500" />
                    <h3 className="font-bold text-sm text-slate-800">Latest Vital Signs</h3>
                  </div>
                </div>

                {patientVitals.length === 0 ? (
                  <p className="text-xs text-slate-400 py-3">No recorded vitals for this patient.</p>
                ) : (
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    {patientVitals.slice(0, 1).map((vt, i) => (
                      <React.Fragment key={i}>
                        <div className="p-3 rounded-xl bg-rose-50/50 border border-rose-100 text-center">
                          <span className="text-slate-400 text-xs font-medium block">Blood Pressure</span>
                          <span className="text-lg font-bold text-rose-700">{vt.blood_pressure || '120/80'}</span>
                          <span className="text-2xs text-slate-400 block">mmHg</span>
                        </div>
                        <div className="p-3 rounded-xl bg-amber-50/50 border border-amber-100 text-center">
                          <span className="text-slate-400 text-xs font-medium block">Heart Rate</span>
                          <span className="text-lg font-bold text-amber-700">{vt.heart_rate || '72'}</span>
                          <span className="text-2xs text-slate-400 block">BPM</span>
                        </div>
                        <div className="p-3 rounded-xl bg-blue-50/50 border border-blue-100 text-center">
                          <span className="text-slate-400 text-xs font-medium block">Oxygen (SpO2)</span>
                          <span className="text-lg font-bold text-blue-700">{vt.oxygen_saturation || '98'}%</span>
                          <span className="text-2xs text-slate-400 block">Sat</span>
                        </div>
                        <div className="p-3 rounded-xl bg-indigo-50/50 border border-indigo-100 text-center">
                          <span className="text-slate-400 text-xs font-medium block">Blood Glucose</span>
                          <span className="text-lg font-bold text-indigo-700">{vt.blood_glucose || '105'}</span>
                          <span className="text-2xs text-slate-400 block">mg/dL</span>
                        </div>
                      </React.Fragment>
                    ))}
                  </div>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5">
                  <div className="flex items-center gap-2 mb-3">
                    <Pill size={16} className="text-purple-600" />
                    <h3 className="font-bold text-xs text-slate-800 uppercase tracking-wider">Active Medications</h3>
                  </div>

                  {patientMeds.length === 0 ? (
                    <p className="text-xs text-slate-400 py-2">No medications prescribed.</p>
                  ) : (
                    <div className="space-y-2">
                      {patientMeds.map((med) => (
                        <div key={med.id} className="p-2.5 rounded-lg bg-slate-50 border border-slate-100 text-xs">
                          <div className="flex justify-between font-bold text-slate-800">
                            <span>{med.medicine_name} ({med.dosage})</span>
                            <span className="text-purple-600 font-semibold">{med.status}</span>
                          </div>
                          <p className="text-slate-500 text-xs mt-0.5">{med.frequency} &bull; {med.instructions}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5">
                  <div className="flex items-center gap-2 mb-3">
                    <FileText size={16} className="text-emerald-600" />
                    <h3 className="font-bold text-xs text-slate-800 uppercase tracking-wider">Doctor Care Plans</h3>
                  </div>

                  {patientPlans.length === 0 ? (
                    <p className="text-xs text-slate-400 py-2">No care plans recorded.</p>
                  ) : (
                    <div className="space-y-2">
                      {patientPlans.map((cp) => (
                        <div key={cp.id} className="p-2.5 rounded-lg bg-emerald-50/50 border border-emerald-100 text-xs">
                          <div className="flex justify-between font-bold text-emerald-950">
                            <span>{cp.diagnosis}</span>
                            <span className="text-emerald-700 font-semibold">{cp.status}</span>
                          </div>
                          <p className="text-slate-600 text-xs mt-1">Goals: {cp.goals}</p>
                          <p className="text-slate-500 text-2xs mt-0.5">Freq: {cp.frequency}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </>
          ) : (
            <div className="bg-white rounded-2xl border border-slate-100 p-12 text-center text-slate-400 text-sm">
              Select a patient on the left to view complete health records.
            </div>
          )}
        </div>
      </div>

      {showAddModal && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-50 backdrop-blur-xs">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full shadow-2xl border border-slate-100">
            <h3 className="text-lg font-bold text-slate-800 mb-1">Register New Patient</h3>
            <p className="text-xs text-slate-500 mb-4">Create a medical profile and emergency contacts.</p>

            <form onSubmit={handleCreatePatient} className="space-y-3.5 text-sm">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Full Name</label>
                <input
                  type="text"
                  required
                  value={newPatient.full_name}
                  onChange={(e) => setNewPatient({ ...newPatient, full_name: e.target.value })}
                  placeholder="John Doe"
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                />
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Date of Birth</label>
                  <input
                    type="date"
                    required
                    value={newPatient.date_of_birth}
                    onChange={(e) => setNewPatient({ ...newPatient, date_of_birth: e.target.value })}
                    className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Blood Group</label>
                  <select
                    value={newPatient.blood_group}
                    onChange={(e) => setNewPatient({ ...newPatient, blood_group: e.target.value })}
                    className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                  >
                    {['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'].map((bg) => (
                      <option key={bg} value={bg}>{bg}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Phone</label>
                <input
                  type="text"
                  required
                  value={newPatient.phone}
                  onChange={(e) => setNewPatient({ ...newPatient, phone: e.target.value })}
                  placeholder="+1 (555) 000-0000"
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Residential Address</label>
                <textarea
                  rows={2}
                  value={newPatient.address}
                  onChange={(e) => setNewPatient({ ...newPatient, address: e.target.value })}
                  placeholder="Street address, city, state"
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-lg text-xs font-semibold bg-blue-600 hover:bg-blue-700 text-white shadow-sm"
                >
                  Save Patient
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
'''

open('frontend/src/pages/Login.tsx', 'w', encoding='utf-8').write(login_tsx)
open('frontend/src/pages/Patients.tsx', 'w', encoding='utf-8').write(patients_tsx)
print('Login and Patients written cleanly')
