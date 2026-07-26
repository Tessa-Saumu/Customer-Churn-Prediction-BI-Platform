"""
Issue #14 -- Real Integration -- app/services/kpi_service.py

NEW FILE (flagged in PR Notes).

Why this exists / cross-team flag: the issue requires /kpis to be
"connected to the finalized analytics data source." sql/views.sql
(Salome, Issue #9) defines view_churn_by_contract and
view_churn_by_tenure_bucket -- both grouped/bucketed views, neither of
which is a single-row summary matching the KPI shape Issue #10's
placeholder committed to (customer_count, overall_churn_rate,
retention_rate, average_monthly_charges, total_monthly_revenue). No
view in views.sql produces that shape directly.

Rather than block on a new SQL view being added, or reshape the
response (forbidden -- Project_Specification.md section 2.3 explicitly
prohibits changing /kpis' response shape as part of this PR), this
computes the same KPI values in Python from
CustomerRepository.get_all(), which is real, database-backed data --
satisfying "no placeholder data remains connected to production
endpoints" without touching the public contract.

Per Project_Specification.md section 4, this is exactly the kind of
mid-sprint interface question that should be flagged to every
downstream owner directly, not just left in a Notes field: recommend
Salome add a dedicated KPI view (e.g. view_executive_kpis) so this
logic can move into SQL. Flagging in PR Notes as a follow-up
suggestion, not blocking this PR on it.
"""

import logging
from typing import Any

from app.repository.customer_repository import CustomerRepository

logger = logging.getLogger(__name__)


def get_kpis(repository: CustomerRepository | None = None) -> dict[str, Any]:
    """
    Computes executive KPIs from real customer data:
    customer_count, overall_churn_rate, retention_rate,
    average_monthly_charges, total_monthly_revenue.

    Shape matches Issue #10's placeholder exactly, per the "no public
    contract changes" rule for Issue #14.
    """
    repo = repository or CustomerRepository()
    customers = repo.get_all()

    customer_count = len(customers)
    if customer_count == 0:
        logger.warning("get_kpis: no customers found in database")
        return {
            "customer_count": 0,
            "overall_churn_rate": 0.0,
            "retention_rate": 0.0,
            "average_monthly_charges": 0.0,
            "total_monthly_revenue": 0.0,
        }

    churned = sum(1 for c in customers if c.get("churn_label") == "Yes")
    total_monthly_charges = sum(float(c.get("monthly_charges") or 0.0) for c in customers)

    overall_churn_rate = round(100.0 * churned / customer_count, 2)
    retention_rate = round(100.0 - overall_churn_rate, 2)
    average_monthly_charges = round(total_monthly_charges / customer_count, 2)
    total_monthly_revenue = round(total_monthly_charges, 2)

    result = {
        "customer_count": customer_count,
        "overall_churn_rate": overall_churn_rate,
        "retention_rate": retention_rate,
        "average_monthly_charges": average_monthly_charges,
        "total_monthly_revenue": total_monthly_revenue,
    }
    logger.info("Computed real KPIs from %d customers: %s", customer_count, result)
    return result