from django.conf import settings
from django.db import models


class CreditWallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credit_wallet')
    balance = models.IntegerField(default=0)
    frozen_balance = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.balance}'


class CreditLedger(models.Model):
    TYPE_RECHARGE = 'recharge'
    TYPE_CONSUME = 'consume'
    TYPE_REFUND = 'refund'
    TYPE_ADMIN_ADJUST = 'admin_adjust'
    LEDGER_TYPES = [
        (TYPE_RECHARGE, 'recharge'),
        (TYPE_CONSUME, 'consume'),
        (TYPE_REFUND, 'refund'),
        (TYPE_ADMIN_ADJUST, 'admin_adjust'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credit_ledgers')
    type = models.CharField(max_length=32, choices=LEDGER_TYPES)
    amount = models.IntegerField()
    before_balance = models.IntegerField()
    after_balance = models.IntegerField()
    related_order = models.ForeignKey('Order', null=True, blank=True, on_delete=models.SET_NULL, related_name='ledgers')
    related_job = models.ForeignKey('ProcessingJob', null=True, blank=True, on_delete=models.SET_NULL, related_name='ledgers')
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} {self.type} {self.amount}'


class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_FAILED = 'failed'
    STATUS_REFUNDED = 'refunded'
    STATUS_CANCELLED = 'cancelled'
    ORDER_STATUSES = [
        (STATUS_PENDING, 'pending'),
        (STATUS_PAID, 'paid'),
        (STATUS_FAILED, 'failed'),
        (STATUS_REFUNDED, 'refunded'),
        (STATUS_CANCELLED, 'cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    amount_yuan = models.DecimalField(max_digits=10, decimal_places=2)
    amount_cents = models.IntegerField()
    credits = models.IntegerField()
    payment_channel = models.CharField(max_length=32, default='mock')
    status = models.CharField(max_length=32, choices=ORDER_STATUSES, default=STATUS_PENDING)
    provider_order_id = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'ORDER-{self.id} {self.user} {self.status}'


class FileAsset(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='files')
    original_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=32)
    mime_type = models.CharField(max_length=128)
    size = models.BigIntegerField()
    storage_path = models.CharField(max_length=500)
    public_url = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.original_name


class ProcessingJob(models.Model):
    STATUS_QUEUED = 'queued'
    STATUS_PROCESSING = 'processing'
    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'
    STATUS_CANCELLED = 'cancelled'
    JOB_STATUSES = [
        (STATUS_QUEUED, 'queued'),
        (STATUS_PROCESSING, 'processing'),
        (STATUS_SUCCESS, 'success'),
        (STATUS_FAILED, 'failed'),
        (STATUS_CANCELLED, 'cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='processing_jobs')
    source_file = models.ForeignKey(FileAsset, null=True, blank=True, on_delete=models.SET_NULL, related_name='source_jobs')
    result_file = models.ForeignKey(FileAsset, null=True, blank=True, on_delete=models.SET_NULL, related_name='result_jobs')
    job_type = models.CharField(max_length=64)
    status = models.CharField(max_length=32, choices=JOB_STATUSES, default=STATUS_QUEUED)
    credit_cost = models.IntegerField(default=0)
    progress = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.job_type} {self.status}'


class SocialAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='social_accounts')
    platform = models.CharField(max_length=64)
    display_name = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=32, default='reserved')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['platform']

    def __str__(self):
        return f'{self.platform} - {self.user}'


class PublishJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='publish_jobs')
    platform = models.CharField(max_length=64)
    source_file = models.ForeignKey(FileAsset, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=32, default='reserved')
    message = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.platform} publish {self.status}'
