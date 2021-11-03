from django.urls import path
from pnl import views

urlpatterns = [
    path('profitandloss/monthlycos/<str:comp_ID>', views.COSMonthlyChart.as_view()),
    path('profitandloss/monthlysales/<str:comp_ID>', views.SalesMonthlyChart.as_view()),
    path('profitandloss/monthlygrossprofit/<str:comp_ID>', views.GrossProfitMonthlyChart.as_view()),
    path('profitandloss/monthlyebidta/<str:comp_ID>', views.EBIDTAMonthly.as_view()),
    path('profitandloss/monthlysgna/<str:comp_ID>', views.SGnA.as_view()),
    path('profitandloss/monthlynetincome/<str:comp_ID>', views.NetIncomeEvolution.as_view())

]