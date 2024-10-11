from django.urls import path
from rest_framework.routers import DefaultRouter

from core.api.v1.views import ProfileViewSet, TransactionViewSet, FinancialReportView, ExportReportCSVView, ExportTransactionsCSVView

router = DefaultRouter()

router.register(r"users", ProfileViewSet, basename="users")
router.register(r"transactions", TransactionViewSet, basename="transactions")

urlpatterns = [
                  path('financial-report/', FinancialReportView.as_view(), name='financial-report'),
                  path('export/transactions/', ExportTransactionsCSVView.as_view(), name='export-transactions-csv'),
                  path('export/report/', ExportReportCSVView.as_view(), name='export-report-csv'),
              ] + router.urls
