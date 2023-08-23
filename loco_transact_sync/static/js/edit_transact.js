function editTransaction(id) {
    document.getElementById("editModal").style.display = "block";
    document.getElementById("editTransactionId").textContent = id;
    populateParentIds(id);  // Populate excluding the current ID

}

function closeEditModal() {
    document.getElementById("editModal").style.display = "none";
}

function submitEdit() {
    const idElement = document.getElementById("editTransactionId");
    const amountElement = document.getElementById("editAmount");
    const typeElement = document.getElementById("editType");
    const parentElement = document.getElementById("editParentId");
    
    const transactionId = idElement ? idElement.textContent.trim() : null;
    const amount = amountElement ? amountElement.value : null;
    const type = typeElement ? typeElement.value : null;
    const parent = parentElement ? parentElement.value : null;

    if (!transactionId || !amount || !type) {
        alert('Transaction ID, Amount, and Type fields are mandatory.');
        return;
    }
    
    const csrfElement = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrfToken = csrfElement ? csrfElement.value : '';

    if(!csrfToken) {
        alert('CSRF token missing. Cannot proceed.');
        return;
    }

    fetch(`/transactionservice/transaction/${transactionId}/`, {
        method: 'PUT',
        body: JSON.stringify({
            amount: amount,
            type: type,
            parent: parent || null  // if parent is empty or null, send null
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        if(response.ok) {
            location.reload();  // Reload the page to see changes
        } else {
            alert('Error updating transaction');
        }
    });
}