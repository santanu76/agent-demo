"""GENERATED from the Hub API Contract page — do not edit by hand.
This is the privacy boundary: attributes not listed here never leave
aigenie-memory. To change it, edit the contract in the Hub and
re-download."""

from aigenie_sdk import FieldSelector

SELECTOR = FieldSelector(
    client_id="acmehealth",
    version=1,
    include=('full_name', 'guardian_id', 'phone', 'plan_tier', 'primary_physician_id', 'visits_count', 'visits_recent_provider', 'visits_recent_time', 'visits_recent_visit_type'),
)
