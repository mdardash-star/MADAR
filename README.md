# MADAR ERP SaaS

[![Release](https://img.shields.io/badge/Release-v0.1.0--beta-blue)](docs/RELEASE_NOTES_v0.1.0_beta.md)
[![Tests](https://img.shields.io/badge/Tests-48%20passing-green)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

**MADAR** is an enterprise-grade ERP SaaS application for small to medium-sized businesses (SMEs). Manage multiple branches, warehouses, customers, suppliers, and complete sales workflows with real-time dashboards and inventory tracking.

**Status**: 🚀 **Public Beta Release (v0.1.0-beta)** — [Read Release Notes](docs/RELEASE_NOTES_v0.1.0_beta.md)

## Overview

- 🏢 **Multi-Tenant Architecture** — Isolated company data with RBAC
- 📊 **Real-Time Dashboards** — 9 KPI metrics with live updates
- 💼 **Master Data Management** — Branches, warehouses, customers, suppliers, products
- 📋 **Sales Workflow** — Quotations → Orders → Invoices with complete traceability
- 📦 **Inventory Tracking** — Stock movements and warehouse management
- 🔐 **Security-First** — JWT auth, password hashing, role-based access control
- 🌐 **Modern Stack** — FastAPI (Python), Next.js (React/TypeScript), PostgreSQL
- 🎨 **Beautiful UI** — Tailwind CSS with RTL Arabic support and responsive design
- 🐳 **Docker Ready** — Full Docker Compose setup for local development
- ✅ **Verified Workflow** — Complete 12-step end-to-end workflow tested and validated

## Repository Structure

- `apps/api` — FastAPI backend with 50+ API endpoints
- `apps/web` — Next.js frontend with 9 CRUD pages
- `scripts/` — Utility scripts (sample data seeding, etc.)
- `docs/` — Documentation and guides
- `docker-compose.yml` — Multi-service orchestration
- `.github/` — GitHub Actions CI and issue templates

## Prerequisites

- Docker
- Docker Compose
- Node.js 20+
- Python 3.12+
- npm

## 🚀 Quick Start (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/mdardash-star/MADAR.git
cd MADAR

# 2. Copy environment files
cp .env.example .env
cp apps/api/.env.example apps/api/.env
cp apps/web/.env.example apps/web/.env

# 3. Start the full stack
docker compose up --build -d

# 4. Run database migrations
docker compose exec api alembic upgrade head

# 5. Seed sample data (optional)
docker compose exec api python scripts/seed_sample_data.py

# 6. Access the application
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo "Demo Email: admin@acme-demo.com"
echo "Demo Password: Demo123!"
```

**That's it!** Your MADAR instance is running.

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[QUICK_START.md](QUICK_START.md)** | 5-minute setup guide |
| **[INSTALL.md](INSTALL.md)** | Complete installation guide |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | Developer guidelines & coding standards |
| **[docs/RELEASE_NOTES_v0.1.0_beta.md](docs/RELEASE_NOTES_v0.1.0_beta.md)** | Beta release details |
| **[docs/DEMO_v1_REPORT.md](docs/DEMO_v1_REPORT.md)** | End-to-end workflow verification |
| **[docs/SCREENSHOTS_GUIDE.md](docs/SCREENSHOTS_GUIDE.md)** | Screenshots & demo video guide |
| **[docs/MANUAL_TESTING_CHECKLIST.md](docs/MANUAL_TESTING_CHECKLIST.md)** | Manual testing procedures |
| **API Documentation** | Available at `/docs` (Swagger UI) when running |

---

## 🎯 Key Features

### Multi-Tenant SaaS
- ✅ Company registration and user management
- ✅ JWT token authentication with refresh tokens
- ✅ Role-based access control (RBAC)
- ✅ Complete data isolation per tenant

### Operations Management
- ✅ Multiple branches per company
- ✅ Warehouse management
- ✅ Customer and supplier contacts

### Sales Workflow
- ✅ Sales quotations with pricing
- ✅ Order management
- ✅ Invoice generation
- ✅ Complete audit trail (quotation → order → invoice)

### Inventory Management
- ✅ Stock movement tracking
- ✅ Purchase and sale transactions
- ✅ Warehouse-level inventory control
- ✅ Automatic quantity updates

### Dashboard & Analytics
- ✅ Real-time KPI dashboard (9 metrics)
- ✅ Branch, warehouse, and customer counts
- ✅ Sales and invoice tracking
- ✅ Live data updates

### Developer Experience
- ✅ Auto-generated API docs (Swagger + ReDoc)
- ✅ TypeScript frontend with type safety
- ✅ Comprehensive test coverage
- ✅ Docker setup for easy local development

---

## 🧪 Verified Workflow

The complete 12-step user journey has been tested and verified:

1. ✅ Register company
2. ✅ Login to account
3. ✅ Create branch
4. ✅ Create warehouse
5. ✅ Create customer
6. ✅ Create supplier
7. ✅ Create product
8. ✅ Create quotation
9. ✅ Convert quotation to order
10. ✅ Generate invoice
11. ✅ Reduce inventory
12. ✅ View updated dashboard KPIs

See [DEMO_v1_REPORT.md](docs/DEMO_v1_REPORT.md) for complete verification details.

---

## 🛠️ Local Development Setup

### Option A: Docker (Recommended)

```bash
docker compose up --build -d
docker compose exec api alembic upgrade head
```

### Option B: Local Setup (Backend)

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Option C: Local Setup (Frontend)

```bash
cd apps/web
npm install
npm run dev
```

See [INSTALL.md](INSTALL.md) for detailed setup instructions.

---

## 🔌 API Endpoints

### Authentication
- `POST /companies/register` — Create company and admin user
- `POST /auth/login` — User login (returns JWT token)
- `POST /auth/refresh` — Refresh expired token
- `GET /api/v1/me` — Current user profile

### Master Data (CRUD)
- `/api/v1/master-data/branches` — Branch management
- `/api/v1/master-data/warehouses` — Warehouse management
- `/api/v1/master-data/customers` — Customer management
- `/api/v1/master-data/suppliers` — Supplier management
- `/api/v1/master-data/products` — Product management

### Sales Management
- `/api/v1/sales/quotations` — Quotations
- `/api/v1/sales/orders` — Sales orders
- `/api/v1/sales/invoices` — Invoices

### Inventory
- `/api/v1/inventory/stock-movements` — Stock tracking

### Analytics
- `GET /api/v1/dashboard/summary` — KPI dashboard data

See API documentation at `/docs` for complete endpoint details.

---

## 🔐 Security

### Built-In Features
- JWT token authentication
- Password hashing (bcrypt)
- Role-based access control (RBAC)
- Multi-tenant data isolation
- Soft delete support (data recovery)
- Input validation and sanitization

### Pre-Production Checklist
- [ ] Change `JWT_SECRET_KEY` environment variable
- [ ] Update `POSTGRES_PASSWORD`
- [ ] Configure `CORS_ORIGINS` for your domain
- [ ] Enable HTTPS/TLS on reverse proxy
- [ ] Set up proper backup strategy
- [ ] Configure monitoring and logging
- [ ] Review and update `.env` for production

---

## 🧪 Testing

### Backend Tests
```bash
cd apps/api
pytest -q  # Run all tests (48 passing)
pytest tests/test_workflow_e2e.py -v  # Run workflow verification
```

### Frontend Tests
```bash
cd apps/web
npm test
```

### Manual Testing
Complete manual testing checklist available at [docs/MANUAL_TESTING_CHECKLIST.md](docs/MANUAL_TESTING_CHECKLIST.md)

---

## 📦 Sample Data

Load demo data for testing:

```bash
docker compose exec api python scripts/seed_sample_data.py
```

Creates:
- Demo company: ACME Corporation
- 3 branches, 3 warehouses
- 4 customers, 3 suppliers
- 5 sample products
- 2 quotations, 2 orders
- 1 invoice with sample transactions

Demo login:
- **Email**: admin@acme-demo.com
- **Password**: Demo123!

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Coding standards and best practices
- Development workflow and branch naming
- Testing requirements
- Pull request process
- Issue and feature request templates

---

## 📋 Project Status

| Component | Status | Notes |
|-----------|--------|-------|
| Backend API | ✅ Complete | 50+ endpoints, 48 tests passing |
| Frontend UI | ✅ Complete | 9 CRUD pages, responsive, RTL support |
| Database | ✅ Complete | 40+ tables, migrations, soft deletes |
| Authentication | ✅ Complete | JWT, refresh tokens, RBAC |
| Documentation | ✅ Complete | Setup guides, API docs, testing checklists |
| Sample Data | ✅ Complete | Full demo company seeding script |
| End-to-End Workflow | ✅ Verified | 12-step journey tested |

---

## 🚀 Roadmap

### v0.2.0 (Next Release)
- [ ] Advanced reporting and exports
- [ ] Email notifications
- [ ] Batch operations
- [ ] Performance optimizations

### v1.0.0 (Stable Release)
- [ ] Production hardening
- [ ] Kubernetes deployment guide
- [ ] Advanced analytics
- [ ] Payment gateway integration

---

## 📞 Support & Feedback

- 📖 **Documentation**: Check [README](README.md) and [INSTALL.md](INSTALL.md)
- 🐛 **Bug Reports**: [Open an issue](https://github.com/mdardash-star/MADAR/issues)
- 💡 **Feature Requests**: [Discussions](https://github.com/mdardash-star/MADAR/discussions)
- 👥 **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

[Specify your license - typically MIT, Apache 2.0, or commercial]

---

## 🎯 Next Steps

1. **Get Started**: Follow [QUICK_START.md](QUICK_START.md)
2. **Read Docs**: Review [INSTALL.md](INSTALL.md) and [CONTRIBUTING.md](CONTRIBUTING.md)
3. **Load Demo Data**: Run `python scripts/seed_sample_data.py`
4. **Explore API**: Visit http://localhost:8000/docs
5. **Build Features**: See [CONTRIBUTING.md](CONTRIBUTING.md) for development workflow

---

**MADAR v0.1.0-beta** — Enterprise ERP for SMEs 🚀
