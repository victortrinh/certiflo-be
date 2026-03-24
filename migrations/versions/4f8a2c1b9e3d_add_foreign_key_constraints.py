"""add foreign key constraints

Revision ID: 4f8a2c1b9e3d
Revises: e3c1048547d8
Create Date: 2026-03-24 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f8a2c1b9e3d'
down_revision = 'e3c1048547d8'
branch_labels = None
depends_on = None


def upgrade():
    # Phase 1 — Data cleanup (delete orphaned rows before adding constraints)

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

    # Phase 2 — Type conversion
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

    # Phase 3 — FK constraints + indexes
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

    op.create_index('ix_assemblies_assemblyTypeId', 'assemblies', ['assemblyTypeId'])
    op.create_index('ix_galleryImages_galleryId', 'galleryImages', ['galleryId'])
    op.create_index('ix_emails_locationId', 'emails', ['locationId'])
    op.create_index('ix_openings_locationId', 'openings', ['locationId'])
    op.create_index('ix_telephones_locationId', 'telephones', ['locationId'])
    op.create_index('ix_jobPostings_locationId', 'jobPostings', ['locationId'])
    op.create_index('ix_manufacturerImages_manufacturerId', 'manufacturerImages', ['manufacturerId'])
    op.create_index('ix_realizations_realizationTypeId', 'realizations', ['realizationTypeId'])
    op.create_index('ix_tankers_tankerTypeId', 'tankers', ['tankerTypeId'])


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
