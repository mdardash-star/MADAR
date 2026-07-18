# Contributing to MADAR

Thank you for your interest in contributing to MADAR! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing](#testing)
6. [Commit Messages](#commit-messages)
7. [Pull Request Process](#pull-request-process)
8. [Reporting Issues](#reporting-issues)

---

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and adhere to our [Code of Conduct](CODE_OF_CONDUCT.md) - although we don't have a specific file yet, treat all contributors with respect.

### Be Respectful
- Use inclusive language
- Be welcoming to newcomers
- Respect differing opinions and experiences

---

## Getting Started

### Prerequisites

- Git
- Docker & Docker Compose (for local development)
- Node.js 20+
- Python 3.12+
- PostgreSQL 16+ (if not using Docker)
- Redis 7+ (if not using Docker)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/MADAR.git
   cd MADAR
   ```

3. Add the upstream remote:
   ```bash
   git remote add upstream https://github.com/mdardash-star/MADAR.git
   ```

### Setup Development Environment

```bash
# Copy environment files
cp .env.example .env
cp apps/api/.env.example apps/api/.env
cp apps/web/.env.example apps/web/.env

# Start the full stack
docker compose up --build -d

# Run migrations
docker compose exec api alembic upgrade head

# Seed sample data (optional but recommended)
docker compose exec api python scripts/seed_sample_data.py
```

Access the application:
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc

---

## Development Workflow

### Branch Naming Convention

Use descriptive branch names following this format:

```
{type}/{description}
```

**Types:**
- `feature/` — New features
- `fix/` — Bug fixes
- `docs/` — Documentation updates
- `test/` — Test additions or modifications
- `refactor/` — Code refactoring
- `perf/` — Performance improvements
- `chore/` — Maintenance tasks

**Examples:**
- `feature/customer-api-endpoints`
- `fix/dashboard-kpi-calculation`
- `docs/installation-guide`
- `test/e2e-workflow`

### Creating a Feature Branch

```bash
# Sync with upstream
git fetch upstream
git rebase upstream/main

# Create feature branch
git checkout -b feature/my-feature
```

### Keep Your Branch Updated

```bash
git fetch upstream
git rebase upstream/main
```

---

## Coding Standards

### Backend (FastAPI/Python)

**Style Guide:** PEP 8 with Black formatter and isort

```bash
# Auto-format code
cd apps/api
black app/
isort app/

# Lint with pylint or flake8
flake8 app/
```

**Key Principles:**
- Use type hints on all function signatures
- Write docstrings for modules, classes, and functions
- Keep functions focused and <50 lines when possible
- Use meaningful variable names
- Add comments for complex logic

**Example:**
```python
def calculate_total_amount(
    subtotal: float,
    tax_rate: float = 0.10,
    discount: float = 0.0
) -> float:
    """
    Calculate total amount including tax and discount.
    
    Args:
        subtotal: Base amount before tax and discount
        tax_rate: Tax rate as decimal (0.10 = 10%)
        discount: Discount amount to apply
    
    Returns:
        Total amount after applying tax and discount
    """
    tax_amount = subtotal * tax_rate
    return subtotal + tax_amount - discount
```

### Frontend (TypeScript/React)

**Style Guide:** Prettier + ESLint (TypeScript strict mode)

```bash
# Auto-format code
cd apps/web
npm run format

# Lint code
npm run lint
```

**Key Principles:**
- Use functional components with hooks
- Use TypeScript interfaces for props
- Keep components focused and <200 lines
- Use meaningful component names
- Organize components in feature folders
- Use Tailwind CSS for styling

**Example:**
```typescript
interface CustomerListProps {
  companyId: number;
  onSelectCustomer?: (customer: Customer) => void;
}

export const CustomerList: React.FC<CustomerListProps> = ({
  companyId,
  onSelectCustomer,
}) => {
  const [customers, setCustomers] = React.useState<Customer[]>([]);
  const [loading, setLoading] = React.useState(false);

  React.useEffect(() => {
    fetchCustomers(companyId).then(setCustomers);
  }, [companyId]);

  return (
    <div className="space-y-4">
      {customers.map((customer) => (
        <div
          key={customer.id}
          onClick={() => onSelectCustomer?.(customer)}
          className="p-4 border rounded hover:bg-gray-50 cursor-pointer"
        >
          {customer.name}
        </div>
      ))}
    </div>
  );
};
```

### Database

**Schema Conventions:**
- Table names: `snake_case` plural (e.g., `customers`, `sales_orders`)
- Column names: `snake_case` (e.g., `customer_id`, `created_at`)
- Primary keys: `id` (auto-increment integer)
- Foreign keys: `{table_singular}_id` (e.g., `customer_id`)
- Timestamps: `created_at` and `updated_at` (UTC timezone aware)
- Soft deletes: `is_deleted` boolean and `deleted_at` timestamp

**Migration Naming:**
```
20260718_000001_add_customer_table.py
{YYYYMMDD}_{sequence}_{description}.py
```

---

## Testing

### Backend Tests

```bash
cd apps/api

# Run all tests
pytest

# Run specific test file
pytest tests/test_workflow_e2e.py

# Run with coverage
pytest --cov=app

# Run with verbose output
pytest -v
```

**Test File Naming:**
- Unit tests: `test_*.py` or `*_test.py`
- Location: `tests/` directory
- Name tests descriptively: `test_create_customer_with_valid_email`

**Test Structure:**
```python
def test_create_customer_with_valid_email():
    """Should create customer when valid email is provided"""
    # Arrange
    customer_data = {"name": "ABC Corp", "email": "valid@email.com"}
    
    # Act
    response = client.post("/customers", json=customer_data)
    
    # Assert
    assert response.status_code == 201
    assert response.json()["email"] == customer_data["email"]
```

### Frontend Tests

```bash
cd apps/web

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test
npm test -- --testNamePattern="CustomerList"
```

### End-to-End Tests

```bash
cd apps/api

# Run E2E workflow verification
pytest tests/test_workflow_e2e.py::test_complete_12step_workflow -v
```

---

## Commit Messages

Follow conventional commits format:

```
{type}({scope}): {description}

{body}

{footer}
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style (formatting, semicolons, etc.)
- `refactor:` Code refactoring
- `perf:` Performance improvement
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

**Examples:**

```
feat(customers): add customer API endpoints

Add CRUD endpoints for managing customers:
- POST /customers - Create new customer
- GET /customers - List customers
- GET /customers/{id} - Get specific customer
- PUT /customers/{id} - Update customer
- DELETE /customers/{id} - Delete customer

Includes comprehensive error handling and validation.
```

```
fix(dashboard): correct KPI calculation for invoices

The dashboard was counting deleted invoices in the total.
Changed query to filter out soft-deleted records.

Fixes #123
```

---

## Pull Request Process

### Before Submitting

1. **Update your branch:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Test locally:**
   ```bash
   # Backend tests
   cd apps/api && pytest

   # Frontend tests
   cd apps/web && npm test

   # Lint code
   npm run lint    # frontend
   black app/      # backend
   ```

3. **Commit with descriptive messages** (see Commit Messages section)

4. **Push to your fork:**
   ```bash
   git push origin feature/my-feature
   ```

### Creating a Pull Request

1. Go to GitHub and create a PR from your fork to the main repository
2. Use the provided PR template (see `.github/pull_request_template.md`)
3. Fill in all sections:
   - Description of changes
   - Type of change (feature, fix, docs, etc.)
   - Related issues
   - Testing instructions
   - Screenshots (if UI changes)
   - Checklist items

### Pull Request Checklist

- [ ] Commit messages follow conventional format
- [ ] Code follows style guidelines (formatted with Black/Prettier)
- [ ] Tests added for new functionality
- [ ] All tests pass locally
- [ ] Documentation updated
- [ ] No new warnings or errors
- [ ] No breaking changes (or documented in PR)
- [ ] Screenshots/GIFs attached (if UI changes)

### Code Review

- Be open to feedback
- Respond to review comments within 48 hours
- Make requested changes in new commits
- Re-request review after making changes
- Be patient — maintainers are volunteers

---

## Reporting Issues

### Bug Reports

Use the [issue template](.github/ISSUE_TEMPLATE/bug_report.md)

**Include:**
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment (OS, browser, Python version, etc.)
- Relevant error messages or logs

### Feature Requests

Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md)

**Include:**
- Clear description of the feature
- Motivation and use case
- Proposed implementation (if any)
- Alternatives considered
- Additional context

---

## Architecture Overview

### Backend Structure

```
apps/api/
├── app/
│   ├── core/
│   │   ├── database.py      # Database configuration
│   │   ├── security.py      # JWT, password hashing
│   │   └── settings.py      # Configuration
│   ├── models/              # SQLAlchemy models
│   │   ├── company.py
│   │   ├── user.py
│   │   └── ...
│   ├── routes/              # API endpoints
│   │   ├── auth.py
│   │   ├── companies.py
│   │   └── ...
│   ├── services/            # Business logic
│   │   ├── company_service.py
│   │   └── ...
│   ├── schemas/             # Pydantic schemas
│   │   ├── company.py
│   │   └── ...
│   └── main.py              # FastAPI app
├── alembic/                 # Database migrations
├── tests/                   # Unit and integration tests
└── requirements.txt
```

### Frontend Structure

```
apps/web/
├── app/                     # Next.js App Router
│   ├── dashboard/
│   ├── customers/
│   ├── products/
│   └── ...
├── components/
│   ├── common/              # Reusable components
│   ├── layout/
│   └── ...
├── lib/
│   ├── api.ts              # API client
│   └── utils.ts            # Utility functions
└── public/                  # Static assets
```

---

## Questions?

- Create a GitHub Discussion for questions
- Check existing issues for similar questions
- Ask in pull request comments
- Reach out to maintainers

---

## License

By contributing to MADAR, you agree that your contributions will be licensed under the same license as the project (check LICENSE file).

Thank you for contributing! 🎉
