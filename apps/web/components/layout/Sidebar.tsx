'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { clearToken, getUser } from '@/lib/api';

const nav = [
  { href: '/dashboard', label: 'لوحة القيادة', icon: '⊞' },
  { href: '/branches', label: 'الفروع', icon: '🏢' },
  { href: '/warehouses', label: 'المستودعات', icon: '🏭' },
  { href: '/customers', label: 'العملاء', icon: '👥' },
  { href: '/suppliers', label: 'الموردون', icon: '🏭' },
  { href: '/products', label: 'المنتجات', icon: '📦' },
  { href: '/quotations', label: 'عروض الأسعار', icon: '💰' },
  { href: '/orders', label: 'أوامر البيع', icon: '📋' },
  { href: '/invoices', label: 'الفواتير', icon: '📄' },
  { href: '/profile', label: 'الملف الشخصي', icon: '👤' },
];

export function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const user = getUser();

  function handleLogout() {
    clearToken();
    router.replace('/login');
  }

  return (
    <aside className="flex h-screen w-56 flex-col border-l border-white/10 bg-slate-900">
      {/* Brand */}
      <div className="border-b border-white/10 px-5 py-4">
        <p className="text-xs font-semibold tracking-widest text-cyan-400">MADAR ERP</p>
        <p className="mt-1 truncate text-sm font-medium text-white">
          {user?.company_name ?? '—'}
        </p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto px-3 py-4">
        <ul className="space-y-1">
          {nav.map(({ href, label, icon }) => {
            const active = pathname === href || pathname.startsWith(href + '/');
            return (
              <li key={href}>
                <Link
                  href={href}
                  className={`flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition ${
                    active
                      ? 'bg-cyan-500/20 font-semibold text-cyan-300'
                      : 'text-slate-300 hover:bg-white/5 hover:text-white'
                  }`}
                >
                  <span className="text-base">{icon}</span>
                  {label}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* User + logout */}
      <div className="border-t border-white/10 px-4 py-3">
        <p className="truncate text-xs text-slate-400">{user?.email ?? ''}</p>
        <button
          onClick={handleLogout}
          className="mt-2 w-full rounded-lg bg-red-500/10 px-3 py-1.5 text-xs text-red-300 transition hover:bg-red-500/20"
        >
          تسجيل الخروج
        </button>
      </div>
    </aside>
  );
}
