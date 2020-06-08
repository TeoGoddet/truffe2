from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.html import format_html, escape
from django.forms.util import flatatt
from django.core.urlresolvers import reverse
from django.template import Context
from django.template.loader import get_template
from django.forms.widgets import Select


from itertools import chain


class LogoSelect(Select):

    def get_option(self, selected_choices, option_value, option_label, logo):
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected = True
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected = False
        return {'value': escape(option_value),
                'selected': selected,
                'label': escape(option_label),
                'img_src': mark_safe(reverse('communication.views.logo_file_get_thumbnail', args=[logo.pk]) + "?w=50&h=30" if logo else '')}

    def get_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        index = -1
        for option_value, option_label, logo_url, unit_pk, unit_name in chain(self.choices, choices):
            if index == -1 or escape(unicode(unit_pk)) != output[index]['unit_pk']:
                output.append({'label': escape(unit_name), 'unit_pk': escape(unicode(unit_pk)), 'options': []})
                index += 1
            output[index]['options'].append(self.get_option(selected_choices, option_value, option_label, logo_url))
        return output

    def render(self, name, value, attrs=None, choices=()):
        final_attrs = self.build_attrs(attrs, name=name)
        optgroups = self.get_options(choices, [value])

        return mark_safe(get_template('communication/widgets/logo_select.html')
                         .render(Context({'attrs': flatatt(final_attrs),
                                          'id': final_attrs['id'],
                                          'optgroups': optgroups})))
