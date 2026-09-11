import { getToken } from './api';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> | undefined),
  };
  if (token) headers.Authorization = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!res.ok) {
    let detail = `HTTP ${res.status}`;
    try {
      const body = await res.json();
      detail = typeof body?.detail === 'string' ? body.detail : detail;
    } catch {}
    throw new Error(detail);
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export interface CustomerContact {
  id: number;
  company_id: number;
  customer_id: number;
  full_name: string;
  position: string | null;
  email: string | null;
  phone: string | null;
  is_primary: boolean;
  is_active: boolean;
}

export interface CustomerAddress {
  id: number;
  company_id: number;
  customer_id: number;
  label: string;
  address_type: 'billing' | 'shipping' | 'other';
  street: string | null;
  city: string | null;
  country: string | null;
  postal_code: string | null;
  is_primary: boolean;
  is_active: boolean;
}

export interface Customer {
  id: number;
  company_id: number;
  branch_id: number | null;
  customer_group_id: number | null;
  sales_owner_id: number | null;
  name: string;
  code: string;
  customer_type: 'company' | 'individual';
  tax_number: string | null;
  email: string | null;
  phone: string | null;
  address: string | null;
  credit_limit: number;
  payment_terms_days: number;
  notes: string | null;
  is_active: boolean;
  is_deleted?: boolean;
  contacts?: CustomerContact[];
  addresses?: CustomerAddress[];
}

export interface CustomerPayload {
  company_id: number;
  name: string;
  code: string;
  customer_type: 'company' | 'individual';
  tax_number?: string | null;
  email?: string | null;
  phone?: string | null;
  address?: string | null;
  branch_id?: number | null;
  customer_group_id?: number | null;
  sales_owner_id?: number | null;
  credit_limit: number;
  payment_terms_days: number;
  notes?: string | null;
  is_active: boolean;
}

export interface CustomerListResponse {
  items: Customer[];
  total: number;
  skip: number;
  limit: number;
}

export async function listCustomers(
  companyId: number,
  params: {
    skip?: number;
    limit?: number;
    search?: string;
    customer_type?: string;
    is_active?: boolean;
    include_archived?: boolean;
  } = {},
) {
  const values: Record<string, string> = {
    company_id: String(companyId),
    with_meta: 'true',
  };
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') values[key] = String(value);
  });
  return request<CustomerListResponse>(`/api/v1/master-data/customers?${new URLSearchParams(values)}`);
}

export function getCustomer(id: number, includeArchived = false) {
  return request<Customer>(`/api/v1/master-data/customers/${id}?include_archived=${includeArchived}`);
}

export function createCustomer(payload: CustomerPayload) {
  return request<Customer>('/api/v1/master-data/customers', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function updateCustomer(id: number, payload: Partial<Omit<CustomerPayload, 'company_id'>>) {
  return request<Customer>(`/api/v1/master-data/customers/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  });
}

export function archiveCustomer(id: number) {
  return request<{ status: string; id: string }>(`/api/v1/master-data/customers/${id}`, { method: 'DELETE' });
}

export function restoreCustomer(id: number) {
  return request<Customer>(`/api/v1/master-data/customers/${id}/restore`, { method: 'POST' });
}

export function createCustomerContact(customerId: number, payload: Omit<CustomerContact, 'id' | 'company_id' | 'customer_id'>) {
  return request<CustomerContact>(`/api/v1/master-data/customers/${customerId}/contacts`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function updateCustomerContact(customerId: number, contactId: number, payload: Partial<Omit<CustomerContact, 'id' | 'company_id' | 'customer_id'>>) {
  return request<CustomerContact>(`/api/v1/master-data/customers/${customerId}/contacts/${contactId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  });
}

export function deleteCustomerContact(customerId: number, contactId: number) {
  return request<{ status: string }>(`/api/v1/master-data/customers/${customerId}/contacts/${contactId}`, { method: 'DELETE' });
}

export function createCustomerAddress(customerId: number, payload: Omit<CustomerAddress, 'id' | 'company_id' | 'customer_id'>) {
  return request<CustomerAddress>(`/api/v1/master-data/customers/${customerId}/addresses`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function updateCustomerAddress(customerId: number, addressId: number, payload: Partial<Omit<CustomerAddress, 'id' | 'company_id' | 'customer_id'>>) {
  return request<CustomerAddress>(`/api/v1/master-data/customers/${customerId}/addresses/${addressId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  });
}

export function deleteCustomerAddress(customerId: number, addressId: number) {
  return request<{ status: string }>(`/api/v1/master-data/customers/${customerId}/addresses/${addressId}`, { method: 'DELETE' });
}
