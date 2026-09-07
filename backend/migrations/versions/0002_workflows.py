from alembic import op
import sqlalchemy as sa
revision="0002"; down_revision="0001"; branch_labels=None; depends_on=None
def upgrade():
 op.create_table("weather_configs",sa.Column("id",sa.Integer(),primary_key=True),sa.Column("user_id",sa.Integer(),sa.ForeignKey("users.id",ondelete="CASCADE"),unique=True),sa.Column("provider",sa.String(80),nullable=False),sa.Column("location",sa.String(160),nullable=False),sa.Column("units",sa.String(20),nullable=False),sa.Column("encrypted_key",sa.Text())); op.create_index("ix_weather_configs_user_id","weather_configs",["user_id"],unique=True)
 op.create_table("otp_challenges",sa.Column("id",sa.Integer(),primary_key=True),sa.Column("email",sa.String(255),nullable=False),sa.Column("otp_hash",sa.String(128),nullable=False),sa.Column("expires_at",sa.DateTime(timezone=True),nullable=False),sa.Column("attempts",sa.Integer(),nullable=False),sa.Column("used",sa.Boolean(),nullable=False)); op.create_index("ix_otp_challenges_email","otp_challenges",["email"])
def downgrade():
 op.drop_table("otp_challenges"); op.drop_table("weather_configs")
