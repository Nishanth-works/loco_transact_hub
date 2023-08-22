from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..models import Transaction
from django.http import JsonResponse
from ..transact_utils import would_form_cycle, calculate_sum


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transaction_by_type(request, type):
    try:
        transactions = Transaction.objects.filter(type=type, user=request.user)
        ids = [trans.id for trans in transactions]
        return JsonResponse(ids, safe=False)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transaction_sum(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        sum_val = calculate_sum(transaction)
        return JsonResponse({"sum": sum_val})
    except ObjectDoesNotExist:
        return JsonResponse({"status": "error", "message": "Transaction not found."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def has_dependents(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        children = Transaction.objects.filter(parent_id=transaction_id)
        return JsonResponse({
            'has_children': children.exists(),
            'parent_id': transaction.parent_id
        })
    except ObjectDoesNotExist:
        return JsonResponse({"status": "error", "message": "Transaction not found."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_potential_parents(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id, user=request.user) if transaction_id != 'null' else None
        all_transactions = Transaction.objects.filter(user=request.user)
        potential_parents = [trans.id for trans in all_transactions if not would_form_cycle(transaction, trans)]
        return JsonResponse(potential_parents, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({"status": "error", "message": "Transaction not found."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def reassign_children(request, transaction_id):
    try:
        data = request.data
        new_parent_id = data.get('parent')
        children = Transaction.objects.filter(parent_id=transaction_id)
        children.update(parent_id=new_parent_id)
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})