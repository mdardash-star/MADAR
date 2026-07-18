'use client';

import { useEffect, useState, useCallback } from 'react';
import { AppShell } from '@/components/layout/AppShell';
import { DataTable } from '@/components/ui/DataTable';
import { Modal } from '@/components/ui/Modal';
import {
  Field,
  PageHeader,
  SearchBar,
  AddButton,
  SubmitButton,
  CancelButton,
  ErrorAlert,
  DeleteConfirmModal,
} from '@/components/ui/Form';
import {
  listBranches,
  createBranch,
  updateBranch,
  deleteBranch,
  getUser,
  type Branch,
} from '@/lib/api';

const EMPTY: Omit<Branch, 'id' | 'company_id' | 'is_active'> = {
  name: '',
  code: '',
  country: '',
  city: '',
  timezone: '',
};

export default function BranchesPage() {
  const [rows, setRows] = useState<Branch[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Branch | null>(null);
  const [form, setForm] = useState(EMPTY);
  const [formError, setFormError] = useState('');
  const [saving, setSaving] = useState(false);

  const [deleting, setDeleting] = useState<Branch | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  const companyId = typeof window !== 'undefined' ? getUser()?.company_id : undefined;

  const load = useCallback(async () => {
    if (!companyId) return;
    setLoading(true);
    try {
      const data = await listBranches(companyId, { search: search || undefined, limit: 100 });
      setRows(data);
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

  function openEdit(row: Branch) {
    setEditing(row);
    setForm({ 
      name: row.name, 
      code: row.code, 
      country: row.country ?? '',
      city: row.city ?? '',
      timezone: row.timezone ?? '',
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
        await updateBranch(editing.id, form);
      } else {
        await createBranch({ ...form, company_id: companyId });
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
      await deleteBranch(deleting.id);
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
    { key: 'name', label: 'اسم الفرع' },
    { key: 'code', label: 'الرمز' },
    { key: 'city', label: 'المدينة' },
    { key: 'country', label: 'الدولة' },
    {
      key: 'is_active',
      label: 'الحالة',
      render: (row: Branch) => (
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
          title="الفروع"
          subtitle={`${rows.length} فرع مسجل`}
          action={<AddButton onClick={openCreate}>إضافة فرع</AddButton>}
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
            emptyMessage="لا يوجد فروع بعد. أضف فرعك الأول."
          />
        )}
      </div>

      {modalOpen && (
        <Modal
          title={editing ? 'تعديل بيانات الفرع' : 'إضافة فرع جديد'}
          onClose={() => setModalOpen(false)}
          footer={
            <>
              <CancelButton onClick={() => setModalOpen(false)} />
              <SubmitButton loading={saving}>{editing ? 'حفظ التعديلات' : 'إضافة الفرع'}</SubmitButton>
            </>
          }
        >
          <form id="branch-form" onSubmit={handleSubmit} className="space-y-4">
            <Field
              label="اسم الفرع *"
              required
              value={form.name}
              onChange={(e) => setForm((p) => ({ ...p, name: e.target.value }))}
            />
            <Field
              label="الرمز (كود) *"
              required
              value={form.code}
              onChange={(e) => setForm((p) => ({ ...p, code: e.target.value }))}
              placeholder="BRANCH-001"
            />
            <Field
              label="المدينة"
              value={form.city ?? ''}
              onChange={(e) => setForm((p) => ({ ...p, city: e.target.value }))}
            />
            <Field
              label="الدولة"
              value={form.country ?? ''}
              onChange={(e) => setForm((p) => ({ ...p, country: e.target.value }))}
            />
            <Field
              label="المنطقة الزمنية"
              value={form.timezone ?? ''}
              onChange={(e) => setForm((p) => ({ ...p, timezone: e.target.value }))}
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
