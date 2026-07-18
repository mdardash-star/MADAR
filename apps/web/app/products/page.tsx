'use client';

import { useEffect, useState, useCallback } from 'react';
import { AppShell } from '@/components/layout/AppShell';
import { DataTable } from '@/components/ui/DataTable';
import { Modal } from '@/components/ui/Modal';
import {
  Field,
  SelectField,
  PageHeader,
  SearchBar,
  AddButton,
  SubmitButton,
  CancelButton,
  ErrorAlert,
  DeleteConfirmModal,
} from '@/components/ui/Form';
import {
  listProducts,
  createProduct,
  updateProduct,
  deleteProduct,
  listProductCategories,
  listUnitsOfMeasure,
  createProductCategory,
  createUnitOfMeasure,
  getUser,
  type Product,
  type ProductCategory,
  type UnitOfMeasure,
} from '@/lib/api';

interface ProductForm {
  name: string;
  sku: string;
  description: string;
  selling_price: string;
  cost_price: string;
  category_id: string;
  unit_of_measure_id: string;
}

const EMPTY_FORM: ProductForm = {
  name: '',
  sku: '',
  description: '',
  selling_price: '',
  cost_price: '',
  category_id: '',
  unit_of_measure_id: '',
};

export default function ProductsPage() {
  const [rows, setRows] = useState<Product[]>([]);
  const [categories, setCategories] = useState<ProductCategory[]>([]);
  const [uoms, setUoms] = useState<UnitOfMeasure[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Product | null>(null);
  const [form, setForm] = useState<ProductForm>(EMPTY_FORM);
  const [formError, setFormError] = useState('');
  const [saving, setSaving] = useState(false);

  // Quick-create category / UoM
  const [catModalOpen, setCatModalOpen] = useState(false);
  const [catName, setCatName] = useState('');
  const [catCode, setCatCode] = useState('');
  const [catSaving, setCatSaving] = useState(false);

  const [uomModalOpen, setUomModalOpen] = useState(false);
  const [uomName, setUomName] = useState('');
  const [uomCode, setUomCode] = useState('');
  const [uomSaving, setUomSaving] = useState(false);

  const [deleting, setDeleting] = useState<Product | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  const companyId = typeof window !== 'undefined' ? getUser()?.company_id : undefined;

  const loadLists = useCallback(async () => {
    if (!companyId) return;
    const [cats, us] = await Promise.all([
      listProductCategories(companyId).catch(() => []),
      listUnitsOfMeasure(companyId).catch(() => []),
    ]);
    setCategories(cats);
    setUoms(us);
  }, [companyId]);

  const load = useCallback(async () => {
    if (!companyId) return;
    setLoading(true);
    try {
      const data = await listProducts(companyId, { search: search || undefined, limit: 100 });
      setRows(data);
      setError('');
    } catch (e) {
      setError(e instanceof Error ? e.message : 'فشل تحميل البيانات');
    } finally {
      setLoading(false);
    }
  }, [companyId, search]);

  useEffect(() => {
    loadLists();
    load();
  }, [loadLists, load]);

  function openCreate() {
    setEditing(null);
    setForm(EMPTY_FORM);
    setFormError('');
    setModalOpen(true);
  }

  function openEdit(row: Product) {
    setEditing(row);
    setForm({
      name: row.name,
      sku: row.sku,
      description: row.description ?? '',
      selling_price: String(row.selling_price),
      cost_price: String(row.cost_price),
      category_id: row.category_id ? String(row.category_id) : '',
      unit_of_measure_id: row.unit_of_measure_id ? String(row.unit_of_measure_id) : '',
    });
    setFormError('');
    setModalOpen(true);
  }

  function f(field: keyof ProductForm) {
    return (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) =>
      setForm((p) => ({ ...p, [field]: e.target.value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!companyId) return;
    setSaving(true);
    setFormError('');
    try {
      const payload = {
        name: form.name,
        sku: form.sku,
        description: form.description || null,
        selling_price: Number(form.selling_price),
        cost_price: Number(form.cost_price),
        category_id: form.category_id ? Number(form.category_id) : null,
        unit_of_measure_id: form.unit_of_measure_id ? Number(form.unit_of_measure_id) : null,
        barcode: null,
      };
      if (editing) {
        await updateProduct(editing.id, payload);
      } else {
        await createProduct({ ...payload, company_id: companyId });
      }
      setModalOpen(false);
      await load();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'فشل الحفظ');
    } finally {
      setSaving(false);
    }
  }

  async function handleCreateCategory(e: React.FormEvent) {
    e.preventDefault();
    if (!companyId) return;
    setCatSaving(true);
    try {
      const cat = await createProductCategory({ company_id: companyId, name: catName, code: catCode });
      setCategories((prev) => [...prev, cat]);
      setForm((p) => ({ ...p, category_id: String(cat.id) }));
      setCatModalOpen(false);
      setCatName('');
      setCatCode('');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'فشل إنشاء الفئة');
    } finally {
      setCatSaving(false);
    }
  }

  async function handleCreateUom(e: React.FormEvent) {
    e.preventDefault();
    if (!companyId) return;
    setUomSaving(true);
    try {
      const uom = await createUnitOfMeasure({ company_id: companyId, name: uomName, code: uomCode });
      setUoms((prev) => [...prev, uom]);
      setForm((p) => ({ ...p, unit_of_measure_id: String(uom.id) }));
      setUomModalOpen(false);
      setUomName('');
      setUomCode('');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'فشل إنشاء وحدة القياس');
    } finally {
      setUomSaving(false);
    }
  }

  async function handleDelete() {
    if (!deleting) return;
    setDeleteLoading(true);
    try {
      await deleteProduct(deleting.id);
      setDeleting(null);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'فشل الحذف');
      setDeleting(null);
    } finally {
      setDeleteLoading(false);
    }
  }

  const catOpts = categories.map((c) => ({ value: c.id, label: c.name }));
  const uomOpts = uoms.map((u) => ({ value: u.id, label: u.name }));

  const catMap = Object.fromEntries(categories.map((c) => [c.id, c.name]));
  const uomMap = Object.fromEntries(uoms.map((u) => [u.id, u.name]));

  const columns = [
    { key: 'name', label: 'اسم المنتج' },
    { key: 'sku', label: 'SKU' },
    {
      key: 'category_id',
      label: 'الفئة',
      render: (row: Product) => catMap[row.category_id ?? ''] ?? '—',
    },
    {
      key: 'selling_price',
      label: 'سعر البيع',
      render: (row: Product) => row.selling_price.toLocaleString('ar-SA'),
    },
    {
      key: 'cost_price',
      label: 'سعر التكلفة',
      render: (row: Product) => row.cost_price.toLocaleString('ar-SA'),
    },
    {
      key: 'unit_of_measure_id',
      label: 'الوحدة',
      render: (row: Product) => uomMap[row.unit_of_measure_id ?? ''] ?? '—',
    },
    {
      key: 'is_active',
      label: 'الحالة',
      render: (row: Product) => (
        <span className={`rounded-full px-2 py-0.5 text-xs ${row.is_active ? 'bg-emerald-500/20 text-emerald-300' : 'bg-slate-500/20 text-slate-400'}`}>
          {row.is_active ? 'نشط' : 'معطل'}
        </span>
      ),
    },
  ];

  return (
    <AppShell>
      <div className="mx-auto max-w-6xl">
        <PageHeader
          title="المنتجات"
          subtitle={`${rows.length} منتج مسجل`}
          action={<AddButton onClick={openCreate}>إضافة منتج</AddButton>}
        />
        <div className="mb-4">
          <SearchBar value={search} onChange={setSearch} placeholder="ابحث بالاسم أو SKU…" />
        </div>
        {error && <ErrorAlert message={error} />}
        {loading ? (
          <div className="py-20 text-center text-slate-500">جاري التحميل…</div>
        ) : (
          <DataTable
            columns={columns}
            rows={rows}
            onEdit={openEdit}
            onDelete={setDeleting}
            emptyMessage="لا يوجد منتجات بعد. أضف منتجاً جديداً."
          />
        )}
      </div>

      {/* Product form modal */}
      {modalOpen && (
        <Modal
          title={editing ? 'تعديل بيانات المنتج' : 'إضافة منتج جديد'}
          onClose={() => setModalOpen(false)}
          footer={
            <>
              <CancelButton onClick={() => setModalOpen(false)} />
              <SubmitButton loading={saving}>{editing ? 'حفظ التعديلات' : 'إضافة المنتج'}</SubmitButton>
            </>
          }
        >
          <form id="product-form" onSubmit={handleSubmit} className="space-y-4">
            <Field label="اسم المنتج *" required value={form.name} onChange={f('name')} />
            <Field label="رمز SKU *" required value={form.sku} onChange={f('sku')} placeholder="PROD-001" />
            <div className="grid grid-cols-2 gap-4">
              <Field label="سعر البيع *" required type="number" min="0" step="0.01" value={form.selling_price} onChange={f('selling_price')} />
              <Field label="سعر التكلفة *" required type="number" min="0" step="0.01" value={form.cost_price} onChange={f('cost_price')} />
            </div>
            <div className="flex gap-2 items-end">
              <div className="flex-1">
                <SelectField
                  label="الفئة"
                  options={catOpts}
                  placeholder="اختر الفئة…"
                  value={form.category_id}
                  onChange={f('category_id')}
                />
              </div>
              <button
                type="button"
                onClick={() => setCatModalOpen(true)}
                className="mb-0.5 rounded-xl bg-white/5 px-3 py-2.5 text-xs text-slate-300 hover:bg-white/10"
              >
                + جديد
              </button>
            </div>
            <div className="flex gap-2 items-end">
              <div className="flex-1">
                <SelectField
                  label="وحدة القياس"
                  options={uomOpts}
                  placeholder="اختر الوحدة…"
                  value={form.unit_of_measure_id}
                  onChange={f('unit_of_measure_id')}
                />
              </div>
              <button
                type="button"
                onClick={() => setUomModalOpen(true)}
                className="mb-0.5 rounded-xl bg-white/5 px-3 py-2.5 text-xs text-slate-300 hover:bg-white/10"
              >
                + جديد
              </button>
            </div>
            <Field label="الوصف" value={form.description} onChange={f('description')} />
            {formError && <ErrorAlert message={formError} />}
          </form>
        </Modal>
      )}

      {/* Quick-create category */}
      {catModalOpen && (
        <Modal title="إضافة فئة جديدة" onClose={() => setCatModalOpen(false)}>
          <form onSubmit={handleCreateCategory} className="space-y-4">
            <Field label="اسم الفئة *" required value={catName} onChange={(e) => setCatName(e.target.value)} />
            <Field label="الرمز *" required value={catCode} onChange={(e) => setCatCode(e.target.value)} placeholder="ELEC" />
            <div className="flex justify-end gap-3">
              <CancelButton onClick={() => setCatModalOpen(false)} />
              <SubmitButton loading={catSaving}>إضافة</SubmitButton>
            </div>
          </form>
        </Modal>
      )}

      {/* Quick-create UoM */}
      {uomModalOpen && (
        <Modal title="إضافة وحدة قياس جديدة" onClose={() => setUomModalOpen(false)}>
          <form onSubmit={handleCreateUom} className="space-y-4">
            <Field label="اسم الوحدة *" required value={uomName} onChange={(e) => setUomName(e.target.value)} />
            <Field label="الرمز *" required value={uomCode} onChange={(e) => setUomCode(e.target.value)} placeholder="PC" />
            <div className="flex justify-end gap-3">
              <CancelButton onClick={() => setUomModalOpen(false)} />
              <SubmitButton loading={uomSaving}>إضافة</SubmitButton>
            </div>
          </form>
        </Modal>
      )}

      {deleting && (
        <DeleteConfirmModal
          name={deleting.name}
          onConfirm={handleDelete}
          onCancel={() => setDeleting(null)}
          loading={deleteLoading}
        />
      )}
    </AppShell>
  );
}
