import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Appointments from "./pages/Appointments";
import Patients from "./pages/Patients";
import Caregivers from "./pages/Caregivers";
import Services from "./pages/Services";
import CarePlans from "./pages/CarePlans";
import Billing from "./pages/Billing";
import Documents from "./pages/Documents";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/portal" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<MainLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="appointments" element={<Appointments />} />
          <Route path="patients" element={<Patients />} />
          <Route path="caregivers" element={<Caregivers />} />
          <Route path="services" element={<Services />} />
          <Route path="care-plans" element={<CarePlans />} />
          <Route path="billing" element={<Billing />} />
          <Route path="documents" element={<Documents />} />
        </Route>
        {/* Direct routes backward compatibility */}
        <Route path="/appointments" element={<Navigate to="/dashboard/appointments" replace />} />
        <Route path="/patients" element={<Navigate to="/dashboard/patients" replace />} />
        <Route path="/caregivers" element={<Navigate to="/dashboard/caregivers" replace />} />
        <Route path="/services" element={<Navigate to="/dashboard/services" replace />} />
        <Route path="/care-plans" element={<Navigate to="/dashboard/care-plans" replace />} />
        <Route path="/billing" element={<Navigate to="/dashboard/billing" replace />} />
        <Route path="/documents" element={<Navigate to="/dashboard/documents" replace />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

