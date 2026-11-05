import json
import re
import os
from collections import Counter

WORKSPACE_DIR = r"C:\Users\avesh\Desktop\mlt-pyq-jee-platform"
DATA_FILE = os.path.join(WORKSPACE_DIR, "data", "questions.json")
JS_BUNDLE_FILE = os.path.join(WORKSPACE_DIR, "data", "questions_data.js")
STATS_FILE = os.path.join(WORKSPACE_DIR, "data", "stats.json")

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    raw_qs = json.load(f)

print(f"Loaded {len(raw_qs)} questions from {DATA_FILE}")

# 1. Clean invalid / instruction questions & convert mislabelled numerical questions
cleaned = []
for q in raw_qs:
    txt = q.get('question_text', '').strip()
    opts = q.get('options', [])
    ans = q.get('correct_answer', [])
    
    # Drop empty records
    if not txt and not opts and not ans:
        continue
    # Drop instruction prompts
    if 'Useful Data has been mentioned above' in txt or any('Useful Data has been mentioned above' in o.get('text', '') for o in opts):
        continue
    if 'ARE YOU SURE' in txt.upper() or 'CROSS CHECK' in txt.upper():
        continue
    if len(opts) == 2 and set(o.get('text', '').strip().upper() for o in opts) == {'YES', 'NO'}:
        continue
        
    # Convert numerical MCQs with no options
    if q.get('question_type') in ['MCQ', 'MSQ'] and len(opts) == 0:
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        # find the numerical answer from the lines
        extracted_ans = None
        ans_idx = -1
        for idx, l in enumerate(lines):
            # check if l matches number or range like '35', '0.34 to 0.40', '0.5', '1', '2.071 to 2.171'
            if re.match(r'^(-?[\d.]+(?:\s*to\s*-?[\d.]+)?)$', l):
                extracted_ans = l
                ans_idx = idx
                break
        if extracted_ans:
            q['question_type'] = 'SA'
            q['correct_answer'] = [extracted_ans]
            # question stem is everything before the answer line
            q['question_text'] = '\n'.join(lines[:ans_idx]).strip()
            
    # Also verify all SA questions have a non-empty correct_answer
    if q.get('question_type') == 'SA' and not q.get('correct_answer'):
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        for idx, l in enumerate(lines):
            if re.match(r'^(-?[\d.]+(?:\s*to\s*-?[\d.]+)?)$', l):
                q['correct_answer'] = [l]
                q['question_text'] = '\n'.join(lines[:idx]).strip()
                break

    cleaned.append(q)

print(f"Valid questions before deduplication: {len(cleaned)}")

# 2. Robust Deduplication
def clean_stem_for_hash(text):
    if not text:
        return ""
    # strip TCS iON metadata lines
    t = re.sub(r'Question\s+(ld|Id|Number|Type|Label)\s*:[^\n\r]*', '', text, flags=re.I)
    t = re.sub(r'Max\.\s*Selectable[^\n\r]*', '', t, flags=re.I)
    t = re.sub(r'Correct\s*Marks\s*:[^\n\r]*', '', t, flags=re.I)
    t = re.sub(r'Response\s*Time\s*:[^\n\r]*', '', t, flags=re.I)
    t = re.sub(r'Think\s*Time\s*:[^\n\r]*', '', t, flags=re.I)
    t = re.sub(r'Is\s*Question\s*Mandatory\s*:[^\n\r]*', '', t, flags=re.I)
    t = re.sub(r'Calculator\s*:[^\n\r]*', '', t, flags=re.I)
    t = re.sub(r'\b\d{9,16}\b', '', t) # strip 9-16 digit internal IDs
    t = re.sub(r'[^\w\s]', '', t) # strip punctuation
    t = re.sub(r'\s+', ' ', t).strip().lower()
    return t

dedup_map = {}
for q in cleaned:
    stem_norm = clean_stem_for_hash(q.get('question_text', ''))
    q_type = q.get('question_type', '')
    ans_key = tuple(sorted(str(a).strip().lower() for a in q.get('correct_answer', [])))
    
    # If stem has >= 25 chars, use first 90 chars of cleaned stem
    if len(stem_norm) >= 25:
        norm_key = (q_type, ans_key, stem_norm[:90])
    else:
        # short stem: use card image path or id
        norm_key = (q_type, ans_key, q.get('id'))
        
    if norm_key not in dedup_map:
        dedup_map[norm_key] = q
    else:
        existing = dedup_map[norm_key]
        # Merge source papers
        p_set = set(existing.get('source_papers', []))
        for p in q.get('source_papers', []):
            p_set.add(p)
        existing['source_papers'] = sorted(list(p_set))
        # Keep the better question text / options / card
        if len(q.get('question_text', '')) > len(existing.get('question_text', '')):
            existing['question_text'] = q.get('question_text', '')
        if len(q.get('options', [])) > len(existing.get('options', [])):
            existing['options'] = q.get('options', [])

unique_qs = list(dedup_map.values())
print(f"Truly unique questions after merging: {len(unique_qs)}")

# 3. Robust Classification
def classify_robust(text, options_text=""):
    t = (text + " " + options_text).lower()
    
    # Week 4 checks
    has_w4 = bool(re.search(r'\b(mle|likelihood|bayesian|gmm|gaussian mixture|prior|posterior|elbo|expectation-maximization|responsibilit|latent variable)\b', t)) or bool(re.search(r'\b(em algorithm|e-step|m-step)\b', t))
    # Week 3 checks
    has_w3 = bool(re.search(r'\b(cluster|clustering|clusters|k-means|kmeans|k-means\+\+|lloyd|centroids?|voronoi|silhouette|elbow method)\b', t))
    # Week 2 checks
    has_w2 = bool(re.search(r'\b(kernel|kernel trick|kpca|kernel pca|gram matrix|rbf kernel|gaussian kernel|polynomial kernel|mercer|feature map)\b', t))
    # Week 1 checks
    has_w1 = bool(re.search(r'\b(pca|principal component|principal components|principal direction|covariance matrix|sample covariance|reconstruction error|rayleigh quotient|spectral theorem|scree plot|variance explained|eigenvalue|eigenvalues|eigenvector|eigenvectors|dimensionality reduction|representation learning|linear regression|perceptron|least squares|ridge loss|gradient descent|precision|recall|f1 score|confusion matrix)\b', t))
    
    # Priority resolution
    if has_w3 and not (has_w2 and 'kernel k-means' not in t) and not ('pca' in t and not 'cluster' in t):
        # Week 3 Clustering
        w = 'Week 3: Unsupervised Learning - Clustering - K-means/Kernel K-means'
        if 'lloyd' in t or 'assignment' in t or 'centroid' in t or 'center' in t:
            st = "3.3 Lloyd's Algorithm: Assignment & Centroid Updates"
        elif 'k-means++' in t or 'kmeans++' in t or 'initialization' in t or 'initialize' in t:
            st = "3.4 Initialization Sensitivity & K-Means++ Algorithm"
        elif 'voronoi' in t or 'partition' in t or 'boundary' in t:
            st = "3.5 Voronoi Partitions & Geometric Cluster Boundaries"
        elif 'distortion' in t or 'objective' in t or 'inertia' in t or 'sse' in t:
            st = "3.2 K-Means Distortion Objective & Mathematical Properties"
        elif 'kernel k-means' in t or 'kernel kmeans' in t:
            st = "3.7 Kernel K-Means & Non-Convex Clustering"
        elif 'elbow' in t or 'silhouette' in t:
            st = "3.6 Model Selection, Silhouette & Elbow Method"
        else:
            st = "3.1 Clustering Formulations & Unsupervised Grouping"
        return w, st
        
    if has_w2:
        # Week 2 Kernel PCA
        w = 'Week 2: Unsupervised Learning - Representation learning - Kernel PCA'
        if 'gram matrix' in t or 'kernel matrix' in t or 'h k h' in t or 'centering' in t:
            st = "2.3 Gram Matrix & Centering in Feature Space"
        elif 'mercer' in t or 'rbf' in t or 'polynomial kernel' in t or 'gaussian kernel' in t:
            st = "2.2 Mercer Kernels & Kernel Types (RBF, Polynomial)"
        elif 'dual' in t or 'alpha' in t:
            st = "2.4 Kernel PCA Dual Eigenvalue Formulations"
        elif 'pre-image' in t or 'pre image' in t:
            st = "2.5 KPCA Projections & Pre-image Problem"
        else:
            st = "2.1 Non-linear Feature Mappings & Kernel Trick"
        return w, st
        
    if has_w4:
        # Week 4 Estimation & GMM
        w = 'Week 4: Unsupervised Learning - Estimation - Recap of MLE + Bayesian estimation, Gaussian Mixture Model - EM algorithm'
        if 'bayesian' in t or 'prior' in t or 'posterior' in t or 'map' in t or 'beta' in t:
            st = "4.2 Bayesian Estimation, Priors & MAP"
        elif 'e-step' in t or 'responsibilit' in t:
            st = "4.5 EM Algorithm: E-Step (Responsibilities / Posterior)"
        elif 'm-step' in t:
            st = "4.6 EM Algorithm: M-Step (Parameter Updates)"
        elif 'elbo' in t or 'lower bound' in t or 'convergence' in t or 'em algorithm' in t:
            st = "4.7 EM Convergence & Evidence Lower Bound (ELBO)"
        elif 'mixture' in t or 'gmm' in t or 'gaussian mixture' in t:
            st = "4.4 Gaussian Mixture Models (GMM) Parameters & Structure"
        elif 'latent' in t:
            st = "4.3 Latent Variable Models & Mixture Modeling"
        else:
            st = "4.1 Likelihood Formulation & Maximum Likelihood (MLE)"
        return w, st
        
    # Week 1 Default / Fallback
    w = 'Week 1: Introduction; Unsupervised Learning - Representation learning - PCA'
    if 'reconstruction' in t or 'residue' in t:
        st = "1.9 Reconstruction & Reconstruction Error Calculation"
    elif 'eigenvalue' in t or 'eigenvalues' in t or 'eigenvector' in t or 'eigenvectors' in t or 'principal direction' in t:
        st = "1.6 Eigen-Decomposition & Principal Directions"
    elif 'covariance' in t or 'centered' in t or 'centering' in t or 'scatter' in t:
        st = "1.4 Data Centering, Preprocessing & Covariance Matrix"
    elif 'variance' in t or 'objective' in t or 'rayleigh' in t:
        st = "1.5 PCA Optimization Objective & Max-Variance Formulation"
    elif 'projection' in t or 'coordinates' in t or 'projected' in t:
        st = "1.8 Low-Dimensional Projections & Coordinates"
    elif 'regularization' in t or 'ridge' in t or 'lasso' in t or 'gradient descent' in t or 'loss' in t or 'perceptron' in t or 'linear regression' in t or 'fits the data' in t:
        st = "1.3 Regularization, Loss Functions & Model Fitting"
    elif 'precision' in t or 'recall' in t or 'f1' in t or 'confusion matrix' in t or 'accuracy' in t:
        st = "1.2 Model Evaluation Metrics & Classification Diagnostics"
    else:
        st = "1.1 Representation Learning Basics & Dimensionality Reduction"
    return w, st

# Apply classification and sort questions cleanly by Week and Subtopic
for q in unique_qs:
    opts_txt = " ".join(o.get('text', '') for o in q.get('options', []))
    w, st = classify_robust(q.get('question_text', ''), opts_txt)
    q['week'] = w
    q['subtopic'] = st

# Sort order
week_order_map = {
    "Week 1: Introduction; Unsupervised Learning - Representation learning - PCA": 1,
    "Week 2: Unsupervised Learning - Representation learning - Kernel PCA": 2,
    "Week 3: Unsupervised Learning - Clustering - K-means/Kernel K-means": 3,
    "Week 4: Unsupervised Learning - Estimation - Recap of MLE + Bayesian estimation, Gaussian Mixture Model - EM algorithm": 4
}
unique_qs.sort(key=lambda x: (week_order_map.get(x['week'], 9), x.get('subtopic', ''), x.get('id', '')))

# Assign fresh consecutive IDs: MLT_001, MLT_002...
for idx, q in enumerate(unique_qs):
    q['id'] = f"MLT_{idx+1:03d}"

# Print breakdown
print("\n--- NEW VERIFIED UNIQUE SYLLABUS BREAKDOWN ---")
week_counter = Counter(q['week'] for q in unique_qs)
for w in sorted(week_counter.keys(), key=lambda x: week_order_map.get(x, 9)):
    print(f"{w}: {week_counter[w]} questions")

subtopic_counter = Counter(q['subtopic'] for q in unique_qs)
print(f"\nTotal subtopics: {len(subtopic_counter)}")
for st, cnt in sorted(subtopic_counter.items()):
    print(f"  - {st}: {cnt} Qs")

# Save JSON data
with open(DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(unique_qs, f, indent=2, ensure_ascii=False)
print(f"Wrote {len(unique_qs)} clean questions to {DATA_FILE}")

# Save JS bundle
with open(JS_BUNDLE_FILE, 'w', encoding='utf-8') as f:
    f.write('// IIT Madras BS Degree - Machine Learning Techniques (MLT) Questions Data\n')
    f.write('window.MLT_QUESTIONS = ')
    json.dump(unique_qs, f, indent=2, ensure_ascii=False)
    f.write(';\nwindow.MLF_QUESTIONS = window.MLT_QUESTIONS;\n')
print(f"Wrote JS bundle to {JS_BUNDLE_FILE}")

# Stats
stats = {
    'total_questions': len(unique_qs),
    'by_week': dict(week_counter),
    'by_subtopic': dict(subtopic_counter),
    'by_type': dict(Counter(q['question_type'] for q in unique_qs))
}
with open(STATS_FILE, 'w', encoding='utf-8') as f:
    json.dump(stats, f, indent=2, ensure_ascii=False)
print(f"Wrote stats to {STATS_FILE}")

