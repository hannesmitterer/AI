# 🏛️ AI-SEA Framework - Quick Start

## AI Sovereignty & Ethics Auditor v1.0.0

**Location:** `/ai-sea/`

---

## Three Universal Principles

1. **Lex Amoris** (Law of Love) - Love as the organizing principle
2. **One Love First (OLF)** - Love and life take precedence
3. **Golden Rule** - Treat others as you wish to be treated

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
cd ai-sea
docker-compose up -d
```

Access:
- API: http://localhost:8000
- Dashboard: http://localhost:8080

### Option 2: Local Development

```bash
cd ai-sea/backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open `ai-sea/frontend/dashboard.html` in your browser.

---

## 📖 Documentation

- **Main README**: `ai-sea/README.md`
- **Lex Amoris & OLF**: `ai-sea/docs/LEX_AMORIS_OLF.md`
- **Golden Rule**: `ai-sea/docs/GOLDEN_RULE.md`
- **Deployment**: `ai-sea/docs/DEPLOYMENT.md`
- **Summary**: `ai-sea/IMPLEMENTATION_SUMMARY.md`

---

## 📡 API Endpoints

- `GET /` - Health check
- `POST /audit` - Run ethics audit
- `GET /logs` - View audit logs
- `GET /stats` - System statistics
- `WS /ws` - Real-time WebSocket stream

---

## 🧪 Test It

```bash
cd ai-sea/examples
python client_example.py
```

---

## 🌐 GitHub Pages

Enable GitHub Pages in repository settings:
- Source: `docs/` folder
- Access landing page at: `https://yourusername.github.io/AI/`
- Access dashboard at: `https://yourusername.github.io/AI/ai-sea/`

---

## ✨ What It Does

AI-SEA audits AI actions through:

1. **ΦNexus Check** - Measures Lex Amoris alignment
2. **NSR Check** - Ensures autonomy (Golden Rule)
3. **OLF Check** - One Love First principle
4. **Golden Rule Check** - Reciprocity verification
5. **Self-Repair** - Automatic correction

Every action is evaluated against love, life, and reciprocity.

---

## 📦 What's Included

- ✅ Production-ready backend (FastAPI)
- ✅ Real-time dashboard (WebSocket)
- ✅ Complete documentation (50KB+)
- ✅ Docker deployment
- ✅ Example code
- ✅ GitHub Pages setup

---

**"IN AETERNUM EST. La Sovranità è Manifesta."**

*Lex Amoris • One Love First • Golden Rule*
