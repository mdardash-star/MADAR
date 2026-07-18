export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 text-white">
      <div className="max-w-3xl rounded-2xl border border-white/10 bg-white/5 p-10 shadow-2xl backdrop-blur">
        <p className="mb-3 text-sm uppercase tracking-[0.3em] text-cyan-300">MADAR ERP SaaS</p>
        <h1 className="text-4xl font-bold md:text-5xl">Unified operations for multi-tenant enterprises</h1>
        <p className="mt-4 max-w-2xl text-slate-300">
          Built with Next.js, Tailwind CSS, FastAPI, PostgreSQL, SQLAlchemy, Alembic, and enterprise-ready deployment practices.
        </p>
      </div>
    </main>
  );
}
