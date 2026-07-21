from sqlalchemy import (
    CheckConstraint,
    Float,
    Integer,
    Text,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)

class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = "customers"


    __table_args__ = (
        CheckConstraint(
            "latitude BETWEEN -90 AND 90",
            name="ck_latitude",
        ),
        CheckConstraint(
            "longitude BETWEEN -180 AND 180",
            name="ck_longitude",
        ),
        CheckConstraint(
            "tenure_months >= 0",
            name="ck_tenure_months",
        ),
        CheckConstraint(
            "monthly_charges >= 0",
            name="ck_monthly_charges",
        ),
        CheckConstraint(
            "total_charges >= 0",
            name="ck_total_charges",
        ),
        CheckConstraint(
            "churn_value IN (0, 1)",
            name="ck_churn_value",
        ),
        CheckConstraint(
            "churn_score BETWEEN 0 AND 100",
            name="ck_churn_score",
        ),
    )

    customer_id: Mapped[str] = mapped_column(
        Text,
        primary_key=True,
        nullable=False,
    )

    country: Mapped[str | None] = mapped_column(Text)

    state: Mapped[str | None] = mapped_column(Text)

    city: Mapped[str | None] = mapped_column(Text)

    zip_code: Mapped[str | None] = mapped_column(Text)

    lat_long: Mapped[str | None] = mapped_column(Text)

    latitude: Mapped[float | None] = mapped_column(Float)

    longitude: Mapped[float | None] = mapped_column(Float)

    gender: Mapped[str | None] = mapped_column(Text)

    senior_citizen: Mapped[str | None] = mapped_column(Text)

    partner: Mapped[str | None] = mapped_column(Text)

    dependents: Mapped[str | None] = mapped_column(Text)

    tenure_months: Mapped[int | None] = mapped_column(Integer)
 
    phone_service: Mapped[str | None] = mapped_column(Text)

    multiple_lines: Mapped[str | None] = mapped_column(Text)

    internet_service: Mapped[str | None] = mapped_column(Text)

    online_security: Mapped[str | None] = mapped_column(Text)

    online_backup: Mapped[str | None] = mapped_column(Text)

    device_protection: Mapped[str | None] = mapped_column(Text)

    tech_support: Mapped[str | None] = mapped_column(Text)

    streaming_tv: Mapped[str | None] = mapped_column(Text)

    streaming_movies: Mapped[str | None] = mapped_column(Text)

    contract: Mapped[str | None] = mapped_column(Text)

    paperless_billing: Mapped[str | None] = mapped_column(Text)

    payment_method: Mapped[str | None] = mapped_column(Text)

    monthly_charges: Mapped[float | None] = mapped_column(Float)

    total_charges: Mapped[float | None] = mapped_column(Float)

    churn_label: Mapped[str] = mapped_column(

        Text,
        
        nullable=False,
    )

    churn_value: Mapped[int | None] = mapped_column(Integer)

    churn_score: Mapped[int | None] = mapped_column(Integer)

    cltv: Mapped[int | None] = mapped_column(Integer)

    churn_reason: Mapped[str | None] = mapped_column(Text)