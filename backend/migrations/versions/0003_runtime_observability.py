from alembic import op
import sqlalchemy as sa
revision="0003"
down_revision="0002"
branch_labels=None
depends_on=None

def upgrade():
    op.add_column("messages", sa.Column("feedback", sa.String(20), nullable=True))
    op.add_column("providers", sa.Column("context_window", sa.Integer(), nullable=False, server_default="128000"))
    op.create_table("provider_usage",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("provider_id", sa.Integer(), sa.ForeignKey("providers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("total_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("requests", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("exact_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("estimated_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_provider_usage_user_id", "provider_usage", ["user_id"])
    op.create_index("ix_provider_usage_provider_id", "provider_usage", ["provider_id"])

def downgrade():
    op.drop_index("ix_provider_usage_provider_id", table_name="provider_usage")
    op.drop_index("ix_provider_usage_user_id", table_name="provider_usage")
    op.drop_table("provider_usage")
    op.drop_column("providers", "context_window")
    op.drop_column("messages", "feedback")
