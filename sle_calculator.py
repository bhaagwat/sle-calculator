import streamlit as st

st.set_page_config(page_title="SLICC 2012 SLE Calculator", layout="wide")

st.title("SLICC Criteria for Systemic Lupus Erythematosus (SLE) - 2012")
st.markdown("""
#### Diagnostic Criteria
- Must have **≥1 clinical** and **≥1 immunologic** criteria.
- **At least 4 total criteria** for a positive diagnosis.
- **OR** Biopsy-proven lupus nephritis + ANA/anti-dsDNA antibodies = Automatically Positive
""")

# Live update logic
def evaluate_sle():
    if lupus_nephritis and ana_or_dsdna:
        return True, "SLE criteria met by lupus nephritis shortcut."
    if len(clinical_selected) >= 1 and len(immunologic_selected) >= 1 and total_criteria >= 4:
        return True, "SLE criteria met by SLICC 2012 rules (≥4 total with ≥1 clinical & ≥1 immunologic)."
    return False, "SLE criteria NOT met."

st.subheader("Lupus Nephritis")
lupus_nephritis = st.checkbox("Biopsy-proven nephritis compatible with SLE")
ana_or_dsdna = st.checkbox("ANA or anti-dsDNA antibodies")

st.subheader("Clinical Criteria (Select all that apply)")
clinical_criteria = {
    "Acute cutaneous lupus": "Malar rash, bullous lupus, etc.",
    "Chronic cutaneous lupus": "Discoid rash, lupus tumidus, etc.",
    "Oral ulcers": "In absence of other causes.",
    "Nonscarring alopecia": "In absence of other causes.",
    "Synovitis": "Swelling/tenderness in ≥2 joints with morning stiffness.",
    "Serositis": "Pleuritis/pericarditis lasting >1 day.",
    "Renal": "Proteinuria ≥500 mg/day or RBC casts.",
    "Neurologic": "Seizures, psychosis, neuropathy.",
    "Hemolytic anemia": "In absence of other causes.",
    "Leukopenia or lymphopenia": "<4,000 WBCs/mm³ or <1,000 lymphocytes/mm³.",
    "Thrombocytopenia": "<100,000 platelets/mm³."
}
clinical_selected = []
for item, desc in clinical_criteria.items():
    if st.checkbox(f"{item}", help=desc):
        clinical_selected.append(item)

st.subheader("Immunological Criteria (Select all that apply)")
immunologic_criteria = {
    "ANA above laboratory reference range": "",
    "Anti-dsDNA above laboratory reference range": "ELISA ≥2x lab range.",
    "Anti-Sm": "",
    "Antiphospholipid antibody": "Lupus anticoagulant, anticardiolipin, β2 glycoprotein.",
    "Low complement": "Low C3, C4, CH50.",
    "Positive direct Coombs test": "Without hemolytic anemia."
}
immunologic_selected = []
for item, desc in immunologic_criteria.items():
    if st.checkbox(f"{item}", help=desc):
        immunologic_selected.append(item)

total_criteria = len(clinical_selected) + len(immunologic_selected)

# Diagnosis box
st.markdown("---")
positive, message = evaluate_sle()
if positive:
    st.success(f"✅ {message}")
else:
    st.error(f"❌ {message}")

# Optional: show summary
with st.expander("Show Selection Summary"):
    st.write("**Clinical criteria selected:**", clinical_selected)
    st.write("**Immunologic criteria selected:**", immunologic_selected)
    st.write(f"**Total criteria selected:** {total_criteria}")

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime

def generate_pdf(clinical, immunologic, total, diagnosis):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "SLICC 2012 SLE Diagnostic Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    y = height - 120
    c.drawString(50, y, f"Diagnosis: {'Positive' if diagnosis else 'Not Positive'}")

    y -= 30
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Clinical Criteria Selected:")
    c.setFont("Helvetica", 12)
    for item in clinical:
        y -= 20
        c.drawString(70, y, f"- {item}")

    y -= 30
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Immunologic Criteria Selected:")
    c.setFont("Helvetica", 12)
    for item in immunologic:
        y -= 20
        c.drawString(70, y, f"- {item}")

    y -= 30
    c.drawString(50, y, f"Total Criteria Selected: {total}")

    c.save()
    buffer.seek(0)
    return buffer

# 📥 Add download button
pdf_buffer = generate_pdf(clinical_selected, immunologic_selected, total_criteria, positive)

st.download_button(
    label="📄 Download PDF Report",
    data=pdf_buffer,
    file_name="sle_diagnosis_report.pdf",
    mime="application/pdf"
)

