"""add initial deposit check constraint

Revision ID: 9af8f69716e2
Revises: 2881ffe9711e
Create Date: 2026-10-16 15:53:08.580335

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9af8f69716e2'
down_revision: Union[str, Sequence[str], None] = '2881ffe9711e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "ck_account_opening_request_initial_deposit_non_negative",
        "account_opening_requests",
        "initial_deposit_amount >= 0",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_account_opening_request_initial_deposit_non_negative",
        "account_opening_requests",
        type_="check",
    )
