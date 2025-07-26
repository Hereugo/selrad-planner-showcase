from api.v1.exports.compare_years import ExportCompareYears
from api.v1.exports.dispatch_list import ExportDispatchList
from api.v1.exports.dispatch_report import ExportDispatchReport
from api.v1.exports.payment_report import ExportPaymentReport
from api.v1.exports.plans import ExportPlans


class Exports(
    ExportPlans,
    ExportDispatchReport,
    ExportDispatchList,
    ExportCompareYears,
    ExportPaymentReport,
):
    pass
