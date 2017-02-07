from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
student_counts2 = Table('student_counts2', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('school', VARCHAR(length=140)),
    Column('total_stu_count', INTEGER),
    Column('female_count', INTEGER),
    Column('male_count', INTEGER),
    Column('lim_eng_yes', INTEGER),
    Column('lim_eng_no', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['student_counts2'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['student_counts2'].create()
