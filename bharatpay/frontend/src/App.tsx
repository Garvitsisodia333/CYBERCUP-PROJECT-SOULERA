import { useState, useEffect } from 'react';
import { AlertCircle, Wallet } from 'lucide-react';

export default function App() {
  const [backendStatus, setBackendStatus] = useState<'checking' | 'connected' | 'disconnected'>('checking');

  useEffect(() => {
    fetch('/health')
      .then(res => res.json())
      .then(data => {
        if (data.status === 'healthy') {
          setBackendStatus('connected');
        } else {
          setBackendStatus('disconnected');
        }
      })
      .catch(() => setBackendStatus('disconnected'));
  }, []);

  return (
    <div className="min-h-screen flex flex-col justify-between bg-slate-50 text-slate-800">
      {/* Top Navbar */}
      <header className="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between sticky top-0 z-10">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-sky-600 flex items-center justify-center text-white font-bold text-xl shadow-sm">
            BP
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xl font-bold tracking-tight text-slate-900">BharatPay</span>
              <span className="px-2 py-0.5 text-xs font-semibold bg-sky-100 text-sky-800 rounded-full">
                DEMO SYSTEM
              </span>
            </div>
            <p className="text-xs text-slate-500">Synthetic Neobank & UPI Banking Simulator</p>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-xs">
            <span className="text-slate-500">Target Backend:</span>
            {backendStatus === 'checking' && (
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-800">
                Checking...
              </span>
            )}
            {backendStatus === 'connected' && (
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-emerald-100 text-emerald-800">
                ● Live API Connected
              </span>
            )}
            {backendStatus === 'disconnected' && (
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-amber-100 text-amber-800">
                ○ Waiting for Backend (Port 8000)
              </span>
            )}
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 max-w-5xl w-full mx-auto p-6 md:p-8">
        <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm mb-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-3 bg-sky-50 text-sky-700 rounded-xl">
              <Wallet className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-slate-900">BharatPay Target Environment</h1>
              <p className="text-sm text-slate-500">Scaffold and API Contract Initialized — CC6-IC07 Target Testbed</p>
            </div>
          </div>

          <p className="text-sm text-slate-600 mb-6 leading-relaxed">
            This application is the deliberately-vulnerable testbed system for API Discovery, Security, and Abuse Prevention.
            All bank accounts, UPI VPAs, Aadhaar, PAN, and transactions are completely synthetic test data.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
            <div className="p-4 rounded-xl border border-slate-100 bg-slate-50">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1">Architecture</span>
              <span className="text-sm font-semibold text-slate-800">FastAPI + SQLite + React</span>
              <p className="text-xs text-slate-500 mt-1">Paise integer accounting, PyJWT</p>
            </div>
            <div className="p-4 rounded-xl border border-slate-100 bg-slate-50">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1">Logging</span>
              <span className="text-sm font-semibold text-slate-800">Structured JSONL + DB</span>
              <p className="text-xs text-slate-500 mt-1">Direct log ingestion pipeline</p>
            </div>
            <div className="p-4 rounded-xl border border-slate-100 bg-slate-50">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1">Inspection Proxy</span>
              <span className="text-sm font-semibold text-slate-800">Nginx Gateway (Port 80)</span>
              <p className="text-xs text-slate-500 mt-1">Gateway access logs captured</p>
            </div>
          </div>
        </div>
      </main>

      {/* Persistent Watermark Footer */}
      <footer className="border-t border-slate-200 bg-white py-4 px-6 text-center text-xs text-slate-500 flex flex-col md:flex-row items-center justify-between">
        <div className="flex items-center space-x-2">
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-50 text-amber-800 border border-amber-200">
            <AlertCircle className="w-3.5 h-3.5 mr-1" />
            SYNTHETIC TEST DATA — CC6-IC07
          </span>
          <span className="text-slate-400">|</span>
          <span>Fictional Neobank Target System</span>
        </div>
        <div className="mt-2 md:mt-0 font-mono text-slate-400 text-[11px]">
          Press <kbd className="px-1.5 py-0.5 bg-slate-100 border border-slate-300 rounded text-slate-600">Shift</kbd> + <kbd className="px-1.5 py-0.5 bg-slate-100 border border-slate-300 rounded text-slate-600">R</kbd> for Red Team Drawer (Checkpoint 7)
        </div>
      </footer>
    </div>
  );
}
