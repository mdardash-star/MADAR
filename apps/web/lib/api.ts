const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const TOKEN_KEY = 'madar-access-token';
const COMPANY_KEY = 'madar-company-id';
const USER_KEY = 'madar-user';

// ─── token helpers ────────────────────────────────────────────────────────────

export function saveToken(token: string) {
  if (typeof window === 'undefined') return;
  localStorage.setItem(TOKEN_KEY, token);
}
export function getToken() {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(TOKEN_KEY);
}
export function clearToken() {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(COMPANY_KEY);
  localStorage.removeItem(USER_KEY);
}
export function isAuthenticated() {
  return Boolean(getToken());
}
export function saveUser(user: UserProfile) {
  if (typeof window === 'undefined') return;
  localStorage.setItem(COMPANY_KEY, String(user.company_id));
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}
export function getCompanyId(): number | null {
  if (typeof window === 'undefined') return null;
  const v = localStorage.getItem(COMPANY_KEY);
  return v ? Number(v) : null;
}
export function getUser(): UserProfile | null {
  if (typeof window === 'undefined') return null;
  const v = localStorage.getItem(USER_KEY);
  return v ? (JSON.parse(v) as UserProfile) : null;
}

// ─── types ────────────────────────────────────────────────────────────────────

export interface UserProfile {
  id: number;
  email: string;
  full_name: string;
  company_id: number;
  company_name: string | null;
  role_id: number | null;
  is_active: boolean;
}

// ─── core fetch wrapper ───────────────────────────────────────────────────────

async function request<T>(
  path: string,
  options: RequestInit = {},
  auth = true,
): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> | undefined),
  };
  if (auth) {
    const token = getToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;
  }
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!res.ok) {
    let detail = `HTTP ${res.status}`;
    try {
      const body = await res.json();
      detail = body?.detail ?? detail;
    } catch {}
    throw new Error(String(detail));
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

// ─── auth ─────────────────────────────────────────────────────────────────────

export async function login(email: string, password: string) {
  const tokens = await request<{ access_token: string; refresh_token: string }>(
    '/auth/login',
    { method: 'POST', body: JSON.stringify({ email, password }) },
    false,
  );
  saveToken(tokens.access_token);
  const profile = await request<UserProfile>('/auth/me');
  saveUser(profile);
  return profile;
}

export async function getProfile() {
  return request<UserProfile>('/auth/me');
}

// ─── dashboard ────────────────────────────────────────────────────────────────

export interface DashboardSummary {
  branches: number;
  warehouses: number;
  customers: number;
  suppliers: number;
  products: number;
  quotations: number;
  sales_orders: number;
  sales_invoices: number;
  crm_leads: number;
}

export async function getDashboardSummary(companyId: number) {
  return request<DashboardSummary>(`/api/v1/dashboard/summary?company_id=${companyId}`);
}

// ─── customers ───────────────────────────────────────────────────────────────

export interface Customer {
  id: number;
  company_id: number;
  name: string;
  code: string;
  email: string | null;
  phone: string | null;
  address: string | null;
  is_active: boolean;
}

export async function listCustomers(
  companyId: number,
  params: { skip?: number; limit?: number; search?: string } = {},
) {
  const q = new URLSearchParams({ company_id: String(companyId), ...Object.fromEntries(Object.entries(params).filter(([, v]) => v != null).map(([k, v]) => [k, String(v)])) });
  return request<Customer[]>(`/api/v1/master-data/customers?${q}`);
}

export async function createCustomer(data: Omit<Customer, 'id' | 'is_active'> & { is_active?: boolean }) {
  return request<Customer>('/api/v1/master-data/customers', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updateCustomer(id: number, data: Partial<Omit<Customer, 'id' | 'company_id'>>) {
  return request<Customer>(`/api/v1/master-data/customers/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function deleteCustomer(id: number) {
  return request<{ status: string }>(`/api/v1/master-data/customers/${id}`, { method: 'DELETE' });
}

// ─── suppliers ───────────────────────────────────────────────────────────────

export interface Supplier {
  id: number;
  company_id: number;
  name: string;
  code: string;
  email: string | null;
  phone: string | null;
  address: string | null;
  is_active: boolean;
}

export async function listSuppliers(
  companyId: number,
  params: { skip?: number; limit?: number; search?: string } = {},
) {
  const q = new URLSearchParams({ company_id: String(companyId), ...Object.fromEntries(Object.entries(params).filter(([, v]) => v != null).map(([k, v]) => [k, String(v)])) });
  return request<Supplier[]>(`/api/v1/master-data/suppliers?${q}`);
}

export async function createSupplier(data: Omit<Supplier, 'id' | 'is_active'> & { is_active?: boolean }) {
  return request<Supplier>('/api/v1/master-data/suppliers', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updateSupplier(id: number, data: Partial<Omit<Supplier, 'id' | 'company_id'>>) {
  return request<Supplier>(`/api/v1/master-data/suppliers/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function deleteSupplier(id: number) {
  return request<{ status: string }>(`/api/v1/master-data/suppliers/${id}`, { method: 'DELETE' });
}

// ─── product categories ───────────────────────────────────────────────────────

export interface ProductCategory {
  id: number;
  company_id: number;
  name: string;
  code: string;
}

export async function listProductCategories(companyId: number) {
  return request<ProductCategory[]>(`/api/v1/master-data/product-categories?company_id=${companyId}&limit=200`);
}

export async function createProductCategory(data: { company_id: number; name: string; code: string }) {
  return request<ProductCategory>('/api/v1/master-data/product-categories', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// ─── units of measure ─────────────────────────────────────────────────────────

export interface UnitOfMeasure {
  id: number;
  company_id: number;
  name: string;
  code: string;
  abbreviation: string | null;
}

export async function listUnitsOfMeasure(companyId: number) {
  return request<UnitOfMeasure[]>(`/api/v1/master-data/units-of-measure?company_id=${companyId}&limit=200`);
}

export async function createUnitOfMeasure(data: { company_id: number; name: string; code: string; abbreviation?: string }) {
  return request<UnitOfMeasure>('/api/v1/master-data/units-of-measure', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// ─── products ─────────────────────────────────────────────────────────────────

export interface Product {
  id: number;
  company_id: number;
  name: string;
  sku: string;
  barcode: string | null;
  description: string | null;
  selling_price: number;
  cost_price: number;
  category_id: number | null;
  unit_of_measure_id: number | null;
  is_active: boolean;
}

export async function listProducts(
  companyId: number,
  params: { skip?: number; limit?: number; search?: string } = {},
) {
  const q = new URLSearchParams({ company_id: String(companyId), ...Object.fromEntries(Object.entries(params).filter(([, v]) => v != null).map(([k, v]) => [k, String(v)])) });
  return request<Product[]>(`/api/v1/master-data/products?${q}`);
}

export async function createProduct(data: Omit<Product, 'id' | 'is_active'> & { is_active?: boolean }) {
  return request<Product>('/api/v1/master-data/products', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updateProduct(id: number, data: Partial<Omit<Product, 'id' | 'company_id'>>) {
  return request<Product>(`/api/v1/master-data/products/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function deleteProduct(id: number) {
  return request<{ status: string }>(`/api/v1/master-data/products/${id}`, { method: 'DELETE' });
}

// ─── branches ─────────────────────────────────────────────────────────────────

export interface Branch {
  id: number;
  company_id: number;
  name: string;
  code: string;
  country: string | null;
  city: string | null;
  timezone: string | null;
  is_active: boolean;
}

export async function listBranches(
  companyId: number,
  params: { skip?: number; limit?: number; search?: string } = {},
) {
  const q = new URLSearchParams({ company_id: String(companyId), ...Object.fromEntries(Object.entries(params).filter(([, v]) => v != null).map(([k, v]) => [k, String(v)])) });
  return request<Branch[]>(`/api/v1/master-data/branches?${q}`);
}

export async function createBranch(data: Omit<Branch, 'id' | 'is_active'> & { is_active?: boolean }) {
  return request<Branch>('/api/v1/master-data/branches', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updateBranch(id: number, data: Partial<Omit<Branch, 'id' | 'company_id'>>) {
  return request<Branch>(`/api/v1/master-data/branches/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function deleteBranch(id: number) {
  return request<{ status: string }>(`/api/v1/master-data/branches/${id}`, { method: 'DELETE' });
}

// ─── warehouses ───────────────────────────────────────────────────────────────

export interface Warehouse {
  id: number;
  company_id: number;
  name: string;
  code: string;
  location: string | null;
  branch_id: number | null;
  is_active: boolean;
}

export async function listWarehouses(
  companyId: number,
  params: { skip?: number; limit?: number; search?: string } = {},
) {
  const q = new URLSearchParams({ company_id: String(companyId), ...Object.fromEntries(Object.entries(params).filter(([, v]) => v != null).map(([k, v]) => [k, String(v)])) });
  return request<Warehouse[]>(`/api/v1/master-data/warehouses?${q}`);
}

export async function createWarehouse(data: Omit<Warehouse, 'id' | 'is_active'> & { is_active?: boolean }) {
  return request<Warehouse>('/api/v1/master-data/warehouses', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updateWarehouse(id: number, data: Partial<Omit<Warehouse, 'id' | 'company_id'>>) {
  return request<Warehouse>(`/api/v1/master-data/warehouses/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function deleteWarehouse(id: number) {
  return request<{ status: string }>(`/api/v1/master-data/warehouses/${id}`, { method: 'DELETE' });
}

// ─── sales quotations ─────────────────────────────────────────────────────────

export interface SalesQuotation {
  id: number;
  company_id: number;
  customer_id: number | null;
  quotation_number: string | null;
  quotation_date: string | null;
  expiry_date: string | null;
  total_amount: number | null;
  warehouse_id: number | null;
  status: string | null;
}

export async function listQuotations(
  companyId: number,
  params: { skip?: number; limit?: number; search?: string } = {},
) {
  const q = new URLSearchParams({ company_id: String(companyId), ...Object.fromEntries(Object.entries(params).filter(([, v]) => v != null).map(([k, v]) => [k, String(v)])) });
  return request<SalesQuotation[]>(`/api/v1/sales/quotations?${q}`);
}

export async function createQuotation(data: Omit<SalesQuotation, 'id'> & { items?: Array<{ product_id: number; quantity: number; unit_price: number }> }) {
  return request<SalesQuotation>('/api/v1/sales/quotations', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updateQuotation(id: number, data: Partial<Omit<SalesQuotation, 'id' | 'company_id'>>) {
  return request<SalesQuotation>(`/api/v1/sales/quotations/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function deleteQuotation(id: number) {
  return request<{ status: string }>(`/api/v1/sales/quotations/${id}`, { method: 'DELETE' });
}

// ─── sales orders ─────────────────────────────────────────────────────────────

export interface SalesOrder {
  id: number;
  company_id: number;
  customer_id: number | null;
  order_number: string | null;
  order_date: string | null;
  total_amount: number | null;
  warehouse_id: number | null;
  status: string | null;
}

export async function listOrders(
  companyId: number,
  params: { skip?: number; limit?: number; search?: string } = {},
) {
  const q = new URLSearchParams({ company_id: String(companyId), ...Object.fromEntries(Object.entries(params).filter(([, v]) => v != null).map(([k, v]) => [k, String(v)])) });
  return request<SalesOrder[]>(`/api/v1/sales/orders?${q}`);
}

export async function createOrder(data: Omit<SalesOrder, 'id'> & { items?: Array<{ product_id: number; quantity: number; unit_price: number }> }) {
  return request<SalesOrder>('/api/v1/sales/orders', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updateOrder(id: number, data: Partial<Omit<SalesOrder, 'id' | 'company_id'>>) {
  return request<SalesOrder>(`/api/v1/sales/orders/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function deleteOrder(id: number) {
  return request<{ status: string }>(`/api/v1/sales/orders/${id}`, { method: 'DELETE' });
}

// ─── sales invoices ───────────────────────────────────────────────────────────

export interface SalesInvoice {
  id: number;
  company_id: number;
  customer_id: number | null;
  invoice_number: string | null;
  invoice_date: string | null;
  total_amount: number | null;
  order_id: number | null;
  warehouse_id: number | null;
  status: string | null;
}

export async function listInvoices(
  companyId: number,
  params: { skip?: number; limit?: number; search?: string } = {},
) {
  const q = new URLSearchParams({ company_id: String(companyId), ...Object.fromEntries(Object.entries(params).filter(([, v]) => v != null).map(([k, v]) => [k, String(v)])) });
  return request<SalesInvoice[]>(`/api/v1/sales/invoices?${q}`);
}

export async function createInvoice(data: Omit<SalesInvoice, 'id'> & { items?: Array<{ product_id: number; quantity: number; unit_price: number }> }) {
  return request<SalesInvoice>('/api/v1/sales/invoices', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updateInvoice(id: number, data: Partial<Omit<SalesInvoice, 'id' | 'company_id'>>) {
  return request<SalesInvoice>(`/api/v1/sales/invoices/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function deleteInvoice(id: number) {
  return request<{ status: string }>(`/api/v1/sales/invoices/${id}`, { method: 'DELETE' });
}
