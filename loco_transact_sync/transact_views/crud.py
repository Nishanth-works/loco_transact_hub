from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Transaction, TransactionRelationship  # Importing TransactionRelationship
from ..serializers import TransactionSerializer
from ..transact_utils import would_form_cycle, create_transaction_relationships
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transaction(request):
    try:
        data = request.data
        potential_parent = Transaction.objects.filter(id=data.get('parent')).first()

        if potential_parent and would_form_cycle(None, potential_parent):
            return JsonResponse({"status": "error", "message": "Setting this parent would form a cycle"})

        transaction = Transaction(user=request.user, amount=data['amount'], type=data['type'], parent=potential_parent)
        transaction.save()

        create_transaction_relationships(transaction)  # Add relationships after transaction creation

        return JsonResponse({"status": "ok", "transaction_id": transaction.id})

    except KeyError:
        return JsonResponse({"status": "error", "message": "Invalid data format."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": "An error occurred: " + str(e)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_transaction_ids(request):
    try:
        user_transactions = Transaction.objects.filter(user=request.user)
        ids = [trans.id for trans in user_transactions]
        return JsonResponse(ids, safe=False)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "An error occurred: " + str(e)})

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def transaction_detail(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id, user=request.user)

        if request.method == 'GET':
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)

        elif request.method == 'PUT':
            data = json.loads(request.body)
            potential_parent = Transaction.objects.filter(id=data.get('parent')).first()
            
            if potential_parent and would_form_cycle(transaction, potential_parent):
                return JsonResponse({"status": "error", "message": "Setting this parent would form a cycle"})

            # If parent is changed, update relationships
            if 'parent' in data:
                TransactionRelationship.objects.filter(descendant=transaction).delete()
                transaction.parent = potential_parent  # Update parent temporarily for relationship creation
                create_transaction_relationships(transaction)
                transaction.parent = None  # Reset parent, as serializer will handle the saving
            
            serializer = TransactionSerializer(transaction, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"status": "ok"})
            return Response(serializer.errors, status=400)

    except ObjectDoesNotExist:
        return JsonResponse({"status": "error", "message": "Transaction not found."})
    except KeyError:
        return JsonResponse({"status": "error", "message": "Invalid data format."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": "An error occurred: " + str(e)})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_transaction(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id, user=request.user)

        children = Transaction.objects.filter(parent_id=transaction_id)
        if children.exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Transaction has dependent transactions.',
                'parent_id': transaction.parent_id
            })

        TransactionRelationship.objects.filter(descendant=transaction).delete()  # Remove relationships
        transaction.delete()

        return JsonResponse({"status": "deleted"})

    except ObjectDoesNotExist:
        return JsonResponse({"status": "error", "message": "Transaction not found."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": "An error occurred: " + str(e)})