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
  listOrders,
  createOrder,
  updateOrder,
  deleteOrder,
  listCustomers,
  listWarehouses,
  getUser,
  type SalesOrder,
  type Customer,
  type Warehouse,
} from '@/lib/api';

const EMPTY: Omit<SalesOrder, 'id' | 'company_id'> = {
  customer_id: null,
  warehouse_id: null,
  code: '',
  order_date: new Date().toISOString().split('T')[0],
  subtotal_amount: 0,
  tax_amount: 0,
  discount_amount: 0,
  total_amount: 0,
  status: 'draft',
  payment_status: 'pending',
  note: '',
};

export default function OrdersPage() {
  const [rows, setRows] = useState<SalesOrder[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [warehouses, setWarehouses] = useState<Warehouse[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<SalesOrder | null>(null);
  const [form, setForm] = useState(EMPTY);
  const [formError, setFormError] = useState('');
  const [saving, setSaving] = useState(false);

  const [deleting, setDeleting] = useState<SalesOrder | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  const companyId = typeof window !== 'undefined' ? getUser()?.company_id : undefined;

  const load = useCallback(async () => {
    if (!companyId) return;
    setLoading(true);
    try {
      const [ordData, custData, wareData] = await Promise.all([
        listOrders(companyId, { search: search || undefined, limit: 100 }),
        listCustomers(companyId, { limit: 200 }),
        listWarehouses(companyId, { limit: 200 }),
      ]);
      setRows(ordData);
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
    setForm({ ...EMPTY, order_date: new Date().toISOString().split('T')[0] });
    setFormError('');
    setModalOpen(true);
  }

  function openEdit(row: SalesOrder) {
    setEditing(row);
    setForm({
      customer_id: row.customer_id,
      warehouse_id: row.warehouse_id,
      code: row.code ?? '',
      order_date: row.order_date ?? '',
      subtotal_amount: row.subtotal_amount ?? 0,
      tax_amount: row.tax_amount ?? 0,
      discount_amount: row.discount_amount ?? 0,
      total_amount: row.total_amount ?? 0,
      status: row.status ?? 'draft',
      payment_status: row.payment_status ?? 'pending',
      note: row.note ?? '',
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
        await updateOrder(editing.id, form);
      } else {
        await createOrder({ ...form, company_id: companyId });
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
      await deleteOrder(deleting.id);
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
    { key: 'code', label: 'رقم الطلب' },
    {
      key: 'customer_id',
      label: 'العميل',
      render: (row: SalesOrder) => {
        const cust = customers.find(c => c.id === row.customer_id);
        return <span>{cust?.name || '-'}</span>;
      }
    },
    { key: 'order_date', label: 'التاريخ' },
    { key: 'total_amount', label: 'المبلغ' },
    { key: 'status', label: 'الحالة' },
  ];

  return (
    <AppShell>
      <div className="mx-auto max-w-6xl">
        <PageHeader
          title="أوامر البيع"
          subtitle={`${rows.length} طلب مسجل`}
          action={<AddButton onClick={openCreate}>إضافة طلب</AddButton>}
        />

        <div className="mb-4">
          <SearchBar value={search} onChange={setSearch} placeholder="ابحث برقم الطلب أو العميل…" />
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
            emptyMessage="لا يوجد طلبات بعد. أضف طلبك الأول."
          />
        )}
      </div>

      {modalOpen && (
        <Modal
          title={editing ? 'تعديل الطلب' : 'إضافة طلب بيع جديد'}
          onClose={() => setModalOpen(false)}
          footer={
            <>
              <CancelButton onClick={() => setModalOpen(false)} />
              <SubmitButton loading={saving}>{editing ? 'حفظ التعديلات' : 'إضافة الطلب'}</SubmitButton>
            </>
          }
        >
          <form id="order-form" onSubmit={handleSubmit} className="space-y-4">
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
              label="رقم الطلب"
              value={form.code ?? ''}
              onChange={(e) => setForm((p) => ({ ...p, code: e.target.value }))}
            />
            <Field
              label="تاريخ الطلب"
              type="date"
              value={form.order_date ?? ''}
              onChange={(e) => setForm((p) => ({ ...p, order_date: e.target.value }))}
            />
            <Field
              label="المبلغ الفرعي"
              type="number"
              value={form.subtotal_amount ?? 0}
              onChange={(e) => setForm((p) => ({ ...p, subtotal_amount: Number(e.target.value) }))}
            />
            <Field
              label="الضريبة"
              type="number"
              value={form.tax_amount ?? 0}
              onChange={(e) => setForm((p) => ({ ...p, tax_amount: Number(e.target.value) }))}
            />
            <Field
              label="الخصم"
              type="number"
              value={form.discount_amount ?? 0}
              onChange={(e) => setForm((p) => ({ ...p, discount_amount: Number(e.target.value) }))}
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
                { value: 'confirmed', label: 'مؤكد' },
                { value: 'processing', label: 'قيد المعالجة' },
                { value: 'shipped', label: 'مشحون' },
                { value: 'delivered', label: 'مسلم' },
              ]}
            />
            <SelectField
              label="حالة الدفع"
              value={form.payment_status ?? 'pending'}
              onChange={(e) => setForm((p) => ({ ...p, payment_status: e.target.value }))}
              options={[
                { value: 'pending', label: 'معلق' },
                { value: 'partial', label: 'جزئي' },
                { value: 'paid', label: 'مدفوع' },
              ]}
            />
            <Field
              label="ملاحظة"
              value={form.note ?? ''}
              onChange={(e) => setForm((p) => ({ ...p, note: e.target.value }))}
            />
            {formError && <ErrorAlert message={formError} />}
          </form>
        </Modal>
      )}

      {deleting && (
        <DeleteConfirmModal
          name={deleting.code ?? 'الطلب'}
          onConfirm={handleDelete}
          onCancel={() => setDeleting(null)}
          loading={deleteLoading}
        />
      )}
    </AppShell>
  );
}
