"""empty message

Revision ID: 17b925eab64d
Revises: 
Create Date: 2019-01-24 14:33:40.236654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17b925eab64d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assignments',
    sa.Column('assignmentid', sa.Integer(), nullable=False),
    sa.Column('assigneduser', sa.String(), nullable=True),
    sa.Column('createduser', sa.String(), nullable=True),
    sa.Column('assignmentname', sa.String(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.Column('roomid', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('assignmentid')
    )
    op.create_table('rooms',
    sa.Column('roomid', sa.Integer(), nullable=False),
    sa.Column('roomname', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('roomid')
    )
    op.create_table('user_registrations',
    sa.Column('entryid', sa.Integer(), nullable=False),
    sa.Column('userid', sa.String(), nullable=True),
    sa.Column('roomid', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('entryid')
    )
    op.drop_table('ROOMS')
    op.drop_table('ASSIGNMENTS')
    op.drop_table('USER_REGISTRATIONS')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('USER_REGISTRATIONS',
    sa.Column('roomId', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('userId', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('entryId', sa.INTEGER(), server_default=sa.text('nextval(\'"USER_REGISTRATIONS_entryId_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('entryId', name='USER_REGISTRATIONS_pkey')
    )
    op.create_table('ASSIGNMENTS',
    sa.Column('assignmentName', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('completed', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('roomId', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('assignedUser', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('createdUser', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('assignmentId', sa.INTEGER(), server_default=sa.text('nextval(\'"ASSIGNMENTS_assignmentId_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('assignmentId', name='ASSIGNMENTS_pkey')
    )
    op.create_table('ROOMS',
    sa.Column('roomName', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('roomId', sa.INTEGER(), server_default=sa.text('nextval(\'"ROOMS_roomId_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('roomId', name='ROOMS_pkey')
    )
    op.drop_table('user_registrations')
    op.drop_table('rooms')
    op.drop_table('assignments')
    # ### end Alembic commands ###