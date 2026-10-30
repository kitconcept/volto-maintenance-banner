from kitconcept.maintenancebanner import PACKAGE_NAME


class TestSetupInstall:
    def test_addon_installed(self, installer):
        """Test if kitconcept.maintenancebanner is installed."""

        assert installer.is_product_installed(PACKAGE_NAME) is True

    def test_browserlayer(self, browser_layers):
        """Test that IBrowserLayer is registered."""
        from kitconcept.maintenancebanner.interfaces import IBrowserLayer

        assert IBrowserLayer in browser_layers
