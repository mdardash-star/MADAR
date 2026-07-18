'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { FormEvent, useState } from 'react';
import { saveToken, saveUser, getProfile } from '@/lib/api';

export default function RegisterCompanyPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    company_name: '',
    company_slug: '',
    legal_name: '',
    email: '',
    phone: '',
    admin_full_name: '',
    admin_email: '',
    admin_password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  function handleChange(field: keyof typeof form) {
    return (e: React.ChangeEvent<HTMLInputElement>) =>
      setForm((prev) => ({ ...prev, [field]: e.target.value }));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError('');
    setLoading(true);
    try {
      const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${API_BASE}/companies/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      if (!res.ok) {
        const body = await res.json();
        throw new Error(body?.detail ?? 'فشل إنشاء الشركة');
      }
      const data = await res.json();
      saveToken(data.tokens.access_token);
      const profile = await getProfile();
      saveUser(profile);
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'تعذر إنشاء الشركة');
    } finally {
      setLoading(false);
    }
  }

  const inp = 'w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 text-sm outline-none focus:border-cyan-500';

  return (
    <main className="min-h-screen bg-slate-950 p-6 text-white" dir="rtl">
      <div className="mx-auto max-w-4xl rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl backdrop-blur">
        <p className="text-sm font-semibold text-cyan-300">MADAR ERP</p>
        <h1 className="mt-2 text-3xl font-bold">تسجيل شركة جديدة</h1>

        <form className="mt-8 grid gap-4 md:grid-cols-2" onSubmit={handleSubmit}>
          <label className="block">
            <span className="mb-2 block text-sm">اسم الشركة *</span>
            <input required className={inp} value={form.company_name} onChange={handleChange('company_name')} />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm">الاسم المختصر (slug) *</span>
            <input required className={inp} value={form.company_slug} onChange={handleChange('company_slug')} placeholder="my-company" />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm">الاسم القانوني</span>
            <input className={inp} value={form.legal_name} onChange={handleChange('legal_name')} />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm">رقم الهاتف</span>
            <input className={inp} value={form.phone} onChange={handleChange('phone')} />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm">البريد الإلكتروني للشركة</span>
            <input type="email" className={inp} value={form.email} onChange={handleChange('email')} />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm">اسم المدير *</span>
            <input required className={inp} value={form.admin_full_name} onChange={handleChange('admin_full_name')} />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm">بريد المدير *</span>
            <input required type="email" className={inp} value={form.admin_email} onChange={handleChange('admin_email')} />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm">كلمة مرور المدير *</span>
            <input required type="password" minLength={8} className={inp} value={form.admin_password} onChange={handleChange('admin_password')} />
          </label>

          {error && (
            <p className="md:col-span-2 rounded-lg bg-red-500/20 px-3 py-2 text-sm text-red-200">{error}</p>
          )}

          <div className="md:col-span-2 flex items-center justify-between gap-3">
            <button
              type="submit"
              disabled={loading}
              className="rounded-xl bg-cyan-500 px-6 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:opacity-60"
            >
              {loading ? 'جاري الإنشاء…' : 'إنشاء الشركة'}
            </button>
            <Link href="/login" className="text-cyan-300 underline text-sm">لديك حساب بالفعل؟</Link>
          </div>
        </form>
      </div>
    </main>
  );
}
