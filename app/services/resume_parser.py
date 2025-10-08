import re
import os
from typing import Dict, List
import docx2txt
from pdfminer.high_level import extract_text as extract_pdf_text

SECTION_HEADERS = [
    r"summary", r"professional summary", r"about", r"profile",
    r"experience", r"work experience", r"employment",
    r"education", r"academics", r"qualifications",
    r"skills", r"technical skills", r"key skills"
]

TITLE_AT_RE = re.compile(r"(?P<title>.+?)\s+(?:at|@|-)\s+(?P<company>.+)", re.I)
YEARS_RE = re.compile(r"(19|20)\d{2}")
SPLIT_BULLET_RE = re.compile(r"[\n\r]+[-•\u2022]?\s*")
DEGREE_KEYWORDS = ["bachelor", "b.sc", "bsc", "b.tech", "m.tech", "master", "m.sc", "msc", "mba", "phd", "diploma"]

def extract_text_from_file(upload_file) -> str:
    filename = upload_file.filename.lower()
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext == ".pdf":
        tmp_path = f"/tmp/resume_{os.getpid()}.pdf"
        with open(tmp_path, "wb") as f:
            f.write(upload_file.file.read())
        try:
            text = extract_pdf_text(tmp_path)
        finally:
            os.remove(tmp_path)
        return text

    elif ext in [".docx", ".doc"]:
        tmp_path = f"/tmp/resume_{os.getpid()}.docx"
        with open(tmp_path, "wb") as f:
            f.write(upload_file.file.read())
        try:
            text = docx2txt.process(tmp_path) or ""
        finally:
            os.remove(tmp_path)
        return text

    else:
        upload_file.file.seek(0)
        return upload_file.file.read().decode(errors="ignore")

def split_into_sections(text: str) -> Dict[str, str]:
    lines = text.splitlines()
    header_positions = []

    for idx, line in enumerate(lines):
        s = line.strip().lower()
        for h in SECTION_HEADERS:
            if re.match(rf'^\s*{h}\s*[:\-]*\s*$', s, re.I):
                header_positions.append((idx, h))
                break
        else:
            if s.isupper() and len(s.split()) <= 4:
                for h in SECTION_HEADERS:
                    if h.split()[0] in s.lower():
                        header_positions.append((idx, s))
                        break

    if not header_positions:
        return {"full": text}

    sections = {}
    for i, (pos, header) in enumerate(header_positions):
        start = pos + 1
        end = header_positions[i + 1][0] if i + 1 < len(header_positions) else len(lines)
        sec_text = "\n".join(lines[start:end]).strip()
        sections[header] = sections.get(header, "") + "\n" + sec_text if sec_text else sections.get(header, "")
    return sections

def parse_skills(section_text: str) -> List[Dict]:
    if not section_text:
        return []
    items = re.split(r"[,;\n\r•\u2022\-]+", section_text)
    skills = []
    for it in items:
        s = it.strip()
        if len(s) < 2:
            continue
        skills.append({"name": s})
    # dedupe
    seen = set()
    deduped = []
    for s in skills:
        key = s["name"].lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(s)
    return deduped

def parse_education(section_text: str) -> List[Dict]:
    if not section_text:
        return []
    items = []
    lines = [l.strip() for l in section_text.splitlines() if l.strip()]
    current = []
    for line in lines:
        if YEARS_RE.search(line) and current:
            current.append(line)
            items.append(" ".join(current))
            current = []
        else:
            lower = line.lower()
            if any(k in lower for k in DEGREE_KEYWORDS) and current:
                items.append(" ".join(current))
                current = [line]
            else:
                current.append(line)
    if current:
        items.append(" ".join(current))

    out = []
    for i in items:
        years_list = re.findall(r"(?:19|20)\d{2}", i)
        start_year = years_list[0] if years_list else None
        end_year = years_list[1] if len(years_list) > 1 else None
        degree = None
        institution = None
        for k in DEGREE_KEYWORDS:
            if k in i.lower():
                degree = i
                break
        out.append({
            "degree": degree,
            "institution": institution,
            "start_year": start_year,
            "end_year": end_year,
            "description": i
        })
    return out

def parse_experience(section_text: str) -> List[Dict]:
    if not section_text:
        return []
    entries = []
    parts = re.split(r"\n{2,}", section_text)
    if len(parts) == 1:
        parts = SPLIT_BULLET_RE.split(section_text)

    for p in parts:
        p = p.strip()
        if not p:
            continue
        m = TITLE_AT_RE.search(p)
        title = m.group("title").strip() if m else p.splitlines()[0][:200]
        company = m.group("company").strip() if m else None
        years_list = re.findall(r"(?:19|20)\d{2}", p)
        start_date = years_list[0] if years_list else None
        end_date = years_list[1] if len(years_list) > 1 else None
        entries.append({
            "title": title,
            "company": company,
            "start_date": start_date,
            "end_date": end_date,
            "description": p
        })
    return entries

def parse_resume(upload_file) -> Dict:
    text = extract_text_from_file(upload_file) or ""
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\t", " ", text)
    secs = split_into_sections(text)

    summary = None
    for k in secs:
        if "summary" in k or "about" in k or "profile" in k:
            summary = secs[k].strip()
            break
    if not summary:
        summary = text.strip().split("\n\n")[0][:500]

    skills = []
    educations = []
    experiences = []

    for k in secs:
        if "skill" in k:
            skills = parse_skills(secs[k])
            break
    for k in secs:
        if "education" in k or "academic" in k or "qualification" in k:
            educations = parse_education(secs[k])
            break
    for k in secs:
        if "experience" in k or "employment" in k or "work" in k:
            experiences = parse_experience(secs[k])
            break

    if not skills:
        candidates = re.findall(r"\b[A-Za-z+#\.]{2,20}\b", text)
        common = ["python","java","javascript","sql","aws","docker","kubernetes","react","node","django","flask","fastapi","c++","c#"]
        found = []
        for c in candidates:
            if c.lower() in common:
                found.append(c)
        skills = [{"name": x} for x in sorted(set(found), key=lambda s: s.lower())]

    return {
        "summary": summary,
        "skills": skills,
        "educations": educations,
        "experiences": experiences,
        "raw_text_snippet": text[:2000]
    }
