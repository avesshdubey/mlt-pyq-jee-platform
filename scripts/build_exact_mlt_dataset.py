import fitz
import os
import re
import json
import glob
import hashlib
from PIL import Image

WORKSPACE_DIR = r"C:\Users\avesh\Desktop\mlt-pyq-jee-platform"
PYQS_DIR = r"C:\Users\avesh\Desktop\PYQS"

DATA_DIR = os.path.join(WORKSPACE_DIR, "data")
ASSETS_DIR = os.path.join(WORKSPACE_DIR, "assets", "q_images")
CARDS_DIR = os.path.join(WORKSPACE_DIR, "assets", "q_cards")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(CARDS_DIR, exist_ok=True)

# 4-Week Taxonomy Mapping for Machine Learning Techniques (MLT)
CATEGORIES = {
    "Week 1: Introduction; Unsupervised Learning - Representation learning - PCA": [
        ("PCA Fundamentals & Projection", [
            "pca", "principal component", "principal components", "first principal", "second principal", 
            "fourth principal", "top principal", "projection", "subspace", "centered dataset", "centering", 
            "data-point", "data point", "dimension reduction", "dimensionality reduction"
        ]),
        ("Covariance Matrix & Eigen-decomposition", [
            "covariance matrix", "sample covariance", "eigenvalue", "eigenvalues", "eigenvector", "eigenvectors", 
            "symmetric", "positive semi-definite", "spectral theorem", "trace of covariance", "diagonal",
            "scatter matrix", "data-matrix"
        ]),
        ("Reconstruction Error & Variance Captured", [
            "reconstruction", "reconstructed", "reconstruction error", "residue", "zero residue", 
            "variance captured", "total variance", "explained variance", "squared error"
        ]),
        ("Representation Learning & Evaluation Metrics", [
            "representation learning", "unsupervised learning", "accuracy", "precision", "recall", 
            "f-1 score", "f1 score", "ridge loss", "lasso loss", "regularization", "confusion matrix", 
            "polynomial transformation", "feature vector", "prediction", "loss value"
        ])
    ],
    "Week 2: Unsupervised Learning - Representation learning - Kernel PCA": [
        ("Kernel Trick & Kernel Functions", [
            "kernel trick", "gaussian kernel", "rbf kernel", "radial basis", "polynomial kernel", 
            "linear kernel", "sigmoid kernel", "mercer", "positive definite kernel", "kernel function", 
            "valid kernel", "valid  kernel"
        ]),
        ("Gram Matrix & Kernel Evaluation", [
            "gram matrix", "kernel matrix", "k(x", "k(x,", "centering the kernel", "centering kernel", 
            "inner product in feature space", "distance in feature space"
        ]),
        ("Kernel PCA Formulation & Dual Space", [
            "kernel pca", "kpca", "non-linear pca", "dual formulation", "feature map", "phi(x)", "\\phi", 
            "eigenvalue problem in kernel space", "alpha"
        ])
    ],
    "Week 3: Unsupervised Learning - Clustering - K-means/Kernel K-means": [
        ("K-means Objective & Convergence", [
            "k-means", "kmeans", "clustering", "cluster", "clusters", "distortion", "distortion measure", 
            "inertia", "objective function", "convergence", "local minimum", "lloyd"
        ]),
        ("Cluster Centers & Distance Metrics", [
            "cluster center", "cluster centers", "cluster mean", "cluster means", "centroid", "centroids", 
            "voronoi", "voronoi partition", "euclidean distance", "assignment step", "update step", 
            "cluster assignment", "clustering problem"
        ]),
        ("Initialization & K-means++", [
            "initialization", "initialize", "k-means++", "kmeans++", "sensitivity to initialization", 
            "seeding", "random initialization"
        ]),
        ("Kernel K-means & Non-linear Clustering", [
            "kernel k-means", "kernel kmeans", "non-convex", "concentric", "clustering in feature space"
        ])
    ],
    "Week 4: Unsupervised Learning - Estimation - Recap of MLE + Bayesian estimation, Gaussian Mixture Model - EM algorithm": [
        ("Maximum Likelihood Estimation (MLE)", [
            "mle", "maximum likelihood", "log-likelihood", "likelihood function", "score function", 
            "estimator", "unbiased", "consistency", "poisson rate", "bernoulli parameter", "normal distribution"
        ]),
        ("Bayesian Estimation & Priors", [
            "bayesian", "prior", "priors", "posterior", "posterior mean", "beta(", "dirichlet", 
            "conjugate", "conjugate prior", "map", "maximum a posteriori", "loss function", "bayes risk"
        ]),
        ("Gaussian Mixture Models (GMM)", [
            "gaussian mixture", "gmm", "mixture model", "mixture weights", "component density", 
            "latent variable", "latent variables", "mixture components", "marginal likelihood"
        ]),
        ("Expectation-Maximization (EM) Algorithm", [
            "em algorithm", "expectation-maximization", "e-step", "m-step", "responsibilities", 
            "responsibility", "jensen", "lower bound", "elbo", "incomplete data"
        ])
    ]
}

def classify_question(text):
    text_lower = text.lower()
    best_week = None
    best_subtopic = None
    best_score = -1
    
    for week, subtopics in CATEGORIES.items():
        for subtopic, kw_list in subtopics:
            score = 0
            for kw in kw_list:
                kw_l = kw.lower()
                if kw_l.startswith("\\"):
                    if kw_l in text_lower:
                        score += 4
                elif re.search(r'\b' + re.escape(kw_l) + r'\b', text_lower):
                    score += 3 + len(kw_l.split())
                elif kw_l in text_lower:
                    score += 1
            if score > best_score:
                best_score = score
                best_week = week
                best_subtopic = subtopic
                
    if best_score <= 0:
        if "kernel" in text_lower or "gram" in text_lower or "rbf" in text_lower or "phi" in text_lower:
            return "Week 2: Unsupervised Learning - Representation learning - Kernel PCA", "Kernel Trick & Kernel Functions"
        elif "cluster" in text_lower or "k-means" in text_lower or "mean" in text_lower:
            return "Week 3: Unsupervised Learning - Clustering - K-means/Kernel K-means", "K-means Objective & Convergence"
        elif "mle" in text_lower or "likelihood" in text_lower or "bayesian" in text_lower or "gmm" in text_lower or "em" in text_lower:
            return "Week 4: Unsupervised Learning - Estimation - Recap of MLE + Bayesian estimation, Gaussian Mixture Model - EM algorithm", "Maximum Likelihood Estimation (MLE)"
        else:
            return "Week 1: Introduction; Unsupervised Learning - Representation learning - PCA", "PCA Fundamentals & Projection"
            
    return best_week, best_subtopic

def clean_stem_text(raw_text):
    t = raw_text
    possible_ans = ""
    ans_m = re.search(r'Possible Answers\s*:\s*([^\n\r]+)', t)
    if ans_m:
        possible_ans = ans_m.group(1).strip()
        
    # Line-based removal without re.DOTALL so question stem is never wiped
    t = re.sub(r'Calculator\s*:[^\n\r]*', '', t)
    t = re.sub(r'Response Time\s*:[^\n\r]*', '', t)
    t = re.sub(r'Think Time\s*:[^\n\r]*', '', t)
    t = re.sub(r'Minimum Instruction\s*Time\s*:[^\n\r]*', '', t)
    t = re.sub(r'Is Question Mandatory\s*:[^\n\r]*', '', t)
    t = re.sub(r'Question Pattern Type\s*:[^\n\r]*', '', t)
    t = re.sub(r'Group Comprehension Questions\s*:[^\n\r]*', '', t)
    t = re.sub(r'Question Numbers\s*:[^\n\r]*', '', t)
    t = re.sub(r'Correct Marks\s*:[^\n\r]*', '', t)
    t = re.sub(r'Max\. Selectable Options\s*:[^\n\r]*', '', t)
    t = re.sub(r'Question Label\s*:[^\n\r]*', '', t)
    t = re.sub(r'Response Type\s*:[^\n\r]*', '', t)
    t = re.sub(r'Evaluation Required[^\n\r]*', '', t)
    t = re.sub(r'Show Word Count[^\n\r]*', '', t)
    t = re.sub(r'Answers Type[^\n\r]*', '', t)
    t = re.sub(r'Text Areas[^\n\r]*', '', t)
    t = re.sub(r'Possible Answers[^\n\r]*', '', t)
    t = re.sub(r'Sub-Section[^\n\r]*', '', t)
    t = re.sub(r'Question Shuffling[^\n\r]*', '', t)
    t = re.sub(r'Is Section Default[^\n\r]*', '', t)
    t = re.sub(r'Question Number\s*:\s*\d+.*', '', t)
    t = re.sub(r'Question Id\s*:\s*\d+.*', '', t)
    t = re.sub(r'THIS IS QUESTION PAPER FOR THE SUBJECT.*', '', t)
    t = re.sub(r'ARE YOU SURE YOU HAVE TO WRITE EXAM.*', '', t)
    t = re.sub(r'\n\s*\n+', '\n', t).strip()
    return t, possible_ans

def find_mlt_boundaries(doc):
    total_pages = len(doc)
    start_p = None
    y_start = 0
    end_p = total_pages - 1
    y_end = 999999
    
    for pno in range(total_pages):
        text = doc[pno].get_text()
        if 'Section Id :' in text:
            lines = [l.strip().replace('\xa0', '').strip() for l in text.splitlines() if l.strip().replace('\xa0', '').strip()]
            for idx, line in enumerate(lines):
                if line == 'Section Id :' and idx > 0:
                    sec_name = lines[idx-1]
                    if sec_name.upper() in ['MLT', 'MACHINE LEARNING TECHNIQUES'] or re.match(r'^(Section\s*:\s*)?MLT$', sec_name, re.IGNORECASE):
                        start_p = pno
                        sr = doc[pno].search_for('Section Id :')
                        y_start = sr[0].y0 - 20 if sr else 0
                        break
        if start_p is not None:
            break
            
    if start_p is None:
        return None, 0, None, 0
        
    for pno in range(start_p, total_pages):
        text = doc[pno].get_text()
        if 'Section Id :' in text:
            lines = [l.strip().replace('\xa0', '').strip() for l in text.splitlines() if l.strip().replace('\xa0', '').strip()]
            for idx, line in enumerate(lines):
                if line == 'Section Id :' and idx > 0:
                    sec_name = lines[idx-1]
                    if sec_name.upper() not in ['MLT', 'MACHINE LEARNING TECHNIQUES']:
                        if pno > start_p or (pno == start_p and idx > 10):
                            end_p = pno
                            sr = doc[pno].search_for('Section Id :')
                            y_end = sr[0].y0 - 20 if sr else 999999
                            return start_p, y_start, end_p, y_end
                            
    return start_p, y_start, total_pages - 1, 999999

def process_paper(pdf_path):
    paper_name = os.path.basename(pdf_path)
    try:
        doc = fitz.open(pdf_path)
    except Exception:
        return []
        
    start_pno, y_start_page, end_pno, y_end_page = find_mlt_boundaries(doc)
    if start_pno is None:
        doc.close()
        return []
        
    extracted_questions = []
    active_comp = None
    
    for pno in range(start_pno, end_pno + 1):
        page = doc[pno]
        blocks = page.get_text('blocks')
        
        # Check for comprehension block
        for b in blocks:
            txt_b = b[4]
            if "Question Label : Comprehension" in txt_b or "Question Type : COMPREHENSION" in txt_b:
                m_qrange = re.search(r'Question Numbers\s*:\s*\((\d+)\s*to\s*(\d+)\)', txt_b)
                if not m_qrange:
                    m_qrange = re.search(r'Sub questions.*?Question Number\s*:\s*(\d+)', txt_b, re.DOTALL)
                    q_from = int(m_qrange.group(1)) if m_qrange else 0
                    q_to = q_from + 10
                else:
                    q_from = int(m_qrange.group(1))
                    q_to = int(m_qrange.group(2))
                    
                clip_comp = fitz.Rect(15, max(15, b[1] - 5), page.rect.width - 15, min(page.rect.height - 15, b[3] + 15))
                pix_c = page.get_pixmap(clip=clip_comp, dpi=150)
                clean_comp_txt, _ = clean_stem_text(txt_b)
                active_comp = {
                    'pno': pno,
                    'q_from': q_from,
                    'q_to': q_to,
                    'text': clean_comp_txt,
                    'image': Image.frombytes('RGB', [pix_c.width, pix_c.height], pix_c.samples)
                }
                
        # Find question starts on this page
        q_starts = []
        for b in blocks:
            if pno == start_pno and b[1] < y_start_page:
                continue
            if pno == end_pno and b[1] >= y_end_page:
                continue
                
            txt = b[4].strip()
            m_qnum = re.search(r'Question Number\s*:\s*(\d+)', txt)
            if m_qnum:
                q_starts.append({
                    'q_num': int(m_qnum.group(1)),
                    'y0': b[1],
                    'y1': b[3],
                    'block_text': txt
                })
                
        q_starts.sort(key=lambda x: x['y0'])
        
        for idx_q, qs in enumerate(q_starts):
            q_num = qs['q_num']
            header = qs['block_text']
            
            m_id = re.search(r'Question Id\s*:\s*(\d+)', header)
            m_type = re.search(r'Question Type\s*:\s*([A-Za-z]+)', header)
            
            if not m_type:
                if "Multiple Select" in header:
                    q_type = "MSQ"
                elif "Short Answer" in header:
                    q_type = "SA"
                else:
                    q_type = "MCQ"
            else:
                q_type = m_type.group(1)
                
            q_id = m_id.group(1) if m_id else f"QID-{q_num}"
            
            # Marks check - filter confirmation question
            m_marks = re.search(r'Correct Marks\s*:\s*([0-9.]+)', header)
            marks = float(m_marks.group(1)) if m_marks else 3.0
            if marks <= 0 or "ARE YOU SURE" in header or "THIS IS QUESTION PAPER FOR THE SUBJECT" in header:
                continue
                
            # Vertical span of question on this page
            y_start = max(15, qs['y0'] - 5)
            
            if idx_q + 1 < len(q_starts):
                next_boundary_y = max(y_start + 40, q_starts[idx_q + 1]['y0'] - 5)
                spans_next_page = False
            else:
                if pno == end_pno and y_end_page < page.rect.height:
                    next_boundary_y = y_end_page - 5
                    spans_next_page = False
                else:
                    next_boundary_y = page.rect.height - 15
                    spans_next_page = True
                    
            clip_rect = fitz.Rect(15, y_start, page.rect.width - 15, next_boundary_y)
            pix = page.get_pixmap(clip=clip_rect, dpi=150)
            im_q = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
            
            # Multi-page stitching if question continues onto next page
            y_end_next = 0
            if spans_next_page and pno + 1 <= end_pno:
                next_p = doc[pno + 1]
                next_blocks = next_p.get_text('blocks')
                y_end_next = next_p.rect.height - 15
                for nb in next_blocks:
                    if re.search(r'Question Number\s*:\s*\d+', nb[4]):
                        y_end_next = max(20, nb[1] - 5)
                        break
                    if "Question Label : Comprehension" in nb[4]:
                        y_end_next = max(20, nb[1] - 5)
                        break
                    if pno + 1 == end_pno and nb[1] >= y_end_page:
                        y_end_next = max(20, y_end_page - 5)
                        break
                        
                if y_end_next > 25:
                    clip_next = fitz.Rect(15, 15, next_p.rect.width - 15, y_end_next)
                    pix_next = next_p.get_pixmap(clip=clip_next, dpi=150)
                    im_next = Image.frombytes('RGB', [pix_next.width, pix_next.height], pix_next.samples)
                    
                    stitched = Image.new('RGB', (max(im_q.width, im_next.width), im_q.height + im_next.height), (255, 255, 255))
                    stitched.paste(im_q, (0, 0))
                    stitched.paste(im_next, (0, im_q.height))
                    im_q = stitched
                    
            # Prepend comprehension if active
            comp_text_to_prepend = ""
            if active_comp and active_comp['q_from'] <= q_num <= active_comp['q_to']:
                comp_img = active_comp['image']
                c_w = max(comp_img.width, im_q.width)
                c_h = comp_img.height + im_q.height + 15
                im_full = Image.new('RGB', (c_w, c_h), (255, 255, 255))
                im_full.paste(comp_img, (0, 0))
                im_full.paste(im_q, (0, comp_img.height + 15))
                im_q = im_full
                comp_text_to_prepend = active_comp['text'] + "\n"
                
            # Resize card if width > 800
            if im_q.width > 800:
                h_new = int(im_q.height * 800 / im_q.width)
                im_q = im_q.resize((800, h_new), Image.Resampling.LANCZOS)
                
            # Save Card Image
            card_filename = f"card_{q_id}_{q_num}.jpg"
            card_rel_path = f"assets/q_cards/{card_filename}"
            card_full_path = os.path.join(CARDS_DIR, card_filename)
            im_q.save(card_full_path, "JPEG", quality=78, optimize=True)
                
            # Extract Text and Options
            full_q_text = page.get_text(clip=clip_rect)
            if spans_next_page and pno + 1 <= end_pno and y_end_next > 25:
                full_q_text += "\n" + doc[pno + 1].get_text(clip=fitz.Rect(15, 15, page.rect.width - 15, y_end_next))
                
            stem_part = full_q_text.split("Options :")[0] if "Options :" in full_q_text else full_q_text
            clean_stem, possible_ans = clean_stem_text(stem_part)
            if comp_text_to_prepend and not clean_stem.startswith(active_comp['text'][:30]):
                clean_stem = comp_text_to_prepend + clean_stem
                
            # Detect Green Checkmark Icons
            green_icons = []
            
            for img_info in page.get_image_info(xrefs=True):
                if img_info['width'] <= 24 and img_info['height'] <= 24 and y_start - 10 <= img_info['bbox'][1] <= next_boundary_y + 10:
                    try:
                        pix_ic = fitz.Pixmap(doc, img_info['xref'])
                        if pix_ic.n >= 3:
                            cx, cy = pix_ic.width // 2, pix_ic.height // 2
                            r, g, b = pix_ic.pixel(cx, cy)[:3]
                            if g > r + 15 and g > b + 15:
                                green_icons.append(('p0', img_info['bbox'][1]))
                    except Exception:
                        pass
                        
            if spans_next_page and pno + 1 <= end_pno and y_end_next > 25:
                next_p = doc[pno + 1]
                for img_info in next_p.get_image_info(xrefs=True):
                    if img_info['width'] <= 24 and img_info['height'] <= 24 and img_info['bbox'][1] <= y_end_next + 10:
                        try:
                            pix_ic = fitz.Pixmap(doc, img_info['xref'])
                            if pix_ic.n >= 3:
                                cx, cy = pix_ic.width // 2, pix_ic.height // 2
                                r, g, b = pix_ic.pixel(cx, cy)[:3]
                                if g > r + 15 and g > b + 15:
                                    green_icons.append(('p1', img_info['bbox'][1]))
                        except Exception:
                            pass
                            
            # Options and Answer Key Matching
            options = []
            correct_ans = []
            
            if q_type in ["MCQ", "MSQ"]:
                opt_blocks = []
                for b in blocks:
                    if y_start <= b[1] <= next_boundary_y:
                        txt = b[4].strip()
                        m = re.match(r'^([0-9]{5,}|[A-D])\.\s*(.*)', txt, re.DOTALL)
                        if m:
                            opt_blocks.append(('p0', b[1], m.group(1), m.group(2)))
                            
                if spans_next_page and pno + 1 <= end_pno and y_end_next > 25:
                    for b in doc[pno + 1].get_text('blocks'):
                        if b[1] <= y_end_next:
                            txt = b[4].strip()
                            m = re.match(r'^([0-9]{5,}|[A-D])\.\s*(.*)', txt, re.DOTALL)
                            if m:
                                opt_blocks.append(('p1', b[1], m.group(1), m.group(2)))
                                
                opt_blocks.sort(key=lambda x: (x[0], x[1]))
                letters = ["A", "B", "C", "D", "E", "F"]
                
                for idx_opt, ob in enumerate(opt_blocks):
                    let = letters[idx_opt] if idx_opt < len(letters) else f"Opt {idx_opt+1}"
                    opt_page, opt_y, opt_id, opt_txt = ob
                    
                    is_correct = False
                    for g_page, g_y in green_icons:
                        if g_page == opt_page and abs(g_y - opt_y) < 18:
                            is_correct = True
                            break
                            
                    if is_correct:
                        correct_ans.append(let)
                        
                    clean_opt_txt = opt_txt.replace('\n', ' ').strip()
                    options.append({
                        'id': opt_id,
                        'letter': let,
                        'text': clean_opt_txt,
                        'is_correct': is_correct
                    })
            elif q_type == "SA":
                if possible_ans:
                    correct_ans.append(possible_ans)
                    
            # Classify Week & Subtopic
            combined_text = clean_stem + " " + " ".join([o['text'] for o in options])
            week, subtopic = classify_question(combined_text)
            
            extracted_questions.append({
                'id': f"MLT_Q_{q_id}",
                'raw_q_id': q_id,
                'question_number': q_num,
                'question_type': q_type,
                'marks': marks,
                'question_text': clean_stem,
                'options': options,
                'correct_answer': correct_ans,
                'card_image': card_rel_path if os.path.exists(card_full_path) else "",
                'week': week,
                'subtopic': subtopic,
                'source_papers': [paper_name]
            })
            
    doc.close()
    return extracted_questions

def main():
    print("Step 1: Discovering all papers with strict MLT section boundaries...", flush=True)
    all_pdfs = sorted(glob.glob(os.path.join(PYQS_DIR, "**", "*.pdf"), recursive=True))
    
    candidate_papers = []
    for p in all_pdfs:
        if "mlf_app" in p or "PDF_COM" in p or "mlt_questions_categorized" in p:
            continue
        candidate_papers.append(p)
        
    print(f"Total candidate exam papers: {len(candidate_papers)}", flush=True)
    
    all_extracted = []
    paper_count = 0
    
    for idx, p in enumerate(candidate_papers):
        qs = process_paper(p)
        if qs:
            paper_count += 1
            all_extracted.extend(qs)
            print(f"[{paper_count}] Extracted {len(qs)} Qs from {os.path.basename(p)}", flush=True)
            
    print(f"\nTotal raw questions extracted across {paper_count} papers: {len(all_extracted)}", flush=True)
    
    # Step 2: Deduplication Engine
    print("\nStep 2: Deduplicating questions across papers...", flush=True)
    unique_questions = {}
    
    for q in all_extracted:
        stem = q['question_text'].strip()
        norm_stem = re.sub(r'[^a-zA-Z0-9]', '', stem.lower())
        if len(norm_stem) < 20:
            opt_ids = "".join([o['id'] for o in q['options']])
            key = f"opt_{opt_ids}" if opt_ids else f"id_{q['raw_q_id']}"
        else:
            key = norm_stem[:150]
            
        if key not in unique_questions:
            unique_questions[key] = q
        else:
            existing = unique_questions[key]
            for src in q['source_papers']:
                if src not in existing['source_papers']:
                    existing['source_papers'].append(src)
            # Merge answers
            if not existing['correct_answer'] and q['correct_answer']:
                existing['correct_answer'] = q['correct_answer']
            elif len(q['correct_answer']) > len(existing['correct_answer']):
                existing['correct_answer'] = q['correct_answer']
            if not existing['card_image'] and q['card_image']:
                existing['card_image'] = q['card_image']
                
    deduped_list = list(unique_questions.values())
    
    # Assign sequential IDs: MLT_001, MLT_002...
    for i, q in enumerate(deduped_list):
        q['id'] = f"MLT_{i+1:03d}"
        
    print(f"Total Unique Questions after Deduplication: {len(deduped_list)}", flush=True)
    
    # Count per Week
    week_counts = {}
    for q in deduped_list:
        wk = q['week']
        week_counts[wk] = week_counts.get(wk, 0) + 1
        
    print("\nTaxonomy Distribution:", flush=True)
    for wk, cnt in week_counts.items():
        print(f" * {wk}: {cnt} questions", flush=True)
        
    # Write JSON data
    json_path = os.path.join(DATA_DIR, "questions.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(deduped_list, f, indent=2, ensure_ascii=False)
    print(f"\nWrote structured dataset to: {json_path}", flush=True)
    
    # Write stats JSON
    stats_path = os.path.join(DATA_DIR, "stats.json")
    stats = {
        'totalQuestions': len(deduped_list),
        'totalRawQuestions': len(all_extracted),
        'totalPapersScanned': paper_count,
        'weekDistribution': week_counts
    }
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
        
    # Write JS bundle
    js_path = os.path.join(DATA_DIR, "questions_data.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("// IIT Madras BS Degree - Machine Learning Techniques (MLT) Questions Data\n")
        f.write("window.MLT_QUESTIONS = ")
        json.dump(deduped_list, f, indent=2, ensure_ascii=False)
        f.write(";\n")
    print(f"Wrote JavaScript bundle to: {js_path}", flush=True)

if __name__ == "__main__":
    main()
