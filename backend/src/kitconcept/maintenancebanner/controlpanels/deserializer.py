from kitconcept.maintenancebanner.controlpanels.maintenance_banner import (
    MaintenanceBannerControlpanel,
)
from plone.restapi.deserializer import json_body
from plone.restapi.deserializer.controlpanels import ControlpanelDeserializeFromJson
from plone.restapi.deserializer.controlpanels import FakeDXContext
from plone.restapi.interfaces import IDeserializeFromJson
from plone.restapi.interfaces import IFieldDeserializer
from z3c.form.interfaces import IManagerValidator
from zExceptions import BadRequest
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.i18n import translate
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface.exceptions import Invalid
from zope.schema import getFields
from zope.schema.interfaces import ValidationError


@implementer(IDeserializeFromJson)
@adapter(MaintenanceBannerControlpanel)
class MaintenanceBannerDeserializeFromJson(ControlpanelDeserializeFromJson):
    """Give the field deserializers a context with the stored values.

    The Datetime field deserializer reads the current value through the
    schema to decide on timezone handling. plone.restapi passes an empty
    context that does not provide the schema, which raises a TypeError.
    """

    def _context(self, proxy, fields):
        context = FakeDXContext()
        for name in fields:
            setattr(context, name, getattr(proxy, name))
        alsoProvides(context, self.schema)
        return context

    def __call__(self, mask_validation_errors=True):
        data = json_body(self.request)
        proxy = self.registry.forInterface(self.schema, prefix=self.schema_prefix)
        fields = getFields(self.schema)
        context = self._context(proxy, fields)

        values = {}
        errors = []
        for name, field in fields.items():
            if field.readonly or name not in data:
                continue
            deserializer = queryMultiAdapter(
                (field, context, self.request), IFieldDeserializer
            )
            try:
                value = deserializer(data[name])
                field.validate(value)
            except ValidationError as e:
                errors.append({"message": e.doc(), "field": name, "error": e})
            except (ValueError, Invalid) as e:
                errors.append({"message": str(e), "field": name, "error": e})
            else:
                values[name] = value
                setattr(proxy, name, value)

        validator = queryMultiAdapter(
            (proxy, self.request, None, self.schema, None), IManagerValidator
        )
        for error in validator.validate(values):
            errors.append({"error": error, "message": str(error)})

        if errors:
            self._raise(errors, mask_validation_errors)

    def _raise(self, errors, mask_validation_errors):
        for error in errors:
            if mask_validation_errors:
                error["error"] = "ValidationError"
            error["message"] = translate(error["message"], context=self.request)
        raise BadRequest(errors)
