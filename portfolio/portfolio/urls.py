"""portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf.urls.static import static
from portfolio.views import *
from portfolioapp.views import *
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', LoginView.as_view(),name='login'),
    url(r'^(?:/)?(?:index.htm)?(?:l)?(?:l)?$', PortfolioHomeView.as_view(), name='portfolio_home'),
    url(r'^portfolio/clients$', PortfolioClientsView.as_view(),name='portfolio_clients'),
    url(r'^portfolio/adjust-stocks$', PortfolioAdjustStocksView.as_view(),name='portfolio_adjust_stocks'),
    url(r'^portfolio/new-investment-calculation$', NewInvestmentCalucationView.as_view(),name='new_investment_calculation'),
    url(r'^portfolio/ledger$', PortfolioNotesView.as_view(),name='portfolio_ledger'),
    url(r'^portfolio/notes$', PortfolioNotesView.as_view(),name='portfolio_notes'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
