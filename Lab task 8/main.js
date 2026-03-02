const qInput = document.getElementById('q');
const btn = document.getElementById('searchBtn');
const results = document.getElementById('results');

btn.addEventListener('click', doSearch);
qInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') doSearch(); });

let currentAudio = null;

function doSearch(){
  const q = qInput.value.trim();
  if (!q) return;
  results.innerHTML = `<p style="color:#9aa4b2">Loading...</p>`;
  fetch(`/search?q=${encodeURIComponent(q)}`)
    .then(r => r.json())
    .then(render)
    .catch(err => {
      console.error(err);
      results.innerHTML = `<p style="color:#ff6b6b">Error fetching results</p>`;
    });
}

function render(payload){
  if (!payload || payload.error){
    results.innerHTML = `<p style="color:#ff6b6b">${payload && payload.error ? payload.error : 'No results'}</p>`;
    return;
  }
  const tracks = payload.tracks || [];
  if (!tracks.length){
    results.innerHTML = `<p style="color:#9aa4b2">No results found</p>`;
    return;
  }

  results.innerHTML = '';
  tracks.forEach(tr => {
    const card = document.createElement('div');
    card.className = 'card';

    const img = document.createElement('img');
    img.className = 'cover';
    img.src = tr.cover || '';
    img.alt = tr.title;

    const meta = document.createElement('div');
    meta.className = 'meta';

    const title = document.createElement('h3');
    title.className = 'title';
    title.textContent = tr.title;

    const sub = document.createElement('div');
    sub.className = 'sub';
    sub.innerHTML = `<span>${tr.artist || ''}</span> <span>•</span> <span>${tr.album || ''}</span>`;

    meta.appendChild(title);
    meta.appendChild(sub);

    const controls = document.createElement('div');
    controls.className = 'controls';

    const play = document.createElement('button');
    play.className = 'play-btn';
    play.textContent = 'Play 30s';
    play.addEventListener('click', () => {
      if (currentAudio){
        currentAudio.pause();
        currentAudio = null;
        // if clicking same track, stop
        if (play.dataset.playing === '1'){
          play.dataset.playing = '0';
          play.textContent = 'Play 30s';
          return;
        }
        // reset other buttons
        document.querySelectorAll('.play-btn').forEach(b => { b.dataset.playing = '0'; b.textContent = 'Play 30s'; });
      }
      if (!tr.preview){
        alert('Preview not available');
        return;
      }
      const audio = new Audio(tr.preview);
      currentAudio = audio;
      audio.play();
      play.dataset.playing = '1';
      play.textContent = 'Pause';
      audio.onended = () => {
        play.dataset.playing = '0';
        play.textContent = 'Play 30s';
        currentAudio = null;
      };
      // toggle pause/resume if clicked again
      play.onclick = () => {
        if (!currentAudio) return;
        if (currentAudio.paused){
          currentAudio.play(); play.textContent = 'Pause';
        } else {
          currentAudio.pause(); play.textContent = 'Play 30s';
        }
      };
    });

    const deezerLink = document.createElement('a');
    deezerLink.className = 'small-link';
    deezerLink.href = tr.link || '#';
    deezerLink.target = '_blank';
    deezerLink.rel = 'noopener';
    deezerLink.textContent = 'Open on Deezer';

    controls.appendChild(play);
    controls.appendChild(deezerLink);

    card.appendChild(img);
    card.appendChild(meta);
    card.appendChild(controls);

    results.appendChild(card);
  });
}
