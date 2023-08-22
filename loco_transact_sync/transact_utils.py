from .models import Transaction

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

def transaction_generator(trans):
    stack = [trans]
    
    while stack:
        current_trans = stack.pop()
        yield current_trans.amount
        stack.extend(current_trans.transaction_set.all())

def calculate_sum(trans):
    return sum(transaction_generator(trans))

def construct_tree(trans):
        return {
            "id": trans.id,
            "amount": trans.amount,
            "type": trans.type,
            "parent": trans.parent.id if trans.parent else None,
            "children": [construct_tree(child) for child in Transaction.objects.filter(parent=trans)]
        }
