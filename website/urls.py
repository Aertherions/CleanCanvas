from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_index, name='api-index'),
    path('auth/register', views.register, name='auth-register'),
    path('auth/login', views.login, name='auth-login'),
    path('auth/me', views.me, name='auth-me'),
    path('wallet', views.wallet, name='wallet'),
    path('credits/ledger', views.credit_ledger, name='credit-ledger'),
    path('orders/create', views.create_order, name='orders-create'),
    path('orders', views.orders, name='orders'),
    path('orders/<int:order_id>', views.order_detail, name='order-detail'),
    path('payments/mock/pay', views.mock_pay, name='mock-pay'),
    path('files/upload', views.upload_file, name='files-upload'),
    path('files', views.files, name='files'),
    path('jobs/create', views.create_job, name='jobs-create'),
    path('jobs', views.jobs, name='jobs'),
    path('jobs/<int:job_id>', views.job_detail, name='job-detail'),
    path('admin/overview', views.admin_overview, name='admin-overview'),
    path('admin/credits/adjust', views.admin_adjust_credits, name='admin-credits-adjust'),
]
