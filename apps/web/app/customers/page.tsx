'use client';

import { FormEvent, useCallback, useEffect, useMemo, useState } from 'react';
import { AppShell } from '@/components/layout/AppShell';
import { Modal } from '@/components/ui/Modal';
import {
  AddButton,
  CancelButton,
  ErrorAlert,
  Field,
  PageHeader,
  SearchBar,
  SelectField,
} from '@/components/ui/Form';
import { getUser } from '@/lib/api';
import {
  archiveCustomer,
  createCustomer,
  createCustomerAddress,
  createCustomerContact,
  deleteCustomerAddress,
  deleteCustomerContact,
  getCustomer,
  listCustomers,
  restoreCustomer,
  updateCustomer,
  type Customer,
  type CustomerPayload,
} from '@/lib/customers';

const PAGE_SIZE = 20;

const EMPTY_FORM: Omit<CustomerPayload, 'company_id'> = {
  name: '',
  code: '',
  customer_type: 'company',
  tax_number: '',
  email: '',
  phone: '',
  address: '',
  branch_id: null,
  customer_group_id: null,
  sales_owner_id: null,
  credit_limit: 0,
  payment_terms_days: 0,
  notes: '',
  is_active: true,
};

function numberOrNull(value: string) {
  if (!value.trim()) return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

export default function CustomersPage() {
  const [rows, setRows] = useState<Customer[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(0);
  const [search, setSearch] = useState('');
  const [customerType, setCustomerType] = useState('');
  const [activeFilter, setActiveFilter] = useState('');
  const [includeArchived, setIncludeArchived] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState<Customer | null>(null);
  const [form, setForm] = useState(EMPTY_FORM);
  const [formError, setFormError] = useState('');
  const [saving, setSaving] = useState(false);

  const [details, setDetails] = useState<Customer | null>(null);
  const [detailsLoading, setDetailsLoading] = useState(false);
  const [contactName, setContactName] = useState('');
  const [contactEmail, setContactEmail] = useState('');
  const [contactPhone, setContactPhone] = useState('');
  const [addressLabel, setAddressLabel] = useState('');
  const [addressType, setAddressType] = useState<'billing' | 'shipping' | 'other'>('other');
  const [addressStreet, setAddressStreet] = useState('');
  const [addressCity, setAddressCity] = useState('');

  const companyId = typeof window !== 'undefined' ? getUser()?.company_id : undefined;
  const pageCount = Math.max(1, Math.ceil(total / PAGE_SIZE));

  const load = useCallback(async () => {
    if (!companyId) return;
    setLoading(true);
    try {
      const data = await listCustomers(companyId, {
        skip: page * PAGE_SIZE,
        limit: PAGE_SIZE,
        search: search || undefined,
        customer_type: customerType || undefined,
        is_active: activeFilter === '' ? undefined : activeFilter === 'active',
        include_archived: includeArchived,
      });
      setRows(data.items);
      setTotal(data.total);
      setError('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'فشل تحميل العملاء');
    } finally {
      setLoading(false);
    }
  }, [activeFilter, companyId, customerType, includeArchived, page, search]);

  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    setPage(0);
  }, [search, customerType, activeFilter, includeArchived]);

  const subtitle = useMemo(() => `${total} عميل`, [total]);

  function openCreate() {
    setEditing(null);
    setForm(EMPTY_FORM);
    setFormError('');
    setFormOpen(true);
  }

  function openEdit(customer: Customer) {
    setEditing(customer);
    setForm({
      name: customer.name,
      code: customer.code,
      customer_type: customer.customer_type,
      tax_number: customer.tax_number ?? '',
      email: customer.email ?? '',
      phone: customer.phone ?? '',
      address: customer.address ?? '',
      branch_id: customer.branch_id,
      customer_group_id: customer.customer_group_id,
      sales_owner_id: customer.sales_owner_id,
      credit_limit: customer.credit_limit,
      payment_terms_days: customer.payment_terms_days,
      notes: customer.notes ?? '',
      is_active: customer.is_active,
    });
    setFormError('');
    setFormOpen(true);
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!companyId) return;
    if (!form.name.trim() || !form.code.trim()) {
      setFormError('اسم العميل والرمز حقول مطلوبة.');
      return;
    }
    if (form.credit_limit < 0 || form.payment_terms_days < 0) {
      setFormError('حد الائتمان وشروط الدفع لا يمكن أن تكون سالبة.');
      return;
    }
    setSaving(true);
    setFormError('');
    try {
      if (editing) {
        await updateCustomer(editing.id, form);
        setSuccess('تم تحديث بيانات العميل بنجاح.');
      } else {
        await createCustomer({ ...form, company_id: companyId });
        setSuccess('تم إنشاء العميل بنجاح.');
      }
      setFormOpen(false);
      await load();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'فشل حفظ بيانات العميل');
    } finally {
      setSaving(false);
    }
  }

  async function openDetails(customer: Customer) {
    setDetailsLoading(true);
    try {
      setDetails(await getCustomer(customer.id, Boolean(customer.is_deleted)));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'فشل تحميل تفاصيل العميل');
    } finally {
      setDetailsLoading(false);
    }
  }

  async function refreshDetails() {
    if (!details) return;
    setDetails(await getCustomer(details.id, Boolean(details.is_deleted)));
  }

  async function handleArchive(customer: Customer) {
    if (!window.confirm(`أرشفة العميل ${customer.name}؟`)) return;
    try {
      await archiveCustomer(customer.id);
      setSuccess('تمت أرشفة العميل.');
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'فشل أرشفة العميل');
    }
  }

  async function handleRestore(customer: Customer) {
    try {
      await restoreCustomer(customer.id);
      setSuccess('تمت استعادة العميل.');
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'فشل استعادة العميل');
    }
  }

  async function addContact(event: FormEvent) {
    event.preventDefault();
    if (!details || !contactName.trim()) return;
    try {
      await createCustomerContact(details.id, {
        full_name: contactName.trim(),
        position: null,
        email: contactEmail || null,
        phone: contactPhone || null,
        is_primary: (details.contacts?.length ?? 0) === 0,
        is_active: true,
      });
      setContactName('');
      setContactEmail('');
      setContactPhone('');
      await refreshDetails();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'فشل إضافة جهة الاتصال');
    }
  }

  async function removeContact(contactId: number) {
    if (!details) return;
    try {
      await deleteCustomerContact(details.id, contactId);
      await refreshDetails();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'فشل حذف جهة الاتصال');
    }
  }

  async function addAddress(event: FormEvent) {
    event.preventDefault();
    if (!details || !addressLabel.trim()) return;
    try {
      await createCustomerAddress(details.id, {
        label: addressLabel.trim(),
        address_type: addressType,
        street: addressStreet || null,
        city: addressCity || null,
        country: null,
        postal_code: null,
        is_primary: (details.addresses?.length ?? 0) === 0,
        is_active: true,
      });
      setAddressLabel('');
      setAddressStreet('');
      setAddressCity('');
      setAddressType('other');
      await refreshDetails();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'فشل إضافة العنوان');
    }
  }

  async function removeAddress(addressId: number) {
    if (!details) return;
    try {
      await deleteCustomerAddress(details.id, addressId);
      await refreshDetails();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'فشل حذف العنوان');
    }
  }

  return (
    <AppShell>
      <div className="mx-auto max-w-7xl">
        <PageHeader title="العملاء" subtitle={subtitle} action={<AddButton onClick={openCreate}>إضافة عميل</AddButton>} />

        <div className="mb-5 grid gap-3 rounded-2xl border border-white/10 bg-slate-900/60 p-4 md:grid-cols-4">
          <SearchBar value={search} onChange={setSearch} placeholder="بحث بالاسم أو الرمز أو الرقم الضريبي…" />
          <select value={customerType} onChange={(e) => setCustomerType(e.target.value)} className="rounded-xl border border-white/10 bg-slate-800 px-3 py-2.5 text-sm">
            <option value="">كل الأنواع</option>
            <option value="company">شركة</option>
            <option value="individual">فرد</option>
          </select>
          <select value={activeFilter} onChange={(e) => setActiveFilter(e.target.value)} className="rounded-xl border border-white/10 bg-slate-800 px-3 py-2.5 text-sm">
            <option value="">كل الحالات</option>
            <option value="active">نشط</option>
            <option value="inactive">غير نشط</option>
          </select>
          <label className="flex items-center gap-2 rounded-xl border border-white/10 bg-slate-800 px-3 py-2.5 text-sm">
            <input type="checkbox" checked={includeArchived} onChange={(e) => setIncludeArchived(e.target.checked)} />
            إظهار المؤرشف
          </label>
        </div>

        {success && <div className="mb-4 rounded-xl bg-emerald-500/15 px-4 py-3 text-sm text-emerald-300">{success}</div>}
        {error && <div className="mb-4"><ErrorAlert message={error} /></div>}

        <div className="overflow-hidden rounded-2xl border border-white/10 bg-slate-900/60">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-white/5 text-slate-300">
                <tr>
                  <th className="px-4 py-3 text-right">العميل</th>
                  <th className="px-4 py-3 text-right">الرمز</th>
                  <th className="px-4 py-3 text-right">النوع</th>
                  <th className="px-4 py-3 text-right">الهاتف</th>
                  <th className="px-4 py-3 text-right">حد الائتمان</th>
                  <th className="px-4 py-3 text-right">الحالة</th>
                  <th className="px-4 py-3 text-right">الإجراءات</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr><td colSpan={7} className="px-4 py-16 text-center text-slate-400">جاري التحميل…</td></tr>
                ) : rows.length === 0 ? (
                  <tr><td colSpan={7} className="px-4 py-16 text-center text-slate-400">لا توجد نتائج.</td></tr>
                ) : rows.map((customer) => (
                  <tr key={customer.id} className="border-t border-white/5 hover:bg-white/[0.03]">
                    <td className="px-4 py-3 font-medium text-white">{customer.name}</td>
                    <td className="px-4 py-3 text-slate-300">{customer.code}</td>
                    <td className="px-4 py-3 text-slate-300">{customer.customer_type === 'company' ? 'شركة' : 'فرد'}</td>
                    <td className="px-4 py-3 text-slate-300">{customer.phone || '—'}</td>
                    <td className="px-4 py-3 text-slate-300">{customer.credit_limit.toLocaleString('ar-SA')}</td>
                    <td className="px-4 py-3">
                      {customer.is_deleted ? (
                        <span className="rounded-full bg-amber-500/15 px-2 py-1 text-xs text-amber-300">مؤرشف</span>
                      ) : customer.is_active ? (
                        <span className="rounded-full bg-emerald-500/15 px-2 py-1 text-xs text-emerald-300">نشط</span>
                      ) : (
                        <span className="rounded-full bg-slate-500/15 px-2 py-1 text-xs text-slate-300">غير نشط</span>
                      )}
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex flex-wrap gap-2">
                        <button onClick={() => void openDetails(customer)} className="rounded-lg border border-white/10 px-2.5 py-1.5 text-xs hover:bg-white/5">تفاصيل</button>
                        {!customer.is_deleted && <button onClick={() => openEdit(customer)} className="rounded-lg border border-white/10 px-2.5 py-1.5 text-xs hover:bg-white/5">تعديل</button>}
                        {customer.is_deleted ? (
                          <button onClick={() => void handleRestore(customer)} className="rounded-lg bg-emerald-500/15 px-2.5 py-1.5 text-xs text-emerald-300">استعادة</button>
                        ) : (
                          <button onClick={() => void handleArchive(customer)} className="rounded-lg bg-amber-500/15 px-2.5 py-1.5 text-xs text-amber-300">أرشفة</button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="flex items-center justify-between border-t border-white/10 px-4 py-3 text-sm text-slate-400">
            <span>صفحة {page + 1} من {pageCount}</span>
            <div className="flex gap-2">
              <button disabled={page === 0} onClick={() => setPage((p) => Math.max(0, p - 1))} className="rounded-lg border border-white/10 px-3 py-1.5 disabled:opacity-40">السابق</button>
              <button disabled={page + 1 >= pageCount} onClick={() => setPage((p) => p + 1)} className="rounded-lg border border-white/10 px-3 py-1.5 disabled:opacity-40">التالي</button>
            </div>
          </div>
        </div>
      </div>

      {formOpen && (
        <Modal title={editing ? 'تعديل بيانات العميل' : 'إضافة عميل'} onClose={() => setFormOpen(false)}>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <Field label="اسم العميل *" required value={form.name} onChange={(e) => setForm((p) => ({ ...p, name: e.target.value }))} />
              <Field label="رمز العميل *" required value={form.code} onChange={(e) => setForm((p) => ({ ...p, code: e.target.value }))} />
              <SelectField label="نوع العميل" value={form.customer_type} onChange={(e) => setForm((p) => ({ ...p, customer_type: e.target.value as 'company' | 'individual' }))} options={[{ value: 'company', label: 'شركة' }, { value: 'individual', label: 'فرد' }]} />
              <Field label="الرقم الضريبي" value={form.tax_number ?? ''} onChange={(e) => setForm((p) => ({ ...p, tax_number: e.target.value }))} />
              <Field label="البريد الإلكتروني" type="email" value={form.email ?? ''} onChange={(e) => setForm((p) => ({ ...p, email: e.target.value }))} />
              <Field label="رقم الهاتف" value={form.phone ?? ''} onChange={(e) => setForm((p) => ({ ...p, phone: e.target.value }))} />
              <Field label="العنوان المختصر" value={form.address ?? ''} onChange={(e) => setForm((p) => ({ ...p, address: e.target.value }))} />
              <Field label="حد الائتمان" type="number" min="0" step="0.01" value={form.credit_limit} onChange={(e) => setForm((p) => ({ ...p, credit_limit: Number(e.target.value) }))} />
              <Field label="شروط الدفع بالأيام" type="number" min="0" value={form.payment_terms_days} onChange={(e) => setForm((p) => ({ ...p, payment_terms_days: Number(e.target.value) }))} />
              <Field label="معرف الفرع" type="number" value={form.branch_id ?? ''} onChange={(e) => setForm((p) => ({ ...p, branch_id: numberOrNull(e.target.value) }))} />
              <Field label="معرف مجموعة العملاء" type="number" value={form.customer_group_id ?? ''} onChange={(e) => setForm((p) => ({ ...p, customer_group_id: numberOrNull(e.target.value) }))} />
              <Field label="معرف مسؤول المبيعات" type="number" value={form.sales_owner_id ?? ''} onChange={(e) => setForm((p) => ({ ...p, sales_owner_id: numberOrNull(e.target.value) }))} />
            </div>
            <Field label="ملاحظات" value={form.notes ?? ''} onChange={(e) => setForm((p) => ({ ...p, notes: e.target.value }))} />
            <label className="flex items-center gap-2 text-sm text-slate-300"><input type="checkbox" checked={form.is_active} onChange={(e) => setForm((p) => ({ ...p, is_active: e.target.checked }))} />عميل نشط</label>
            {formError && <ErrorAlert message={formError} />}
            <div className="flex justify-end gap-3 pt-2">
              <CancelButton onClick={() => setFormOpen(false)} />
              <button type="submit" disabled={saving} className="rounded-xl bg-cyan-500 px-5 py-2.5 text-sm font-semibold text-slate-950 disabled:opacity-60">{saving ? 'جاري الحفظ…' : editing ? 'حفظ التعديلات' : 'إضافة العميل'}</button>
            </div>
          </form>
        </Modal>
      )}

      {(details || detailsLoading) && (
        <Modal title="تفاصيل العميل" onClose={() => setDetails(null)}>
          {detailsLoading && !details ? <div className="py-10 text-center text-slate-400">جاري التحميل…</div> : details && (
            <div className="space-y-6">
              <div className="rounded-xl border border-white/10 bg-white/[0.03] p-4 text-sm">
                <div className="grid gap-2 md:grid-cols-2">
                  <div><span className="text-slate-400">الاسم:</span> {details.name}</div>
                  <div><span className="text-slate-400">الرمز:</span> {details.code}</div>
                  <div><span className="text-slate-400">الرقم الضريبي:</span> {details.tax_number || '—'}</div>
                  <div><span className="text-slate-400">البريد:</span> {details.email || '—'}</div>
                  <div><span className="text-slate-400">الهاتف:</span> {details.phone || '—'}</div>
                  <div><span className="text-slate-400">شروط الدفع:</span> {details.payment_terms_days} يوم</div>
                </div>
              </div>

              <section>
                <h3 className="mb-3 font-semibold text-white">جهات الاتصال</h3>
                <div className="space-y-2">
                  {(details.contacts ?? []).map((contact) => (
                    <div key={contact.id} className="flex items-center justify-between rounded-lg border border-white/10 p-3 text-sm">
                      <div><div className="font-medium">{contact.full_name}{contact.is_primary ? ' · أساسي' : ''}</div><div className="text-slate-400">{contact.email || contact.phone || 'بدون بيانات اتصال'}</div></div>
                      <button onClick={() => void removeContact(contact.id)} className="text-xs text-red-300">حذف</button>
                    </div>
                  ))}
                </div>
                {!details.is_deleted && <form onSubmit={addContact} className="mt-3 grid gap-2 md:grid-cols-3"><Field label="اسم جهة الاتصال" value={contactName} onChange={(e) => setContactName(e.target.value)} required /><Field label="البريد" type="email" value={contactEmail} onChange={(e) => setContactEmail(e.target.value)} /><Field label="الهاتف" value={contactPhone} onChange={(e) => setContactPhone(e.target.value)} /><button type="submit" className="rounded-lg bg-cyan-500/15 px-3 py-2 text-sm text-cyan-300 md:col-span-3">إضافة جهة اتصال</button></form>}
              </section>

              <section>
                <h3 className="mb-3 font-semibold text-white">العناوين</h3>
                <div className="space-y-2">
                  {(details.addresses ?? []).map((address) => (
                    <div key={address.id} className="flex items-center justify-between rounded-lg border border-white/10 p-3 text-sm">
                      <div><div className="font-medium">{address.label}{address.is_primary ? ' · أساسي' : ''}</div><div className="text-slate-400">{address.address_type} · {[address.street, address.city].filter(Boolean).join('، ') || 'بدون تفاصيل'}</div></div>
                      <button onClick={() => void removeAddress(address.id)} className="text-xs text-red-300">حذف</button>
                    </div>
                  ))}
                </div>
                {!details.is_deleted && <form onSubmit={addAddress} className="mt-3 grid gap-2 md:grid-cols-2"><Field label="اسم العنوان" value={addressLabel} onChange={(e) => setAddressLabel(e.target.value)} required /><SelectField label="نوع العنوان" value={addressType} onChange={(e) => setAddressType(e.target.value as 'billing' | 'shipping' | 'other')} options={[{ value: 'billing', label: 'فوترة' }, { value: 'shipping', label: 'شحن' }, { value: 'other', label: 'أخرى' }]} /><Field label="الشارع" value={addressStreet} onChange={(e) => setAddressStreet(e.target.value)} /><Field label="المدينة" value={addressCity} onChange={(e) => setAddressCity(e.target.value)} /><button type="submit" className="rounded-lg bg-cyan-500/15 px-3 py-2 text-sm text-cyan-300 md:col-span-2">إضافة عنوان</button></form>}
              </section>
            </div>
          )}
        </Modal>
      )}
    </AppShell>
  );
}
