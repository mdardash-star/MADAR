'use client';

import { useEffect, useState } from 'react';
import { AppShell } from '@/components/layout/AppShell';
import { getDashboardSummary, getUser, type DashboardSummary } from '@/lib/api';

const TILES = [
  { key: 'branches' as keyof DashboardSummary, label: 'الفروع', href: '/branches', color: 'blue' },
  { key: 'warehouses' as keyof DashboardSummary, label: 'المستودعات', href: '/warehouses', color: 'indigo' },
  { key: 'customers' as keyof DashboardSummary, label: 'العملاء', href: '/customers', color: 'cyan' },
  { key: 'suppliers' as keyof DashboardSummary, label: 'الموردون', href: '/suppliers', color: 'emerald' },
  { key: 'products' as keyof DashboardSummary, label: 'المنتجات', href: '/products', color: 'violet' },
  { key: 'quotations' as keyof DashboardSummary, label: 'عروض الأسعار', href: '/quotations', color: 'yellow' },
  { key: 'sales_orders' as keyof DashboardSummary, label: 'طلبات البيع', href: '/orders', color: 'amber' },
  { key: 'sales_invoices' as keyof DashboardSummary, label: 'الفواتير', href: '/invoices', color: 'rose' },
  { key: 'crm_leads' as keyof DashboardSummary, label: 'فرص CRM', href: '#', color: 'sky' },
];

const colorMap: Record<string, string> = {
  blue: 'border-blue-400/30 bg-blue-500/10 text-blue-300',
  indigo: 'border-indigo-400/30 bg-indigo-500/10 text-indigo-300',
  cyan: 'border-cyan-400/30 bg-cyan-500/10 text-cyan-300',
  emerald: 'border-emerald-400/30 bg-emerald-500/10 text-emerald-300',
  violet: 'border-violet-400/30 bg-violet-500/10 text-violet-300',
  yellow: 'border-yellow-400/30 bg-yellow-500/10 text-yellow-300',
  amber: 'border-amber-400/30 bg-amber-500/10 text-amber-300',
  rose: 'border-rose-400/30 bg-rose-500/10 text-rose-300',
  sky: 'border-sky-400/30 bg-sky-500/10 text-sky-300',
};

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [error, setError] = useState('');
  const user = typeof window !== 'undefined' ? getUser() : null;

  useEffect(() => {
    const u = getUser();
    if (!u) return;
    getDashboardSummary(u.company_id)
      .then(setSummary)
      .catch((e) => setError(e.message));
  }, []);

  return (
    <AppShell>
      <div className="mx-auto max-w-6xl">
        {/* Header */}
        <div className="mb-8">
          <p className="text-sm text-slate-400">مرحباً بك</p>
          <h1 className="text-3xl font-bold text-white">لوحة القيادة</h1>
          {user && (
            <p className="mt-1 text-sm text-cyan-400">{user.company_name}</p>
          )}
        </div>

        {error && (
          <div className="mb-4 rounded-xl bg-red-500/15 px-4 py-3 text-sm text-red-300">{error}</div>
        )}

        {/* KPI tiles */}
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {TILES.map(({ key, label, href, color }) => (
            <a
              key={key}
              href={href}
              className={`rounded-2xl border p-5 transition hover:opacity-90 ${colorMap[color]}`}
            >
              <p className="text-sm font-medium">{label}</p>
              <p className="mt-3 text-4xl font-bold">
                {summary == null ? (
                  <span className="inline-block h-8 w-16 animate-pulse rounded bg-white/10" />
                ) : (
                  summary[key].toLocaleString('ar-SA')
                )}
              </p>
            </a>
          ))}
        </div>

        {/* Quick links */}
        <div className="mt-8">
          <h2 className="mb-4 text-sm font-semibold text-slate-400">إجراءات سريعة</h2>
          <div className="flex flex-wrap gap-3">
            <a href="/customers" className="rounded-xl bg-white/5 px-4 py-2.5 text-sm text-slate-200 transition hover:bg-white/10">
              + إضافة عميل جديد
            </a>
            <a href="/suppliers" className="rounded-xl bg-white/5 px-4 py-2.5 text-sm text-slate-200 transition hover:bg-white/10">
              + إضافة مورد جديد
            </a>
            <a href="/products" className="rounded-xl bg-white/5 px-4 py-2.5 text-sm text-slate-200 transition hover:bg-white/10">
              + إضافة منتج جديد
            </a>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
