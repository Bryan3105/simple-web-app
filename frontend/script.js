document.getElementById('calculatorForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    const number1 = document.getElementById('number1').value;
    const number2 = document.getElementById('number2').value;

    // Basic client-side validation
    if (!number1 || !number2) {
        alert('Please enter both numbers.');
        return;
    }

    // Send data to the backend (replace with your actual API endpoint)
    fetch('/api/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ number1: number1, number2: number2 })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').textContent = `Sum: ${data.sum}`;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').textContent = 'An error occurred.';
    });
});
