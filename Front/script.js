document.addEventListener("DOMContentLoaded", function () {
  const searchButton = document.getElementById("searchButton");
  const searchInput = document.getElementById("searchInput");
  const resultsDiv = document.getElementById("results");
  const player = document.getElementById("music-player");
  const cover = document.getElementById("cover");
  const songTitle = document.getElementById("song-title");
  const artist = document.getElementById("artist");
  const youtubePlayer = document.getElementById("youtube-player");
  const playButton = document.getElementById("play");
  let currentVideoIndex = 0;
  let videoList = [];

  document.querySelectorAll(".emoji").forEach(button => {
      button.addEventListener("click", function () {
          const emoji = this.getAttribute("data-emoji");
          searchMusic(emoji, "");
      });
  });

  searchButton.addEventListener("click", function () {
      const query = searchInput.value.trim();
      searchMusic("", query);
  });

  function searchMusic(sentiment, customQuery) {
      const url = `http://127.0.0.1:5000/search?sentiment=${encodeURIComponent(sentiment)}&custom_query=${encodeURIComponent(customQuery)}`;

      fetch(url)
          .then(response => response.json())
          .then(data => {
              resultsDiv.innerHTML = "";
              videoList = data;

              if (data.error) {
                  resultsDiv.innerHTML = `<p>${data.error}</p>`;
                  return;
              }

              if (data.message) {
                  resultsDiv.innerHTML = `<p>${data.message}</p>`;
                  return;
              }

              data.forEach((video, index) => {
                  const videoCard = document.createElement("div");
                  videoCard.classList.add("video-card");
                  videoCard.dataset.index = index;

                  videoCard.innerHTML = `
                      <img src="${video.thumbnail}" alt="Thumbnail">
                      <div>
                          <h2>${video.title}</h2>
                          <p>${video.channel}</p>
                      </div>
                  `;

                  videoCard.addEventListener("click", function () {
                      currentVideoIndex = parseInt(this.dataset.index);
                      loadVideo(videoList[currentVideoIndex]);
                  });

                  resultsDiv.appendChild(videoCard);
              });
          })
          .catch(error => {
              console.error("Erro ao buscar vídeos:", error);
              resultsDiv.innerHTML = `<p>Erro ao buscar vídeos.</p>`;
          });
  }

  function loadVideo(video) {
      cover.src = video.thumbnail;
      songTitle.textContent = video.title;
      artist.textContent = video.channel;
      youtubePlayer.src = video.embed + "?autoplay=1";
  }
});
