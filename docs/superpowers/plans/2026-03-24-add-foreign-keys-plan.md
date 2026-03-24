# Add Foreign Key Constraints and Relationships — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add proper `db.ForeignKey()` constraints, `db.relationship()` definitions, and cascade deletes to all 9 parent-child relationships in the database.

**Architecture:** Single Alembic migration handles all schema changes (data cleanup, type conversions, FK constraints, indexes). Model files updated with ForeignKey and relationship definitions. Parent service delete functions leverage cascade deletes.

**Tech Stack:** Flask, SQLAlchemy, Alembic, PostgreSQL

**Spec:** `docs/superpowers/specs/2026-03-24-add-foreign-keys-design.md`

---

## File Map

### Models — add `db.ForeignKey()` to child models
- `app/main/model/assembly.py` — add FK on `assemblyTypeId`
- `app/main/model/galleryImage.py` — add FK on `galleryId`
- `app/main/model/email.py` — change `locationId` from `String(255)` to `Integer` + FK
- `app/main/model/opening.py` — change `locationId` from `String(255)` to `Integer` + FK
- `app/main/model/telephone.py` — change `locationId` from `String(255)` to `Integer` + FK
- `app/main/model/jobPosting.py` — add FK on `locationId`
- `app/main/model/manufacturerImage.py` — add FK on `manufacturerId`
- `app/main/model/realization.py` — add FK on `realizationTypeId`
- `app/main/model/tanker.py` — add FK on `tankerTypeId`

### Models — add `db.relationship()` to parent models
- `app/main/model/assemblyType.py` — add `assemblies` relationship
- `app/main/model/gallery.py` — add `images` relationship
- `app/main/model/location.py` — add `emails`, `openings`, `telephones`, `job_postings` relationships
- `app/main/model/manufacturer.py` — add `images` relationship
- `app/main/model/realizationType.py` — add `realizations` relationship
- `app/main/model/tankerType.py` — add `tankers` relationship

### Migration
- `migrations/versions/<generated>_add_foreign_key_constraints.py` — data cleanup, type conversion, FK constraints, indexes

### Services — no functional changes needed
The existing `db.session.delete()` calls in parent services already trigger SQLAlchemy cascade deletes once `cascade='all, delete-orphan'` is set on the relationship. The `ondelete='CASCADE'` on the FK handles database-level cascades. Both ORM-level and database-level cascades are in play, making the existing code doubly safe. No service code changes required.

### Frontend impact
After the migration, `locationId` in `Email`, `Opening`, and `Telephone` API responses will change from a string (e.g., `"1"`) to an integer (e.g., `1`). Verify the frontend handles this — most JSON parsers handle it transparently.

---

### Task 1: Update child models — add `db.ForeignKey()` to Integer FK columns

**Files:**
- Modify: `app/main/model/assembly.py:8`
- Modify: `app/main/model/galleryImage.py:8`
- Modify: `app/main/model/jobPosting.py:16`
- Modify: `app/main/model/manufacturerImage.py:8`
- Modify: `app/main/model/realization.py:8`
- Modify: `app/main/model/tanker.py:8`

These 6 models already have the correct `Integer` type. Only need to add `db.ForeignKey()`.

- [ ] **Step 1: Update `assembly.py`**

Change line 8 from:
```python
    assemblyTypeId = db.Column(db.Integer, unique=False)
```
to:
```python
    assemblyTypeId = db.Column(db.Integer, db.ForeignKey('assemblyTypes.id', ondelete='CASCADE'))
```

- [ ] **Step 2: Update `galleryImage.py`**

Change line 8 from:
```python
    galleryId = db.Column(db.Integer, unique=False)
```
to:
```python
    galleryId = db.Column(db.Integer, db.ForeignKey('galleries.id', ondelete='CASCADE'))
```

- [ ] **Step 3: Update `jobPosting.py`**

Change line 16 from:
```python
    locationId = db.Column(db.Integer, unique=False)
```
to:
```python
    locationId = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete='CASCADE'))
```

- [ ] **Step 4: Update `manufacturerImage.py`**

Change line 8 from:
```python
    manufacturerId = db.Column(db.Integer, unique=False)
```
to:
```python
    manufacturerId = db.Column(db.Integer, db.ForeignKey('manufacturer.id', ondelete='CASCADE'))
```

Note: table name is `manufacturer` (singular).

- [ ] **Step 5: Update `realization.py`**

Change line 8 from:
```python
    realizationTypeId = db.Column(db.Integer, unique=False)
```
to:
```python
    realizationTypeId = db.Column(db.Integer, db.ForeignKey('realizationTypes.id', ondelete='CASCADE'))
```

- [ ] **Step 6: Update `tanker.py`**

Change line 8 from:
```python
    tankerTypeId = db.Column(db.Integer, unique=False)
```
to:
```python
    tankerTypeId = db.Column(db.Integer, db.ForeignKey('tankerTypes.id', ondelete='CASCADE'))
```

- [ ] **Step 7: Commit**

```bash
git add app/main/model/assembly.py app/main/model/galleryImage.py app/main/model/jobPosting.py app/main/model/manufacturerImage.py app/main/model/realization.py app/main/model/tanker.py
git commit -m "feat: add db.ForeignKey() to integer FK columns in child models"
```

---

### Task 2: Update child models — convert `locationId` from String to Integer + add FK

**Files:**
- Modify: `app/main/model/email.py:8`
- Modify: `app/main/model/opening.py:8`
- Modify: `app/main/model/telephone.py:8`

These 3 models have `locationId` as `String(255)` and need conversion to `Integer` with FK.

- [ ] **Step 1: Update `email.py`**

Change line 8 from:
```python
    locationId = db.Column(db.String(255), unique=False)
```
to:
```python
    locationId = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete='CASCADE'))
```

- [ ] **Step 2: Update `opening.py`**

Change line 8 from:
```python
    locationId = db.Column(db.String(255), unique=False)
```
to:
```python
    locationId = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete='CASCADE'))
```

- [ ] **Step 3: Update `telephone.py`**

Change line 8 from:
```python
    locationId = db.Column(db.String(255), unique=False)
```
to:
```python
    locationId = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete='CASCADE'))
```

- [ ] **Step 4: Commit**

```bash
git add app/main/model/email.py app/main/model/opening.py app/main/model/telephone.py
git commit -m "feat: convert locationId from String to Integer + add FK in email, opening, telephone models"
```

---

### Task 3: Add `db.relationship()` to parent models

**Files:**
- Modify: `app/main/model/assemblyType.py`
- Modify: `app/main/model/gallery.py`
- Modify: `app/main/model/location.py`
- Modify: `app/main/model/manufacturer.py`
- Modify: `app/main/model/realizationType.py`
- Modify: `app/main/model/tankerType.py`

- [ ] **Step 1: Update `assemblyType.py`**

Add after line 10 (`displayOrder` column):
```python
    assemblies = db.relationship('Assembly', backref='assembly_type', cascade='all, delete-orphan', passive_deletes=True, lazy=True)
```

- [ ] **Step 2: Update `gallery.py`**

Add after line 9 (`displayOrder` column):
```python
    images = db.relationship('GalleryImage', backref='gallery', cascade='all, delete-orphan', passive_deletes=True, lazy=True)
```

- [ ] **Step 3: Update `location.py`**

Add after line 11 (`displayOrder` column):
```python
    emails = db.relationship('Email', backref='location', cascade='all, delete-orphan', passive_deletes=True, lazy=True)
    openings = db.relationship('Opening', backref='location', cascade='all, delete-orphan', passive_deletes=True, lazy=True)
    telephones = db.relationship('Telephone', backref='location', cascade='all, delete-orphan', passive_deletes=True, lazy=True)
    job_postings = db.relationship('JobPosting', backref='location', cascade='all, delete-orphan', passive_deletes=True, lazy=True)
```

- [ ] **Step 4: Update `manufacturer.py`**

Add after line 10 (`displayOrder` column):
```python
    images = db.relationship('ManufacturerImage', backref='manufacturer', cascade='all, delete-orphan', passive_deletes=True, lazy=True)
```

- [ ] **Step 5: Update `realizationType.py`**

Add after line 10 (`displayOrder` column):
```python
    realizations = db.relationship('Realization', backref='realization_type', cascade='all, delete-orphan', passive_deletes=True, lazy=True)
```

- [ ] **Step 6: Update `tankerType.py`**

Add after line 10 (`displayOrder` column):
```python
    tankers = db.relationship('Tanker', backref='tanker_type', cascade='all, delete-orphan', passive_deletes=True, lazy=True)
```

- [ ] **Step 7: Commit**

```bash
git add app/main/model/assemblyType.py app/main/model/gallery.py app/main/model/location.py app/main/model/manufacturer.py app/main/model/realizationType.py app/main/model/tankerType.py
git commit -m "feat: add db.relationship() with cascade deletes to parent models"
```

---

### Task 4: Write the Alembic migration

**Files:**
- Create: `migrations/versions/<generated>_add_foreign_key_constraints.py`

The migration has 3 phases: data cleanup, type conversion, FK constraints + indexes. The current head revision is `e3c1048547d8`.

- [ ] **Step 1: Generate an empty migration**

```bash
cd /Users/victortrinh/Documents/GitHub/certiflo-be
flask db revision -m "add foreign key constraints"
```

This creates a new file in `migrations/versions/`. Note the generated filename.

- [ ] **Step 2: Write the upgrade function**

Replace the generated `upgrade()` function body with:

```python
def upgrade():
    # Phase 1: Clean up orphaned data
    # Integer FK columns — delete children referencing nonexistent parents
    op.execute('DELETE FROM assemblies WHERE "assemblyTypeId" IS NOT NULL AND "assemblyTypeId" NOT IN (SELECT id FROM "assemblyTypes")')
    op.execute('DELETE FROM "galleryImages" WHERE "galleryId" IS NOT NULL AND "galleryId" NOT IN (SELECT id FROM galleries)')
    op.execute('DELETE FROM "manufacturerImages" WHERE "manufacturerId" IS NOT NULL AND "manufacturerId" NOT IN (SELECT id FROM manufacturer)')
    op.execute('DELETE FROM realizations WHERE "realizationTypeId" IS NOT NULL AND "realizationTypeId" NOT IN (SELECT id FROM "realizationTypes")')
    op.execute('DELETE FROM tankers WHERE "tankerTypeId" IS NOT NULL AND "tankerTypeId" NOT IN (SELECT id FROM "tankerTypes")')
    op.execute('DELETE FROM "jobPostings" WHERE "locationId" IS NOT NULL AND "locationId" NOT IN (SELECT id FROM locations)')

    # String FK columns — delete rows with non-numeric locationId, then orphans
    op.execute("""DELETE FROM emails WHERE "locationId" IS NOT NULL AND "locationId" !~ '^\\d+$'""")
    op.execute("""DELETE FROM emails WHERE "locationId" IS NOT NULL AND CAST("locationId" AS INTEGER) NOT IN (SELECT id FROM locations)""")
    op.execute("""DELETE FROM openings WHERE "locationId" IS NOT NULL AND "locationId" !~ '^\\d+$'""")
    op.execute("""DELETE FROM openings WHERE "locationId" IS NOT NULL AND CAST("locationId" AS INTEGER) NOT IN (SELECT id FROM locations)""")
    op.execute("""DELETE FROM telephones WHERE "locationId" IS NOT NULL AND "locationId" !~ '^\\d+$'""")
    op.execute("""DELETE FROM telephones WHERE "locationId" IS NOT NULL AND CAST("locationId" AS INTEGER) NOT IN (SELECT id FROM locations)""")

    # Phase 2: Convert locationId from String to Integer
    op.alter_column('emails', 'locationId',
                    existing_type=sa.String(255),
                    type_=sa.Integer(),
                    postgresql_using='"locationId"::integer')
    op.alter_column('openings', 'locationId',
                    existing_type=sa.String(255),
                    type_=sa.Integer(),
                    postgresql_using='"locationId"::integer')
    op.alter_column('telephones', 'locationId',
                    existing_type=sa.String(255),
                    type_=sa.Integer(),
                    postgresql_using='"locationId"::integer')

    # Phase 3: Add foreign key constraints and indexes
    op.create_foreign_key('fk_assemblies_assemblyTypeId', 'assemblies', 'assemblyTypes',
                          ['assemblyTypeId'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('fk_galleryImages_galleryId', 'galleryImages', 'galleries',
                          ['galleryId'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('fk_emails_locationId', 'emails', 'locations',
                          ['locationId'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('fk_openings_locationId', 'openings', 'locations',
                          ['locationId'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('fk_telephones_locationId', 'telephones', 'locations',
                          ['locationId'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('fk_jobPostings_locationId', 'jobPostings', 'locations',
                          ['locationId'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('fk_manufacturerImages_manufacturerId', 'manufacturerImages', 'manufacturer',
                          ['manufacturerId'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('fk_realizations_realizationTypeId', 'realizations', 'realizationTypes',
                          ['realizationTypeId'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('fk_tankers_tankerTypeId', 'tankers', 'tankerTypes',
                          ['tankerTypeId'], ['id'], ondelete='CASCADE')

    # Add indexes on FK columns for cascade delete performance
    op.create_index('ix_assemblies_assemblyTypeId', 'assemblies', ['assemblyTypeId'])
    op.create_index('ix_galleryImages_galleryId', 'galleryImages', ['galleryId'])
    op.create_index('ix_emails_locationId', 'emails', ['locationId'])
    op.create_index('ix_openings_locationId', 'openings', ['locationId'])
    op.create_index('ix_telephones_locationId', 'telephones', ['locationId'])
    op.create_index('ix_jobPostings_locationId', 'jobPostings', ['locationId'])
    op.create_index('ix_manufacturerImages_manufacturerId', 'manufacturerImages', ['manufacturerId'])
    op.create_index('ix_realizations_realizationTypeId', 'realizations', ['realizationTypeId'])
    op.create_index('ix_tankers_tankerTypeId', 'tankers', ['tankerTypeId'])
```

- [ ] **Step 3: Write the downgrade function**

Replace the generated `downgrade()` function body with:

```python
def downgrade():
    # Drop indexes
    op.drop_index('ix_tankers_tankerTypeId', 'tankers')
    op.drop_index('ix_realizations_realizationTypeId', 'realizations')
    op.drop_index('ix_manufacturerImages_manufacturerId', 'manufacturerImages')
    op.drop_index('ix_jobPostings_locationId', 'jobPostings')
    op.drop_index('ix_telephones_locationId', 'telephones')
    op.drop_index('ix_openings_locationId', 'openings')
    op.drop_index('ix_emails_locationId', 'emails')
    op.drop_index('ix_galleryImages_galleryId', 'galleryImages')
    op.drop_index('ix_assemblies_assemblyTypeId', 'assemblies')

    # Drop foreign key constraints
    op.drop_constraint('fk_tankers_tankerTypeId', 'tankers', type_='foreignkey')
    op.drop_constraint('fk_realizations_realizationTypeId', 'realizations', type_='foreignkey')
    op.drop_constraint('fk_manufacturerImages_manufacturerId', 'manufacturerImages', type_='foreignkey')
    op.drop_constraint('fk_jobPostings_locationId', 'jobPostings', type_='foreignkey')
    op.drop_constraint('fk_telephones_locationId', 'telephones', type_='foreignkey')
    op.drop_constraint('fk_openings_locationId', 'openings', type_='foreignkey')
    op.drop_constraint('fk_emails_locationId', 'emails', type_='foreignkey')
    op.drop_constraint('fk_galleryImages_galleryId', 'galleryImages', type_='foreignkey')
    op.drop_constraint('fk_assemblies_assemblyTypeId', 'assemblies', type_='foreignkey')

    # Convert locationId back to String
    op.alter_column('telephones', 'locationId',
                    existing_type=sa.Integer(),
                    type_=sa.String(255),
                    postgresql_using='"locationId"::text')
    op.alter_column('openings', 'locationId',
                    existing_type=sa.Integer(),
                    type_=sa.String(255),
                    postgresql_using='"locationId"::text')
    op.alter_column('emails', 'locationId',
                    existing_type=sa.Integer(),
                    type_=sa.String(255),
                    postgresql_using='"locationId"::text')
```

- [ ] **Step 4: Ensure imports are present at top of migration file**

The file should have these imports (some may already be there from generation):
```python
from alembic import op
import sqlalchemy as sa
```

- [ ] **Step 5: Commit**

```bash
git add migrations/versions/*_add_foreign_key_constraints.py
git commit -m "feat: add alembic migration for foreign key constraints, indexes, and data cleanup"
```

---

### Task 5: Verify and deploy

- [ ] **Step 1: Verify the Flask app starts without import errors**

```bash
cd /Users/victortrinh/Documents/GitHub/certiflo-be
python -c "from app.main.model.assembly import Assembly; from app.main.model.assemblyType import AssemblyType; from app.main.model.email import Email; from app.main.model.gallery import Gallery; from app.main.model.galleryImage import GalleryImage; from app.main.model.jobPosting import JobPosting; from app.main.model.location import Location; from app.main.model.manufacturer import Manufacturer; from app.main.model.manufacturerImage import ManufacturerImage; from app.main.model.opening import Opening; from app.main.model.realization import Realization; from app.main.model.realizationType import RealizationType; from app.main.model.tanker import Tanker; from app.main.model.tankerType import TankerType; from app.main.model.telephone import Telephone; print('All models imported successfully')"
```

Expected: `All models imported successfully`

- [ ] **Step 2: Verify relationships are accessible on parent models**

```bash
python -c "
from app.main.model.assemblyType import AssemblyType
from app.main.model.gallery import Gallery
from app.main.model.location import Location
from app.main.model.manufacturer import Manufacturer
from app.main.model.realizationType import RealizationType
from app.main.model.tankerType import TankerType
assert hasattr(AssemblyType, 'assemblies'), 'AssemblyType missing assemblies relationship'
assert hasattr(Gallery, 'images'), 'Gallery missing images relationship'
assert hasattr(Location, 'emails'), 'Location missing emails relationship'
assert hasattr(Location, 'openings'), 'Location missing openings relationship'
assert hasattr(Location, 'telephones'), 'Location missing telephones relationship'
assert hasattr(Location, 'job_postings'), 'Location missing job_postings relationship'
assert hasattr(Manufacturer, 'images'), 'Manufacturer missing images relationship'
assert hasattr(RealizationType, 'realizations'), 'RealizationType missing realizations relationship'
assert hasattr(TankerType, 'tankers'), 'TankerType missing tankers relationship'
print('All relationships verified')
"
```

Expected: `All relationships verified`

- [ ] **Step 3: Run the migration against the production database**

On the Oracle Cloud VM:
```bash
cd /opt/certiflo
source .env
flask db upgrade
```

Expected: Migration applies successfully with no errors. Any orphaned rows are cleaned up in Phase 1.

- [ ] **Step 4: Final commit (if any fixups needed)**

```bash
git add -A
git commit -m "fix: address any migration or model issues found during verification"
```
