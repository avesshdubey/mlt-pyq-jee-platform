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
        ("1.1 Representation Learning Basics & Dimensionality Reduction", [
            "representation learning", "unsupervised learning", "dimensionality reduction", 
            "dimension reduction", "curse of dimensionality", "manifold", "feature space", 
            "high dimensional", "input space", "intrinsic dimension", "compression", "encoder",
            "feature vector", "polynomial transformation", "alphabet", "models fits the data best", "visual inspection", "pca"
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
            "percentage of variance", "variance ratio", "eigenvalue spectrum"
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
            "mapping", "inner product in feature space", "distance in feature space", "higher dimension"
        ]),
        ("2.2 Mercer Kernels & Kernel Types (RBF, Polynomial)", [
            "mercer", "positive definite kernel", "kernel function", "rbf kernel", "gaussian kernel", 
            "radial basis", "polynomial kernel", "linear kernel", "sigmoid kernel", "valid kernel", 
            "kernel evaluation"
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
            "unsupervised classification", "partitioning", "distance measure"
        ]),
        ("3.2 K-Means Distortion Objective & Mathematical Properties", [
            "distortion", "distortion measure", "objective function", "sse", "sum of squared error", 
            "inertia", "r_nk", "indicator variable", "cluster objective"
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
            "decision boundary", "spherical clusters", "hyperplane"
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
            "conjugate prior", "map", "maximum a posteriori", "bayes risk", 
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

def classify_question(text):
    text_lower = text.lower()
    
    # Week 4 checks
    has_w4 = bool(re.search(r'\b(mle|likelihood|bayesian|gmm|gaussian mixture|prior|posterior|elbo|expectation-maximization|responsibilit|latent variable)\b', text_lower)) or bool(re.search(r'\b(em algorithm|e-step|m-step)\b', text_lower))
    # Week 3 checks
    has_w3 = bool(re.search(r'\b(cluster|clustering|clusters|k-means|kmeans|k-means\+\+|lloyd|centroids?|voronoi|silhouette|elbow method)\b', text_lower))
    # Week 2 checks
    has_w2 = bool(re.search(r'\b(kernel|kernel trick|kpca|kernel pca|gram matrix|rbf kernel|gaussian kernel|polynomial kernel|mercer|feature map)\b', text_lower))
    # Week 1 checks
    has_w1 = bool(re.search(r'\b(pca|principal component|principal components|principal direction|covariance matrix|sample covariance|reconstruction error|rayleigh quotient|spectral theorem|scree plot|variance explained|eigenvalue|eigenvalues|eigenvector|eigenvectors|dimensionality reduction|representation learning|linear regression|perceptron|least squares|ridge loss|gradient descent|precision|recall|f1 score|confusion matrix)\b', text_lower))
    
    # Priority resolution
    if has_w3 and not (has_w2 and 'kernel k-means' not in text_lower) and not ('pca' in text_lower and not 'cluster' in text_lower):
        w = 'Week 3: Unsupervised Learning - Clustering - K-means/Kernel K-means'
        if 'lloyd' in text_lower or 'assignment' in text_lower or 'centroid' in text_lower or 'center' in text_lower:
            st = "3.3 Lloyd's Algorithm: Assignment & Centroid Updates"
        elif 'k-means++' in text_lower or 'kmeans++' in text_lower or 'initialization' in text_lower or 'initialize' in text_lower:
            st = "3.4 Initialization Sensitivity & K-Means++ Algorithm"
        elif 'voronoi' in text_lower or 'partition' in text_lower or 'boundary' in text_lower:
            st = "3.5 Voronoi Partitions & Geometric Cluster Boundaries"
        elif 'distortion' in text_lower or 'objective' in text_lower or 'inertia' in text_lower or 'sse' in text_lower:
            st = "3.2 K-Means Distortion Objective & Mathematical Properties"
        elif 'kernel k-means' in text_lower or 'kernel kmeans' in text_lower:
            st = "3.7 Kernel K-Means & Non-Convex Clustering"
        elif 'elbow' in text_lower or 'silhouette' in text_lower:
            st = "3.6 Model Selection, Silhouette & Elbow Method"
        else:
            st = "3.1 Clustering Formulations & Unsupervised Grouping"
        return w, st
        
    if has_w2:
        w = 'Week 2: Unsupervised Learning - Representation learning - Kernel PCA'
        if 'gram matrix' in text_lower or 'kernel matrix' in text_lower or 'h k h' in text_lower or 'centering' in text_lower:
            st = "2.3 Gram Matrix & Centering in Feature Space"
        elif 'mercer' in text_lower or 'rbf' in text_lower or 'polynomial kernel' in text_lower or 'gaussian kernel' in text_lower:
            st = "2.2 Mercer Kernels & Kernel Types (RBF, Polynomial)"
        elif 'dual' in text_lower or 'alpha' in text_lower:
            st = "2.4 Kernel PCA Dual Eigenvalue Formulations"
        elif 'pre-image' in text_lower or 'pre image' in text_lower:
            st = "2.5 KPCA Projections & Pre-image Problem"
        else:
            st = "2.1 Non-linear Feature Mappings & Kernel Trick"
        return w, st
        
    if has_w4:
        w = 'Week 4: Unsupervised Learning - Estimation - Recap of MLE + Bayesian estimation, Gaussian Mixture Model - EM algorithm'
        if 'bayesian' in text_lower or 'prior' in text_lower or 'posterior' in text_lower or 'map' in text_lower or 'beta' in text_lower:
            st = "4.2 Bayesian Estimation, Priors & MAP"
        elif 'e-step' in text_lower or 'responsibilit' in text_lower:
            st = "4.5 EM Algorithm: E-Step (Responsibilities / Posterior)"
        elif 'm-step' in text_lower:
            st = "4.6 EM Algorithm: M-Step (Parameter Updates)"
        elif 'elbo' in text_lower or 'lower bound' in text_lower or 'convergence' in text_lower or 'em algorithm' in text_lower:
            st = "4.7 EM Convergence & Evidence Lower Bound (ELBO)"
        elif 'mixture' in text_lower or 'gmm' in text_lower or 'gaussian mixture' in text_lower:
            st = "4.4 Gaussian Mixture Models (GMM) Parameters & Structure"
        elif 'latent' in text_lower:
            st = "4.3 Latent Variable Models & Mixture Modeling"
        else:
            st = "4.1 Likelihood Formulation & Maximum Likelihood (MLE)"
        return w, st
        
    # Week 1 Default / Fallback
    w = 'Week 1: Introduction; Unsupervised Learning - Representation learning - PCA'
    if 'reconstruction' in text_lower or 'residue' in text_lower:
        st = "1.9 Reconstruction & Reconstruction Error Calculation"
    elif 'eigenvalue' in text_lower or 'eigenvalues' in text_lower or 'eigenvector' in text_lower or 'eigenvectors' in text_lower or 'principal direction' in text_lower:
        st = "1.6 Eigen-Decomposition & Principal Directions"
    elif 'covariance' in text_lower or 'centered' in text_lower or 'centering' in text_lower or 'scatter' in text_lower:
        st = "1.4 Data Centering, Preprocessing & Covariance Matrix"
    elif 'variance' in text_lower or 'objective' in text_lower or 'rayleigh' in text_lower:
        st = "1.5 PCA Optimization Objective & Max-Variance Formulation"
    elif 'projection' in text_lower or 'coordinates' in text_lower or 'projected' in text_lower:
        st = "1.8 Low-Dimensional Projections & Coordinates"
    elif 'regularization' in text_lower or 'ridge' in text_lower or 'lasso' in text_lower or 'gradient descent' in text_lower or 'loss' in text_lower or 'perceptron' in text_lower or 'linear regression' in text_lower or 'fits the data' in text_lower:
        st = "1.3 Regularization, Loss Functions & Model Fitting"
    elif 'precision' in text_lower or 'recall' in text_lower or 'f1' in text_lower or 'confusion matrix' in text_lower or 'accuracy' in text_lower:
        st = "1.2 Model Evaluation Metrics & Classification Diagnostics"
    else:
        st = "1.1 Representation Learning Basics & Dimensionality Reduction"
    return w, st
            
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
    is_legacy = False
    
    for pno in range(total_pages):
        text = doc[pno].get_text()
        lines = [l.strip().replace('\xa0', '').strip() for l in text.splitlines() if l.strip().replace('\xa0', '').strip()]
        for idx, line in enumerate(lines):
            # Modern format
            if line == 'Section Id :' and idx > 0:
                sec_name = lines[idx-1]
                if sec_name.upper() in ['MLT', 'MACHINE LEARNING TECHNIQUES'] or re.match(r'^(Section\s*:\s*)?MLT$', sec_name, re.IGNORECASE):
                    start_p = pno
                    sr = doc[pno].search_for('Section Id :')
                    y_start = sr[0].y0 - 20 if sr else 0
                    break
            # Legacy format: MLT followed by Number of Questions
            elif line.upper() == 'MLT' and idx + 1 < len(lines) and 'Number of Questions' in lines[idx+1]:
                start_p = pno
                sr = doc[pno].search_for('MLT')
                y_start = sr[0].y0 - 10 if sr else 0
                is_legacy = True
                break
        if start_p is not None:
            break
            
    if start_p is None:
        return None, 0, None, 0
        
    for pno in range(start_p, total_pages):
        text = doc[pno].get_text()
        lines = [l.strip().replace('\xa0', '').strip() for l in text.splitlines() if l.strip().replace('\xa0', '').strip()]
        for idx, line in enumerate(lines):
            if not is_legacy:
                if line == 'Section Id :' and idx > 0:
                    sec_name = lines[idx-1]
                    if sec_name.upper() not in ['MLT', 'MACHINE LEARNING TECHNIQUES']:
                        sr = doc[pno].search_for('Section Id :')
                        if pno == start_p:
                            sr = [rect for rect in sr if rect.y0 > y_start + 100]
                        y_sec = min((rect.y0 for rect in sr), default=0) - 10 if sr else 0
                        if pno > start_p or (pno == start_p and y_sec > y_start + 100):
                            end_p = pno
                            y_end = y_sec
                            return start_p, y_start, end_p, y_end
            else:
                # In legacy papers (QPG1/QPG2), MLT ends when a new subject header appears (e.g. Java) with 'Number of Questions :'
                if line == 'Number of Questions :' and (pno > start_p or (pno == start_p and idx > 3)):
                    sec_name = lines[idx-1] if idx > 0 else ''
                    if sec_name.upper() not in ['MLT', 'MACHINE LEARNING TECHNIQUES']:
                        sr = doc[pno].search_for('Number of Questions :')
                        if pno == start_p:
                            sr = [rect for rect in sr if rect.y0 > y_start + 100]
                        y_sec = min((rect.y0 for rect in sr), default=0) - 10 if sr else 0
                        if pno > start_p or (pno == start_p and y_sec > y_start + 100):
                            end_p = pno
                            y_end = y_sec
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
                
            if m_id:
                q_id = m_id.group(1)
            else:
                base_clean = re.sub(r'[^A-Za-z0-9]', '_', paper_name.replace('.pdf', ''))
                q_id = f"{base_clean}_Q{q_num}"
            
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
