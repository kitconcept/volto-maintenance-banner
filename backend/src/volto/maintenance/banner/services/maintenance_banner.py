from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service
from volto.maintenance.banner.controlpanels.maintenance_banner import (
    MaintenanceBannerControlpanel,
)


class MaintenanceBannerService(Service):
    def reply(self):
        panel = MaintenanceBannerControlpanel(self.context, self.request)
        panel.__name__ = "maintenance-banner"
        result = ISerializeToJson(panel)()
        return {
            "@id": f"{self.context.absolute_url()}/@maintenance-banner",
            **result["data"],
        }
