'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { FormEvent, useState } from 'react';
import { saveToken } from '@/lib/auth';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('admin@madar.local');
  const [password, setPassword] = useState('Admin123!');
  const [error, setError] = useState('');

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError('');

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('فشل تسجيل الدخول. تحقق من البيانات.');
      }

      const data = await response.json();
      saveToken(data.access_token);
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'حدث خطأ غير متوقع');
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 p-6 text-white" dir="rtl">
      <div className="w-full max-w-md rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl backdrop-blur">
        <p className="text-sm font-semibold text-cyan-300">MADAR ERP</p>
        <h1 className="mt-2 text-3xl font-bold">تسجيل الدخول</h1>
        <p className="mt-2 text-sm text-slate-300">مرحباً بك في لوحة التشغيل الموحدة.</p>

        <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
          <label className="block">
            <span className="mb-2 block text-sm">البريد الإلكتروني</span>
            <input
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 outline-none ring-0"
              placeholder="admin@madar.local"
            />
          </label>

          <label className="block">
            <span className="mb-2 block text-sm">كلمة المرور</span>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 outline-none ring-0"
              placeholder="********"
            />
          </label>

          {error ? <p className="rounded-lg bg-red-500/20 px-3 py-2 text-sm text-red-200">{error}</p> : null}

          <button className="w-full rounded-xl bg-cyan-500 px-4 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400" type="submit">
            تسجيل الدخول
          </button>
        </form>

        <div className="mt-6 text-sm text-slate-300">
          ليس لديك شركة؟{' '}
          <Link className="text-cyan-300 underline" href="/register">
            إنشاء شركة جديدة
          </Link>
        </div>
      </div>
    </main>
  );
}
