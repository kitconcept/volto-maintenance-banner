from datetime import datetime
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


PREFIX = "kitconcept.maintenance_banner"


def migrate_date(context):
    """Move the single date to date_from as datetime and drop the old record."""
    registry = getUtility(IRegistry)
    old_key = f"{PREFIX}.date"
    if old_key not in registry.records:
        return
    date = registry.records[old_key].value
    if date:
        api.portal.set_registry_record(
            f"{PREFIX}.date_from", datetime(date.year, date.month, date.day)
        )
    del registry.records[old_key]
