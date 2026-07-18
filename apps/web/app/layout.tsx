import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'MADAR ERP',
  description: 'A production-ready enterprise ERP SaaS platform for multi-tenant operations.',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
