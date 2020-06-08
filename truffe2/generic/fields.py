from functools import partial

from django.forms.models import ModelChoiceIterator, ModelChoiceField
from django.forms.fields import ChoiceField


class ModelChoiceWithObjAndFilterIterator(ModelChoiceIterator):
    def __init__(self, field, filter, choice_builder):
        super(ModelChoiceWithObjAndFilterIterator, self).__init__(field)
        self.filter = filter if filter else lambda obj: True
        self.choice_builder = choice_builder if choice_builder else lambda obj, prepare_value, label_from_instance: (prepare_value(obj), label_from_instance(obj))

    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = self.queryset.all().filter(self.filter).map(self.choice)
            for choice in self.field.choice_cache:
                yield choice
        else:
            for obj in self.queryset.all():
                if(self.filter(obj)):
                    yield self.choice(obj)

    def choice(self, obj):
        return self.field.choice_builder(obj, self.field.prepare_value, self.field.label_from_instance)

class ModelChoiceWithObjAndFilterField(ModelChoiceField):
    def __init__(self, filter=None, choice_builder=None, label_from_instance=None, *args, **kwargs):
        self.filter = filter
        self.choice_builder = choice_builder
        super(ModelChoiceWithObjAndFilterField, self).__init__(*args, **kwargs)
        if label_from_instance:
            self.label_from_instance = label_from_instance

    def _get_choices(self):
        # If self._choices is set, then somebody must have manually set
        # the property self.choices. In this case, just return self._choices.
        if hasattr(self, '_choices'):
            return self._choices

        # Otherwise, execute the QuerySet in self.queryset to determine the
        # choices dynamically. Return a fresh ModelChoiceIterator that has not been
        # consumed. Note that we're instantiating a new ModelChoiceIterator *each*
        # time _get_choices() is called (and, thus, each time self.choices is
        # accessed) so that we can ensure the QuerySet has not been consumed. This
        # construct might look complicated but it allows for lazy evaluation of
        # the queryset.
        return ModelChoiceWithObjAndFilterIterator(self, self.filter, self.choice_builder)

    choices = property(_get_choices, ChoiceField._set_choices)
