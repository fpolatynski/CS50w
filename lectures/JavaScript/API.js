
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('form').onsubmit = () => {
        fetch('https://open.er-api.com/v6/latest/USD')
        .then(response => response.json())
        .then(data => {
            const currency = document.querySelector('#currency').value.toUpperCase();
            const rate = data.rates[currency];
            if (rate !== undefined){
               document.querySelector('h1').innerHTML = `1 USD is equal to ${rate.toFixed(3)} ${currency}`;
            } else {
                document.querySelector('h1').innerHTML = 'invalid'
            }
        })
        .catch(error => {
            console.log('Error:', error);
        });

        return false;
    }
});
