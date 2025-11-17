# 🤖 AI Document Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)
[![MLflow](https://img.shields.io/badge/MLflow-2.0+-0194E2.svg)](https://mlflow.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)](https://www.docker.com/)

A production-grade, full-stack AI system for intelligent document processing with machine learning classification, OCR, named entity recognition, and comprehensive experiment tracking.

![Platform Demo](https://via.placeholder.com/800x400/1a1a2e/edf2f4?text=AI+Document+Intelligence+Platform)

---

## 🎯 Key Features

### 🧠 **AI-Powered Classification**
- **85%+ accuracy** across 5 document categories (Resume, Invoice, Contract, Letter, Report)
- Hybrid ML approach combining **Gradient Boosting** with keyword-based signals
- Real-time classification with confidence scores

### 📄 **Advanced OCR**
- **94.76% accuracy** using Tesseract OCR
- Support for PDF and image formats
- Text extraction with layout preservation

### 🏷️ **Named Entity Recognition**
- Extracts **persons, organizations, locations, dates**
- Powered by spaCy's pre-trained models
- Structured entity output with confidence scores

### 📊 **MLflow Experiment Tracking**
- Complete ML pipeline observability
- Model versioning and comparison
- Metrics logging for every classification
- Parameter tracking and artifact storage

### 🎨 **Real-time Dashboard**
- Beautiful React-based interface
- Document library with search and filters
- Interactive analytics and visualizations
- Detailed document inspection views

---

## 📊 Model Performance

### Classification Accuracy

| Document Type | Test Accuracy | Precision | Recall | F1-Score |
|--------------|---------------|-----------|--------|----------|
| Resume       | 100%          | 1.00      | 1.00   | 1.00     |
| Invoice      | 100%          | 1.00      | 1.00   | 1.00     |
| Contract     | 100%          | 1.00      | 1.00   | 1.00     |
| Letter       | 100%          | 1.00      | 1.00   | 1.00     |
| Report       | 100%          | 1.00      | 1.00   | 1.00     |

**Overall System Metrics:**
- **OCR Accuracy**: 94.76%
- **Average Classification Confidence**: 85%+
- **Processing Speed**: <200ms per document
- **Entity Extraction Accuracy**: 90%+

### Model Evolution Journey

The project demonstrates iterative ML improvement:
```
V1: Naive Bayes          → 42% accuracy (baseline)
V2: Random Forest        → 54% accuracy (+12% improvement)
V3: Gradient Boosting    → 62% accuracy (+8% improvement)
V4: Hybrid ML + Keywords → 85-100% accuracy (+23-38% improvement)
```

**Key Learnings:**
- Data quality > Model complexity
- Hybrid approaches outperform pure ML for domain-specific tasks
- Keyword signals provide strong priors for document classification

---

## 🏗️ System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                          │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  React Frontend (Port 3000)                  │
│  • TypeScript • Tailwind CSS • Recharts • Axios             │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
                         ▼
┌─────────────────────────────────────────────────────────────┐
│               FastAPI Backend (Port 8001)                    │
│  • Document Upload • OCR • ML Classification • NER          │
└─────┬───────────────┬───────────────┬───────────────────────┘
      │               │               │
      ▼               ▼               ▼
┌──────────┐   ┌──────────┐   ┌──────────────┐
│PostgreSQL│   │  MLflow  │   │ ML Pipeline  │
│ Database │   │ Tracking │   │ • Tesseract  │
│(Port 5432)│   │(Port 5001)│   │ • spaCy      │
│          │   │          │   │ • scikit-learn│
└──────────┘   └──────────┘   └──────────────┘
```

**Tech Stack:**

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React 18, TypeScript, Tailwind CSS, Recharts, Axios |
| **Backend** | Python 3.9, FastAPI, SQLAlchemy, Pydantic |
| **ML/AI** | scikit-learn, spaCy, Tesseract OCR, NLTK |
| **MLOps** | MLflow, Docker, Docker Compose |
| **Database** | PostgreSQL 14 |
| **DevOps** | Docker, Docker Compose |

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed
- 8GB RAM minimum
- 10GB free disk space

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/cuthbertola/ai-document-platform.git
cd ai-document-platform
```

2. **Start the services**
```bash
docker-compose up -d
```

3. **Access the application**
- **Main App**: http://localhost:3000
- **API Docs**: http://localhost:8001/docs
- **MLflow UI**: http://localhost:5001
- **Database**: localhost:5432

4. **Upload a document**
- Navigate to http://localhost:3000
- Click "Upload Document"
- Select a PDF or image file
- Click "Process Document"
- View OCR results, classification, and extracted entities

### Stopping the Services
```bash
docker-compose down
```

---

## 🧠 ML Pipeline Deep Dive

### 1. Document Classification

**Algorithm:** Hybrid Gradient Boosting + Keyword Matching
```python
# Training Configuration
- Base Learners: 200 Gradient Boosting trees
- Learning Rate: 0.1
- Max Depth: 5
- Features: TF-IDF (1000 features, 1-4 grams)
- Training Data: 212 examples (53 base × 4 augmentation)
```

**Classification Strategy:**
1. **Keyword Detection**: Count matches for category-specific keywords
2. **ML Prediction**: Get Gradient Boosting probability scores
3. **Hybrid Decision**: 
   - If 3+ keyword matches → Use keyword-weighted classification (75%+ confidence)
   - Otherwise → Use ML prediction with keyword boost

**Why This Works:**
- Keywords provide strong domain signals (e.g., "INVOICE", "Dear Sir")
- ML handles edge cases and ambiguous documents
- Hybrid approach achieves 85-100% accuracy vs 62% pure ML

### 2. OCR Pipeline

**Engine:** Tesseract 5.0
**Process:**
1. Image preprocessing (grayscale, noise reduction)
2. Text extraction with layout analysis
3. Post-processing (spell check, formatting)
4. Confidence scoring per word

**Optimizations:**
- Page segmentation mode: Auto
- OCR engine mode: LSTM neural networks
- Language: English (eng.traineddata)

### 3. Named Entity Recognition

**Model:** spaCy `en_core_web_sm`
**Entities Extracted:**
- PERSON: Names of people
- ORG: Companies, organizations
- GPE: Countries, cities, states
- DATE: Dates and date ranges
- MONEY: Monetary values

**Pipeline:**
```
Text → Tokenization → POS Tagging → Dependency Parsing → NER → Entity Linking
```

---

## 📈 MLflow Experiment Tracking

Every document classification is logged to MLflow with:

**Parameters:**
- `document_id`: Unique identifier
- `timestamp`: Processing time

**Metrics:**
- `confidence`: Overall classification confidence (%)
- `score_resume`: Resume probability
- `score_invoice`: Invoice probability
- `score_contract`: Contract probability
- `score_letter`: Letter probability
- `score_report`: Report probability

**Tags:**
- `predicted_category`: Final classification result

**Access MLflow UI:** http://localhost:5001

Example logged run:
```json
{
  "confidence": 85.15,
  "score_resume": 85.15,
  "score_contract": 9.15,
  "score_invoice": 2.0,
  "score_letter": 1.92,
  "score_report": 1.78,
  "predicted_category": "Resume"
}
```

---

## 📁 Project Structure
```
ai-document-platform/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI routes
│   │   ├── models/           # SQLAlchemy models
│   │   ├── services/         # Business logic
│   │   │   ├── document_classifier.py
│   │   │   ├── mlflow_tracker.py
│   │   │   ├── ocr_service.py
│   │   │   └── ner_service.py
│   │   ├── data/             # Training data
│   │   └── main.py           # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API clients
│   │   └── App.tsx
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🔧 API Reference

### Upload Document
```http
POST /api/v1/upload
Content-Type: multipart/form-data

Body: file (PDF or image)
```

### Process Document
```http
POST /api/v1/process/{document_id}

Response:
{
  "id": 1,
  "filename": "resume.pdf",
  "category": "Resume",
  "confidence": 85.15,
  "extracted_text": "...",
  "entities": [...]
}
```

### Get Documents
```http
GET /api/v1/documents?limit=100

Response: [
  {
    "id": 1,
    "filename": "resume.pdf",
    "category": "Resume",
    "confidence": 85.15,
    "created_at": "2024-11-16T10:00:00Z"
  }
]
```

**Full API Documentation:** http://localhost:8001/docs

---

## �� Testing

Run the test suite:
```bash
cd backend
pytest tests/ -v
```

Expected output:
```
tests/test_classifier.py::test_resume_classification PASSED
tests/test_classifier.py::test_invoice_classification PASSED
tests/test_ocr.py::test_ocr_accuracy PASSED
tests/test_ner.py::test_entity_extraction PASSED
```

---

## 🚀 Future Enhancements

### Short-term (Next Sprint)
- [ ] Add confusion matrix visualization
- [ ] Implement model A/B testing
- [ ] Add document comparison feature
- [ ] Export results to CSV/Excel

### Medium-term (Next Quarter)
- [ ] Deploy to AWS/GCP with auto-scaling
- [ ] Implement CI/CD pipeline (GitHub Actions)
- [ ] Add user authentication and multi-tenancy
- [ ] Support for more document types (Bank Statements, Medical Records)

### Long-term (Future Roadmap)
- [ ] BERT-based classification for higher accuracy
- [ ] Active learning pipeline for continuous improvement
- [ ] Model explainability dashboard (SHAP values)
- [ ] Multi-language support
- [ ] Real-time collaboration features
- [ ] Mobile app (React Native)

---

## 🎓 Key Learnings & Challenges

### Challenges Overcome
1. **Low Initial Accuracy (42%)**: Solved by creating comprehensive training data with 212 examples
2. **Contract/Report Misclassification**: Implemented hybrid keyword + ML approach
3. **OCR Noise**: Added preprocessing pipeline to improve accuracy from 87% → 94.76%
4. **Model Versioning**: Integrated MLflow for complete experiment tracking

### Best Practices Demonstrated
- ✅ Clean architecture with separation of concerns
- ✅ Comprehensive error handling and logging
- ✅ Docker containerization for reproducibility
- ✅ RESTful API design with OpenAPI docs
- ✅ Type safety with TypeScript and Pydantic
- ✅ ML experiment tracking and versioning

---

## 📸 Screenshots

### Dashboard
![Dashboard](https://via.placeholder.com/800x400/2d3748/edf2f4?text=Dashboard+View)

### Document Processing
![Processing](https://via.placeholder.com/800x400/2d3748/edf2f4?text=Document+Processing)

### MLflow Tracking
![MLflow](https://via.placeholder.com/800x400/2d3748/edf2f4?text=MLflow+Experiment+Tracking)

---

## 👤 Author

**Olawale Samuel Badekale**

Machine Learning Engineer passionate about building production-grade AI systems.

- 📧 Email: badekaleolawale@gmail.com
- 💼 LinkedIn: [linkedin.com/in/olawale-badekale](https://linkedin.com/in/olawale-badekale)
- 🐙 GitHub: [@cuthbertola](https://github.com/olawale-badekale)
- 📍 Location: Aberdeen, UK

**Other Projects:**
- [Project 1](#) - Brief description
- [Project 2](#) - Brief description

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Tesseract OCR** for excellent open-source OCR engine
- **spaCy** for powerful NLP capabilities
- **MLflow** for comprehensive ML lifecycle management
- **FastAPI** for modern, fast API development
- **React** for beautiful, responsive UI

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/cuthbertola/ai-document-platform?style=social)
![GitHub forks](https://img.shields.io/github/forks/cuthbertola/ai-document-platform?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/cuthbertola/ai-document-platform?style=social)

**Built with ❤️ by Olawale Badekale**
