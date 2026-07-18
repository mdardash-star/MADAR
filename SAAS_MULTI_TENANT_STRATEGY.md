# MADAR — SaaS Multi-Tenant Strategy

**Version**: 1.0  
**Date**: 2026-07-18  
**Status**: Active  
**Owner**: CTO / Product Manager  

---

## 1. Multi-Tenancy Model

MADAR uses **shared-infrastructure, application-level isolation** (pooled multi-tenancy):

```
┌─────────────────────────────────────────────────────────────┐
│                    MADAR Platform                           │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Tenant A    │  │  Tenant B    │  │  Tenant C    │     │
│  │  (company 1) │  │  (company 2) │  │  (company 3) │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         └─────────────────┴─────────────────┘             │
│                            │                               │
│                   ┌────────▼────────┐                      │
│                   │ Shared Database │                      │
│                   │ (company_id     │                      │
│                   │  row-level      │                      │
│                   │  isolation)     │                      │
│                   └─────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

### Isolation Levels Compared

| Model | Isolation | Cost | Complexity | MADAR Choice |
|-------|-----------|------|------------|--------------|
| Separate DB per tenant | Highest | High | High | Enterprise tier only |
| Separate schema per tenant | High | Medium | Medium | Future option |
| Shared DB, `company_id` filter | Medium | Low | Low | ✅ **Current** |
| Shared DB, PostgreSQL RLS | High | Low | Medium | Phase 2 upgrade |

---

## 2. Tenant Lifecycle

```
Registration
     │
     ▼ POST /companies/register
Company created (status: trial)
     │
     ▼ SeedService.seed_initial_permissions()
Roles + Permissions bootstrapped
     │
     ▼ Admin user created
     │
     ▼ 14-day trial starts
     │
     ├── [Upgrade] → status: active (paid)
     │
     ├── [Trial expires] → status: trial_expired
     │       └── Data frozen, login redirected to upgrade page
     │
     ├── [Cancellation] → status: cancelled
     │       └── Data retained 90 days
     │       └── Day 90: data anonymized / deleted
     │
     └── [Reactivation] → status: active
```

### Company Status State Machine

```python
class CompanyStatus(str, Enum):
    TRIAL         = "trial"         # 14-day trial
    ACTIVE        = "active"        # Paid, in good standing
    TRIAL_EXPIRED = "trial_expired" # Trial ended, no payment
    SUSPENDED     = "suspended"     # Payment failed (grace period)
    CANCELLED     = "cancelled"     # Voluntarily cancelled
    CHURNED       = "churned"       # Permanently deactivated
```

---

## 3. Data Isolation Enforcement

### Current Implementation (Application-layer)

```python
# Every query includes company_id filter
# enforced in service layer:

class MasterDataService:
    @staticmethod
    def list_customers(db: Session, company_id: int):
        return db.query(Customer).filter(
            Customer.company_id == company_id,
            Customer.is_deleted == False
        ).all()
```

### Phase 2: PostgreSQL Row Level Security (RLS)

```sql
-- Upgrade path: add RLS as additional safety net
-- Does NOT replace application-layer filtering

-- Enable RLS
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;

-- Policy: users can only see their company's rows
CREATE POLICY tenant_isolation ON customers
    USING (company_id = current_setting('app.current_company_id', true)::int);

-- Set context on each request
SET app.current_company_id = '42';
```

### JWT Token Claims

```python
# JWT payload includes company context
{
    "sub": "user_id:42",
    "company_id": 7,         # tenant identifier
    "role": "admin",
    "exp": 1753000000
}

# API middleware extracts and validates company_id
# from token — prevents company_id spoofing in request body
```

---

## 4. Tenant Onboarding Flow

### Self-Service Registration

```
Step 1: POST /companies/register
  {
    "company_name": "Acme Corp",
    "company_slug": "acme-corp",  # URL-safe, unique
    "admin_email": "admin@acme.com",
    "admin_password": "...",
    "admin_full_name": "John Smith"
  }

Step 2: System creates:
  ├── Company record
  ├── Default permissions (20 system permissions)
  ├── Default roles (admin, manager, staff, viewer)
  ├── Admin user with admin role
  └── Default "Head Office" branch

Step 3: Admin logs in → JWT issued with company context

Step 4: Admin invites team members via /users/invite (planned)
```

### Admin Portal Actions

| Action | Endpoint | Description |
|--------|----------|-------------|
| Register | `POST /companies/register` | Create company + admin |
| Update company | `PUT /companies/{id}` | Update company info |
| List users | `GET /users?company_id=X` | View all company users |
| Invite user | `POST /users/invite` | Email invitation (planned) |
| Set role | `PUT /users/{id}/role` | Assign user role |
| Remove user | `DELETE /users/{id}` | Deactivate user |
| View usage | `GET /companies/{id}/usage` | Storage, seats (planned) |

---

## 5. Role-Based Access Control (RBAC)

### Default Roles per Company

| Role | Permissions | Typical User |
|------|-------------|-------------|
| **admin** | All permissions | Business owner, IT admin |
| **manager** | CRUD on operational data; view reports | Department manager |
| **staff** | Create/read operational data; no delete | Sales rep, warehouse staff |
| **viewer** | Read-only on all data | Auditor, executive |

### Permission Categories

```
company.*          → company management
users.*            → user management
branches.*         → branch operations
warehouses.*       → warehouse operations
customers.*        → customer management
suppliers.*        → supplier management
products.*         → product catalog
quotations.*       → quotation workflow
orders.*           → order management
invoices.*         → invoice management
inventory.*        → stock management
reports.*          → analytics and exports
settings.*         → system configuration
```

### Custom Role Creation (Professional+ tier)

```python
# POST /companies/{id}/roles
{
    "name": "Sales Manager",
    "permissions": [
        "quotations.create", "quotations.update",
        "orders.create", "orders.update",
        "customers.read", "customers.create",
        "reports.sales"
    ]
}
```

---

## 6. Resource Quotas per Tier

```python
TIER_LIMITS = {
    "starter": {
        "max_users": 1,
        "max_branches": 1,
        "max_warehouses": 1,
        "max_products": 50,
        "max_customers": 50,
        "max_suppliers": 25,
        "monthly_transactions": 50,
        "storage_mb": 100,
        "api_calls_per_day": 0,
    },
    "growth": {
        "max_users": 5,
        "max_branches": 3,
        "max_warehouses": 3,
        "max_products": 500,
        "max_customers": 500,
        "max_suppliers": 100,
        "monthly_transactions": -1,  # unlimited
        "storage_mb": 5_000,
        "api_calls_per_day": 1_000,
    },
    "professional": {
        "max_users": 25,
        "max_branches": -1,
        "max_warehouses": -1,
        "max_products": -1,
        "max_customers": -1,
        "max_suppliers": -1,
        "monthly_transactions": -1,
        "storage_mb": 50_000,
        "api_calls_per_day": 10_000,
    },
    "enterprise": {
        # All limits custom per contract
    }
}
```

---

## 7. Data Portability and Retention

### Export Rights
- Growth+: Full data export (CSV/JSON) on demand
- Professional+: Scheduled exports to S3/SFTP
- All tiers: 30-day post-cancellation export window

### Data Deletion
- User-triggered: Immediate soft-delete → 30-day hard-delete
- Subscription cancellation: 90-day retention then anonymization
- Legal hold: Override retention for compliance requirements
- "Right to erasure" (GDPR Article 17): Manual process, 30-day SLA

### Backup Retention per Tier

| Tier | Daily Backups | Weekly Backups | Monthly Backups |
|------|--------------|----------------|-----------------|
| Starter | 7 days | No | No |
| Growth | 14 days | 4 weeks | No |
| Professional | 30 days | 8 weeks | 6 months |
| Enterprise | 90 days | 52 weeks | 3 years |

---

## 8. Compliance Readiness

| Standard | Status | Notes |
|----------|--------|-------|
| GDPR | Planned | Data processing agreement template needed |
| PDPL (Saudi Arabia) | Planned | Personal Data Protection Law compliance |
| UAE PDPL | Planned | 2023 UAE data protection law |
| PCI-DSS | Not applicable | No card data stored |
| SOC 2 Type II | Future | Needed for enterprise sales |
| ISO 27001 | Future | Needed for government contracts |

---

## 9. Tenant Health Monitoring

```python
# Per-tenant health metrics tracked in Redis:
{
    "company_id": 42,
    "last_login": "2026-07-18T10:00:00Z",
    "active_users_7d": 3,
    "transactions_30d": 150,
    "storage_used_mb": 45,
    "api_calls_today": 234,
    "tier": "growth",
    "subscription_status": "active",
    "trial_days_remaining": null
}
```

### Churn Risk Signals
- 0 logins in 14 days → in-app re-engagement
- Usage < 20% of tier limits → downgrade prompt
- Failed payment → payment retry + email sequence
- Support tickets > 3/month → CSM assignment

---

## 10. Scalability Roadmap

| Phase | Tenant Count | Architecture | Timeline |
|-------|-------------|-------------|----------|
| Phase 1 | 0-500 | Shared single DB | Launch |
| Phase 2 | 500-5,000 | Shared DB + RLS + read replicas | 6 months |
| Phase 3 | 5,000-50,000 | DB sharding by region | 18 months |
| Phase 4 | 50,000+ | Dedicated DB pools for Enterprise | 36 months |
