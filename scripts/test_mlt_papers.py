import fitz
import glob
import os
import re

PYQS_DIR = r"C:\Users\avesh\Desktop\PYQS"

def find_mlt_boundaries(doc):
    total_pages = len(doc)
    mlt_start = None
    mlt_end = None
    
    # 1. Scan for MLT Section start
    for pno in range(total_pages):
        page = doc[pno]
        text = page.get_text()
        
        # Look for "MLT" as a section title or header
        # In TCS iON: usually "MLT\nSection Id :" or similar
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        for idx, line in enumerate(lines):
            if line == "MLT" or line == "Section : MLT" or line == "Section Name: MLT" or line == "MACHINE LEARNING TECHNIQUES":
                # Verify that it is followed by or precedes "Section Id :" or "Section Number :"
                context = " ".join(lines[max(0, idx-2):min(len(lines), idx+5)])
                if "Section Id" in context or "Section Number" in context or "Section type" in context or "Mandatory" in context:
                    mlt_start = pno
                    break
            elif re.match(r'^(Section\s*:\s*)?MLT$', line, re.IGNORECASE):
                mlt_start = pno
                break
        if mlt_start is not None:
            break
            
    if mlt_start is None:
        return None, None
        
    # 2. Scan for Section end (next subject header)
    for pno in range(mlt_start, total_pages):
        page = doc[pno]
        text = page.get_text()
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        for idx, line in enumerate(lines):
            # Check for other subjects e.g. MLP, BA, TDS, BDM, Deep Learning, etc. followed by Section Id
            if line in ["MLP", "BA", "BDM", "TDS", "DL", "AI", "DBMS", "PDSA", "SC"] or (len(line) <= 5 and line.isupper() and line != "MLT" and line not in ["YES", "NO", "MCQ", "MSQ", "SA", "MAX"]):
                context = " ".join(lines[max(0, idx-2):min(len(lines), idx+5)])
                if "Section Id :" in context and ("Section Number :" in context or "Section type :" in context):
                    if pno > mlt_start or (pno == mlt_start and idx > 15):
                        mlt_end = pno
                        return mlt_start, mlt_end
                        
    return mlt_start, total_pages - 1

def main():
    all_pdfs = sorted(glob.glob(os.path.join(PYQS_DIR, "**", "*.pdf"), recursive=True))
    print(f"Total PDFs found in {PYQS_DIR}: {len(all_pdfs)}")
    
    mlt_found = []
    for p in all_pdfs:
        if "mlf_app" in p or "PDF_COM" in p:
            continue
        try:
            doc = fitz.open(p)
            s, e = find_mlt_boundaries(doc)
            if s is not None:
                # Count Question Number : X between s and e
                q_count = 0
                for pno in range(s, e + 1):
                    txt = doc[pno].get_text()
                    matches = re.findall(r'Question Number\s*:\s*(\d+)', txt)
                    q_count += len(matches)
                mlt_found.append((p, s, e, len(doc), q_count))
            doc.close()
        except Exception as ex:
            pass
            
    print(f"\nPapers with MLT Section Identified: {len(mlt_found)}")
    total_q_instances = 0
    for p, s, e, total_p, qc in mlt_found:
        total_q_instances += qc
        rel = os.path.relpath(p, PYQS_DIR)
        print(f" * {rel}: Pages {s+1} to {e+1} (Total: {total_p}) | Qs: {qc}")
    print(f"\nTotal raw question instances: {total_q_instances}")

if __name__ == "__main__":
    main()
