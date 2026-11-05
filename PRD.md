# Product Requirements Document (PRD) - MLT PYQ & JEE CBT Test Platform

## Tasks Breakdown

- [x] **Task 1: Establish Git & 4-Tier Configuration Baseline (`/addgit`)**
  - Initialize local Git repository on `main` branch.
  - Generate comprehensive `.gitignore` tailored to Python, web assets, and raw binary archives.
  - Create baseline commit.
  - Create remote GitHub repository via GitHub CLI (`gh repo create mlt-pyq-jee-platform --public --source=. --remote=origin --push`) and configure upstream tracking.

- [x] **Task 2: Precision Multi-Paper MLT Section Scanner & Visual Card Cropper**
  - Scanned all 67 candidate question paper PDFs in `C:\Users\avesh\Desktop\PYQS`, identifying all 44 papers containing the official `MLT` section (the remaining 23 PDFs belong to non-MLT courses such as MLF, Math, etc.).
  - Filter out generic subject confirmation prompts.
  - Crop 150 DPI high-resolution visual question cards capturing complete problem stems, equations, plots, and option choices.
  - Extract verbatim question text, option texts, question type (MCQ, MSQ, SA), marks, and official answer keys.

- [x] **Task 3: Exact Deduplication Engine & 4-Week Syllabus Classifier**
  - Implement exact normalized text and visual hash deduplication across multiple paper slots.
  - Classify unique questions into the official 4-week syllabus taxonomy:
    - Week 1: PCA (Representation Learning, Covariance, Eigenvalues, Reconstruction Error)
    - Week 2: Kernel PCA (Kernel Trick, Gram Matrix, RBF/Gaussian/Polynomial Kernels)
    - Week 3: Clustering (K-means, Kernel K-means, Distortion, Voronoi Partitions)
    - Week 4: Estimation & GMM (MLE, Bayesian Estimation, GMM, EM Algorithm)
  - Generate structured `data/questions.json` and standalone bundle `data/questions_data.js`.

- [x] **Task 4: Publication-Quality Categorized PDF Generator (`generate_pdf.py`)**
  - Build `scripts/generate_pdf.py` using ReportLab to render `mlt_questions_categorized.pdf`.
  - Format categorized questions by Week and Subtopic with running headers, footers, page numbering, embedded question cards, and verified answer keys.
  - Ensure total PDF file size is optimized under 50 MB.

- [x] **Task 5: Interactive JEE CBT Examination Web Application & Admin Control Panel**
  - Develop `index.html`, `css/jee_style.css`, and `js/jee_app.js` replicating the NTA/JEE CBT examination system.
  - Embed full authentication system (`js/auth.js`) with Student/Admin roles and persistent local storage.
  - Build Admin Control Panel (`js/admin.js`) with system metrics, user controls, exam log viewer, question bank explorer, and data export.
  - Provide interactive Exam Mode (countdown timer, palette sidebar, mark for review, clear response) and comprehensive scorecard review.

- [x] **Task 6: Automated Test Verification, CodeRabbit QA & Git Auto-Push**
  - Write test suite `tests/test_platform.py` verifying question schema, PDF integrity, image resolution, and application assets.
  - Run CodeRabbit code review audit (`coderabbit review --agent`) and fix any flagged issues.
  - Commit atomic changes and auto-push upstream to GitHub remote.

- [x] **Task 7: Comprehensive 46-Paper Audit, WinRT OCR Text Recovery, 20 Granular Subcategories, Random Practice Mode & CodeRabbit Fixes**
  - Re-audited all 69 PDFs in `C:\Users\avesh\Desktop\PYQS`, identifying and unlocking legacy TCS iON format papers `QPG1` and `QPG2` (questions 78–99).
  - Filtered out all confirmation prompts and instruction blocks (e.g. `MLT_038`) and empty records.
  - Converted mislabelled numerical questions with empty options to proper `SA` type and extracted verified numerical values.
  - Implemented normalized stem and answer key cross-session deduplication, merging slot duplicates into single questions with multi-paper citation history, establishing the true verified count of 426 unique examination questions across 45 exam sessions.
  - Deployed hardware-accelerated Windows WinRT OCR to recover question stems for image-rendered math formulas and equations without altering high-fidelity visual cards.
  - Decomposed 4 weeks into 20 granular pedagogical subcategories with robust priority classification (Week 1: 234 Qs, Week 2: 55 Qs, Week 3: 68 Qs, Week 4: 69 Qs).
  - Added "🎲 Random Question" / "Quick Random Practice" modes across sub-bar, question meta bar, question palette, and footer navigation with review mark preservation.
  - Re-compiled 28.16 MB publication-ready categorized PDF (`mlt_questions_categorized.pdf`) with 426 questions and updated running headers.
  - Addressed all 8 CodeRabbit review findings: legacy section boundary handling, position-based header search, word-boundary EM matching, subtopic category synchronization, and question schema validation tests.
  - Updated all test suites, passed `test_platform.py` (6/6 tests passing), and auto-pushed to GitHub remote.
