document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('player-form');
    const resultsDiv = document.getElementById('results');
    const playerInfoSection = document.querySelector('.player-info-section');
    const analyzeButton = document.querySelector('button[type="submit"]');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const playerName = document.getElementById('player-name').value;
        const season = document.getElementById('season-selector').value;

        // Add loading animation to the button
        analyzeButton.classList.add('loading');
        analyzeButton.disabled = true;

        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `player_name=${encodeURIComponent(playerName)}&season=${encodeURIComponent(season)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultsDiv.innerHTML = `<p>Error: ${data.error}</p>`;
                playerInfoSection.style.display = 'none';
            } else {
                const sentimentClass = data.overall_sentiment > 0 ? 'positive-sentiment' : 'negative-sentiment';
                playerInfoSection.innerHTML = `
                <h2>${data.player_info.name} stats for ${season} season</h2>
                <div class="player-info">
                    <div class="player-image-container ${sentimentClass}">
                        <img src="${data.player_info.image_url}" alt="${data.player_info.name}" class="player-image">
                    </div>
                    <div class="player-stats">
                        <p>Points per game: ${data.player_info.ppg.toFixed(1)}</p>
                        <p>Rebounds per game: ${data.player_info.rpg.toFixed(1)}</p>
                        <p>Assists per game: ${data.player_info.apg.toFixed(1)}</p>
                    </div>
                </div>
            `;
                playerInfoSection.style.display = 'block';

                resultsDiv.innerHTML = `
                    <h2>Results for ${playerName} (${season} season)</h2>
                    <p class="overall-sentiment">Overall Sentiment: ${data.overall_sentiment} &nbsp;(${data.sentiment_label})</p>
                    <h3>Sentiment Trend</h3>
                    <div class="chart-container">
                        <iframe src="${data.chart_path}" width="100%" height="400px" scrolling="no"></iframe>
                    </div>
                    <h3>Points per Game</h3>
                    <div class="chart-container">
                        <iframe src="${data.points_chart_path}" width="100%" height="400px" scrolling="no"></iframe>
                    </div>
                `;
            }
        })
        .catch(error => {
            resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
            playerInfoSection.style.display = 'none';
        })
        .finally(() => {
            // Remove loading animation from the button
            analyzeButton.classList.remove('loading');
            analyzeButton.disabled = false;
        });
    });
});