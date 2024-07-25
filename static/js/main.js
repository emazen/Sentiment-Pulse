document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('player-form');
    const resultsDiv = document.getElementById('results');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const playerName = document.getElementById('player-name').value;
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;

        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `player_name=${encodeURIComponent(playerName)}&start_date=${encodeURIComponent(startDate)}&end_date=${encodeURIComponent(endDate)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultsDiv.innerHTML = `<p>Error: ${data.error}</p>`;
            } else {
                resultsDiv.innerHTML = `
                    <h2>Results for ${playerName}</h2>
                    <h3>Sentiment Trend</h3>
                    <iframe src="${data.chart_path}" width="100%" height="500px"></iframe>
                    <h3>Word Cloud</h3>
                    <img src="${data.word_cloud_path}" alt="Word Cloud">
                `;
            }
        })
        .catch(error => {
            resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
        });
    });
});