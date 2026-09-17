document.addEventListener('DOMContentLoaded', () => {
  // Elements
  const tabText = document.getElementById('tab-text');
  const tabFile = document.getElementById('tab-file');
  const viewText = document.getElementById('view-text');
  const viewFile = document.getElementById('view-file');

  const emailTextarea = document.getElementById('email-content');
  const charCounter = document.getElementById('char-counter');
  const pasteBtn = document.getElementById('paste-btn');
  const clearBtn = document.getElementById('clear-btn');
  const analyzeBtn = document.getElementById('analyze-btn');

  const fileDropzone = document.getElementById('file-dropzone');
  const fileInput = document.getElementById('file-input');
  const browseBtn = document.getElementById('browse-btn');
  const filePreview = document.getElementById('file-preview');
  const fileNameDisplay = document.getElementById('file-name-display');
  const fileSizeDisplay = document.getElementById('file-size-display');
  const removeFileBtn = document.getElementById('remove-file-btn');

  const stateIdle = document.getElementById('state-idle');
  const stateActive = document.getElementById('state-active');

  // Result Card Elements
  const verdictBanner = document.getElementById('verdict-banner');
  const verdictIcon = document.getElementById('verdict-icon');
  const verdictHeading = document.getElementById('verdict-heading');
  const verdictSummary = document.getElementById('verdict-summary');

  const confidenceVal = document.getElementById('confidence-val');
  const confidenceBar = document.getElementById('confidence-bar');
  const riskCategoryVal = document.getElementById('risk-category-val');
  const heuristicScoreVal = document.getElementById('heuristic-score-val');

  const spamProbText = document.getElementById('spam-prob-text');
  const hamProbText = document.getElementById('ham-prob-text');
  const barSpam = document.getElementById('bar-spam');
  const barHam = document.getElementById('bar-ham');

  const indicatorList = document.getElementById('indicator-list');
  const metaWords = document.getElementById('meta-words');
  const metaChars = document.getElementById('meta-chars');
  const snippetText = document.getElementById('snippet-text');

  let activeTab = 'text';
  let selectedFile = null;
  let cachedSamples = null;

  // 1. Tab Switching
  function switchTab(tab) {
    activeTab = tab;
    if (tab === 'text') {
      tabText.classList.add('active');
      tabText.setAttribute('aria-selected', 'true');
      tabFile.classList.remove('active');
      tabFile.setAttribute('aria-selected', 'false');

      viewText.hidden = false;
      viewFile.hidden = true;
    } else {
      tabFile.classList.add('active');
      tabFile.setAttribute('aria-selected', 'true');
      tabText.classList.remove('active');
      tabText.setAttribute('aria-selected', 'false');

      viewFile.hidden = false;
      viewText.hidden = true;
    }
  }

  tabText.addEventListener('click', () => switchTab('text'));
  tabFile.addEventListener('click', () => switchTab('file'));

  // 2. Character & Word Counter
  function updateTextStats() {
    const text = emailTextarea.value;
    const chars = text.length;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    charCounter.textContent = `${chars} characters · ${words} words`;
  }

  emailTextarea.addEventListener('input', updateTextStats);

  // 3. Paste from Clipboard
  pasteBtn.addEventListener('click', async () => {
    try {
      const clipboardText = await navigator.clipboard.readText();
      if (clipboardText) {
        emailTextarea.value = clipboardText;
        updateTextStats();
      }
    } catch (err) {
      console.warn('Clipboard access not permitted:', err);
    }
  });

  // 4. Quick Sample Chips
  async function loadSamples() {
    try {
      const res = await fetch('/api/samples');
      cachedSamples = await res.json();
    } catch (e) {
      console.error('Failed to load preset samples:', e);
    }
  }
  loadSamples();

  document.querySelectorAll('.chip').forEach((chip) => {
    chip.addEventListener('click', () => {
      const sampleKey = chip.getAttribute('data-sample');
      if (cachedSamples && cachedSamples[sampleKey]) {
        switchTab('text');
        emailTextarea.value = cachedSamples[sampleKey].text;
        updateTextStats();
        // Automatically trigger classification
        classifyEmail();
      }
    });
  });

  // 5. File Drag & Drop Handling
  browseBtn.addEventListener('click', () => fileInput.click());
  fileDropzone.addEventListener('click', (e) => {
    if (e.target !== browseBtn) fileInput.click();
  });

  ['dragenter', 'dragover'].forEach((eventName) => {
    fileDropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      fileDropzone.classList.add('dragover');
    });
  });

  ['dragleave', 'drop'].forEach((eventName) => {
    fileDropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      fileDropzone.classList.remove('dragover');
    });
  });

  fileDropzone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelected(files[0]);
    }
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      handleFileSelected(e.target.files[0]);
    }
  });

  function formatBytes(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  }

  function handleFileSelected(file) {
    selectedFile = file;
    fileNameDisplay.textContent = file.name;
    fileSizeDisplay.textContent = formatBytes(file.size);
    filePreview.style.display = 'flex';
    fileDropzone.style.display = 'none';

    // Auto classify on file drop
    classifyEmail();
  }

  removeFileBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    selectedFile = null;
    fileInput.value = '';
    filePreview.style.display = 'none';
    fileDropzone.style.display = 'block';
  });

  // 6. Clear All
  clearBtn.addEventListener('click', () => {
    emailTextarea.value = '';
    updateTextStats();
    selectedFile = null;
    fileInput.value = '';
    filePreview.style.display = 'none';
    fileDropzone.style.display = 'block';

    stateActive.style.display = 'none';
    stateIdle.style.display = 'block';
  });

  // 7. Classify Email Logic
  async function classifyEmail() {
    let payload;
    let isFile = false;

    if (activeTab === 'file' && selectedFile) {
      isFile = true;
      payload = new FormData();
      payload.append('file', selectedFile);
    } else {
      const text = emailTextarea.value.trim();
      if (!text) {
        alert('Please enter or paste an email message to classify.');
        emailTextarea.focus();
        return;
      }
      payload = JSON.stringify({ text });
    }

    // Set loading state
    analyzeBtn.disabled = true;
    analyzeBtn.classList.add('loading');

    try {
      const response = await fetch('/api/classify', {
        method: 'POST',
        headers: isFile ? {} : { 'Content-Type': 'application/json' },
        body: payload,
      });

      const data = await response.json();

      if (!response.ok) {
        alert(data.error || 'Classification failed.');
        return;
      }

      renderResults(data);
    } catch (err) {
      console.error('Error classifying email:', err);
      alert('Network error communicating with the classifier engine.');
    } finally {
      analyzeBtn.disabled = false;
      analyzeBtn.classList.remove('loading');
    }
  }

  analyzeBtn.addEventListener('click', classifyEmail);

  // 8. Render Results in the Side Panel
  function renderResults(res) {
    stateIdle.style.display = 'none';
    stateActive.style.display = 'block';

    const isSpam = res.prediction === 'SPAM';
    const confPct = (res.confidence * 100).toFixed(2);
    const spamPct = (res.spam_probability * 100).toFixed(1);
    const hamPct = (res.ham_probability * 100).toFixed(1);

    // Update Verdict Banner
    verdictBanner.className = `verdict-banner ${isSpam ? 'spam' : 'ham'}`;
    verdictIcon.textContent = isSpam ? '🚨' : '✅';
    verdictHeading.textContent = isSpam ? 'SPAM DETECTED' : 'LEGITIMATE EMAIL';
    verdictSummary.textContent = isSpam
      ? 'This email exhibits strong hallmarks of spam, advance-fee fraud, or phishing.'
      : 'This communication shows normal characteristics of authentic, legitimate correspondence.';

    // Confidence Card
    confidenceVal.textContent = `${confPct}%`;
    confidenceBar.style.width = `${confPct}%`;
    confidenceBar.style.backgroundColor = isSpam ? 'var(--color-spam)' : 'var(--color-ham)';

    // Risk Category Card
    if (isSpam) {
      riskCategoryVal.textContent = res.heuristic_score > 6 ? 'Critical Threat' : 'High Suspicion';
      riskCategoryVal.style.color = 'var(--color-spam)';
    } else {
      riskCategoryVal.textContent = 'Low Risk';
      riskCategoryVal.style.color = 'var(--color-ham)';
    }
    heuristicScoreVal.textContent = `Heuristic Risk Score: ${res.heuristic_score.toFixed(1)}`;

    // Probabilities Distribution
    spamProbText.textContent = `${spamPct}%`;
    hamProbText.textContent = `${hamPct}%`;
    barSpam.style.width = `${spamPct}%`;
    barHam.style.width = `${hamPct}%`;

    // Indicators List
    indicatorList.innerHTML = '';
    if (res.triggered_rules && res.triggered_rules.length > 0) {
      res.triggered_rules.forEach((rule) => {
        const li = document.createElement('li');
        li.className = 'indicator-item';
        li.innerHTML = `<span>⚠️</span> <span>${escapeHtml(rule)}</span>`;
        indicatorList.appendChild(li);
      });
    } else {
      const li = document.createElement('li');
      li.className = 'indicator-none';
      li.innerHTML = `<span>🛡️</span> <span>No malicious scam or phishing patterns detected.</span>`;
      indicatorList.appendChild(li);
    }

    // Metadata & Snippet
    metaWords.textContent = `${res.word_count} words`;
    metaChars.textContent = `${res.char_count} characters`;
    snippetText.textContent = res.preview || '(None)';
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }
});
