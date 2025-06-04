const express = require('express');
const multer = require('multer');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;
const MEDIA_DIR = path.join(__dirname, 'media');

if (!fs.existsSync(MEDIA_DIR)) fs.mkdirSync(MEDIA_DIR);

const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, MEDIA_DIR),
  filename: (req, file, cb) => cb(null, Date.now() + '_' + file.originalname)
});
const upload = multer({ storage });

app.use(cors());
app.use(express.static(MEDIA_DIR));

app.get('/media/list', (req, res) => {
  const page = parseInt(req.query.page || '0');
  const limit = 5;

  fs.readdir(MEDIA_DIR, (err, files) => {
    if (err) return res.status(500).json({ error: 'Failed to read media directory' });
    const sorted = files.sort((a, b) => fs.statSync(path.join(MEDIA_DIR, b)).mtimeMs - fs.statSync(path.join(MEDIA_DIR, a)).mtimeMs);
    const paged = sorted.slice(page * limit, (page + 1) * limit);
    res.json(paged);
  });
});

app.post('/upload', upload.single('file'), (req, res) => {
  if (!req.file) return res.status(400).send('No file uploaded.');
  res.send('File uploaded successfully.');
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
