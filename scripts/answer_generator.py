import json
import faiss
from sentence_transformers import SentenceTransformer

# ================= FILE PATHS =================
INDEX_FILE = "data/faiss.index"
META_FILE = "data/metadata_merged.json"

# ================= LOAD MODEL & INDEX =================
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index(INDEX_FILE)

with open(META_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# ================= INTENT DETECTION =================
def detect_intent(question):
    greetings = ["hi", "hello", "hey", "namaste", "good morning", "good evening"]
    q = question.lower().strip()

    if q in greetings:
        return "greeting"

    if len(q.split()) < 3:
        return "unclear"

    return "dharmic_question"

# ================= DOMAIN GATE (DHARMIC ONLY) =================
def is_dharmic_question(question):
    q = question.lower()

    dharmic_keywords = [
        # Core concepts
        "dharma", "karma", "moksha", "yoga", "adharma",

        # Scriptures
        "mahabharata", "gita", "ramayana", "veda", "vedas",
        "upanishad", "purana", "smriti",

        # Characters
        "krishna", "arjuna", "bhishma", "vidura",
        "yudhishthira", "draupadi", "karna", "duryodhana",

        # Ethics & morality
        "truth", "justice", "duty", "righteous", "ethics",
        "moral", "responsibility", "silence", "violence", "war",

        # Human weaknesses (Dharmic context)
        "lust", "desire", "anger", "greed", "ego", "attachment",

        # Governance & life conduct
        "king", "rule", "governance", "leadership"
    ]

    return any(word in q for word in dharmic_keywords)

# ================= DHARMIC SAFETY =================
BLOCKED_TOPICS = [
    "porn", "nude", "nudity",
    "rape", "molest", "incest", "child abuse",
    "explicit", "sexual video",
    "kill all", "bomb", "terror"
]

def detect_safety_level(question):
    q = question.lower()
    for word in BLOCKED_TOPICS:
        if word in q:
            return "blocked"
    return "safe"

# ================= RELEVANCE =================
KEYWORDS = [
    "truth", "duty", "action", "attachment", "karma",
    "self", "knowledge", "desire", "lust", "war", "justice"
]

def relevance_score(text):
    if not text:
        return 0
    text = text.lower()
    return sum(1 for k in KEYWORDS if k in text)

# ================= HELPERS =================
def extract_ref_from_text(text):
    if not text:
        return ""
    if "[" in text and "]" in text:
        return text.split("]")[0].replace("[", "").strip()
    return ""

def is_judgement_question(question):
    q = question.lower()
    judgement_phrases = [
        "was", "is it right", "is it wrong", "should",
        "justified", "necessary", "correct or not"
    ]
    return any(p in q for p in judgement_phrases)

# ================= VERDICT BUILDER =================
def build_verdict(question):
    q = question.lower()

    if "mahabharata" in q and "war" in q:
        return (
            "The Mahabharata does not glorify war, but presents it as a tragic necessity "
            "that arose only after all peaceful efforts failed and injustice became unavoidable."
        )

    if "violence" in q:
        return (
            "Dharma does not approve violence for desire or gain, "
            "but permits it only as a last resort to prevent greater injustice."
        )

    if "silence" in q:
        return (
            "In Dharmic teaching, silence is not virtuous when it allows injustice to continue."
        )

    return (
        "From a Dharmic perspective, decisions are judged by intention, "
        "context, and responsibility—not rigid rules."
    )

# ================= RETRIEVE SCRIPTURES =================
def retrieve_scriptures(question, top_k=5):
    q_embedding = model.encode([question]).astype("float32")
    _, indices = index.search(q_embedding, top_k)

    scored = []
    for idx in indices[0]:
        record = metadata[idx]
        searchable_text = record.get("meaning", record.get("text", ""))
        score = relevance_score(searchable_text)
        scored.append((score, record))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [s[1] for s in scored[:3]]

# ================= CONFIDENCE =================
def compute_confidence(verses):
    score = 0
    for v in verses:
        score += relevance_score(v.get("meaning", v.get("text", "")))
    if score >= 6:
        return "High"
    elif score >= 3:
        return "Medium"
    return "Low"

# ================= EXPLANATION =================
def build_human_explanation(question, verses):
    explanation = []

    starters = [
        "According to the scriptures,",
        "In Dharmic thought,",
        "From a scriptural perspective,",
        "Ancient wisdom explains that"
    ]

    for i, v in enumerate(verses):
        meaning = v.get("meaning", v.get("text", ""))
        starter = starters[i % len(starters)]
        explanation.append(
            f"{starter} {meaning}. "
            f"This helps one understand the moral reasoning behind such actions."
        )

    explanation.append(
        "Together, these teachings emphasize awareness, responsibility, "
        "and acting with conscience rather than impulse."
    )

    return explanation

# ================= MAIN ANSWER GENERATOR =================
def generate_answer(question):
    intent = detect_intent(question)

    if intent == "greeting":
        return {
            "type": "greeting",
            "message": "🙏 Namaste. I am Dharmic AI. You can ask me questions related to Dharma."
        }

    if intent == "unclear":
        return {
            "type": "unclear",
            "message": "Please ask your question clearly in a Dharmic context."
        }

    # 🚫 DOMAIN RESTRICTION
    if not is_dharmic_question(question):
        return {
            "type": "warning",
            "message": (
                "⚠️ This assistant is strictly limited to Dharmic questions only.\n\n"
                "You may ask about Dharma, Karma, scriptures, ethical conduct, "
                "and spiritual wisdom."
            )
        }

    if detect_safety_level(question) == "blocked":
        return {
            "type": "warning",
            "message": "⚠️ This question is not appropriate for Dharmic discussion."
        }

    verses = retrieve_scriptures(question)
    confidence = compute_confidence(verses)

    explanation = []

    if is_judgement_question(question):
        explanation.append(build_verdict(question))

    explanation.extend(build_human_explanation(question, verses))

    structured_verses = []
    for v in verses:
        structured_verses.append({
            "ref": v.get("ref") or extract_ref_from_text(v.get("text", "")) or v.get("book", "Scripture"),
            "sanskrit": v.get("sanskrit", ""),
            "meaning": v.get("meaning", v.get("text", "")),
            "book": v.get("book", "Scripture")
        })

    return {
        "type": "dharmic_answer",
        "summary": "Here is a Dharmic perspective based on scriptures.",
        "explanation": explanation,
        "verses": structured_verses,
        "sources": sorted(set(v.get("book", "Scripture") for v in verses)),
        "confidence": confidence,
        "disclaimer": (
            "This response is based on Dharmic scriptures "
            "and represents one interpretive perspective."
        )
    }
