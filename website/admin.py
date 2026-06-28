from django.contrib import admin

from .models import CreditLedger, CreditWallet, FileAsset, Order, ProcessingJob, PublishJob, SocialAccount


@admin.register(CreditWallet)
class CreditWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'frozen_balance', 'updated_at')
    search_fields = ('user__username', 'user__email')


@admin.register(CreditLedger)
class CreditLedgerAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'amount', 'before_balance', 'after_balance', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('user__username', 'description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount_yuan', 'credits', 'payment_channel', 'status', 'created_at', 'paid_at')
    list_filter = ('status', 'payment_channel', 'created_at')
    search_fields = ('user__username', 'provider_order_id')


@admin.register(FileAsset)
class FileAssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'original_name', 'file_type', 'mime_type', 'size', 'created_at')
    list_filter = ('file_type', 'mime_type', 'created_at')
    search_fields = ('user__username', 'original_name')


@admin.register(ProcessingJob)
class ProcessingJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'job_type', 'status', 'credit_cost', 'progress', 'created_at', 'finished_at')
    list_filter = ('status', 'job_type', 'created_at')
    search_fields = ('user__username', 'job_type', 'error_message')


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'display_name', 'status', 'created_at')
    list_filter = ('platform', 'status')
    search_fields = ('user__username', 'display_name')


@admin.register(PublishJob)
class PublishJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'status', 'created_at')
    list_filter = ('platform', 'status')
    search_fields = ('user__username', 'message')
