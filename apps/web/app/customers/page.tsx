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
  listCustomers,
  createCustomer,
  updateCustomer,
  deleteCustomer,
  getUser,
  type Customer,
} from '@/lib/api';

const EMPTY: Omit<Customer, 'id' | 'company_id' | 'is_active'> = {
  name: '',
  code: '',
  email: '',
  phone: '',
  address: '',
};

export default function CustomersPage() {
  const [rows, setRows] = useState<Customer[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Customer | null>(null);
  const [form, setForm] = useState(EMPTY);
  const [formError, setFormError] = useState('');
  const [saving, setSaving] = useState(false);

  // Delete state
  const [deleting, setDeleting] = useState<Customer | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  const companyId = typeof window !== 'undefined' ? getUser()?.company_id : undefined;

  const load = useCallback(async () => {
    if (!companyId) return;
    setLoading(true);
    try {
      const data = await listCustomers(companyId, { search: search || undefined, limit: 100 });
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

  function openEdit(row: Customer) {
    setEditing(row);
    setForm({ name: row.name, code: row.code, email: row.email ?? '', phone: row.phone ?? '', address: row.address ?? '' });
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
        await updateCustomer(editing.id, form);
      } else {
        await createCustomer({ ...form, company_id: companyId });
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
      await deleteCustomer(deleting.id);
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
    { key: 'name', label: 'الاسم' },
    { key: 'code', label: 'الرمز' },
    { key: 'email', label: 'البريد الإلكتروني' },
    { key: 'phone', label: 'الهاتف' },
    {
      key: 'is_active',
      label: 'الحالة',
      render: (row: Customer) => (
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
          title="العملاء"
          subtitle={`${rows.length} عميل مسجل`}
          action={<AddButton onClick={openCreate}>إضافة عميل</AddButton>}
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
            emptyMessage="لا يوجد عملاء بعد. أضف عميلك الأول."
          />
        )}
      </div>

      {/* Create / Edit modal */}
      {modalOpen && (
        <Modal
          title={editing ? 'تعديل بيانات العميل' : 'إضافة عميل جديد'}
          onClose={() => setModalOpen(false)}
          footer={
            <>
              <CancelButton onClick={() => setModalOpen(false)} />
              <SubmitButton loading={saving}>{editing ? 'حفظ التعديلات' : 'إضافة العميل'}</SubmitButton>
            </>
          }
        >
          <form id="customer-form" onSubmit={handleSubmit} className="space-y-4">
            <Field
              label="اسم العميل *"
              required
              value={form.name}
              onChange={(e) => setForm((p) => ({ ...p, name: e.target.value }))}
            />
            <Field
              label="الرمز (كود) *"
              required
              value={form.code}
              onChange={(e) => setForm((p) => ({ ...p, code: e.target.value }))}
              placeholder="CUST-001"
            />
            <Field
              label="البريد الإلكتروني"
              type="email"
              value={form.email ?? ''}
              onChange={(e) => setForm((p) => ({ ...p, email: e.target.value }))}
            />
            <Field
              label="رقم الهاتف"
              value={form.phone ?? ''}
              onChange={(e) => setForm((p) => ({ ...p, phone: e.target.value }))}
            />
            <Field
              label="العنوان"
              value={form.address ?? ''}
              onChange={(e) => setForm((p) => ({ ...p, address: e.target.value }))}
            />
            {formError && <ErrorAlert message={formError} />}
          </form>
        </Modal>
      )}

      {/* Delete confirm */}
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
