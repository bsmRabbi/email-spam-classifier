# Email Spam Classifier & Threat Detector

An end-to-end Machine Learning pipeline and modern Web UI that classifies emails and text messages as **Spam** or **Ham** (legitimate).

Trained on `spam.csv` and augmented with real-world email threat vectors (419 advance-fee fraud, DMCA extortion phishing, fake invoices, and legitimate business correspondence).

---

## 🌟 Features

- **Hybrid Intelligence Architecture:** Combines TF-IDF n-gram Machine Learning (`MultinomialNB`) with SpamAssassin-style heuristic threat scoring.
- **Professional Web Dashboard:** Modern, accessible, side-by-side UI with drag-and-drop file upload, instant risk breakdown, and one-click demo samples.
- **File Upload Support:** Upload `.eml` (raw email exports with headers & MIME body) and `.txt` files.
- **High Performance:** **99.19% test accuracy** and **100% spam precision** (zero false positives on legitimate emails).
- **Multiple Interfaces:** Web Interface (`app.py`), CLI & Interactive Terminal (`predict.py`), and Python library integration.

---

## 🚀 Quick Start

### Launch the Web Interface

#### link- **https://email-spam-classifier-8nul.onrender.com/**

You can:
- **Paste any email** into the input box and click **Scan & Classify Email**.
- **Drag & drop `.eml` or `.txt` email files** directly into the upload area.
- Click any of the **Quick Test Samples** (e.g. *419 Wire Scam*, *DMCA Extortion*, *Fake Invoice*, *Work Meeting*) for instant one-click analysis.
- Inspect the **side-by-side results card** showing the verdict banner, confidence meter, probability breakdown, and detected threat indicators.

---




