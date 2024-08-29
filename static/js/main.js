document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('player-form');
    const resultsDiv = document.getElementById('results');
    const playerInfoSection = document.querySelector('.player-info-section');
    const analyzeButton = document.querySelector('button[type="submit"]');
    const playerNameInput = document.getElementById('player-name');

    // Autocomplete for player names
    $(playerNameInput).autocomplete({
        source: function(request, response) {
            $.getJSON("/player-names", { q: request.term }, function(data) {
                response(data);
            });
        },
        minLength: 2,
        select: function(event, ui) {
            playerNameInput.value = ui.item.value;
        }
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const playerName = playerNameInput.value;
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
                resultsDiv.innerHTML = `<p class="error">${data.error}</p>`;
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
                            <p>Correlation: <span class="correlation-score" title="The correlation score measures the relationship between the player's sentiment trends and their on-court performance (points per game). A score closer to 1 indicates a stronger positive correlation, while a score closer to -1 indicates a stronger negative correlation. A score near 0 suggests little to no correlation.">${data.correlation.toFixed(2)}</span></p>
                        </div>
                    </div>
                `;
                playerInfoSection.style.display = 'block';

                resultsDiv.innerHTML = `
                    <h2>Results for ${playerName} (${season} season)</h2>
                    <p class="overall-sentiment">Overall Sentiment: <span class="sentiment-score">${data.overall_sentiment.toFixed(2)}</span> (${data.sentiment_label})</p>
                    <h3>Sentiment Trend</h3>
                    <div class="chart-container">
                        <iframe src="${data.chart_path}" width="100%" height="400px" scrolling="no"></iframe>
                    </div>
                    <h3>Points per Game</h3>
                    <div class="chart-container">
                        <iframe src="${data.points_chart_path}" width="100%" height="400px" scrolling="no"></iframe>
                    </div>
                `;

                // Initialize tooltip for correlation score
                $('.correlation-score').tooltip({
                    position: {
                        my: "center bottom-20",
                        at: "center top",
                        using: function(position, feedback) {
                            $(this).css(position);
                            $("<div>")
                                .addClass("arrow")
                                .addClass(feedback.vertical)
                                .addClass(feedback.horizontal)
                                .appendTo(this);
                        }
                    }
                });
            }
        })
        .catch(error => {
            resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
            playerInfoSection.style.display = 'none';
        })
        .finally(() => {
            // Remove loading animation from the button
            analyzeButton.classList.remove('loading');
            analyzeButton.disabled = false;
        });
    });
});