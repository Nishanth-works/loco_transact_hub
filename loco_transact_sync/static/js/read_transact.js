



function renderTree(node) {
    let content = `<ul><li>ID: ${node.id}, Amount: ${node.amount}, Type: ${node.type}`;

    if (node.children && node.children.length > 0) {
        node.children.forEach(child => {
            content += renderTree(child);
        });
    }

    content += `</li></ul>`;
    return content;
}

function displayTransactionTree(id) {
    fetch(`/transactionservice/transaction_tree/${id}/`)
    .then(response => response.json())
    .then(data => {
        const treeContentElement = document.getElementById('transactionTreeContent');
        treeContentElement.innerHTML = renderTree(data);  // Nested lists representation

        const treeTitleElement = document.getElementById('transactionTreeId');
        treeTitleElement.textContent = id;

        // Use Bootstrap's modal method to show the modal
        $('#transactionTree').modal('show');
    })
    .catch(error => {
        console.error("Error fetching transaction tree:", error);
        alert("Error fetching the transaction structure.");
    });
}

function closeTransactionTreeModal() {
    // Use Bootstrap's modal method to hide the modal
    $('#transactionTree').modal('hide');
}



