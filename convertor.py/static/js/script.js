document.getElementById('converterForm').addEventListener('submit', function(event) {
    event.preventDefault();
    let from_unit = document.getElementById('from_unit').value;
    let to_unit = document.getElementById('to_unit').value;
    let amount = parseFloat(document.getElementById('amount').value);

    if (from_unit === to_unit) {
        document.getElementById('result').innerText = 'Invalid conversion: Units are the same.';
        document.getElementById('resultContainer').style.display = 'block';
        return;
    }

    fetch('/convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ from_unit, to_unit, amount }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = `Result: ${data.result}`;
        document.getElementById('resultContainer').style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
