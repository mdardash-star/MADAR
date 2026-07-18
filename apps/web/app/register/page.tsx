'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { FormEvent, useState } from 'react';
import { saveToken } from '@/lib/auth';

export default function RegisterCompanyPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    company_name: 'شركة المثال',
    company_slug: 'al-mathal',
    legal_name: 'شركة المثال القابضة',
    email: 'hello@madar.local',
    phone: '+971500000000',
    admin_full_name: 'محمد المدير',
    admin_email: 'admin@madar.local',
    admin_password: 'Admin123!',
  });
  const [error, setError] = useState('');

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError('');

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/companies/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });

      if (!response.ok) {
        throw new Error('فشل إنشاء الشركة. تأكد من توفر البيانات.');
      }

      const data = await response.json();
      saveToken(data.tokens.access_token);
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'تعذر إنشاء الشركة');
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 p-6 text-white" dir="rtl">
      <div className="mx-auto max-w-4xl rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl backdrop-blur">
        <p className="text-sm font-semibold text-cyan-300">إنشاء مؤسسة جديدة</p>
        <h1 className="mt-2 text-3xl font-bold">تسجيل الشركة والإدارة</h1>

        <form className="mt-8 grid gap-4 md:grid-cols-2" onSubmit={handleSubmit}>
          <label className="block">
            <span className="mb-2 block text-sm">اسم الشركة</span>
            <input className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3" value={form.company_name} onChange={(event) => setForm({ ...form, company_name: event.target.value })} />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm">الاسم المختصر</span>
            <input className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3" value={form.company_slug} onChange={(event) => setForm({ ...form, company_slug: event.target.value })} />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm">الاسم القانوني</span>
            <input className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3" value={form.legal_name} onChange={(event) => setForm({ ...form, legal_name: event.target.value })} />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm">رقم الهاتف</span>
            <input className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3" value={form.phone} onChange={(event) => setForm({ ...form, phone: event.target.value })} />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm">البريد الإلكتروني للشركة</span>
            <input className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm">اسم المدير</span>
            <input className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3" value={form.admin_full_name} onChange={(event) => setForm({ ...form, admin_full_name: event.target.value })} />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm">بريد المدير</span>
            <input className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3" value={form.admin_email} onChange={(event) => setForm({ ...form, admin_email: event.target.value })} />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm">كلمة مرور المدير</span>
            <input type="password" className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3" value={form.admin_password} onChange={(event) => setForm({ ...form, admin_password: event.target.value })} />
          </label>

          {error ? <p className="md:col-span-2 rounded-lg bg-red-500/20 px-3 py-2 text-sm text-red-200">{error}</p> : null}

          <div className="md:col-span-2 flex items-center justify-between gap-3">
            <button type="submit" className="rounded-xl bg-cyan-500 px-6 py-3 font-semibold text-slate-950">إنشاء الشركة</button>
            <Link href="/login" className="text-cyan-300 underline">لديك حساب بالفعل؟</Link>
          </div>
        </form>
      </div>
    </main>
  );
}
