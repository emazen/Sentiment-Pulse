document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('player-form');
    const resultsDiv = document.getElementById('results');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const playerName = document.getElementById('player-name').value;

        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `player_name=${encodeURIComponent(playerName)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultsDiv.innerHTML = `<p>Error: ${data.error}</p>`;
            } else {
                const timestamp = new Date().getTime();
                resultsDiv.innerHTML = `
                    <h2>Results for ${playerName}</h2>
                    <h3>Sentiment Trend</h3>
                    <img src="${data.chart_path}?t=${timestamp}" alt="Sentiment Trend">
                    <h3>Word Cloud</h3>
                    <img src="${data.word_cloud_path}?t=${timestamp}" alt="Word Cloud">
                `;
            }
        })
        .catch(error => {
            resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
        });
    });
});