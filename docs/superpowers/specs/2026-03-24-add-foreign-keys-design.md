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

| Parent Model | Child Model | FK Column | Current Type | Relationship Attr |
|-------------|-------------|-----------|-------------|-------------------|
| AssemblyType | Assembly | assemblyTypeId | Integer | `assemblies` |
| Gallery | GalleryImage | galleryId | Integer | `images` |
| Location | Email | locationId | String → Integer | `emails` |
| Location | Opening | locationId | String → Integer | `openings` |
| Location | Telephone | locationId | String → Integer | `telephones` |
| Location | JobPosting | locationId | Integer | `job_postings` |
| Manufacturer | ManufacturerImage | manufacturerId | Integer | `images` |
| RealizationType | Realization | realizationTypeId | Integer | `realizations` |
| TankerType | Tanker | tankerTypeId | Integer | `tankers` |

## Model Changes

### Child models — add `db.ForeignKey()`

Each FK column gets a foreign key constraint with `ondelete='CASCADE'`:

```python
# Example: Assembly
assemblyTypeId = db.Column(db.Integer, db.ForeignKey('assembly_type.id', ondelete='CASCADE'), nullable=False)
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

## Migration

Single Alembic migration:

1. Convert `locationId` from `String(255)` to `Integer` in `email`, `opening`, `telephone` tables using `USING location_id::integer` (PostgreSQL)
2. Add `FOREIGN KEY` constraints with `ON DELETE CASCADE` on all 8 columns
3. Downgrade reverses: drop foreign keys, convert `locationId` back to `String(255)`

## Service Layer Refactor

### Cascade deletes

Parent delete services automatically clean up children — no manual child deletion needed. Child delete services remain for deleting individual children.

### API contract

No changes to API response shape. The frontend currently expects flat lists from `/all` endpoint and that stays the same. The refactor is backend-internal only.

### Column naming

Keep existing camelCase column names (`assemblyTypeId`, `galleryId`, etc.) to avoid breaking the frontend API contract. Can be addressed in a separate cleanup.

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
