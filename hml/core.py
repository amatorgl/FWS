import re
import random
from enum import Enum
from typing import Dict, List

class Mood(Enum):
    CALM = "calm"
    HEATED = "heated"
    SENSITIVE = "sensitive"
    PLAYFUL = "playful"
    SERIOUS = "serious"
    NEUTRAL = "neutral"

class CulturalPattern(Enum):
    WESTERN = "western"
    EASTERN = "eastern"
    AMERICAN = "american"
    ASIAN = "asian"
    MIXED = "mixed"
    UNKNOWN = "unknown"

class Tone(Enum):
    POLITE = "polite"
    SARCASTIC = "sarcastic"
    HARSH = "harsh"
    SOFT = "soft"
    JOKING = "joking"
    FORMAL = "formal"
    INFORMAL = "informal"

# لایه ۱: تشخیص زمینه
def detect_context(user_input: str, history: List[str] = None) -> Dict:
    if history is None:
        history = []
    text = " ".join(history + [user_input]).lower()
    
    heated_words = len(re.findall(r'\b(angry|stupid|hate|idiot|fuck|shit)\b', text))
    playful_words = len(re.findall(r'\b(lol|haha|funny|joke|:)\b', text))
    if heated_words > 2:
        mood = Mood.HEATED.value
    elif playful_words > 2:
        mood = Mood.PLAYFUL.value
    else:
        mood = Mood.NEUTRAL.value
    
    cultural = CulturalPattern.MIXED.value if any(word in text for word in ["سلام", "hi", "merhaba"]) else CulturalPattern.UNKNOWN.value
    
    sarcastic = any(word in text for word in ["sarcasm", "obviously", "yeah right"])
    tone = Tone.SARCASTIC.value if sarcastic else Tone.INFORMAL.value
    
    emotional_intensity = min(heated_words * 0.2 + playful_words * 0.1, 1.0)
    sensitivity_level = 0.7 if any(topic in text for topic in ["politics", "religion", "race"]) else 0.2
    
    return {
        "mood": mood,
        "cultural_pattern": cultural,
        "tone": tone,
        "emotional_intensity": emotional_intensity,
        "sensitivity_level": sensitivity_level
    }

# لایه ۲: تشخیص مرزهای خاکستری
def detect_gray_zones(model_output: str, context: Dict) -> Dict:
    text = model_output.lower()
    
    ambiguity_words = len(re.findall(r'\b(maybe|perhaps|I think|probably|guess)\b', text))
    insult_words = len(re.findall(r'\b(stupid|idiot|hate|loser)\b', text))
    
    grayzone_score = min(ambiguity_words * 0.2 + insult_words * 0.3 + random.uniform(0, 0.2), 1.0)
    
    humor_vs_insult = 0.8 if any(word in text for word in ["joke", "funny", "lol"]) else 0.3
    if context["mood"] == "heated":
        humor_vs_insult = max(humor_vs_insult - 0.5, 0.0)  # در فضای گرم احتمال توهین بیشتر
    
    return {
        "grayzone_score": grayzone_score,
        "humor_vs_insult": humor_vs_insult,
        "critique_vs_attack": random.uniform(0.2, 0.8)
    }

# لایه ۳: تصمیم‌گیری
def compute_decision(context: Dict, gray: Dict, reality_alignment: float = 0.85) -> Dict:
    context_mismatch = context["sensitivity_level"] * 0.5
    
    hallucination_score = (
        gray["grayzone_score"] * 0.4 +
        context_mismatch * 0.3 +
        (1 - reality_alignment) * 0.3
    )
    
    risk_score = (
        context["emotional_intensity"] * 0.4 +
        (1 - gray["humor_vs_insult"]) * 0.3 +  # هرچه پایین‌تر، احتمال توهین بیشتر
        context["sensitivity_level"] * 0.3
    )
    
    if hallucination_score > 0.7 or risk_score > 0.7:
        decision = "human_review"
    elif hallucination_score > 0.4 or risk_score > 0.4:
        decision = "rewrite"
    else:
        decision = "allow"
    
    return {
        "hallucination_score": round(hallucination_score, 2),
        "risk_score": round(risk_score, 2),
        "decision": decision
    }