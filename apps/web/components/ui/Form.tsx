'use client';

interface FieldProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

export function Field({ label, error, id, ...props }: FieldProps) {
  const inputId = id ?? label;
  return (
    <label className="block" htmlFor={inputId}>
      <span className="mb-1.5 block text-sm font-medium text-slate-300">{label}</span>
      <input
        id={inputId}
        className={`w-full rounded-xl border bg-slate-800 px-4 py-2.5 text-sm outline-none transition focus:ring-2 ${
          error
            ? 'border-red-500 focus:ring-red-500/30'
            : 'border-white/10 focus:border-cyan-500 focus:ring-cyan-500/20'
        }`}
        {...props}
      />
      {error && <p className="mt-1 text-xs text-red-400">{error}</p>}
    </label>
  );
}

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label: string;
  error?: string;
  options: { value: string | number; label: string }[];
  placeholder?: string;
}

export function SelectField({ label, error, id, options, placeholder, ...props }: SelectProps) {
  const inputId = id ?? label;
  return (
    <label className="block" htmlFor={inputId}>
      <span className="mb-1.5 block text-sm font-medium text-slate-300">{label}</span>
      <select
        id={inputId}
        className={`w-full rounded-xl border bg-slate-800 px-4 py-2.5 text-sm outline-none transition focus:ring-2 ${
          error
            ? 'border-red-500 focus:ring-red-500/30'
            : 'border-white/10 focus:border-cyan-500 focus:ring-cyan-500/20'
        }`}
        {...props}
      >
        {placeholder && <option value="">{placeholder}</option>}
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      {error && <p className="mt-1 text-xs text-red-400">{error}</p>}
    </label>
  );
}

export function SubmitButton({
  loading,
  children,
}: {
  loading?: boolean;
  children: React.ReactNode;
}) {
  return (
    <button
      type="submit"
      disabled={loading}
      className="rounded-xl bg-cyan-500 px-5 py-2.5 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:opacity-60"
    >
      {loading ? 'جاري الحفظ…' : children}
    </button>
  );
}

export function CancelButton({ onClick }: { onClick: () => void }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="rounded-xl border border-white/10 px-5 py-2.5 text-sm text-slate-300 transition hover:bg-white/5"
    >
      إلغاء
    </button>
  );
}

export function ErrorAlert({ message }: { message: string }) {
  return (
    <div className="rounded-xl bg-red-500/15 px-4 py-3 text-sm text-red-300">
      {message}
    </div>
  );
}

export function PageHeader({
  title,
  subtitle,
  action,
}: {
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="mb-6 flex items-start justify-between gap-4">
      <div>
        <h1 className="text-2xl font-bold text-white">{title}</h1>
        {subtitle && <p className="mt-1 text-sm text-slate-400">{subtitle}</p>}
      </div>
      {action}
    </div>
  );
}

export function SearchBar({
  value,
  onChange,
  placeholder = 'بحث…',
}: {
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
}) {
  return (
    <input
      type="search"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      className="w-full max-w-xs rounded-xl border border-white/10 bg-slate-800 px-4 py-2.5 text-sm outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
    />
  );
}

export function AddButton({
  onClick,
  children,
}: {
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      className="flex items-center gap-2 rounded-xl bg-cyan-500 px-4 py-2.5 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400"
    >
      <span className="text-base leading-none">+</span>
      {children}
    </button>
  );
}

export function DeleteConfirmModal({
  name,
  onConfirm,
  onCancel,
  loading,
}: {
  name: string;
  onConfirm: () => void;
  onCancel: () => void;
  loading?: boolean;
}) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
      <div className="w-full max-w-sm rounded-2xl border border-white/10 bg-slate-900 p-6 shadow-2xl">
        <h2 className="text-lg font-semibold text-white">تأكيد الحذف</h2>
        <p className="mt-2 text-sm text-slate-300">
          هل أنت متأكد من حذف <span className="font-semibold text-white">{name}</span>؟ لا يمكن التراجع عن هذه العملية.
        </p>
        <div className="mt-5 flex justify-end gap-3">
          <CancelButton onClick={onCancel} />
          <button
            onClick={onConfirm}
            disabled={loading}
            className="rounded-xl bg-red-500 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-red-400 disabled:opacity-60"
          >
            {loading ? 'جاري الحذف…' : 'تأكيد الحذف'}
          </button>
        </div>
      </div>
    </div>
  );
}
