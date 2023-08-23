function deleteTransaction(id) {
    fetch(`/transactionservice/has_dependents/${id}/`)
    .then(response => response.json())
    .then(data => {
        if(data.has_children) {
            const choice = confirm("This transaction has dependent transactions. Do you still want to delete? If you choose OK, the dependent transactions' parent will be set to null or reassigned to the current transaction's parent, based on your preference.");
            
            if (choice) {
                if(data.parent_id) {
                    const reassignChoice = confirm("Do you want to reassign the child transactions to the current transaction's parent? If you choose Cancel, the child transactions' parent ID will be set to null.");
                    
                    if(reassignChoice) {
                        // Reassign the child transactions to the current transaction's parent
                        reassignChildren(id, data.parent_id);
                    } else {
                        // Set the child transactions' parent ID to null
                        reassignChildren(id, null);
                    }
                }
                else {
                    reassignChildren(id, null);
                }
                proceedToDelete(id);  // Finally, delete the transaction
            }
        } else {
            const choice = confirm("Are you sure you want to delete this transaction?");
            if(choice) {
                proceedToDelete(id);
            }
        }
    })
    .catch(error => {
        console.error("Error checking dependent transactions:", error);
        alert("Error checking dependent transactions.");
    });
}

function proceedToDelete(id) {
    const csrfElement = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrfToken = csrfElement ? csrfElement.value : null;

    if(!csrfToken) {
        alert('CSRF token missing. Cannot proceed.');
        return;
    }

    fetch(`/transactionservice/delete_transaction/${id}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        if(response.ok) {
            location.reload();  // Reload the page to see changes
        } else {
            alert('Error deleting transaction');
        }
    })
    .catch(error => {
        console.error("Error deleting transaction:", error);
        alert("Error deleting the transaction.");
    });
}
