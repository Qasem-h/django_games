from django.contrib import admin
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _


class GameFilter(admin.FieldListFilter):


    title = _("Game")

    def expected_parameters(self):
        return [self.field.name]

    def choices(self, changelist):
        value = self.used_parameters.get(self.field.name)
        yield {
            "selected": value is None,
            "query_string": changelist.get_query_string({}, [self.field.name]),
            "display": _("All"),
        }
        for lookup, title in self.lookup_choices(changelist):
            yield {
                "selected": value == force_str(lookup),
                "query_string": changelist.get_query_string(
                    {self.field.name: lookup}, []
                ),
                "display": title,
            }

    def lookup_choices(self, changelist):
        qs = changelist.model._default_manager.all()
        codes = set(
            qs.distinct()
            .order_by(self.field.name)
            .values_list(self.field.name, flat=True)
        )
        for k, v in self.field.get_choices(include_blank=False):
            if k in codes:
                yield k, v