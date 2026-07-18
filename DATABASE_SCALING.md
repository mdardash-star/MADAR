# MADAR — Database Scaling Strategy

**Version**: 1.0  
**Date**: 2026-07-18  
**Status**: Active  
**Owner**: CTO / DevOps Lead  

---

## 1. Current State (v1.0.0-rc1)

| Property | Value |
|----------|-------|
| Engine | PostgreSQL 16-alpine |
| Mode | Single node, single instance |
| Max connections | 100 (PG default) |
| Connection pooling | None (SQLAlchemy pool, size=5) |
| Replication | None |
| Backups | Manual `pg_dump` (planned) |
| Max tested load | ~50 concurrent users (estimated) |
| Estimated capacity | ~500 active tenants |

---

## 2. Scaling Phases

### Phase 1: Single Node Optimization (0-500 tenants)

**Goal**: Maximize performance of single PostgreSQL instance.

**Actions:**

```sql
-- 1. Tune postgresql.conf for 8GB RAM server
-- File: /etc/postgresql/16/main/postgresql.conf

# Memory
shared_buffers = 2GB              # 25% of RAM
effective_cache_size = 6GB        # 75% of RAM
work_mem = 64MB                    # per sort/hash operation
maintenance_work_mem = 512MB       # for VACUUM, CREATE INDEX

# Query planner
random_page_cost = 1.1             # SSD (vs 4.0 for HDD)
effective_io_concurrency = 200     # SSD concurrent I/O

# WAL and checkpoints
wal_buffers = 64MB
checkpoint_completion_target = 0.9
min_wal_size = 1GB
max_wal_size = 4GB

# Connections
max_connections = 200             # with PgBouncer in front

# Logging (for query analysis)
log_min_duration_statement = 500  # log queries > 500ms
log_checkpoints = on
log_connections = on
log_lock_waits = on
track_io_timing = on
```

**Add PgBouncer (connection pooler):**

```ini
# pgbouncer.ini
[databases]
madar_prod = host=db port=5432 dbname=madar_prod

[pgbouncer]
pool_mode = transaction          # transaction-level pooling
max_client_conn = 500            # max frontend connections
default_pool_size = 20           # connections to PostgreSQL
min_pool_size = 5
server_idle_timeout = 600
client_idle_timeout = 300
```

**Add Critical Indexes:**

```sql
-- Multi-tenant query indexes (company_id is always in WHERE clause)
CREATE INDEX CONCURRENTLY idx_branches_company ON branches(company_id) WHERE is_deleted = FALSE;
CREATE INDEX CONCURRENTLY idx_customers_company ON customers(company_id) WHERE is_deleted = FALSE;
CREATE INDEX CONCURRENTLY idx_suppliers_company ON suppliers(company_id) WHERE is_deleted = FALSE;
CREATE INDEX CONCURRENTLY idx_products_company ON products(company_id) WHERE is_deleted = FALSE;
CREATE INDEX CONCURRENTLY idx_products_sku ON products(company_id, sku);
CREATE INDEX CONCURRENTLY idx_quotations_company_date ON sales_quotations(company_id, quote_date DESC);
CREATE INDEX CONCURRENTLY idx_orders_company_date ON sales_orders(company_id, order_date DESC);
CREATE INDEX CONCURRENTLY idx_invoices_company_date ON sales_invoices(company_id, invoice_date DESC);
CREATE INDEX CONCURRENTLY idx_stock_movements_product ON stock_movements(product_id, warehouse_id);
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
CREATE INDEX CONCURRENTLY idx_companies_slug ON companies(slug);

-- Soft-delete partial indexes (only index active records)
CREATE INDEX CONCURRENTLY idx_products_active ON products(company_id, name) WHERE is_deleted = FALSE;
CREATE INDEX CONCURRENTLY idx_customers_active ON customers(company_id, name) WHERE is_deleted = FALSE;
```

---

### Phase 2: Read Replica (500-5,000 tenants)

**Goal**: Separate read and write workloads.

```
                    ┌──────────────────────┐
Application ───WRITE─► PostgreSQL Primary  │
                    │  (Read + Write)      │
                    └──────────┬───────────┘
                               │ Streaming replication
                    ┌──────────▼───────────┐
Application ──READ──► PostgreSQL Replica   │
(dashboards,        │  (Read Only)         │
 reports)           └──────────────────────┘
```

**SQLAlchemy Read/Write Split:**

```python
# Two database engines
write_engine = create_engine(settings.database_url_primary)
read_engine = create_engine(settings.database_url_replica)

# Route queries
class ReadWriteSession:
    def get_read_session(self) -> Session:
        return Session(read_engine)
    
    def get_write_session(self) -> Session:
        return Session(write_engine)
```

**Replication Setup:**

```bash
# On primary: postgresql.conf
wal_level = replica
max_wal_senders = 3
wal_keep_size = 1GB

# On replica:
pg_basebackup -h primary_host -U replicator -D /var/lib/postgresql/16/main -P -Xs -R
```

---

### Phase 3: Horizontal Sharding (5,000-50,000 tenants)

**Goal**: Distribute tenant data across multiple database clusters.

```
Tenant Router (company_id % num_shards)
   │
   ├── Shard 0: company_ids 0,4,8,12...  (PostgreSQL cluster 0)
   ├── Shard 1: company_ids 1,5,9,13...  (PostgreSQL cluster 1)
   ├── Shard 2: company_ids 2,6,10,14... (PostgreSQL cluster 2)
   └── Shard 3: company_ids 3,7,11,15... (PostgreSQL cluster 3)
```

**OR: Citus (PostgreSQL extension for distributed queries):**

```sql
-- Convert to Citus distributed table
SELECT create_distributed_table('companies', 'id');
SELECT create_distributed_table('users', 'company_id');
SELECT create_distributed_table('products', 'company_id');
-- All tables co-located by company_id for join performance
```

---

## 3. Redis Caching Strategy

### Cache Layers

| Cache Layer | Key | TTL | When to invalidate |
|-------------|-----|-----|--------------------|
| Dashboard KPIs | `cache:dashboard:{company_id}` | 30s | On any transaction |
| Product list | `cache:products:{company_id}` | 5min | On product CRUD |
| Company info | `cache:company:{company_id}` | 60min | On company update |
| User permissions | `cache:perms:{user_id}` | 15min | On role change |
| Rate limit | `ratelimit:{ip}:{endpoint}` | 1min | Auto-expire |

### Cache Implementation

```python
import redis
import json
from functools import wraps

redis_client = redis.Redis(host=settings.redis_host, port=settings.redis_port)

def cached(key_pattern: str, ttl: int = 60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = key_pattern.format(**kwargs)
            cached_value = redis_client.get(cache_key)
            if cached_value:
                return json.loads(cached_value)
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator

@cached("cache:dashboard:{company_id}", ttl=30)
def get_dashboard_summary(db, company_id: int):
    # expensive query
    ...
```

---

## 4. Database Migration Strategy

### Zero-Downtime Migrations

```
Rule: Never drop columns in the same migration as removing code.
      Use expand-contract pattern:

Phase 1 (current release):
  - Add new column (nullable)
  - Deploy new code that writes to both old + new columns

Phase 2 (next release):
  - Backfill existing rows
  - Switch reads to new column

Phase 3 (following release):
  - Drop old column
```

### Migration Naming Convention

```
{YYYYMMDD}_{sequence}_{description}
20260718_000015_add_pgbouncer_user.py
20260801_000001_add_company_status_enum.py
20260801_000002_add_product_search_index.py
```

### Rollback Constraints

```python
# In every migration file:
def upgrade():
    # Forward migration
    ...

def downgrade():
    # Backward migration — MUST be implemented
    # No exceptions — tested before every release
    ...
```

---

## 5. Query Optimization Guidelines

### N+1 Prevention

```python
# BAD: N+1 query
products = db.query(Product).all()
for p in products:
    print(p.category.name)  # extra query per product

# GOOD: Eager loading
products = db.query(Product).options(
    joinedload(Product.category),
    joinedload(Product.unit_of_measure)
).filter(Product.company_id == company_id).all()
```

### Pagination (Required for Phase 2)

```python
def list_with_pagination(
    db: Session,
    company_id: int,
    page: int = 1,
    page_size: int = 50
) -> dict:
    offset = (page - 1) * page_size
    total = db.query(func.count(Product.id)).filter(
        Product.company_id == company_id,
        Product.is_deleted == False
    ).scalar()
    
    items = db.query(Product).filter(
        Product.company_id == company_id,
        Product.is_deleted == False
    ).offset(offset).limit(page_size).all()
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "pages": ceil(total / page_size)
    }
```

### EXPLAIN ANALYZE for Slow Queries

```sql
-- Always test new queries with EXPLAIN ANALYZE before deployment
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM sales_orders
WHERE company_id = 1
  AND order_date >= '2026-01-01'
ORDER BY order_date DESC
LIMIT 50;
```

---

## 6. Monitoring Database Health

### Key Metrics to Track

```sql
-- Active connections
SELECT count(*), state FROM pg_stat_activity GROUP BY state;

-- Long-running queries
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 seconds';

-- Table sizes
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- Index usage
SELECT schemaname, tablename, attname, n_distinct, correlation
FROM pg_stats
WHERE tablename = 'products';

-- Cache hit ratio (should be > 99%)
SELECT sum(blks_hit) / (sum(blks_hit) + sum(blks_read)) as cache_hit_ratio
FROM pg_stat_database;
```

### Prometheus Postgres Exporter

```yaml
# Add to docker-compose.prod.yml
postgres-exporter:
  image: prometheuscommunity/postgres-exporter
  environment:
    DATA_SOURCE_NAME: "postgresql://madar:${POSTGRES_PASSWORD}@db:5432/madar_prod?sslmode=disable"
  ports:
    - "9187:9187"
  networks:
    - backend
    - observability
```

---

## 7. Backup Strategy Summary

See `BACKUP_AND_RECOVERY.md` for full details.

| Frequency | Method | Retention | Storage |
|-----------|--------|-----------|---------|
| Continuous WAL | pg_basebackup + WAL archive | 7 days | Local + S3 |
| Daily full dump | pg_dump compressed | 30 days | S3 |
| Weekly snapshot | pg_dumpall | 12 weeks | S3 |
| Monthly archive | pg_dumpall | 1 year | S3 Glacier |
