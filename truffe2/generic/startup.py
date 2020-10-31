
from generic.models import GenericModel


def startup():
    """Create urls, models and cie at startup"""

    GenericModel.startup()
