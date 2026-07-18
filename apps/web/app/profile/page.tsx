'use client';

import { AuthGuard } from '@/components/auth/auth-guard';

export default function ProfilePage() {
  return (
    <AuthGuard>
      <main className="min-h-screen bg-slate-950 p-6 text-white" dir="rtl">
        <div className="mx-auto max-w-3xl rounded-3xl border border-white/10 bg-white/5 p-8">
          <p className="text-sm text-cyan-300">الملف الشخصي</p>
          <h1 className="mt-2 text-3xl font-bold">بيانات المستخدم</h1>
          <div className="mt-8 space-y-4 text-slate-100">
            <div className="rounded-2xl bg-slate-900 p-4">الاسم الكامل: محمد المدير</div>
            <div className="rounded-2xl bg-slate-900 p-4">البريد الإلكتروني: admin@madar.local</div>
            <div className="rounded-2xl bg-slate-900 p-4">الدور: Admin</div>
          </div>
        </div>
      </main>
    </AuthGuard>
  );
}
