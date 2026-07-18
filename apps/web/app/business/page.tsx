'use client';

const sections = [
  { title: 'المؤسسة', items: ['الشركات', 'الفروع', 'الأقسام', 'مراكز التكلفة'] },
  { title: 'العلاقات', items: ['العملاء', 'مجموعات العملاء', 'جهات الاتصال', 'العناوين'] },
  { title: 'الموردون', items: ['الموردون', 'جهات الاتصال', 'العناوين'] },
  { title: 'المنتجات', items: ['الفئات', 'العلامات التجارية', 'الوحدات', 'المنتجات', 'التنوعات', 'الباركود', 'التسعير', 'الصور'] },
  { title: 'المخازن', items: ['المخازن', 'أماكن التخزين', 'الرصيد الافتتاحي'] },
];

export default function BusinessFoundationPage() {
  return (
    <main className="min-h-screen bg-slate-950 p-6 text-white" dir="rtl">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 rounded-2xl border border-cyan-400/30 bg-cyan-500/10 p-6">
          <p className="text-sm text-cyan-300">الحالة الحالية</p>
          <h1 className="mt-2 text-3xl font-bold">قاعدة الأعمال</h1>
          <p className="mt-2 max-w-3xl text-slate-300">تمت إضافة طبقة البيانات الأساسية للمنظمة، إدارة العلاقات، الموردين، المنتجات، والمخازن مع CRUD منشور على واجهة API موحدة.</p>
        </div>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {sections.map((section) => (
            <div key={section.title} className="rounded-2xl border border-white/10 bg-white/5 p-5">
              <h2 className="text-lg font-semibold text-cyan-300">{section.title}</h2>
              <ul className="mt-3 space-y-2 text-sm text-slate-200">
                {section.items.map((item) => (
                  <li key={item} className="rounded-xl bg-slate-900/60 px-3 py-2">{item}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
