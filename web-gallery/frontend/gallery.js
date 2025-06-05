const API_BASE = 'http://192.168.1.117:5000'; // uprav dle potřeby
const galleryGrid = document.getElementById('galleryGrid');
const emptyMessage = document.getElementById('emptyMessage');
const uploadBtn = document.getElementById('uploadBtn');
const fileInput = document.getElementById('fileInput');

const modal = document.getElementById('mediaModal');
const modalContent = document.getElementById('modalContent');
const modalCloseBtn = document.getElementById('modalCloseBtn');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const downloadBtn = document.getElementById('downloadBtn');

let mediaList = [];
let start = 0;
const count = 8;
let currentIndex = -1;

// Načtení další várky médií
async function loadMore() {
  try {
    const res = await fetch(`${API_BASE}/media?start=${start}&count=${count}`);
    if (!res.ok) throw new Error('Chyba při načítání médií');
    const files = await res.json();

    if (start === 0 && files.length === 0) {
      emptyMessage.style.display = 'block';
      return;
    } else {
      emptyMessage.style.display = 'none';
    }

    files.forEach(f => {
      mediaList.push(f);
      const isVideo = /\.(mp4|mov)$/i.test(f);
      const el = document.createElement(isVideo ? 'video' : 'img');
      el.src = `${API_BASE}/media/${encodeURIComponent(f)}`;
      if (isVideo) {
        el.controls = false;
        el.muted = true;
        el.preload = 'metadata';
      }
      el.setAttribute('data-index', mediaList.length - 1);
      el.tabIndex = 0;
      el.classList.add('media-thumb');

      el.addEventListener('click', () => openModal(parseInt(el.dataset.index)));
      el.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openModal(parseInt(el.dataset.index));
        }
      });

      galleryGrid.appendChild(el);
    });
    start += count;
  } catch (e) {
    console.error(e);
  }
}

// Otevření modalu na indexu
function openModal(idx) {
  if (idx < 0 || idx >= mediaList.length) return;
  currentIndex = idx;
  modal.classList.add('active');
  modal.setAttribute('aria-hidden', 'false');
  renderModalContent();
}

// Zavření modalu
function closeModal() {
  modal.classList.remove('active');
  modal.setAttribute('aria-hidden', 'true');
  modalContent.innerHTML = '';
  currentIndex = -1;
}

// Render obsahu v modalu
function renderModalContent() {
  const file = mediaList[currentIndex];
  if (!file) return;

  const isVideo = /\.(mp4|mov)$/i.test(file);
  modalContent.innerHTML = '';

  if (isVideo) {
    const video = document.createElement('video');
    video.src = `${API_BASE}/media/${encodeURIComponent(file)}`;
    video.controls = true;
    video.autoplay = true;
    video.style.maxHeight = '85vh';
    modalContent.appendChild(video);
  } else {
    const img = document.createElement('img');
    img.src = `${API_BASE}/media/${encodeURIComponent(file)}`;
    modalContent.appendChild(img);
  }

  // Update download link
  downloadBtn.onclick = () => {
    window.open(`${API_BASE}/media/${encodeURIComponent(file)}`, '_blank');
  };
}

// Navigace
function showPrev() {
  if (currentIndex > 0) {
    currentIndex--;
    renderModalContent();
  }
}

function showNext() {
  if (currentIndex < mediaList.length - 1) {
    currentIndex++;
    renderModalContent();
  }
}

// Upload media
uploadBtn.addEventListener('click', () => {
  fileInput.value = '';
  fileInput.click();
});

fileInput.addEventListener('change', async () => {
  const file = fileInput.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await fetch(`${API_BASE}/upload`, {
      method: 'POST',
      body: formData
    });
    if (!res.ok) throw new Error('Chyba při nahrávání');

    // Reset gallery a načíst znovu od začátku
    start = 0;
    mediaList = [];
    galleryGrid.innerHTML = '';
    await loadMore();
  } catch (e) {
    alert('Nepodařilo se nahrát soubor.');
    console.error(e);
  }
});

// Zavření modalu
modalCloseBtn.addEventListener('click', closeModal);
modal.addEventListener('click', (e) => {
  if (e.target === modal) closeModal();
});

// Navigace v modalu
prevBtn.addEventListener('click', showPrev);
nextBtn.addEventListener('click', showNext);

// Načtení dalších médií při scrollu
document.querySelector('.gallery-container').addEventListener('scroll', () => {
  const container = document.querySelector('.gallery-container');
  if (container.scrollTop + container.clientHeight >= container.scrollHeight - 150) {
    loadMore();
  }
});

// Inicializace
loadMore();
