from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
student_counts = Table('student_counts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('school', String(length=140)),
    Column('total_stu_count', Integer),
    Column('female_count', Integer),
    Column('male_count', Integer),
    Column('lim_eng_yes', Integer),
    Column('lim_eng_no', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['student_counts'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['student_counts'].drop()
