'use client';

import { AuthGuard } from '@/components/auth/auth-guard';

const cards = [
  { title: 'الشركات', value: '01' },
  { title: 'الفروع', value: '05' },
  { title: 'المستخدمين', value: '24' },
  { title: 'الطلبات', value: '128' },
];

export default function DashboardPage() {
  return (
    <AuthGuard>
      <main className="min-h-screen bg-slate-950 p-6 text-white" dir="rtl">
        <div className="mx-auto max-w-6xl">
          <div className="mb-8 flex items-center justify-between gap-4">
            <div>
              <p className="text-sm text-cyan-300">لوحة القيادة</p>
              <h1 className="text-3xl font-bold">MADAR ERP</h1>
            </div>
            <div className="rounded-2xl border border-cyan-400/30 bg-cyan-500/10 px-4 py-3 text-sm">الإدارة المتعددة للجهات</div>
          </div>

          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {cards.map((card) => (
              <div key={card.title} className="rounded-2xl border border-white/10 bg-white/5 p-5">
                <p className="text-sm text-slate-300">{card.title}</p>
                <p className="mt-3 text-3xl font-bold">{card.value}</p>
              </div>
            ))}
          </div>
        </div>
      </main>
    </AuthGuard>
  );
}
