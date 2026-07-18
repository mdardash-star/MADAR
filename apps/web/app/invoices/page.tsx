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
  listInvoices,
  createInvoice,
  updateInvoice,
  deleteInvoice,
  listCustomers,
  listOrders,
  listWarehouses,
  getUser,
  type SalesInvoice,
  type Customer,
  type SalesOrder,
  type Warehouse,
} from '@/lib/api';

const EMPTY: Omit<SalesInvoice, 'id' | 'company_id'> = {
  customer_id: null,
  invoice_number: '',
  invoice_date: new Date().toISOString().split('T')[0],
  total_amount: 0,
  order_id: null,
  warehouse_id: null,
  status: 'draft',
};

export default function InvoicesPage() {
  const [rows, setRows] = useState<SalesInvoice[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [orders, setOrders] = useState<SalesOrder[]>([]);
  const [warehouses, setWarehouses] = useState<Warehouse[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<SalesInvoice | null>(null);
  const [form, setForm] = useState(EMPTY);
  const [formError, setFormError] = useState('');
  const [saving, setSaving] = useState(false);

  const [deleting, setDeleting] = useState<SalesInvoice | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  const companyId = typeof window !== 'undefined' ? getUser()?.company_id : undefined;

  const load = useCallback(async () => {
    if (!companyId) return;
    setLoading(true);
    try {
      const [invData, custData, ordData, wareData] = await Promise.all([
        listInvoices(companyId, { search: search || undefined, limit: 100 }),
        listCustomers(companyId, { limit: 200 }),
        listOrders(companyId, { limit: 200 }),
        listWarehouses(companyId, { limit: 200 }),
      ]);
      setRows(invData);
      setCustomers(custData);
      setOrders(ordData);
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
    setForm({ ...EMPTY, invoice_date: new Date().toISOString().split('T')[0] });
    setFormError('');
    setModalOpen(true);
  }

  function openEdit(row: SalesInvoice) {
    setEditing(row);
    setForm({
      customer_id: row.customer_id,
      invoice_number: row.invoice_number ?? '',
      invoice_date: row.invoice_date ?? '',
      total_amount: row.total_amount ?? 0,
      order_id: row.order_id,
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
        await updateInvoice(editing.id, form);
      } else {
        await createInvoice({ ...form, company_id: companyId });
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
      await deleteInvoice(deleting.id);
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
    { key: 'invoice_number', label: 'رقم الفاتورة' },
    {
      key: 'customer_id',
      label: 'العميل',
      render: (row: SalesInvoice) => {
        const cust = customers.find(c => c.id === row.customer_id);
        return <span>{cust?.name || '-'}</span>;
      }
    },
    { key: 'invoice_date', label: 'التاريخ' },
    { key: 'total_amount', label: 'المبلغ' },
    { key: 'status', label: 'الحالة' },
  ];

  return (
    <AppShell>
      <div className="mx-auto max-w-6xl">
        <PageHeader
          title="الفواتير"
          subtitle={`${rows.length} فاتورة مسجلة`}
          action={<AddButton onClick={openCreate}>إضافة فاتورة</AddButton>}
        />

        <div className="mb-4">
          <SearchBar value={search} onChange={setSearch} placeholder="ابحث برقم الفاتورة أو العميل…" />
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
            emptyMessage="لا يوجد فواتير بعد. أضف فاتورتك الأولى."
          />
        )}
      </div>

      {modalOpen && (
        <Modal
          title={editing ? 'تعديل الفاتورة' : 'إضافة فاتورة جديدة'}
          onClose={() => setModalOpen(false)}
          footer={
            <>
              <CancelButton onClick={() => setModalOpen(false)} />
              <SubmitButton loading={saving}>{editing ? 'حفظ التعديلات' : 'إضافة الفاتورة'}</SubmitButton>
            </>
          }
        >
          <form id="invoice-form" onSubmit={handleSubmit} className="space-y-4">
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
              label="رقم الفاتورة"
              value={form.invoice_number ?? ''}
              onChange={(e) => setForm((p) => ({ ...p, invoice_number: e.target.value }))}
            />
            <Field
              label="تاريخ الفاتورة"
              type="date"
              value={form.invoice_date ?? ''}
              onChange={(e) => setForm((p) => ({ ...p, invoice_date: e.target.value }))}
            />
            <Field
              label="المبلغ الإجمالي"
              type="number"
              value={form.total_amount ?? 0}
              onChange={(e) => setForm((p) => ({ ...p, total_amount: Number(e.target.value) }))}
            />
            <SelectField
              label="الطلب المرتبط"
              value={form.order_id ? String(form.order_id) : ''}
              onChange={(e) => setForm((p) => ({ ...p, order_id: e.target.value ? Number(e.target.value) : null }))}
              options={[
                { value: '', label: 'اختر طلب (اختياري)' },
                ...orders.map(o => ({ value: String(o.id), label: o.order_number || `الطلب ${o.id}` }))
              ]}
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
                { value: 'issued', label: 'مصدرة' },
                { value: 'paid', label: 'مدفوعة' },
                { value: 'cancelled', label: 'ملغاة' },
              ]}
            />
            {formError && <ErrorAlert message={formError} />}
          </form>
        </Modal>
      )}

      {deleting && (
        <DeleteConfirmModal
          name={deleting.invoice_number ?? 'الفاتورة'}
          onConfirm={handleDelete}
          onCancel={() => setDeleting(null)}
          loading={deleteLoading}
        />
      )}
    </AppShell>
  );
}
