'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { FormEvent, useState } from 'react';
import { login } from '@/lib/api';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(email, password);
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'حدث خطأ غير متوقع');
    } finally {
      setLoading(false);
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
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 outline-none focus:border-cyan-500"
              placeholder="admin@example.com"
            />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm">كلمة المرور</span>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 outline-none focus:border-cyan-500"
              placeholder="••••••••"
            />
          </label>
          {error && (
            <p className="rounded-lg bg-red-500/20 px-3 py-2 text-sm text-red-200">{error}</p>
          )}
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-xl bg-cyan-500 px-4 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:opacity-60"
          >
            {loading ? 'جاري التحقق…' : 'تسجيل الدخول'}
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

