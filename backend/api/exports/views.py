from .compare_years import ExportCompareYears
from .dispatch_list import ExportDispatchList
from .dispatch_report import ExportDispatchReport
from .payment_report import ExportPaymentReport
from .plans import ExportPlans


class Exports(
    ExportPlans,
    ExportDispatchReport,
    ExportDispatchList,
    ExportCompareYears,
    ExportPaymentReport,
):
    pass
