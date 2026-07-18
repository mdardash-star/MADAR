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
  listWarehouses,
  createWarehouse,
  updateWarehouse,
  deleteWarehouse,
  listBranches,
  getUser,
  type Warehouse,
  type Branch,
} from '@/lib/api';

const EMPTY: Omit<Warehouse, 'id' | 'company_id' | 'is_active'> = {
  name: '',
  code: '',
  location: '',
  branch_id: null,
};

export default function WarehousesPage() {
  const [rows, setRows] = useState<Warehouse[]>([]);
  const [branches, setBranches] = useState<Branch[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Warehouse | null>(null);
  const [form, setForm] = useState(EMPTY);
  const [formError, setFormError] = useState('');
  const [saving, setSaving] = useState(false);

  const [deleting, setDeleting] = useState<Warehouse | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  const companyId = typeof window !== 'undefined' ? getUser()?.company_id : undefined;

  const load = useCallback(async () => {
    if (!companyId) return;
    setLoading(true);
    try {
      const [wareData, branchData] = await Promise.all([
        listWarehouses(companyId, { search: search || undefined, limit: 100 }),
        listBranches(companyId, { limit: 200 }),
      ]);
      setRows(wareData);
      setBranches(branchData);
      setError('');
    } catch (e) {
      setError(e instanceof Error ? e.message : 'فشل تحميل البيانات');
    } finally {
      setLoading(false);
    }
  }, [companyId, search]);

  useEffect(() => { load(); }, [load]);

  function openCreate() {
    setEditing(null);
    setForm(EMPTY);
    setFormError('');
    setModalOpen(true);
  }

  function openEdit(row: Warehouse) {
    setEditing(row);
    setForm({ 
      name: row.name, 
      code: row.code, 
      location: row.location ?? '',
      branch_id: row.branch_id,
    });
    setFormError('');
    setModalOpen(true);
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!companyId) return;
    setSaving(true);
    setFormError('');
    try {
      if (editing) {
        await updateWarehouse(editing.id, form);
      } else {
        await createWarehouse({ ...form, company_id: companyId });
      }
      setModalOpen(false);
      await load();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'فشل الحفظ');
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete() {
    if (!deleting) return;
    setDeleteLoading(true);
    try {
      await deleteWarehouse(deleting.id);
      setDeleting(null);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'فشل الحذف');
      setDeleting(null);
    } finally {
      setDeleteLoading(false);
    }
  }

  const columns = [
    { key: 'name', label: 'اسم المستودع' },
    { key: 'code', label: 'الرمز' },
    { key: 'location', label: 'الموقع' },
    {
      key: 'branch_id',
      label: 'الفرع',
      render: (row: Warehouse) => {
        const br = branches.find(b => b.id === row.branch_id);
        return <span>{br?.name || '-'}</span>;
      }
    },
    {
      key: 'is_active',
      label: 'الحالة',
      render: (row: Warehouse) => (
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
          title="المستودعات"
          subtitle={`${rows.length} مستودع مسجل`}
          action={<AddButton onClick={openCreate}>إضافة مستودع</AddButton>}
        />

        <div className="mb-4">
          <SearchBar value={search} onChange={setSearch} placeholder="ابحث بالاسم أو الرمز…" />
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
            emptyMessage="لا يوجد مستودعات بعد. أضف مستودعك الأول."
          />
        )}
      </div>

      {modalOpen && (
        <Modal
          title={editing ? 'تعديل بيانات المستودع' : 'إضافة مستودع جديد'}
          onClose={() => setModalOpen(false)}
          footer={
            <>
              <CancelButton onClick={() => setModalOpen(false)} />
              <SubmitButton loading={saving}>{editing ? 'حفظ التعديلات' : 'إضافة المستودع'}</SubmitButton>
            </>
          }
        >
          <form id="warehouse-form" onSubmit={handleSubmit} className="space-y-4">
            <Field
              label="اسم المستودع *"
              required
              value={form.name}
              onChange={(e) => setForm((p) => ({ ...p, name: e.target.value }))}
            />
            <Field
              label="الرمز (كود) *"
              required
              value={form.code}
              onChange={(e) => setForm((p) => ({ ...p, code: e.target.value }))}
              placeholder="WH-001"
            />
            <Field
              label="الموقع"
              value={form.location ?? ''}
              onChange={(e) => setForm((p) => ({ ...p, location: e.target.value }))}
            />
            <SelectField
              label="الفرع"
              value={form.branch_id ? String(form.branch_id) : ''}
              onChange={(e) => setForm((p) => ({ ...p, branch_id: e.target.value ? Number(e.target.value) : null }))}
              options={[
                { value: '', label: 'اختر فرع (اختياري)' },
                ...branches.map(b => ({ value: String(b.id), label: b.name }))
              ]}
            />
            {formError && <ErrorAlert message={formError} />}
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
