from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer
from django.http import JsonResponse
import json


def would_form_cycle(child, potential_parent):
    # Base cases
    if not potential_parent:
        return False
    if child == potential_parent:
        return True
    
    current = potential_parent
    while current.parent:
        if current.parent == child:
            return True
        current = current.parent
    
    return False

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transaction(request):
    data = request.data
    potential_parent = Transaction.objects.filter(id=data.get('parent')).first()

    # Check for cycle
    if would_form_cycle(None, potential_parent):
        return JsonResponse({"status": "error", "message": "Setting this parent would form a cycle"})

    transaction = Transaction(user=request.user, amount=data['amount'], type=data['type'], parent=potential_parent)
    transaction.save()
    return JsonResponse({"status": "ok", "transaction_id": transaction.id})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_transaction_ids(request):
    user_transactions = Transaction.objects.filter(user=request.user)
    ids = [trans.id for trans in user_transactions]
    return JsonResponse(ids, safe=False)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def transaction_detail(request, transaction_id):
    if request.method == 'GET':
        transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = json.loads(request.body)
        transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        potential_parent = Transaction.objects.filter(id=data.get('parent')).first()
        # Check for cycle
        if would_form_cycle(transaction, potential_parent):
            return JsonResponse({"status": "error", "message": "Setting this parent would form a cycle"})
        
        
        serializer = TransactionSerializer(transaction, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": "ok"})
        return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_transaction(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id, user=request.user)

    children = Transaction.objects.filter(parent_id=transaction_id)
    if children.exists():
        return JsonResponse({
            'status': 'error',
            'message': 'Transaction has dependent transactions.',
            'parent_id': transaction.parent_id
        })

    transaction.delete()
    return JsonResponse({"status": "deleted"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transaction_by_type(request, type):
    transactions = Transaction.objects.filter(type=type, user=request.user)
    ids = [trans.id for trans in transactions]
    return JsonResponse(ids, safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transaction_sum(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id, user=request.user)
    
    def calculate_sum(trans):
        total = trans.amount
        for child in trans.transaction_set.all():
            total += calculate_sum(child)
        return total

    sum_val = calculate_sum(transaction)
    return JsonResponse({"sum": sum_val})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def has_dependents(request, transaction_id):
    # Check for child transactions
    children = Transaction.objects.filter(parent_id=transaction_id)
    transaction = Transaction.objects.get(id=transaction_id)

    if children.exists():
        return JsonResponse({
            'has_children': True,
            'parent_id': transaction.parent_id
        })

    return JsonResponse({
        'has_children': False,
        'parent_id': transaction.parent_id
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_potential_parents(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id, user=request.user) if transaction_id != 'null' else None
    all_transactions = Transaction.objects.filter(user=request.user)
    potential_parents = [trans.id for trans in all_transactions if not would_form_cycle(transaction, trans)]
    return JsonResponse(potential_parents, safe=False)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def reassign_children(request, transaction_id):
    data = request.data
    new_parent_id = data.get('parent')

    children = Transaction.objects.filter(parent_id=transaction_id)
    children.update(parent_id=new_parent_id)

    return JsonResponse({'status': 'ok'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_tree(request, transaction_id):
    def construct_tree(trans):
        return {
            "id": trans.id,
            "amount": trans.amount,
            "type": trans.type,
            "parent": trans.parent.id if trans.parent else None,
            "children": [construct_tree(child) for child in Transaction.objects.filter(parent=trans)]
        }

    try:
        transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        return JsonResponse(construct_tree(transaction))
    except Transaction.DoesNotExist:
        return JsonResponse({"error": "Transaction not found"}, status=404)

# You can also add the DRF's ViewSets and Routers for CRUD operations