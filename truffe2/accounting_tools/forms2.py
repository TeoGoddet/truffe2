from django.forms import ModelForm

from accounting_tools.models import ExpenseClaimLine, CashBookLine, POSRequestLine


class ExpenseClaimLineForm(ModelForm):

    class Meta:
        model = ExpenseClaimLine
        exclude = ('expense_claim', 'order',)


class CashBookLineForm(ModelForm):

    class Meta:
        model = CashBookLine
        exclude = ('cashbook', 'order',)

class POSRequestLineForm(ModelForm):

    class Meta:
        model = POSRequestLine
        exclude = ('pos_request', 'order',)
