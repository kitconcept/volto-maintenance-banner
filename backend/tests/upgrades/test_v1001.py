from datetime import date
from kitconcept.maintenancebanner.upgrades.v1001 import migrate_date
from plone import api
from plone.registry import field
from plone.registry.record import Record

import pytest


OLD_KEY = "kitconcept.maintenance_banner.date"


class TestUpgradeV1001:
    @pytest.fixture(autouse=True)
    def _setup(self, portal):
        self.registry = portal.portal_registry

    def add_old_record(self, value):
        self.registry.records[OLD_KEY] = Record(field.Date(required=False), value)

    def test_date_moved_to_date_from(self):
        self.add_old_record(date(2026, 10, 31))
        migrate_date(None)
        assert OLD_KEY not in self.registry.records
        assert api.portal.get_registry_record(
            "kitconcept.maintenance_banner.date_from"
        ) == date(2026, 10, 31)

    def test_empty_date_removed(self):
        self.add_old_record(None)
        migrate_date(None)
        assert OLD_KEY not in self.registry.records
        assert (
            api.portal.get_registry_record("kitconcept.maintenance_banner.date_from")
            is None
        )

    def test_no_old_record(self):
        migrate_date(None)
        assert OLD_KEY not in self.registry.records
