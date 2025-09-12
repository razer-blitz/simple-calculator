async function calculate() {
    const expression = document.getElementById('expression').value;
    if (!expression) {
        alert('Enter an expression');
        return;
    }

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expression })
        });

        if (!response.ok) {
            const error = await response.json();
            document.getElementById('result').textContent = error.error;
            return;
        }

        const data = await response.json();
        document.getElementById('result').textContent = `Result: ${data.result}`;

        // Update past calculations list
        const pastList = document.getElementById('past-list');
        pastList.innerHTML = '';
        data.past_calculations.forEach(calc => {
            const li = document.createElement('li');
            li.textContent = `${calc.expression} = ${calc.result} (${calc.timestamp})`;
            pastList.appendChild(li);
        });
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').textContent = 'An error occurred';
    }
}