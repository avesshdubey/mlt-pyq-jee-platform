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
            "data-point", "data point", "dimension reduction", "dimensionality reduction", "representation learning"
        ]),
        ("Covariance Matrix & Eigen-decomposition", [
            "covariance matrix", "sample covariance", "eigenvalue", "eigenvalues", "eigenvector", "eigenvectors", 
            "symmetric", "positive semi-definite", "spectral theorem", "trace of covariance", "diagonal"
        ]),
        ("Reconstruction Error & Variance Captured", [
            "reconstruction", "reconstructed", "reconstruction error", "residue", "zero residue", 
            "variance captured", "total variance", "explained variance", "squared error"
        ]),
        ("Representation Learning Basics", [
            "unsupervised learning", "latent representation", "linear representation", "feature space", "synthetic"
        ])
    ],
    "Week 2: Unsupervised Learning - Representation learning - Kernel PCA": [
        ("Kernel Trick & Kernel Functions", [
            "kernel trick", "gaussian kernel", "rbf kernel", "radial basis", "polynomial kernel", 
            "linear kernel", "sigmoid kernel", "mercer", "positive definite kernel", "kernel function"
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
            "voronoi", "voronoi partition", "euclidean distance", "assignment step", "update step"
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
                        score += 3
                elif re.search(r'\b' + re.escape(kw_l) + r'\b', text_lower):
                    score += 2 + len(kw_l.split())
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

def find_mlt_section(doc):
    total_pages = len(doc)
    mlt_start = None
    mlt_end = None
    
    for pno in range(total_pages):
        text = doc[pno].get_text()
        if "Section Id :" in text:
            lines = [l.strip() for l in text.splitlines() if l.strip()]
            for idx, line in enumerate(lines):
                if line == "Section Id :" and idx > 0:
                    sec_name = lines[idx-1]
                    if sec_name.upper() in ["MLT", "MACHINE LEARNING TECHNIQUES"] or re.match(r'^(Section\s*:\s*)?MLT$', sec_name, re.IGNORECASE):
                        mlt_start = pno
                        break
        if mlt_start is not None:
            break
            
    if mlt_start is None:
        return None, None
        
    for pno in range(mlt_start, total_pages):
        text = doc[pno].get_text()
        if "Section Id :" in text:
            lines = [l.strip() for l in text.splitlines() if l.strip()]
            for idx, line in enumerate(lines):
                if line == "Section Id :" and idx > 0:
                    sec_name = lines[idx-1]
                    if sec_name.upper() not in ["MLT", "MACHINE LEARNING TECHNIQUES"]:
                        if pno > mlt_start or (pno == mlt_start and idx > 15):
                            mlt_end = pno
                            return mlt_start, mlt_end
                            
    return mlt_start, total_pages - 1

def find_green_checkmarks(doc, pno):
    page = doc[pno]
    green_rects = []
    
    # 1. Check embedded 16x16 raster icons
    try:
        imgs = page.get_images()
        for img in imgs:
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.width <= 24 and pix.height <= 24 and pix.colorspace:
                s = [0, 0, 0]
                n = pix.width * pix.height
                for x in range(pix.width):
                    for y in range(pix.height):
                        p = pix.pixel(x, y)
                        for i in range(min(3, len(p))): s[i] += p[i]
                avg_r = s[0] // n
                avg_g = s[1] // n
                avg_b = s[2] // n
                if avg_g > avg_r + 15 and avg_g > avg_b + 15:
                    rects = page.get_image_rects(xref)
                    for r in rects:
                        green_rects.append(r)
    except Exception:
        pass
        
    # 2. Check vector drawings
    try:
        drawings = page.get_drawings()
        for d in drawings:
            fill = d.get('fill')
            color = d.get('color')
            for c in [fill, color]:
                if c and len(c) >= 3:
                    r, g, b = c[0], c[1], c[2]
                    if r < 0.25 and g > 0.45 and b < 0.25:
                        rect = d.get('rect')
                        if rect and rect.width <= 24 and rect.height <= 24:
                            green_rects.append(rect)
    except Exception:
        pass
        
    return green_rects

def extract_from_paper(pdf_path):
    paper_name = os.path.basename(pdf_path)
    try:
        doc = fitz.open(pdf_path)
    except Exception:
        return []
        
    start_p, end_p = find_mlt_section(doc)
    if start_p is None:
        doc.close()
        return []
        
    extracted_questions = []
    
    # Keep track of comprehension passages
    active_comp = None
    
    for pno in range(start_p, end_p + 1):
        page = doc[pno]
        text = page.get_text()
        
        # Check for comprehension block
        if "Question Type : COMPREHENSION" in text:
            comp_rects = page.search_for("Question Type : COMPREHENSION")
            if comp_rects:
                active_comp = {
                    'pno': pno,
                    'y0': max(0, comp_rects[0].y0 - 10),
                    'y1': page.rect.height
                }
                
        # Find all questions on this page
        q_matches = list(re.finditer(r'Question Number\s*:\s*(\d+)\s+Question Id\s*:\s*(\d+)(?:\s+Question Type\s*:\s*(\w+))?', text))
        
        # Get green checkmarks on this page
        green_rects = find_green_checkmarks(doc, pno)
        
        for q_idx, match in enumerate(q_matches):
            q_num = int(match.group(1))
            q_id = match.group(2)
            q_type = match.group(3) or "MCQ"
            
            start_pos = match.start()
            end_pos = q_matches[q_idx + 1].start() if q_idx + 1 < len(q_matches) else len(text)
            q_chunk = text[start_pos:end_pos]
            
            # Filter out subject confirmation
            if "ARE YOU SURE YOU HAVE TO WRITE EXAM FOR THIS SUBJECT" in q_chunk.upper() or "THIS IS QUESTION PAPER FOR THE SUBJECT" in q_chunk.upper():
                continue
                
            marks_match = re.search(r'Correct Marks\s*:\s*(\d+)', q_chunk)
            marks = int(marks_match.group(1)) if marks_match else 3
            
            if "Multiple Select Question" in q_chunk:
                q_type = "MSQ"
            elif "Short Answer Question" in q_chunk or "Response Type : Numeric" in q_chunk:
                q_type = "SA"
            elif "Multiple Choice Question" in q_chunk:
                q_type = "MCQ"
                
            # Question stem text
            q_stem = ""
            stem_m = re.search(r'Question Label\s*:\s*[^\n\r]+\n(.*?)(?:Options\s*:|Response Type\s*:|Sub-Section\s*:|$)', q_chunk, re.DOTALL)
            if stem_m:
                q_stem = stem_m.group(1).strip()
            if not q_stem:
                q_stem = re.sub(r'Question Number\s*:\s*\d+.*', '', q_chunk)
                q_stem = re.sub(r'Correct Marks\s*:\s*\d+.*', '', q_stem).strip()
                
            options = []
            correct_answers = []
            
            # Options extraction
            if q_type in ["MCQ", "MSQ"]:
                opt_matches = list(re.finditer(r'(\d{10,16})\.\s*(.*?)(?=(?:\d{10,16}\.|\n\s*Sub-Section|\n\s*Question Number|$))', q_chunk, re.DOTALL))
                letters = ["A", "B", "C", "D", "E", "F"]
                for o_idx, om in enumerate(opt_matches):
                    opt_id = om.group(1)
                    opt_val = om.group(2).strip()
                    let = letters[o_idx] if o_idx < len(letters) else f"Opt {o_idx+1}"
                    
                    # Match green checkmark to option y-coord
                    opt_rects = page.search_for(opt_id)
                    is_correct = False
                    if opt_rects and green_rects:
                        oy = opt_rects[0].y0
                        for gr in green_rects:
                            if abs(oy - gr.y0) < 18:
                                is_correct = True
                                break
                                
                    if is_correct:
                        correct_answers.append(let)
                        
                    options.append({
                        'id': opt_id,
                        'letter': let,
                        'text': opt_val,
                        'is_correct': is_correct
                    })
            elif q_type == "SA":
                ans_m = re.search(r'Possible Answers\s*:\s*([^\n\r]+)', q_chunk)
                if ans_m:
                    val = ans_m.group(1).strip()
                    correct_answers.append(val)
                    
            # Visual Card Cropping
            card_filename = f"card_{q_id}_{pno}.jpg"
            card_rel_path = f"assets/q_cards/{card_filename}"
            card_full_path = os.path.join(CARDS_DIR, card_filename)
            
            # Calculate vertical boundaries
            rects = page.search_for(f"Question Number : {q_num}")
            if rects:
                y0 = max(0, rects[0].y0 - 8)
                y1 = page.rect.height - 30
                if q_idx + 1 < len(q_matches):
                    next_q_num = q_matches[q_idx + 1].group(1)
                    next_rects = page.search_for(f"Question Number : {next_q_num}")
                    if next_rects:
                        y1 = next_rects[0].y0 - 5
                else:
                    sec_rects = page.search_for("Sub-Section Number :")
                    if sec_rects:
                        for sr in sec_rects:
                            if sr.y0 > y0 + 40:
                                y1 = sr.y0 - 4
                                break
                                
                crop_rect = fitz.Rect(20, y0, page.rect.width - 20, min(page.rect.height, y1 + 5))
                if crop_rect.height > 40:
                    pix = page.get_pixmap(clip=crop_rect, dpi=150)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    
                    # Prepend comprehension if part of active passage
                    if active_comp and active_comp['pno'] == pno and active_comp['y0'] < y0:
                        comp_crop = fitz.Rect(20, active_comp['y0'], page.rect.width - 20, y0 - 4)
                        if comp_crop.height > 50:
                            cpix = page.get_pixmap(clip=comp_crop, dpi=150)
                            cimg = Image.frombytes("RGB", [cpix.width, cpix.height], cpix.samples)
                            stitched = Image.new("RGB", (max(img.width, cimg.width), cimg.height + img.height + 10), (255, 255, 255))
                            stitched.paste(cimg, (0, 0))
                            stitched.paste(img, (0, cimg.height + 10))
                            img = stitched
                            
                    # Scale down if width > 800px
                    if img.width > 800:
                        ratio = 800.0 / img.width
                        new_h = int(img.height * ratio)
                        img = img.resize((800, new_h), Image.Resampling.LANCZOS)
                        
                    img.save(card_full_path, "JPEG", quality=78, optimize=True)
                    
            week, subtopic = classify_question(q_stem + " " + q_chunk)
            
            extracted_questions.append({
                'id': f"MLT_Q_{q_id}",
                'raw_q_id': q_id,
                'question_number': q_num,
                'question_type': q_type,
                'marks': marks,
                'question_text': q_stem,
                'options': options,
                'correct_answer': correct_answers,
                'card_image': card_rel_path if os.path.exists(card_full_path) else "",
                'week': week,
                'subtopic': subtopic,
                'source_papers': [paper_name]
            })
            
    doc.close()
    return extracted_questions

def main():
    print("Step 1: Discovering all papers with strict MLT section boundaries...")
    all_pdfs = sorted(glob.glob(os.path.join(PYQS_DIR, "**", "*.pdf"), recursive=True))
    
    candidate_papers = []
    for p in all_pdfs:
        if "mlf_app" in p or "PDF_COM" in p or "mlt_questions_categorized" in p:
            continue
        candidate_papers.append(p)
        
    print(f"Total candidate exam papers: {len(candidate_papers)}")
    
    all_extracted = []
    paper_count = 0
    
    for idx, p in enumerate(candidate_papers):
        qs = extract_from_paper(p)
        if qs:
            paper_count += 1
            all_extracted.extend(qs)
            print(f"[{paper_count}] Extracted {len(qs)} Qs from {os.path.basename(p)}")
            
    print(f"\nTotal raw questions extracted across {paper_count} papers: {len(all_extracted)}")
    
    # Step 2: Deduplication Engine
    print("\nStep 2: Deduplicating questions across papers...")
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
            # Prefer non-empty answer key
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
        
    print(f"Total Unique Questions after Deduplication: {len(deduped_list)}")
    
    # Count per Week
    week_counts = {}
    for q in deduped_list:
        wk = q['week']
        week_counts[wk] = week_counts.get(wk, 0) + 1
        
    print("\nTaxonomy Distribution:")
    for wk, cnt in week_counts.items():
        print(f" * {wk}: {cnt} questions")
        
    # Write JSON data
    json_path = os.path.join(DATA_DIR, "questions.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(deduped_list, f, indent=2, ensure_ascii=False)
    print(f"\nWrote structured dataset to: {json_path}")
    
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
        
    # Write JS bundle for offline/CORS-safe execution
    js_path = os.path.join(DATA_DIR, "questions_data.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("// IIT Madras BS Degree - Machine Learning Techniques (MLT) Questions Data\n")
        f.write("window.MLT_QUESTIONS = ")
        json.dump(deduped_list, f, indent=2, ensure_ascii=False)
        f.write(";\n")
    print(f"Wrote JavaScript bundle to: {js_path}")

if __name__ == "__main__":
    main()
