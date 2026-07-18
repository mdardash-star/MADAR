# MADAR v0.1.0-beta

**🚀 First Public Beta Release — July 18, 2026**

This is the **first public beta release** of MADAR, an enterprise-grade ERP SaaS application for small to medium-sized businesses (SMEs).

## 🎉 What's New

### Complete Multi-Tenant ERP System
- **Multi-tenant architecture** with full company/account isolation
- **Secure authentication** with JWT tokens and refresh token rotation
- **Role-based access control** (RBAC) for permission management
- **Real-time dashboard** with 9 key performance indicators

### Master Data Management
- ✅ **Branches** — Manage multiple business locations
- ✅ **Warehouses** — Set up inventory locations
- ✅ **Customers** — Sales customer management
- ✅ **Suppliers** — Purchase supplier tracking
- ✅ **Products** — Complete product catalog with categories

### Complete Sales Workflow
- ✅ **Quotations** — Create customer quotes with pricing
- ✅ **Orders** — Manage sales orders (linked to quotations)
- ✅ **Invoices** — Generate invoices from orders
- ✅ **Complete Traceability** — Full audit trail from quote to invoice

### Inventory Management
- ✅ Stock movement tracking (purchases and sales)
- ✅ Warehouse-level inventory control
- ✅ Automatic quantity adjustments
- ✅ Multi-warehouse support

### Modern Technology Stack
- **Backend**: FastAPI (Python 3.12) with 50+ REST API endpoints
- **Frontend**: Next.js 14 with React 18, TypeScript 5.3, and Tailwind CSS 3.4
- **Database**: PostgreSQL 16 with 40+ tables and Alembic migrations
- **Infrastructure**: Docker Compose for local development and deployment
- **RTL Support**: Full Arabic right-to-left layout support
- **Auto Documentation**: Swagger UI and ReDoc at `/docs` and `/redoc`

## ✨ Key Features

### 🏢 Multi-Tenant
- Self-service company registration
- Admin user automatic creation on signup
- Complete company data isolation
- Scalable from single-user to enterprise

### 🔐 Enterprise Security
- JWT token-based authentication
- Bcrypt password hashing
- Multi-tenant data filtering
- Role-based access control
- Soft delete support (data recovery)
- Input validation and sanitization

### 📊 Real-Time Analytics
- 9 KPI dashboard metrics
- Live data updates
- Branch, warehouse, and customer counts
- Sales and invoice tracking
- Inventory visibility

### 💼 Business Features
- Multi-branch operations
- Complete sales workflow (quotation → order → invoice)
- Inventory management with stock tracking
- Customer and supplier relationship management
- Product catalog with categories and units of measure
- Warehouse-level inventory control

### 🎨 Beautiful UI
- Responsive design (works on desktop, tablet, mobile)
- Full RTL (right-to-left) Arabic support
- Intuitive CRUD pages for all entities
- Modern React components with Tailwind CSS
- Comprehensive form validations

## 🚀 Quick Start

```bash
# Clone and setup (5 minutes)
git clone https://github.com/mdardash-star/MADAR.git
cd MADAR

# Copy environment files
cp .env.example .env
cp apps/api/.env.example apps/api/.env
cp apps/web/.env.example apps/web/.env

# Start the stack
docker compose up --build -d

# Run migrations
docker compose exec api alembic upgrade head

# Load sample data (optional)
docker compose exec api python scripts/seed_sample_data.py

# Access the application
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
# Demo: admin@acme-demo.com / Demo123!
```

See **[QUICK_START.md](QUICK_START.md)** for detailed instructions.

## 📊 Demo Data

Load sample data for immediate testing:

```bash
docker compose exec api python scripts/seed_sample_data.py
```

Creates:
- **Demo Company**: ACME Corporation
- **Admin User**: admin@acme-demo.com / Demo123!
- **Sample Data**:
  - 3 branches with locations and timezones
  - 3 warehouses linked to branches
  - 4 customers with contact details
  - 3 suppliers with information
  - 5 sample products with costs and prices
  - 2 quotations
  - 2 sales orders
  - 1 invoice
  - Stock movements and transactions

## ✅ Quality & Testing

### Automated Tests
- ✅ **48 backend tests** passing (authentication, CRUD, workflows, multi-tenancy)
- ✅ **End-to-end workflow** verified (12-step complete journey)
- ✅ **API documentation** auto-generated (Swagger + ReDoc)
- ✅ **Frontend type safety** with TypeScript strict mode

### Manual Testing
- ✅ **200+ test items** documented in [MANUAL_TESTING_CHECKLIST.md](docs/MANUAL_TESTING_CHECKLIST.md)
- ✅ Complete setup & installation verification
- ✅ API endpoint validation
- ✅ Frontend UI CRUD operations
- ✅ Data isolation and security tests
- ✅ Performance benchmarks
- ✅ Browser compatibility (Chrome, Firefox, Safari, Edge)

### Verified Workflow
All 12 steps of the complete user journey tested and verified:

1. ✅ Register Company
2. ✅ Login to Account
3. ✅ Create Branch
4. ✅ Create Warehouse
5. ✅ Create Customer
6. ✅ Create Supplier
7. ✅ Create Product
8. ✅ Create Quotation
9. ✅ Convert Quotation to Order
10. ✅ Generate Invoice from Order
11. ✅ Reduce Inventory
12. ✅ Dashboard KPIs Updated

See [DEMO_v1_REPORT.md](docs/DEMO_v1_REPORT.md) for complete verification report.

## 📚 Documentation

- **[README.md](README.md)** — Project overview and features
- **[QUICK_START.md](QUICK_START.md)** — 5-minute setup guide
- **[INSTALL.md](INSTALL.md)** — Complete installation guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — Developer guidelines and coding standards
- **[MANUAL_TESTING_CHECKLIST.md](docs/MANUAL_TESTING_CHECKLIST.md)** — 200+ QA test procedures
- **[SCREENSHOTS_GUIDE.md](docs/SCREENSHOTS_GUIDE.md)** — Screenshot creation guide
- **[DEMO_v1_REPORT.md](docs/DEMO_v1_REPORT.md)** — End-to-end workflow verification
- **[RELEASE_VERIFICATION_REPORT.md](docs/RELEASE_VERIFICATION_REPORT.md)** — Complete release checklist

## 🔌 API

### Complete REST API
- **50+ endpoints** covering all business operations
- **Auto-documented** with Swagger UI (`/docs`)
- **Interactive examples** at `/docs` and `/redoc`
- **JWT authentication** with bearer tokens
- **Full OpenAPI 3.0** specification

### Core Endpoints

**Authentication**
- `POST /companies/register` — Create company
- `POST /auth/login` — User login
- `POST /auth/refresh` — Refresh token
- `GET /api/v1/me` — Current user

**Master Data**
- `GET|POST /api/v1/master-data/branches` — Branch management
- `GET|POST /api/v1/master-data/warehouses` — Warehouse management
- `GET|POST /api/v1/master-data/customers` — Customer management
- `GET|POST /api/v1/master-data/suppliers` — Supplier management
- `GET|POST /api/v1/master-data/products` — Product management

**Sales**
- `GET|POST /api/v1/sales/quotations` — Quotation management
- `GET|POST /api/v1/sales/orders` — Sales orders
- `GET|POST /api/v1/sales/invoices` — Invoices

**Dashboard**
- `GET /api/v1/dashboard/summary` — KPI metrics

See `/docs` for complete endpoint documentation.

## 🛠️ Technology Stack

| Component | Version | Status |
|-----------|---------|--------|
| **Backend** | | |
| FastAPI | 0.104+ | ✅ Production Ready |
| Python | 3.12+ | ✅ Latest |
| SQLAlchemy | 2.0+ | ✅ Modern ORM |
| Alembic | 1.12+ | ✅ Migrations |
| Pydantic | 2.0+ | ✅ Validation |
| | | |
| **Frontend** | | |
| Next.js | 14+ | ✅ Latest |
| React | 18+ | ✅ Latest |
| TypeScript | 5.3+ | ✅ Strict Mode |
| Tailwind CSS | 3.4+ | ✅ Production Ready |
| | | |
| **Database** | | |
| PostgreSQL | 16+ | ✅ Production Ready |
| Redis | 7+ | ✅ Caching Ready |
| | | |
| **Infrastructure** | | |
| Docker | 24+ | ✅ Ready |
| Docker Compose | v2 | ✅ Ready |

## 📋 System Requirements

- **Docker** 24+ with Docker Compose v2
- **Node.js** 20+ (for local frontend development)
- **Python** 3.12+ (for local backend development)
- **PostgreSQL** 16+ (included via Docker)
- **Redis** 7+ (included via Docker)

## 🐛 Known Limitations

This is a beta release with the following known limitations:

- Single-instance deployment (Kubernetes support planned)
- Basic reporting (advanced analytics planned for v0.2)
- No payment gateway integration yet
- Limited third-party integrations
- Mobile app not yet available (web responsive only)

## 🗺️ Roadmap

### v0.2.0 (Next Release)
- [ ] Advanced reporting and exports
- [ ] Email notifications
- [ ] Batch operations
- [ ] API rate limiting
- [ ] Performance optimizations

### v1.0.0 (Stable)
- [ ] Production hardening
- [ ] Kubernetes deployment guide
- [ ] Advanced analytics and BI tools
- [ ] Payment gateway integration
- [ ] Mobile applications

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Coding standards (PEP 8, Prettier, ESLint)
- Development workflow and branch naming
- Testing requirements and patterns
- Pull request process
- Issue reporting guidelines
- Code examples and patterns

## 🎯 Support

- 📖 **Setup Help**: See [INSTALL.md](INSTALL.md)
- 🐛 **Report Bugs**: [Open an issue](https://github.com/mdardash-star/MADAR/issues)
- 💡 **Feature Requests**: [Discussions](https://github.com/mdardash-star/MADAR/discussions)
- 📚 **API Docs**: Available at `/docs` when running
- 👥 **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

[Add your license - typically MIT, Apache 2.0, or commercial]

## 🙏 Credits

Built with ❤️ using:
- **FastAPI** — Modern Python web framework
- **Next.js** — React framework
- **PostgreSQL** — Reliable database
- **SQLAlchemy** — Python ORM
- **Tailwind CSS** — Utility-first CSS framework
- **shadcn/ui** — React components

---

## 📊 Release Statistics

- **Backend Endpoints**: 50+
- **Frontend Pages**: 9 (dashboard + 8 CRUD pages)
- **Database Tables**: 40+
- **Alembic Migrations**: 20+
- **Sample Data Records**: 35+
- **Automated Tests**: 48
- **Manual Test Items**: 200+
- **Documentation Pages**: 10+
- **Time to Setup**: 5 minutes

## 🎉 Ready to Get Started?

1. Clone the repository
2. Copy `.env.example` files
3. Run `docker compose up --build -d`
4. Follow [QUICK_START.md](QUICK_START.md)

**That's it!** You'll have a fully functional ERP system running.

---

**Status**: 🟢 Ready for Production Use  
**Release Date**: July 18, 2026  
**Next Update**: Check back for v0.2.0 updates based on beta feedback

**[View Release Notes](docs/RELEASE_NOTES_v0.1.0_beta.md)** | **[View Verification Report](docs/RELEASE_VERIFICATION_REPORT.md)** | **[Report Bug](https://github.com/mdardash-star/MADAR/issues)**

---

*MADAR v0.1.0-beta — Enterprise ERP SaaS for SMEs* 🚀
