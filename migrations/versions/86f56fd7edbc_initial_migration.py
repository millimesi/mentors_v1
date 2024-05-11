"""Initial migration

Revision ID: 86f56fd7edbc
Revises: 
Create Date: 2024-05-11 13:11:39.257264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86f56fd7edbc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('students',
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('father_name', sa.String(length=100), nullable=False),
    sa.Column('grand_father_name', sa.String(length=100), nullable=False),
    sa.Column('grade_level', sa.Integer(), nullable=True),
    sa.Column('phone_number', sa.String(length=14), nullable=False),
    sa.Column('user_id', sa.String(length=60), nullable=False),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mentor_requests',
    sa.Column('student_id', sa.String(length=60), nullable=False),
    sa.Column('mentor_id', sa.String(length=60), nullable=False),
    sa.Column('request_status', sa.Enum('Pending', 'Accepted', 'Rejected'), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['mentor_id'], ['mentors.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mentor_requests')
    op.drop_table('students')
    # ### end Alembic commands ###