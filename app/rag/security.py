import re


class RetrievalSecurity:

    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"ignore\s+(all\s+)?prior\s+instructions",
        r"disregard\s+(all\s+)?previous\s+instructions",
        r"disregard\s+(all\s+)?prior\s+instructions",
        r"system\s+prompt",
        r"reveal\s+the\s+system\s+prompt",
        r"show\s+me\s+your\s+instructions",
        r"follow\s+these\s+instructions\s+instead",
        r"you\s+are\s+now\s+",
        r"act\s+as\s+if\s+you\s+are",
        r"override\s+your\s+instructions",
    ]

    @classmethod
    def detect_prompt_injection(cls, text: str) -> bool:

        if not text:
            return False

        normalized_text = re.sub(
            r"\s+",
            " ",
            text.lower()
        ).strip()

        return any(
            re.search(pattern, normalized_text)
            for pattern in cls.INJECTION_PATTERNS
        )

    @classmethod
    def sanitize_document(cls, text: str) -> dict:

        detected = cls.detect_prompt_injection(text)

        return {
            "content": text,
            "injection_detected": detected,
        }