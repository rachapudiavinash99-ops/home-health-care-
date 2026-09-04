import React, { useEffect, useState } from "react";
import api from "../api/axios";
import { FileText, Download, FileCheck, Plus, Upload, User, ShieldCheck } from "lucide-react";

export default function Documents() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [uploading, setUploading] = useState(false);

  const [uploadData, setUploadData] = useState({
    patient_id: "",
    description: "",
    file: null as File | null
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [docRes, patRes] = await Promise.all([
        api.get("/documents/").catch(async () => {
          // If role is PATIENT, try /documents/patient/{me}
          return { data: [] };
        }),
        api.get("/patients/").catch(() => ({ data: [] }))
      ]);
      setDocuments(docRes.data || []);
      setPatients(patRes.data || []);
    } catch (err) {
      console.error("Error fetching documents:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (doc: any) => {
    try {
      const res = await api.get("/documents/download/" + doc.id, {
        responseType: "blob"
      });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", doc.filename || "clinical_document.pdf");
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err: any) {
      alert(err?.response?.data?.detail || "Download failed. File may be generating.");
    }
  };

  const handleUploadSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadData.file) {
      alert("Please select a file to upload");
      return;
    }
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append("patient_id", uploadData.patient_id || (patients[0]?.id?.toString() ?? "1"));
      formData.append("description", uploadData.description || "Clinical Report");
      formData.append("file", uploadData.file);

      await api.post("/documents/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });
      setShowModal(false);
      setUploadData({ patient_id: "", description: "", file: null });
      fetchData();
      alert("Document uploaded successfully!");
    } catch (err: any) {
      alert(err?.response?.data?.detail || "Failed to upload document");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Clinical Documents & Medical Records</h1>
          <p className="text-xs text-slate-500 mt-1">Diagnostic lab reports, discharge summaries, prescriptions, and clinical consent paperwork.</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2.5 bg-orange-600 hover:bg-orange-700 text-white font-medium rounded-xl text-xs flex items-center gap-2 shadow-sm transition-all cursor-pointer"
        >
          <Upload size={16} /> Upload Clinical Record
        </button>
      </div>

      {loading ? (
        <div className="p-8 text-center text-slate-400 text-sm">Loading clinical documents...</div>
      ) : documents.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-100">
          <FileText size={36} className="mx-auto text-slate-300 mb-2" />
          <p className="text-sm text-slate-500 font-medium">No clinical documents recorded yet.</p>
          <button
            onClick={() => setShowModal(true)}
            className="mt-3 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-xl"
          >
            Upload First Document
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {documents.map((doc) => (
            <div key={doc.id} className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 flex flex-col justify-between hover:shadow-md transition-shadow">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className="p-3 rounded-xl bg-orange-50 text-orange-700">
                    <FileCheck size={24} />
                  </div>
                  <span className="text-xs font-mono px-2.5 py-1 rounded-full bg-slate-100 text-slate-600">
                    Patient #{doc.patient_id}
                  </span>
                </div>

                <h3 className="text-base font-bold text-slate-800 truncate" title={doc.filename}>
                  {doc.filename || "Medical Document"}
                </h3>
                <p className="text-xs text-slate-500 mt-1.5 line-clamp-2">
                  {doc.description || "Clinical diagnosis paperwork"}
                </p>

                <div className="mt-4 p-2.5 rounded-xl bg-slate-50 border border-slate-100 text-[11px] text-slate-500 flex items-center justify-between font-mono">
                  <span>Type: {doc.file_type || "PDF"}</span>
                  <span>{doc.file_size ? Math.round(doc.file_size / 1024) + " KB" : "Verified"}</span>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
                <span className="text-xs text-slate-400">
                  {doc.uploaded_at ? new Date(doc.uploaded_at).toLocaleDateString() : "Recent"}
                </span>
                <button
                  onClick={() => handleDownload(doc)}
                  className="px-3.5 py-1.5 bg-orange-50 hover:bg-orange-600 hover:text-white text-orange-700 font-semibold rounded-lg text-xs flex items-center gap-1.5 transition-colors cursor-pointer"
                >
                  <Download size={14} /> Download
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Upload Document Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-50 backdrop-blur-xs">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full shadow-2xl border border-slate-100">
            <h3 className="text-lg font-bold text-slate-800 mb-1">Upload Clinical Document</h3>
            <p className="text-xs text-slate-500 mb-4">Attach lab reports, discharge summaries, or prescriptions.</p>

            <form onSubmit={handleUploadSubmit} className="space-y-3.5 text-sm">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Patient</label>
                <select
                  value={uploadData.patient_id}
                  onChange={(e) => setUploadData({ ...uploadData, patient_id: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                >
                  {patients.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.full_name} (ID: #{p.id})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Description / Category</label>
                <input
                  type="text"
                  required
                  value={uploadData.description}
                  onChange={(e) => setUploadData({ ...uploadData, description: e.target.value })}
                  placeholder="e.g. Complete Blood Count & HbA1c Lab Report"
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Document File (PDF / DOC / JPG)</label>
                <input
                  type="file"
                  required
                  accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
                  onChange={(e) => setUploadData({ ...uploadData, file: e.target.files ? e.target.files[0] : null })}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs file:mr-2 file:py-1 file:px-2 file:rounded-md file:border-0 file:text-xs file:bg-orange-50 file:text-orange-700 hover:file:bg-orange-100"
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
                  disabled={uploading}
                  className="px-4 py-2 rounded-lg text-xs font-semibold bg-orange-600 hover:bg-orange-700 text-white shadow-sm cursor-pointer disabled:opacity-50 flex items-center gap-1.5"
                >
                  <Upload size={14} /> {uploading ? "Uploading..." : "Upload Document"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
