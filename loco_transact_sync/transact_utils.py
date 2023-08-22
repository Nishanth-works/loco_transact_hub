from .models import TransactionRelationship

# Using closure table to check if adding a parent forms a cycle
def would_form_cycle(child, potential_parent):
    return TransactionRelationship.objects.filter(ancestor=child, descendant=potential_parent).exists()

# Helper function to create transaction relationships
def create_transaction_relationships(transaction):
    # Relationship of transaction to itself
    TransactionRelationship.objects.create(ancestor=transaction, descendant=transaction, depth=0)
    
    # Relationships based on the parent's relationships
    if transaction.parent:
        parent_relations = TransactionRelationship.objects.filter(descendant=transaction.parent)
        for relation in parent_relations:
            TransactionRelationship.objects.create(
                ancestor=relation.ancestor, 
                descendant=transaction, 
                depth=relation.depth + 1
            )

def construct_tree(trans):
    child_relations = TransactionRelationship.objects.filter(ancestor=trans, depth=1)
    children_transactions = [relation.descendant for relation in child_relations]

    return {
        "id": trans.id,
        "amount": trans.amount,
        "type": trans.type,
        "parent": trans.parent.id if trans.parent else None,
        "children": [construct_tree(child) for child in children_transactions]
    }
