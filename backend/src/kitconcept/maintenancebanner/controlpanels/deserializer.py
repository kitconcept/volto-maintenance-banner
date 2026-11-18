from kitconcept.maintenancebanner.controlpanels.maintenance_banner import (
    MaintenanceBannerControlpanel,
)
from plone.restapi.deserializer import json_body
from plone.restapi.deserializer.controlpanels import ControlpanelDeserializeFromJson
from plone.restapi.interfaces import IDeserializeFromJson
from plone.restapi.types.utils import _deserialize_schema_values
from plone.restapi.types.utils import _format_errors
from z3c.form.interfaces import IManagerValidator
from zExceptions import BadRequest
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.schema import getFieldNames


@implementer(IDeserializeFromJson)
@adapter(MaintenanceBannerControlpanel)
class MaintenanceBannerDeserializeFromJson(ControlpanelDeserializeFromJson):
    """Pass the stored values to the field deserializers.

    The Datetime field deserializer reads the current value to decide on
    timezone handling, which fails without them.
    """

    def __call__(self, mask_validation_errors=True):
        data = json_body(self.request)
        proxy = self.registry.forInterface(self.schema, prefix=self.schema_prefix)
        current = {name: getattr(proxy, name) for name in getFieldNames(self.schema)}

        values, errors = _deserialize_schema_values(
            self.context, self.request, self.schema, data, current=current
        )
        for name, value in values.items():
            setattr(proxy, name, value)

        validator = queryMultiAdapter(
            (proxy, self.request, None, self.schema, None), IManagerValidator
        )
        for error in validator.validate(values):
            errors.append({"error": error, "message": str(error)})

        if errors:
            raise BadRequest(
                _format_errors(errors, self.request, mask=mask_validation_errors)
            )
