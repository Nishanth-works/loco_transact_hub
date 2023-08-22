from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..models import Transaction
from django.http import JsonResponse

from ..models import TransactionRelationship

def would_form_cycle(child, potential_parent):
    """Check if setting potential_parent as the parent of child would create a cycle"""
    if child and potential_parent:
        return TransactionRelationship.objects.filter(ancestor=child, descendant=potential_parent).exists()
    return False

def transaction_generator(trans):
    """Generator to yield amounts for the transaction and its descendants"""
    descendant_relations = TransactionRelationship.objects.filter(ancestor=trans)
    for relation in descendant_relations:
        yield relation.descendant.amount

def calculate_sum(trans):
    """Calculate the sum of amounts for the transaction and its descendants"""
    return sum(transaction_generator(trans))


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
        children = TransactionRelationship.objects.filter(ancestor=transaction, depth=1)
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
        children_relations = TransactionRelationship.objects.filter(ancestor__id=transaction_id, depth=1)
        for relation in children_relations:
            relation.descendant.parent_id = new_parent_id
            relation.descendant.save()
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})