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
  listQuotations,
  createQuotation,
  updateQuotation,
  deleteQuotation,
  listCustomers,
  listWarehouses,
  getUser,
  type SalesQuotation,
  type Customer,
  type Warehouse,
} from '@/lib/api';

const EMPTY: Omit<SalesQuotation, 'id' | 'company_id'> = {
  customer_id: null,
  quotation_number: '',
  quotation_date: new Date().toISOString().split('T')[0],
  expiry_date: '',
  total_amount: 0,
  warehouse_id: null,
  status: 'draft',
};

export default function QuotationsPage() {
  const [rows, setRows] = useState<SalesQuotation[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [warehouses, setWarehouses] = useState<Warehouse[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<SalesQuotation | null>(null);
  const [form, setForm] = useState(EMPTY);
  const [formError, setFormError] = useState('');
  const [saving, setSaving] = useState(false);

  const [deleting, setDeleting] = useState<SalesQuotation | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  const companyId = typeof window !== 'undefined' ? getUser()?.company_id : undefined;

  const load = useCallback(async () => {
    if (!companyId) return;
    setLoading(true);
    try {
      const [quotData, custData, wareData] = await Promise.all([
        listQuotations(companyId, { search: search || undefined, limit: 100 }),
        listCustomers(companyId, { limit: 200 }),
        listWarehouses(companyId, { limit: 200 }),
      ]);
      setRows(quotData);
      setCustomers(custData);
      setWarehouses(wareData);
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
    setForm({ ...EMPTY, quotation_date: new Date().toISOString().split('T')[0] });
    setFormError('');
    setModalOpen(true);
  }

  function openEdit(row: SalesQuotation) {
    setEditing(row);
    setForm({
      customer_id: row.customer_id,
      quotation_number: row.quotation_number ?? '',
      quotation_date: row.quotation_date ?? '',
      expiry_date: row.expiry_date ?? '',
      total_amount: row.total_amount ?? 0,
      warehouse_id: row.warehouse_id,
      status: row.status ?? 'draft',
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
        await updateQuotation(editing.id, form);
      } else {
        await createQuotation({ ...form, company_id: companyId });
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
      await deleteQuotation(deleting.id);
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
    { key: 'quotation_number', label: 'رقم العرض' },
    {
      key: 'customer_id',
      label: 'العميل',
      render: (row: SalesQuotation) => {
        const cust = customers.find(c => c.id === row.customer_id);
        return <span>{cust?.name || '-'}</span>;
      }
    },
    { key: 'quotation_date', label: 'التاريخ' },
    { key: 'total_amount', label: 'المبلغ' },
    { key: 'status', label: 'الحالة' },
  ];

  return (
    <AppShell>
      <div className="mx-auto max-w-6xl">
        <PageHeader
          title="عروض الأسعار"
          subtitle={`${rows.length} عرض مسجل`}
          action={<AddButton onClick={openCreate}>إضافة عرض</AddButton>}
        />

        <div className="mb-4">
          <SearchBar value={search} onChange={setSearch} placeholder="ابحث برقم العرض أو العميل…" />
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
            emptyMessage="لا يوجد عروض بعد. أضف عرض الأسعار الأول."
          />
        )}
      </div>

      {modalOpen && (
        <Modal
          title={editing ? 'تعديل العرض' : 'إضافة عرض أسعار جديد'}
          onClose={() => setModalOpen(false)}
          footer={
            <>
              <CancelButton onClick={() => setModalOpen(false)} />
              <SubmitButton loading={saving}>{editing ? 'حفظ التعديلات' : 'إضافة العرض'}</SubmitButton>
            </>
          }
        >
          <form id="quotation-form" onSubmit={handleSubmit} className="space-y-4">
            <SelectField
              label="العميل *"
              required
              value={form.customer_id ? String(form.customer_id) : ''}
              onChange={(e) => setForm((p) => ({ ...p, customer_id: e.target.value ? Number(e.target.value) : null }))}
              options={[
                { value: '', label: 'اختر عميل' },
                ...customers.map(c => ({ value: String(c.id), label: c.name }))
              ]}
            />
            <Field
              label="رقم العرض"
              value={form.quotation_number ?? ''}
              onChange={(e) => setForm((p) => ({ ...p, quotation_number: e.target.value }))}
            />
            <Field
              label="تاريخ العرض"
              type="date"
              value={form.quotation_date ?? ''}
              onChange={(e) => setForm((p) => ({ ...p, quotation_date: e.target.value }))}
            />
            <Field
              label="تاريخ الانتهاء"
              type="date"
              value={form.expiry_date ?? ''}
              onChange={(e) => setForm((p) => ({ ...p, expiry_date: e.target.value }))}
            />
            <Field
              label="المبلغ الإجمالي"
              type="number"
              value={form.total_amount ?? 0}
              onChange={(e) => setForm((p) => ({ ...p, total_amount: Number(e.target.value) }))}
            />
            <SelectField
              label="المستودع"
              value={form.warehouse_id ? String(form.warehouse_id) : ''}
              onChange={(e) => setForm((p) => ({ ...p, warehouse_id: e.target.value ? Number(e.target.value) : null }))}
              options={[
                { value: '', label: 'اختر مستودع (اختياري)' },
                ...warehouses.map(w => ({ value: String(w.id), label: w.name }))
              ]}
            />
            <SelectField
              label="الحالة"
              value={form.status ?? 'draft'}
              onChange={(e) => setForm((p) => ({ ...p, status: e.target.value }))}
              options={[
                { value: 'draft', label: 'مسودة' },
                { value: 'sent', label: 'مرسل' },
                { value: 'accepted', label: 'مقبول' },
                { value: 'rejected', label: 'مرفوض' },
              ]}
            />
            {formError && <ErrorAlert message={formError} />}
          </form>
        </Modal>
      )}

      {deleting && (
        <DeleteConfirmModal
          name={deleting.quotation_number ?? 'العرض'}
          onConfirm={handleDelete}
          onCancel={() => setDeleting(null)}
          loading={deleteLoading}
        />
      )}
    </AppShell>
  );
}
