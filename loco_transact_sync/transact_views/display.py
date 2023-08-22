from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..models import Transaction
from django.http import JsonResponse
from ..transact_utils import construct_tree


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_tree(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        return JsonResponse(construct_tree(transaction))
    except Transaction.DoesNotExist:
        return JsonResponse({"error": "Transaction not found"}, status=404)