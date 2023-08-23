function populateParentIds(excludeId) {
    // excludeId is optional and is used for edit transaction
    let endpoint = '/transactionservice/all_transaction_ids/';  // Default endpoint

    if (excludeId !== undefined) {
        endpoint = `/transactionservice/potential_parents/${excludeId}/`;
}

    fetch(endpoint)
    .then(response => response.json())
    .then(data => {
        const addParentIdSelect = document.getElementById('addParentId');
        const editParentIdSelect = document.getElementById('editParentId');
        
        // Clear previous options
        addParentIdSelect.innerHTML = '<option value="">Select Parent ID</option>';
        editParentIdSelect.innerHTML = '<option value="">Select Parent ID</option>';

        data.forEach(id => {
            if (id !== excludeId) {  // Exclude the current ID for edit
                addParentIdSelect.innerHTML += `<option value="${id}">${id}</option>`;
                editParentIdSelect.innerHTML += `<option value="${id}">${id}</option>`;
            }
        });
    });
}

function calculateSum(id) {
    fetch(`/transactionservice/sum/${id}/`)
    .then(response => response.json())
    .then(data => {
        alert(`Sum for Transaction ID ${id}: ${data.sum}`);

        // Display the transaction tree after displaying the sum
        displayTransactionTree(id);
    })
    .catch(error => {
        console.error("Error fetching sum:", error);
        alert("Error fetching sum for the transaction.");
    });
}


function reassignChildren(transactionId, newParentId) {
    const csrfElement = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrfToken = csrfElement ? csrfElement.value : null;

    if(!csrfToken) {
        alert('CSRF token missing. Cannot proceed.');
        return;
    }

    fetch(`/transactionservice/reassign_children/${transactionId}/`, {
        method: 'PUT',
        body: JSON.stringify({
            parent: newParentId
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        if(!response.ok) {
            alert('Error reassigning children transactions');
        }
    })
    .catch(error => {
        console.error("Error reassigning children transactions:", error);
        alert("Error reassigning children transactions.");
    });
}