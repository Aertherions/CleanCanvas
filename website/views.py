import json
import mimetypes
import os
import shutil
import uuid
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core import signing
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import CreditLedger, CreditWallet, FileAsset, Order, ProcessingJob

TOKEN_SALT = 'clean-creation-mvp-auth'
TOKEN_MAX_AGE = 60 * 60 * 24 * 30
ORDER_PACKAGES = {
    10: 100,
    30: 300,
    100: 1000,
    300: 3000,
}
JOB_COSTS = {
    'image_compress': 10,
    'cover_crop': 5,
    'image_repair': 20,
    'own_watermark_repair': 20,
    'video_compress': 30,
    'video_crop': 30,
    'video_convert': 30,
    'video_repair': 30,
}
User = get_user_model()

def api_index(request):
    return JsonResponse({'message': 'Hello from Django API!', 'status': 'ok'})


def json_error(message, status=400, code='error'):
    return JsonResponse({'error': message, 'code': code}, status=status)


def read_json(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return {}


def ensure_wallet(user):
    wallet, _ = CreditWallet.objects.get_or_create(user=user, defaults={'balance': 0, 'frozen_balance': 0})
    return wallet


def create_token(user):
    return signing.dumps({'uid': user.id}, salt=TOKEN_SALT)


def token_user(request):
    header = request.headers.get('Authorization', '')
    if request.user.is_authenticated:
        return request.user
    if not header.startswith('Bearer '):
        return None
    token = header.replace('Bearer ', '', 1).strip()
    try:
        payload = signing.loads(token, salt=TOKEN_SALT, max_age=TOKEN_MAX_AGE)
    except signing.BadSignature:
        return None
    try:
        return User.objects.get(id=payload.get('uid'), is_active=True)
    except User.DoesNotExist:
        return None


def require_user(request):
    user = token_user(request)
    if not user:
        return None, json_error('Authentication required.', status=401, code='auth_required')
    ensure_wallet(user)
    return user, None


def require_admin(request):
    user, error = require_user(request)
    if error:
        return None, error
    if not (user.is_staff or user.is_superuser):
        return None, json_error('Admin access required.', status=403, code='admin_required')
    return user, None


def user_payload(user):
    wallet = ensure_wallet(user)
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_staff or user.is_superuser,
        'credits': wallet.balance,
    }


def wallet_payload(wallet):
    return {
        'balance': wallet.balance,
        'frozen_balance': wallet.frozen_balance,
        'updated_at': wallet.updated_at.isoformat(),
    }


def ledger_payload(row):
    return {
        'id': row.id,
        'user_id': row.user_id,
        'type': row.type,
        'amount': row.amount,
        'before_balance': row.before_balance,
        'after_balance': row.after_balance,
        'related_order_id': row.related_order_id,
        'related_job_id': row.related_job_id,
        'description': row.description,
        'created_at': row.created_at.isoformat(),
    }


def order_payload(order):
    return {
        'id': order.id,
        'order_no': f'CC{order.id:08d}',
        'user_id': order.user_id,
        'amount_yuan': str(order.amount_yuan),
        'amount_cents': order.amount_cents,
        'credits': order.credits,
        'payment_channel': order.payment_channel,
        'status': order.status,
        'provider_order_id': order.provider_order_id,
        'created_at': order.created_at.isoformat(),
        'paid_at': order.paid_at.isoformat() if order.paid_at else None,
    }


def file_payload(file_asset):
    return {
        'id': file_asset.id,
        'user_id': file_asset.user_id,
        'original_name': file_asset.original_name,
        'file_type': file_asset.file_type,
        'mime_type': file_asset.mime_type,
        'size': file_asset.size,
        'storage_path': file_asset.storage_path,
        'public_url': file_asset.public_url,
        'created_at': file_asset.created_at.isoformat(),
    }


def job_payload(job):
    return {
        'id': job.id,
        'user_id': job.user_id,
        'source_file_id': job.source_file_id,
        'result_file_id': job.result_file_id,
        'job_type': job.job_type,
        'status': job.status,
        'credit_cost': job.credit_cost,
        'progress': job.progress,
        'error_message': job.error_message,
        'created_at': job.created_at.isoformat(),
        'started_at': job.started_at.isoformat() if job.started_at else None,
        'finished_at': job.finished_at.isoformat() if job.finished_at else None,
        'result_file': file_payload(job.result_file) if job.result_file else None,
    }


@csrf_exempt
def register(request):
    if request.method != 'POST':
        return json_error('POST required.', status=405)
    data = read_json(request)
    account = (data.get('account') or data.get('email') or data.get('phone') or '').strip()
    password = data.get('password') or ''
    confirm_password = data.get('confirm_password') or data.get('confirmPassword') or ''
    if not account or not password:
        return json_error('Account and password are required.')
    if confirm_password and password != confirm_password:
        return json_error('Passwords do not match.')
    if User.objects.filter(username=account).exists() or User.objects.filter(email=account).exists():
        return json_error('Account already exists.', status=409, code='account_exists')

    user = User.objects.create_user(
        username=account,
        email=account if '@' in account else '',
        password=password,
    )
    ensure_wallet(user)
    return JsonResponse({'user': user_payload(user), 'message': 'Registration complete.'}, status=201)


@csrf_exempt
def login(request):
    if request.method != 'POST':
        return json_error('POST required.', status=405)
    data = read_json(request)
    account = (data.get('account') or data.get('email') or data.get('phone') or '').strip()
    password = data.get('password') or ''
    username = account
    if '@' in account:
        match = User.objects.filter(email=account).first()
        if match:
            username = match.username
    user = authenticate(request, username=username, password=password)
    if not user:
        return json_error('Invalid account or password.', status=401, code='invalid_credentials')
    token = create_token(user)
    return JsonResponse({'token': token, 'user': user_payload(user)})


def me(request):
    user, error = require_user(request)
    if error:
        return error
    return JsonResponse({'user': user_payload(user), 'wallet': wallet_payload(ensure_wallet(user))})


def wallet(request):
    user, error = require_user(request)
    if error:
        return error
    return JsonResponse({'wallet': wallet_payload(ensure_wallet(user))})


def credit_ledger(request):
    user, error = require_user(request)
    if error:
        return error
    rows = CreditLedger.objects.filter(user=user)[:100]
    return JsonResponse({'items': [ledger_payload(row) for row in rows]})


@csrf_exempt
def create_order(request):
    user, error = require_user(request)
    if error:
        return error
    if request.method != 'POST':
        return json_error('POST required.', status=405)
    data = read_json(request)
    try:
        amount_yuan = int(data.get('amount_yuan') or data.get('amount') or 0)
    except (TypeError, ValueError):
        amount_yuan = 0
    if amount_yuan not in ORDER_PACKAGES:
        return json_error('Invalid recharge package.')
    order = Order.objects.create(
        user=user,
        amount_yuan=Decimal(amount_yuan),
        amount_cents=amount_yuan * 100,
        credits=ORDER_PACKAGES[amount_yuan],
        payment_channel='mock',
        status=Order.STATUS_PENDING,
    )
    return JsonResponse({'order': order_payload(order)}, status=201)


def orders(request):
    user, error = require_user(request)
    if error:
        return error
    rows = Order.objects.filter(user=user)[:100]
    return JsonResponse({'items': [order_payload(row) for row in rows]})


def order_detail(request, order_id):
    user, error = require_user(request)
    if error:
        return error
    try:
        order = Order.objects.get(id=order_id, user=user)
    except Order.DoesNotExist:
        return json_error('Order not found.', status=404)
    return JsonResponse({'order': order_payload(order)})


@csrf_exempt
def mock_pay(request):
    user, error = require_user(request)
    if error:
        return error
    if request.method != 'POST':
        return json_error('POST required.', status=405)
    data = read_json(request)
    order_id = data.get('order_id') or data.get('id')
    if not order_id:
        return json_error('order_id is required.')
    with transaction.atomic():
        try:
            order = Order.objects.select_for_update().get(id=order_id, user=user)
        except Order.DoesNotExist:
            return json_error('Order not found.', status=404)
        if order.status == Order.STATUS_PAID:
            return JsonResponse({'order': order_payload(order), 'wallet': wallet_payload(ensure_wallet(user))})
        if order.status != Order.STATUS_PENDING:
            return json_error('Only pending orders can be paid.')
        wallet = CreditWallet.objects.select_for_update().get(user=user)
        before = wallet.balance
        wallet.balance += order.credits
        wallet.save(update_fields=['balance', 'updated_at'])
        order.status = Order.STATUS_PAID
        order.paid_at = timezone.now()
        order.provider_order_id = order.provider_order_id or f'MOCK-{order.id}-{uuid.uuid4().hex[:8]}'
        order.save(update_fields=['status', 'paid_at', 'provider_order_id'])
        CreditLedger.objects.create(
            user=user,
            type=CreditLedger.TYPE_RECHARGE,
            amount=order.credits,
            before_balance=before,
            after_balance=wallet.balance,
            related_order=order,
            description='Mock payment recharge',
        )
    return JsonResponse({'order': order_payload(order), 'wallet': wallet_payload(wallet)})


def safe_file_name(name):
    suffix = Path(name).suffix[:16]
    return f'{uuid.uuid4().hex}{suffix}'


@csrf_exempt
def upload_file(request):
    user, error = require_user(request)
    if error:
        return error
    if request.method != 'POST':
        return json_error('POST required.', status=405)
    consent = request.POST.get('consent') in ['true', '1', 'yes', 'on']
    if not consent:
        return json_error('Legal processing consent is required.', code='consent_required')
    uploaded = request.FILES.get('file')
    if not uploaded:
        return json_error('file is required.')
    max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024
    if uploaded.size > max_bytes:
        return json_error(f'File exceeds {settings.MAX_UPLOAD_MB}MB.', code='file_too_large')
    mime_type = uploaded.content_type or mimetypes.guess_type(uploaded.name)[0] or 'application/octet-stream'
    if mime_type.startswith('image/'):
        file_type = 'image'
    elif mime_type.startswith('video/'):
        file_type = 'video'
    else:
        return json_error('Only image or video files are supported in the MVP.')
    upload_dir = settings.MEDIA_ROOT / 'uploads'
    upload_dir.mkdir(parents=True, exist_ok=True)
    stored_name = safe_file_name(uploaded.name)
    relative_path = f'uploads/{stored_name}'
    absolute_path = settings.MEDIA_ROOT / relative_path
    with open(absolute_path, 'wb+') as destination:
        for chunk in uploaded.chunks():
            destination.write(chunk)
    asset = FileAsset.objects.create(
        user=user,
        original_name=uploaded.name,
        file_type=file_type,
        mime_type=mime_type,
        size=uploaded.size,
        storage_path=relative_path,
        public_url=f'{settings.MEDIA_URL}{relative_path}',
    )
    return JsonResponse({'file': file_payload(asset)}, status=201)


def files(request):
    user, error = require_user(request)
    if error:
        return error
    rows = FileAsset.objects.filter(user=user)[:100]
    return JsonResponse({'items': [file_payload(row) for row in rows]})


def make_result_file(user, source_file, job_type):
    result_dir = settings.MEDIA_ROOT / 'results'
    result_dir.mkdir(parents=True, exist_ok=True)
    source_suffix = Path(source_file.original_name).suffix if source_file else '.txt'
    result_name = f'{uuid.uuid4().hex}{source_suffix or ".txt"}'
    relative_path = f'results/{result_name}'
    absolute_path = settings.MEDIA_ROOT / relative_path
    if source_file and os.path.exists(settings.MEDIA_ROOT / source_file.storage_path):
        shutil.copyfile(settings.MEDIA_ROOT / source_file.storage_path, absolute_path)
        size = os.path.getsize(absolute_path)
        mime_type = source_file.mime_type
        file_type = source_file.file_type
        original_name = f'result-{source_file.original_name}'
    else:
        absolute_path.write_text('Mock processing result for Clean Creation MVP.', encoding='utf-8')
        size = os.path.getsize(absolute_path)
        mime_type = 'text/plain'
        file_type = 'result'
        original_name = f'{job_type}-result.txt'
    return FileAsset.objects.create(
        user=user,
        original_name=original_name,
        file_type=file_type,
        mime_type=mime_type,
        size=size,
        storage_path=relative_path,
        public_url=f'{settings.MEDIA_URL}{relative_path}',
    )


@csrf_exempt
def create_job(request):
    user, error = require_user(request)
    if error:
        return error
    if request.method != 'POST':
        return json_error('POST required.', status=405)
    data = read_json(request)
    job_type = data.get('job_type') or ''
    source_file_id = data.get('source_file_id')
    if job_type not in JOB_COSTS:
        return json_error('Invalid job_type.')
    try:
        source_file = FileAsset.objects.get(id=source_file_id, user=user) if source_file_id else None
    except FileAsset.DoesNotExist:
        return json_error('Source file not found.', status=404)
    if not source_file:
        return json_error('source_file_id is required.')
    if job_type.startswith('video_') and not settings.ENABLE_FFMPEG:
        mock_message = 'Video processing is mocked while ENABLE_FFMPEG=false.'
    else:
        mock_message = ''

    with transaction.atomic():
        wallet = CreditWallet.objects.select_for_update().get(user=user)
        cost = JOB_COSTS[job_type]
        if wallet.balance < cost:
            return json_error('Insufficient credits.', status=402, code='insufficient_credits')
        before = wallet.balance
        wallet.balance -= cost
        wallet.save(update_fields=['balance', 'updated_at'])
        job = ProcessingJob.objects.create(
            user=user,
            source_file=source_file,
            job_type=job_type,
            status=ProcessingJob.STATUS_PROCESSING,
            credit_cost=cost,
            progress=35,
            started_at=timezone.now(),
            error_message=mock_message,
        )
        CreditLedger.objects.create(
            user=user,
            type=CreditLedger.TYPE_CONSUME,
            amount=-cost,
            before_balance=before,
            after_balance=wallet.balance,
            related_job=job,
            description=f'Create {job_type} task',
        )
        result_file = make_result_file(user, source_file, job_type)
        job.result_file = result_file
        job.status = ProcessingJob.STATUS_SUCCESS
        job.progress = 100
        job.finished_at = timezone.now()
        job.save(update_fields=['result_file', 'status', 'progress', 'finished_at', 'error_message'])
    return JsonResponse({'job': job_payload(job), 'wallet': wallet_payload(wallet)}, status=201)


def jobs(request):
    user, error = require_user(request)
    if error:
        return error
    rows = ProcessingJob.objects.filter(user=user).select_related('result_file')[:100]
    return JsonResponse({'items': [job_payload(row) for row in rows]})


def job_detail(request, job_id):
    user, error = require_user(request)
    if error:
        return error
    try:
        job = ProcessingJob.objects.select_related('result_file').get(id=job_id, user=user)
    except ProcessingJob.DoesNotExist:
        return json_error('Job not found.', status=404)
    return JsonResponse({'job': job_payload(job)})


def admin_overview(request):
    admin_user, error = require_admin(request)
    if error:
        return error
    users = []
    for user in User.objects.all().order_by('-date_joined')[:100]:
        users.append(user_payload(user))
    payload = {
        'admin': user_payload(admin_user),
        'users': users,
        'orders': [order_payload(row) for row in Order.objects.all()[:100]],
        'ledger': [ledger_payload(row) for row in CreditLedger.objects.select_related('user')[:100]],
        'files': [file_payload(row) for row in FileAsset.objects.all()[:100]],
        'jobs': [job_payload(row) for row in ProcessingJob.objects.select_related('result_file')[:100]],
        'stats': {
            'users': User.objects.count(),
            'orders': Order.objects.count(),
            'paid_orders': Order.objects.filter(status=Order.STATUS_PAID).count(),
            'ledger_rows': CreditLedger.objects.count(),
            'files': FileAsset.objects.count(),
            'jobs': ProcessingJob.objects.count(),
        },
    }
    return JsonResponse(payload)


@csrf_exempt
def admin_adjust_credits(request):
    admin_user, error = require_admin(request)
    if error:
        return error
    if request.method != 'POST':
        return json_error('POST required.', status=405)
    data = read_json(request)
    user_id = data.get('user_id')
    amount = int(data.get('amount') or 0)
    description = data.get('description') or f'Admin adjustment by {admin_user.username}'
    if not user_id or amount == 0:
        return json_error('user_id and non-zero amount are required.')
    with transaction.atomic():
        try:
            target = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return json_error('User not found.', status=404)
        wallet = CreditWallet.objects.select_for_update().get(user=target)
        if wallet.balance + amount < 0:
            return json_error('Adjustment would make balance negative.', status=400)
        before = wallet.balance
        wallet.balance += amount
        wallet.save(update_fields=['balance', 'updated_at'])
        CreditLedger.objects.create(
            user=target,
            type=CreditLedger.TYPE_ADMIN_ADJUST,
            amount=amount,
            before_balance=before,
            after_balance=wallet.balance,
            description=description,
        )
    return JsonResponse({'user': user_payload(target), 'wallet': wallet_payload(wallet)})
