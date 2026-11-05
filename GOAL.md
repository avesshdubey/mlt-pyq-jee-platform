# Goal Specification: IIT Madras - Machine Learning Techniques (MLT) Past Year Questions (PYQ) & JEE CBT Platform

## 1. Objective
Build an end-to-end examination platform and categorized question bank for IIT Madras BS Degree - Machine Learning Techniques (MLT - Diploma Level).
The system extracts all unique questions verbatim with 100% visual fidelity directly from the official TCS iON past year question papers located in `C:\Users\avesh\Desktop\PYQS`, categorizes them into the official 4-week syllabus taxonomy, compiles a publication-ready PDF document, and provides an interactive NTA/JEE CBT exam web application with authentication and an admin control dashboard.

---

## 2. Acceptance Criteria
- [ ] **Data Source Scanning**: Scan all 52+ past year question papers and archives in `C:\Users\avesh\Desktop\PYQS` and accurately identify all `MLT` sections between their start boundary (`MLT` header) and end boundary (next subject or EOF).
- [ ] **100% Fidelity Question Card Cropping**: Capture high-resolution visual cards directly from the source PDF pages for each question, preserving intricate mathematical derivations, Greek symbols, eigenvalues/eigenvectors, kernel matrices, plots, and formulas without OCR corruption or dropped characters.
- [ ] **Verbatim Text & Option Extraction**: Extract question stems, option choices, marks, question type (MCQ, MSQ, SA/NAT), and official answer keys verbatim. Filter out standard subject confirmation prompts ("ARE YOU SURE YOU HAVE TO WRITE EXAM FOR THIS SUBJECT?").
- [ ] **Exact Deduplication**: Group duplicate questions occurring across multiple exam sessions/slots into unique records while retaining complete cross-session citation metadata (`source_papers`).
- [ ] **4-Week Syllabus Taxonomy**:
  - **Week 1**: Introduction; Unsupervised Learning - Representation learning - PCA
  - **Week 2**: Unsupervised Learning - Representation learning - Kernel PCA
  - **Week 3**: Unsupervised Learning - Clustering - K-means/Kernel K-means
  - **Week 4**: Unsupervised Learning - Estimation - Recap of MLE + Bayesian estimation, Gaussian Mixture Model - EM algorithm.
- [ ] **Publication-Ready PDF**: Generate `mlt_questions_categorized.pdf` (ReportLab) formatted by Week and Subtopic, embedding high-resolution question cards, official answer keys, and syllabus summary tables.
- [ ] **NTA/JEE CBT Web Platform (`index.html`)**:
  - Full JEE examination interface (candidate banner, subject/week tabs, countdown timer, question panel, palette sidebar with standard JEE status colors).
  - Secure Authentication Gate (Student & Admin login, registration, persistent session).
  - Admin Control Panel (user management, attempt analytics, question bank explorer, JSON/CSV exports).
  - Post-Exam Scorecard Review with detailed question-by-question analysis, official answer keys, and accuracy metrics.
- [ ] **Git & GitHub Integration (`/addgit`)**: Local repository initialized on `main`, remote linked (`avesshdubey/mlt-pyq-jee-platform`), and auto-push enabled with atomic commits.
- [ ] **Automated Test Suite**: Unit tests (`tests/test_platform.py`) verifying question counts, schema integrity, PDF generation, and frontend assets.

---

## 3. Constraints & Guidelines
- Strict adherence to official IITM syllabus boundaries.
- No dummy/placeholder content.
- Respect local storage and browser performance for smooth rendering of hundreds of question cards.
- Automatic Git commits and push after each task verification.
