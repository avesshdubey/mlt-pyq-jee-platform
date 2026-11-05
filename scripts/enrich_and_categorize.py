"""
High-Precision OCR Enrichment & Granular Subcategorization for MLT PYQ Bank
"""
import os
import json
import re
import asyncio
from PIL import Image

import winrt.windows.media.ocr as win_ocr
import winrt.windows.graphics.imaging as win_imaging
import winrt.windows.storage as win_storage

WORKSPACE_DIR = r"C:\Users\avesh\Desktop\mlt-pyq-jee-platform"
DATA_FILE = os.path.join(WORKSPACE_DIR, "data", "questions.json")
JS_BUNDLE_FILE = os.path.join(WORKSPACE_DIR, "data", "questions_data.js")
STATS_FILE = os.path.join(WORKSPACE_DIR, "data", "stats.json")

# 4-Week Granular Taxonomy Mapping
CATEGORIES = {
    "Week 1: Introduction; Unsupervised Learning - Representation learning - PCA": [
        ("1.1 Representation Learning Basics & Dimensionality Reduction", [
            "representation learning", "unsupervised learning", "dimensionality reduction", 
            "dimension reduction", "curse of dimensionality", "manifold", "feature space", 
            "high dimensional", "input space", "intrinsic dimension", "compression", "encoder",
            "feature vector", "polynomial transformation", "alphabet", "models fits the data best", "visual inspection"
        ]),
        ("1.2 Model Evaluation Metrics & Classification Diagnostics", [
            "precision", "recall", "f-1 score", "f1 score", "accuracy", "confusion matrix", 
            "true positive", "false positive", "true negative", "false negative", "classification problem", 
            "multi label", "single label", "binary class", "multi-label", "multi-class"
        ]),
        ("1.3 Regularization, Loss Functions & Model Fitting", [
            "ridge loss", "lasso loss", "regularization", "linear regression model", "perceptron", 
            "gradient descent", "loss value", "squared error", "mean squared error", "model perfectly fits", 
            "linear regression", "ridge regression", "regularization parameter", "least squares"
        ]),
        ("1.4 Data Centering, Preprocessing & Covariance Matrix", [
            "covariance matrix", "sample covariance", "centered", "centering", "mean vector", 
            "scatter matrix", "positive semi-definite", "symmetric matrix", "trace of covariance", 
            "data-matrix", "centering matrix", "centered dataset", "empirical covariance"
        ]),
        ("1.5 PCA Optimization Objective & Max-Variance Formulation", [
            "maximum variance", "max variance", "rayleigh quotient", "lagrangian", "unit norm", 
            "constrained optimization", "direction of maximum variance", "variance along", "pca objective",
            "variance of the projected", "maximize the variance"
        ]),
        ("1.6 Eigen-Decomposition & Principal Directions", [
            "eigenvalue", "eigenvalues", "eigenvector", "eigenvectors", "spectral theorem", 
            "principal direction", "principal directions", "top principal", "orthogonal directions", 
            "first principal direction", "second principal component", "first principal", "second principal", 
            "third principal", "fourth principal", "leading principal", "spectral decomposition", "diagonalization"
        ]),
        ("1.7 Variance Explained, Scree Plots & Component Selection", [
            "variance captured", "total variance", "explained variance", "fraction of variance", 
            "proportion of variance", "scree plot", "retained variance", "sum of eigenvalues", 
            "percentage of variance", "variance ratio", "eigenvalue spectrum", "proportion of total variance"
        ]),
        ("1.8 Low-Dimensional Projections & Coordinates", [
            "projection", "projected", "projecting", "subspace", "projection matrix", 
            "low-dimensional", "coordinates", "w^t x", "latent coordinates", "1d projection", 
            "2d projection", "affine subspace", "orthogonal projection", "project points", "projecting onto"
        ]),
        ("1.9 Reconstruction & Reconstruction Error Calculation", [
            "reconstruction", "reconstructed", "reconstruction error", "residue", "zero residue", 
            "squared error", "reconstruction formula", "loss of information", "distortion error", 
            "norm of residue", "best rank", "squared reconstruction error", "minimum reconstruction"
        ])
    ],
    "Week 2: Unsupervised Learning - Representation learning - Kernel PCA": [
        ("2.1 Non-linear Feature Mappings & Kernel Trick", [
            "kernel trick", "non-linear", "nonlinear", "feature map", "phi(x)", "\\phi", 
            "mapping", "inner product in feature space", "distance in feature space", "higher dimension",
            "infinite dimensional"
        ]),
        ("2.2 Mercer Kernels & Kernel Types (RBF, Polynomial)", [
            "mercer", "positive definite kernel", "kernel function", "rbf kernel", "gaussian kernel", 
            "radial basis", "polynomial kernel", "linear kernel", "sigmoid kernel", "valid kernel", 
            "kernel evaluation", "kernel width"
        ]),
        ("2.3 Gram Matrix & Centering in Feature Space", [
            "gram matrix", "kernel matrix", "k(x", "k(x,", "centering the kernel", "centering kernel", 
            "h k h", "centered kernel matrix", "psd matrix"
        ]),
        ("2.4 Kernel PCA Dual Eigenvalue Formulations", [
            "kernel pca", "kpca", "dual formulation", "dual space", "alpha", 
            "eigenvalue problem in kernel space", "normalization condition", "eigenvector in feature space"
        ]),
        ("2.5 KPCA Projections & Pre-image Problem", [
            "pre-image", "pre image", "projection onto kernel", "kpca projection", "evaluating non-linear"
        ])
    ],
    "Week 3: Unsupervised Learning - Clustering - K-means/Kernel K-means": [
        ("3.1 Clustering Formulations & Unsupervised Grouping", [
            "clustering", "clusters", "cluster", "grouping", "inter-cluster", "intra-cluster", 
            "unsupervised classification", "partitioning", "distance measure", "cluster similarity"
        ]),
        ("3.2 K-Means Distortion Objective & Mathematical Properties", [
            "distortion", "distortion measure", "objective function", "sse", "sum of squared error", 
            "inertia", "r_nk", "indicator variable", "loss function", "cluster objective", "distortion function"
        ]),
        ("3.3 Lloyd's Algorithm: Assignment & Centroid Updates", [
            "lloyd", "assignment step", "update step", "centroid update", "mean vector", 
            "closest centroid", "iteration", "iterative", "cluster center", "centroid", "centroids"
        ]),
        ("3.4 Initialization Sensitivity & K-Means++ Algorithm", [
            "initialization", "initialize", "k-means++", "kmeans++", "sensitivity to initialization", 
            "seeding", "d^2 weighting", "random initialization", "local minimum", "local minima"
        ]),
        ("3.5 Voronoi Partitions & Geometric Cluster Boundaries", [
            "voronoi", "voronoi partition", "voronoi diagram", "convex", "bisector", 
            "decision boundary", "spherical clusters", "hyperplane", "voronoi cell"
        ]),
        ("3.6 Model Selection, Silhouette & Elbow Method", [
            "elbow method", "elbow curve", "silhouette", "silhouette score", "choosing k", 
            "optimal number of clusters", "cluster validation", "gap statistic"
        ]),
        ("3.7 Kernel K-Means & Non-Convex Clustering", [
            "kernel k-means", "kernel kmeans", "non-convex", "concentric", "clustering in feature space", 
            "kernel clustering", "spectral clustering"
        ])
    ],
    "Week 4: Unsupervised Learning - Estimation - Recap of MLE + Bayesian estimation, Gaussian Mixture Model - EM algorithm": [
        ("4.1 Likelihood Formulation & Maximum Likelihood (MLE)", [
            "mle", "maximum likelihood", "log-likelihood", "likelihood function", "score function", 
            "estimator", "unbiased", "consistency", "poisson", "bernoulli", "normal distribution", 
            "parameter estimation", "likelihood of data"
        ]),
        ("4.2 Bayesian Estimation, Priors & MAP", [
            "bayesian", "prior", "posterior", "posterior mean", "beta(", "dirichlet", 
            "conjugate prior", "map", "maximum a posteriori", "bayes risk", "loss function", 
            "bayesian inference"
        ]),
        ("4.3 Latent Variable Models & Mixture Modeling", [
            "latent variable", "latent variables", "mixture model", "mixture weights", 
            "mixing coefficients", "mixture density", "marginal distribution", "incomplete data"
        ]),
        ("4.4 Gaussian Mixture Models (GMM) Parameters & Structure", [
            "gaussian mixture", "gmm", "component density", "covariance matrix", 
            "spherical covariance", "diagonal covariance", "multivariate gaussian", "mixture components"
        ]),
        ("4.5 EM Algorithm: E-Step (Responsibilities / Posterior)", [
            "e-step", "expectation step", "responsibilities", "responsibility", 
            "posterior probability of component", "soft assignment", "gamma"
        ]),
        ("4.6 EM Algorithm: M-Step (Parameter Updates)", [
            "m-step", "maximization step", "update means", "update covariances", 
            "mixing weights update", "n_k", "weighted mean"
        ]),
        ("4.7 EM Convergence & Evidence Lower Bound (ELBO)", [
            "em algorithm", "expectation-maximization", "elbo", "jensen", "lower bound", 
            "monotonicity", "convergence of em", "local maximum of likelihood"
        ])
    ]
}

def classify(text):
    text_l = text.lower()
    best_w, best_st, best_s = None, None, -1
    for w, sts in CATEGORIES.items():
        for st, kws in sts:
            s = 0
            for kw in kws:
                kw_l = kw.lower()
                if kw_l.startswith("\\"):
                    if kw_l in text_l:
                        s += 5
                elif re.search(r'\b' + re.escape(kw_l) + r'\b', text_l):
                    s += 3 + len(kw_l.split())
                elif kw_l in text_l:
                    s += 1
            if s > best_s:
                best_s, best_w, best_st = s, w, st
                
    if best_s <= 0:
        if any(k in text_l for k in ["kernel", "gram", "rbf", "phi"]):
            return "Week 2: Unsupervised Learning - Representation learning - Kernel PCA", "2.1 Non-linear Feature Mappings & Kernel Trick"
        elif any(k in text_l for k in ["cluster", "k-means", "centroid", "voronoi"]):
            return "Week 3: Unsupervised Learning - Clustering - K-means/Kernel K-means", "3.1 Clustering Formulations & Unsupervised Grouping"
        elif any(k in text_l for k in ["mle", "likelihood", "bayesian", "gmm", "em", "prior"]):
            return "Week 4: Unsupervised Learning - Estimation - Recap of MLE + Bayesian estimation, Gaussian Mixture Model - EM algorithm", "4.1 Likelihood Formulation & Maximum Likelihood (MLE)"
        else:
            return "Week 1: Introduction; Unsupervised Learning - Representation learning - PCA", "1.1 Representation Learning Basics & Dimensionality Reduction"
            
    return best_w, best_st

def clean_ocr_text(raw_text):
    t = raw_text
    t = re.sub(r'Question\s+Number\s*:\s*\d+', '', t, flags=re.I)
    t = re.sub(r'Question\s+Type\s*:\s*\w+', '', t, flags=re.I)
    t = re.sub(r'Question\s+Id\s*:\s*\d+', '', t, flags=re.I)
    t = re.sub(r'Question\s+Label\s*:\s*[\w\s]+?(?=[A-Z0-9]|$)', '', t, flags=re.I)
    t = re.sub(r'Correct\s+Marks\s*:\s*[\d.]+', '', t, flags=re.I)
    t = re.sub(r'Response\s+Type\s*:[^\n\r]*', '', t, flags=re.I)
    t = re.sub(r'Evaluation\s+Required[^\n\r]*', '', t, flags=re.I)
    t = re.sub(r'Show\s+Word\s+Count[^\n\r]*', '', t, flags=re.I)
    t = re.sub(r'Answers\s+Type[^\n\r]*', '', t, flags=re.I)
    t = re.sub(r'Text\s+Areas[^\n\r]*', '', t, flags=re.I)
    t = re.sub(r'Possible\s+Answers[^\n\r]*', '', t, flags=re.I)
    t = re.sub(r'Options\s*:', '', t, flags=re.I)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

async def main():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"Loaded {len(data)} raw questions from {DATA_FILE}")
    engine = win_ocr.OcrEngine.try_create_from_user_profile_languages()
    
    clean_questions = []
    enriched_count = 0
    
    for q in data:
        # 1. Filter out confirmation prompts
        txt = (q.get('question_text') or '').upper()
        opts = [o.get('text', '').strip().upper() for o in q.get('options', [])]
        is_conf = (
            'CROSS CHECK YOUR HALL TICKET' in txt or 
            'ARE YOU SURE' in txt or 
            'THIS IS QUESTION PAPER' in txt or 
            (len(opts) == 2 and set(opts) == {'YES', 'NO'})
        )
        if is_conf:
            continue
            
        cur_text = q.get('question_text', '').strip()
        card_rel = q.get('card_image', '').replace('/', os.sep)
        card_full = os.path.join(WORKSPACE_DIR, card_rel)
        
        # 2. OCR card if text is too short or empty
        if len(cur_text) < 25 and os.path.exists(card_full):
            try:
                f_obj = await win_storage.StorageFile.get_file_from_path_async(os.path.abspath(card_full))
                stream = await f_obj.open_async(win_storage.FileAccessMode.READ)
                decoder = await win_imaging.BitmapDecoder.create_async(stream)
                bitmap = await decoder.get_software_bitmap_async()
                res = await engine.recognize_async(bitmap)
                ocr_raw = res.text
                recovered = clean_ocr_text(ocr_raw)
                if len(recovered) > len(cur_text):
                    q['question_text'] = recovered
                    enriched_count += 1
            except Exception as e:
                pass
                
        # 3. Classify with full text (stem + options)
        combined_text = q.get('question_text', '') + " " + " ".join(o.get('text', '') for o in q.get('options', []))
        w, st = classify(combined_text)
        q['week'] = w
        q['subtopic'] = st
        clean_questions.append(q)
        
    print(f"Enriched {enriched_count} questions via OCR. Total clean questions: {len(clean_questions)}")
    
    # Re-index questions cleanly: MLT_001, MLT_002 ...
    for idx, q in enumerate(clean_questions):
        q['id'] = f"MLT_{idx+1:03d}"
        
    # Save JSON data
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(clean_questions, f, indent=2, ensure_ascii=False)
        
    # Save JS bundle
    with open(JS_BUNDLE_FILE, 'w', encoding='utf-8') as f:
        f.write('// IIT Madras BS Degree - Machine Learning Techniques (MLT) Questions Data\n')
        f.write('window.MLT_QUESTIONS = ')
        json.dump(clean_questions, f, indent=2, ensure_ascii=False)
        f.write(';\nwindow.MLF_QUESTIONS = window.MLT_QUESTIONS;\n')
        
    # Stats
    stats = {
        'total_questions': len(clean_questions),
        'by_week': {},
        'by_subtopic': {},
        'by_type': {}
    }
    for q in clean_questions:
        w = q['week']
        st = q['subtopic']
        t = q['question_type']
        stats['by_week'][w] = stats['by_week'].get(w, 0) + 1
        stats['by_subtopic'][st] = stats['by_subtopic'].get(st, 0) + 1
        stats['by_type'][t] = stats['by_type'].get(t, 0) + 1
        
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
        
    print("\n--- FINAL SUBTOPIC BREAKDOWN ---")
    by_week_st = {}
    for q in clean_questions:
        by_week_st.setdefault(q['week'], {})
        by_week_st[q['week']][q['subtopic']] = by_week_st[q['week']].get(q['subtopic'], 0) + 1
        
    for w in sorted(by_week_st):
        tot = sum(by_week_st[w].values())
        print(f"\n{w} ({tot} Questions):")
        for st, count in sorted(by_week_st[w].items()):
            pct = round((count / tot) * 100, 1)
            print(f"   {st}: {count} questions ({pct}%)")

if __name__ == "__main__":
    asyncio.run(main())
