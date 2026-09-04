import React, { useEffect, useState } from "react";
import api from "../api/axios";
import { IndianRupee, CheckCircle2, Clock, ShieldCheck, QrCode } from "lucide-react";

export default function Billing() {
  const [invoices, setInvoices] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [payingId, setPayingId] = useState<number | null>(null);

  useEffect(() => {
    fetchInvoices();
  }, []);

  const fetchInvoices = async () => {
    setLoading(true);
    try {
      const res = await api.get("/billing/invoices").catch(async () => {
        return { data: [] };
      });
      setInvoices(res.data || []);
    } catch (err) {
      console.error("Error fetching invoices:", err);
    } finally {
      setLoading(false);
    }
  };

  const handlePayInvoice = async (invoice: any) => {
    setPayingId(invoice.id);
    try {
      await api.post("/billing/payments", {
        invoice_id: invoice.id,
        amount: invoice.total,
        payment_method: "UPI_GPAY_SANDBOX"
      });
      alert("Payment of ₹" + invoice.total?.toFixed(2) + " completed via UPI / RuPay!");
      fetchInvoices();
    } catch (err: any) {
      alert(err?.response?.data?.detail || "Payment failed.");
    } finally {
      setPayingId(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">GST Invoices & Billing (INR ₹)</h1>
          <p className="text-xs text-slate-500 mt-1">18% GST Compliant Healthcare Invoices, UPI, RuPay & NetBanking.</p>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-semibold">
          <ShieldCheck size={16} /> UPI & Razorpay Sandbox Active
        </div>
      </div>

      {loading ? (
        <div className="p-8 text-center text-slate-400 text-sm">Loading invoices...</div>
      ) : invoices.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-100">
          <IndianRupee size={36} className="mx-auto text-slate-300 mb-2" />
          <p className="text-sm text-slate-500 font-medium">No invoices found.</p>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-slate-100 text-slate-400 text-xs font-semibold uppercase bg-slate-50/50">
                  <th className="p-4">Invoice #</th>
                  <th className="p-4">Patient ID</th>
                  <th className="p-4">Base Fee (₹)</th>
                  <th className="p-4">GST (18%)</th>
                  <th className="p-4">Total Amount (₹)</th>
                  <th className="p-4">Payment Status</th>
                  <th className="p-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-xs">
                {invoices.map((inv) => (
                  <tr key={inv.id} className="hover:bg-slate-50/70 transition-colors">
                    <td className="p-4 font-mono font-bold text-slate-800">{inv.invoice_number}</td>
                    <td className="p-4 text-slate-600 font-mono">#{inv.patient_id}</td>
                    <td className="p-4 text-slate-700 font-medium">₹{inv.base_price?.toFixed(2)}</td>
                    <td className="p-4 text-slate-500">₹{inv.tax?.toFixed(2)}</td>
                    <td className="p-4 font-bold text-slate-900 text-sm">₹{inv.total?.toFixed(2)}</td>
                    <td className="p-4">
                      {inv.status === "PAID" ? (
                        <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200 flex items-center gap-1 w-fit">
                          <CheckCircle2 size={12} /> PAID
                        </span>
                      ) : (
                        <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-amber-100 text-amber-800 border border-amber-200 flex items-center gap-1 w-fit">
                          <Clock size={12} /> PENDING
                        </span>
                      )}
                    </td>
                    <td className="p-4 text-right">
                      {inv.status === "PENDING" ? (
                        <button
                          disabled={payingId === inv.id}
                          onClick={() => handlePayInvoice(inv)}
                          className="px-3 py-1.5 bg-orange-600 hover:bg-orange-700 text-white font-semibold rounded-lg shadow-sm transition-all flex items-center gap-1.5 ml-auto text-xs disabled:opacity-50 cursor-pointer"
                        >
                          <QrCode size={14} /> {payingId === inv.id ? "Processing..." : "Pay via UPI (₹)"}
                        </button>
                      ) : (
                        <span className="text-emerald-600 font-medium text-xs">Settled (UPI)</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
