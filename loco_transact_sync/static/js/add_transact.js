// Call this function when the page loads to populate for Add Transaction

function showAddTransactionModal() {
    populateParentIds();
    document.getElementById("addTransactionModal").style.display = "block";
}

function closeAddTransactionModal() {
    document.getElementById("addTransactionModal").style.display = "none";
}

function submitAddTransaction() {
    const amountElement = document.getElementById("addAmount");
    const typeElement = document.getElementById("addType");
    const parentElement = document.getElementById("addParentId");
    
    const amount = amountElement ? amountElement.value : null;
    const type = typeElement ? typeElement.value : null;
    const parent = parentElement ? parentElement.value : null;

    if (!amount || !type) {
        alert('Amount and Type fields are mandatory.');
        return;
    }
    
    const csrfElement = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrfToken = csrfElement ? csrfElement.value : '';

    if(!csrfToken) {
        alert('CSRF token missing. Cannot proceed.');
        return;
    }

    fetch(`/transactionservice/transaction/`, {
        method: 'POST', 
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
            location.reload(); 
        } else {
            alert('Error adding transaction');
        }
    });
}