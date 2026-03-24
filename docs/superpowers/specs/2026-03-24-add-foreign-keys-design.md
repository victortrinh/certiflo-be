# Add Foreign Key Constraints and Relationships

## Problem

The database models use plain integer/string columns to reference related tables instead of proper `db.ForeignKey()` constraints and `db.relationship()` definitions. This means:

- No referential integrity — you can save a child row pointing to a nonexistent parent
- No cascade deletes — deleting a parent leaves orphaned children
- No ORM relationships — no `gallery.images` convenience, all joins done manually
- Inconsistent types — `locationId` is `String(255)` in 3 models but `Integer` in 1

## Approach

Single big-bang migration + service layer refactor. One migration handles all schema changes atomically. Services are updated to leverage cascade deletes.

## Relationships

| Parent Model | Parent Table | Child Model | FK Column | FK Reference | Current Type | Relationship Attr |
|-------------|-------------|-------------|-----------|-------------|-------------|-------------------|
| AssemblyType | `assemblyTypes` | Assembly | assemblyTypeId | `assemblyTypes.id` | Integer | `assemblies` |
| Gallery | `galleries` | GalleryImage | galleryId | `galleries.id` | Integer | `images` |
| Location | `locations` | Email | locationId | `locations.id` | String → Integer | `emails` |
| Location | `locations` | Opening | locationId | `locations.id` | String → Integer | `openings` |
| Location | `locations` | Telephone | locationId | `locations.id` | String → Integer | `telephones` |
| Location | `locations` | JobPosting | locationId | `locations.id` | Integer | `job_postings` |
| Manufacturer | `manufacturer` | ManufacturerImage | manufacturerId | `manufacturer.id` | Integer | `images` |
| RealizationType | `realizationTypes` | Realization | realizationTypeId | `realizationTypes.id` | Integer | `realizations` |
| TankerType | `tankerTypes` | Tanker | tankerTypeId | `tankerTypes.id` | Integer | `tankers` |

Note: `manufacturer` table name is singular while all others are plural.

## Model Changes

### Child models — add `db.ForeignKey()`

Each FK column gets a foreign key constraint with `ondelete='CASCADE'`. Columns remain nullable (matching current behavior — no `nullable=False` added to avoid migration failures on existing NULL data):

```python
# Example: Assembly
assemblyTypeId = db.Column(db.Integer, db.ForeignKey('assemblyTypes.id', ondelete='CASCADE'))
```

For `Email`, `Opening`, `Telephone` — change column type from `String(255)` to `Integer` simultaneously.

### Parent models — add `db.relationship()`

Each parent gets a relationship with cascade and a backref:

```python
# Example: Gallery
images = db.relationship('GalleryImage', backref='gallery', cascade='all, delete-orphan', lazy=True)
```

Full list of parent relationship attributes:
- `AssemblyType.assemblies` (backref: `assembly_type`)
- `Gallery.images` (backref: `gallery`)
- `Location.emails` (backref: `location`)
- `Location.openings` (backref: `location`)
- `Location.telephones` (backref: `location`)
- `Location.job_postings` (backref: `location`)
- `Manufacturer.images` (backref: `manufacturer`)
- `RealizationType.realizations` (backref: `realization_type`)
- `TankerType.tankers` (backref: `tanker_type`)

Ensure no backref name collides with an existing column on the child model. Verified: no collisions exist currently.

## Migration

Single Alembic migration with 3 internal phases:

### Phase 1: Data cleanup

Before adding constraints, clean up any orphaned data:

```sql
-- Remove orphaned children referencing nonexistent parents
DELETE FROM assemblies WHERE "assemblyTypeId" NOT IN (SELECT id FROM "assemblyTypes");
DELETE FROM "galleryImages" WHERE "galleryId" NOT IN (SELECT id FROM galleries);
DELETE FROM "manufacturerImages" WHERE "manufacturerId" NOT IN (SELECT id FROM manufacturer);
DELETE FROM realizations WHERE "realizationTypeId" NOT IN (SELECT id FROM "realizationTypes");
DELETE FROM tankers WHERE "tankerTypeId" NOT IN (SELECT id FROM "tankerTypes");
DELETE FROM "jobPostings" WHERE "locationId" NOT IN (SELECT id FROM locations);

-- For String columns: remove rows with non-numeric or empty locationId, then orphans
DELETE FROM emails WHERE "locationId" !~ '^\d+$';
DELETE FROM emails WHERE CAST("locationId" AS INTEGER) NOT IN (SELECT id FROM locations);
DELETE FROM openings WHERE "locationId" !~ '^\d+$';
DELETE FROM openings WHERE CAST("locationId" AS INTEGER) NOT IN (SELECT id FROM locations);
DELETE FROM telephones WHERE "locationId" !~ '^\d+$';
DELETE FROM telephones WHERE CAST("locationId" AS INTEGER) NOT IN (SELECT id FROM locations);
```

### Phase 2: Type conversion

Convert `locationId` from `String(255)` to `Integer` in `emails`, `openings`, `telephones` tables using `USING "locationId"::integer`.

### Phase 3: Add foreign key constraints

Add `FOREIGN KEY` with `ON DELETE CASCADE` on all 9 FK columns. Add index on each FK column for cascade delete performance.

### Downgrade

Reverses: drop foreign keys and indexes, convert `locationId` back to `String(255)`.

## Service Layer Refactor

### Cascade deletes

Parent delete services automatically clean up children — no manual child deletion needed. Child delete services remain for deleting individual children.

### API contract

No changes to API response shape. The frontend currently expects flat lists from the `/all` endpoint and that stays the same. Parent `serialize()` methods must NOT include relationship data to avoid N+1 queries on the `/all` endpoint.

Note: `locationId` in `Email`, `Opening`, and `Telephone` API responses will change from string to integer after the type conversion. The frontend should be verified to handle this (most JSON parsers/frameworks handle this transparently).

### Column naming

Keep existing camelCase column names (`assemblyTypeId`, `galleryId`, etc.) to avoid breaking the frontend API contract.

## Files Changed

### Models (add ForeignKey + relationship)
- `app/main/model/assembly.py`
- `app/main/model/assemblyType.py`
- `app/main/model/email.py`
- `app/main/model/gallery.py`
- `app/main/model/galleryImage.py`
- `app/main/model/jobPosting.py`
- `app/main/model/location.py`
- `app/main/model/manufacturer.py`
- `app/main/model/manufacturerImage.py`
- `app/main/model/opening.py`
- `app/main/model/realization.py`
- `app/main/model/realizationType.py`
- `app/main/model/tanker.py`
- `app/main/model/tankerType.py`
- `app/main/model/telephone.py`

### Migration
- `migrations/versions/<new>_add_foreign_keys.py`

### Services (leverage cascade deletes)
- `app/main/service/assembly_type_service.py`
- `app/main/service/gallery_service.py`
- `app/main/service/location_service.py`
- `app/main/service/manufacturer_service.py`
- `app/main/service/realization_type_service.py`
- `app/main/service/tankerType_service.py`
