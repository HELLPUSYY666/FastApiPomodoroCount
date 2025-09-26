"""update models for AI prompts

Revision ID: 140daf5575b3
Revises: d7c426c09ec3
Create Date: 2025-09-26 15:53:34.205900

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "140daf5575b3"
down_revision: Union[str, None] = "d7c426c09ec3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # создаём типы для enum
    task_status_enum = sa.Enum(
        "COMPLETE", "PENDING", "NOT_START", name="task_status_enum"
    )
    task_priority_enum = sa.Enum("HIGH", "MEDIUM", "LOW", name="task_priority_enum")

    task_status_enum.create(op.get_bind(), checkfirst=True)
    task_priority_enum.create(op.get_bind(), checkfirst=True)

    # таблицы
    op.create_table(
        "UsersPrompts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("currently_use", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["UserProfile.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "WeekTaskPlan",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("day", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["task_id"], ["Task.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # теперь можно добавлять колонки с enum
    op.add_column(
        "Task",
        sa.Column(
            "status", task_status_enum, nullable=False, server_default="NOT_START"
        ),
    )
    op.add_column(
        "Task",
        sa.Column(
            "priority", task_priority_enum, nullable=False, server_default="MEDIUM"
        ),
    )
    op.add_column("Task", sa.Column("description", sa.Text(), nullable=True))
    op.add_column("Task", sa.Column("deadline", sa.DateTime(), nullable=False))
    op.add_column(
        "Task", sa.Column("progress", sa.Float(), nullable=False, server_default="0.0")
    )
    op.drop_column("Task", "pomodoro_count")

    op.alter_column(
        "UserProfile", "is_verified", existing_type=sa.BOOLEAN(), nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "UserProfile", "is_verified", existing_type=sa.BOOLEAN(), nullable=True
    )

    op.add_column(
        "Task",
        sa.Column("pomodoro_count", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_column("Task", "progress")
    op.drop_column("Task", "deadline")
    op.drop_column("Task", "description")
    op.drop_column("Task", "priority")
    op.drop_column("Task", "status")

    op.drop_table("WeekTaskPlan")
    op.drop_table("UsersPrompts")

    # удаляем типы, чтобы база осталась чистой
    task_status_enum = sa.Enum(
        "COMPLETE", "PENDING", "NOT_START", name="task_status_enum"
    )
    task_priority_enum = sa.Enum("HIGH", "MEDIUM", "LOW", name="task_priority_enum")

    task_status_enum.drop(op.get_bind(), checkfirst=True)
    task_priority_enum.drop(op.get_bind(), checkfirst=True)

    # ### end Alembic commands ###
