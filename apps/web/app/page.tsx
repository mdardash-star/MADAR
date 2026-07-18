export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 text-white" dir="rtl">
      <div className="max-w-3xl rounded-2xl border border-white/10 bg-white/5 p-10 shadow-2xl backdrop-blur">
        <p className="mb-3 text-sm uppercase tracking-[0.3em] text-cyan-300">MADAR ERP SaaS</p>
        <h1 className="text-4xl font-bold md:text-5xl">منصة ERP موحدة للشركات المتعددة</h1>
        <p className="mt-4 max-w-2xl text-slate-300">
          تم توسيع قاعدة الأعمال لتشمل المؤسسة، CRM، الموردين، المنتجات، والمخازن مع واجهات API جاهزة للتشغيل.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <a href="/login" className="rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950">تسجيل الدخول</a>
          <a href="/business" className="rounded-xl border border-emerald-400/50 px-5 py-3 font-semibold text-emerald-300">قاعدة الأعمال</a>
        </div>
      </div>
    </main>
  );
}
