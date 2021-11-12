from django.urls import path
from pnl import views

urlpatterns = [
    path('profitandloss/monthlycos/<str:company_identifier>/<str:date>', views.COSMonthlyChart.as_view()),
    path('profitandloss/monthlysales/<str:company_identifier>/<str:date>', views.SalesMonthlyChart.as_view()),
    path('profitandloss/monthlygrossprofit/<str:company_identifier>/<str:date>', views.GrossProfitMonthlyChart.as_view()),
    path('profitandloss/monthlyebitda/<str:company_identifier>/<str:date>', views.EBIDTAMonthly.as_view()),
    path('profitandloss/monthlysgna/<str:company_identifier>/<str:date>', views.SGnA.as_view()),
    path('profitandloss/monthlynetincome/<str:company_identifier>/<str:date>', views.NetIncomeEvolution.as_view()),
    path('profitandloss/ltmsales/<str:company_identifier>/<str:date>', views.LTMSalesChart.as_view()),
    path('profitandloss/ltmebitda/<str:company_identifier>/<str:date>', views.LTMEBITDA.as_view()),
    path('profitandloss/ltmcos/<str:company_identifier>/<str:date>', views.LTMCOS.as_view()),
    path('profitandloss/ltmgrossprofit/<str:company_identifier>/<str:date>', views.LTMGrossProfit.as_view()),
    path('profitandloss/ltmnetincome/<str:company_identifier>/<str:date>', views.LTMNetIncome.as_view()),
    path('profitandloss/ltmsgna/<str:company_identifier>/<str:date>', views.LTMSGnA.as_view())
]