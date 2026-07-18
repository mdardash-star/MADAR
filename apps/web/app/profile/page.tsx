'use client';

import { useEffect, useState } from 'react';
import { AppShell } from '@/components/layout/AppShell';
import { getProfile, getUser, type UserProfile } from '@/lib/api';
import { PageHeader } from '@/components/ui/Form';

export default function ProfilePage() {
  const [profile, setProfile] = useState<UserProfile | null>(
    typeof window !== 'undefined' ? getUser() : null,
  );

  useEffect(() => {
    getProfile().then(setProfile).catch(() => {});
  }, []);

  return (
    <AppShell>
      <div className="mx-auto max-w-2xl">
        <PageHeader title="الملف الشخصي" subtitle="بيانات حسابك وشركتك" />
        {profile && (
          <div className="space-y-3 text-sm">
            {[
              { label: 'الاسم الكامل', value: profile.full_name },
              { label: 'البريد الإلكتروني', value: profile.email },
              { label: 'الشركة', value: profile.company_name ?? '\u2014' },
              { label: 'معرف الشركة', value: String(profile.company_id) },
              { label: 'الحالة', value: profile.is_active ? 'نشط' : 'معطل' },
            ].map(({ label, value }) => (
              <div key={label} className="flex items-center justify-between rounded-xl border border-white/10 bg-white/5 px-5 py-3">
                <span className="text-slate-400">{label}</span>
                <span className="font-medium text-white">{value}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </AppShell>
  );
}
