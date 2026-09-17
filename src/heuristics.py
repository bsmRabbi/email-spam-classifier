import re
from typing import List, Tuple, Dict


class SpamHeuristicEngine:
    """Rule-based heuristic engine modeled after SpamAssassin to detect classic email

    spam, phishing, DMCA copyright extortion, and advance-fee fraud patterns.
    """

    PATTERNS: List[Tuple[str, str, float]] = [
        # --- 1. Advance-Fee / 419 / Nigerian Scam Indicators ---
        (
            r"(?:transfer|manage|receive|release|claim|deposit)\s+(?:of\s+)?(?:the\s+)?(?:huge\s+|significant\s+)?(?:sum|funds)",
            "Advance-fee fund transfer solicitation",
            3.5
        ),
        (
            r"(?:us\$|[$£€¥]|\busd\s*)\s*\d+(?:\.\d+)?\s*(?:million|billion|trillion)",
            "Extravagant monetary claim (millions/billions)",
            4.0
        ),
        (
            r"\b\d+(?:\.\d+)?\s*(?:million|billion|trillion)\s*(?:dollars?|pounds?|euros?|usd)\b",
            "Extravagant monetary sum promise",
            4.0
        ),
        (
            r"\b(?:vip|prince|barrister|diplomat|general|attorney|dr\.|mr\.|mrs\.)\s+(?:in|from)\s+(?:one\s+of\s+the\s+)?(?:african|foreign|overseas)\s+countr(?:y|ies)",
            "419 foreign dignitary / VIP trope",
            4.0
        ),
        (
            r"\bmodalities\s+(?:that\s+will\s+perfect)?\b",
            "Classic 419 scam jargon ('modalities')",
            3.0
        ),
        (
            r"\b(?:operational\s+)?bank\s+account\s+where\s+(?:the\s+)?funds\s+(?:shall|will|can)\s+be\s+transferred\b",
            "Request for bank account to transfer funds",
            4.0
        ),
        (
            r"\breturn\s+on\s+investment\s+annually\b",
            "Unsolicited investment scheme / ROI promise",
            3.0
        ),
        (
            r"\b(?:transfer|remittance|disbursement)\s+of\s+(?:the\s+)?funds\b",
            "Fund transfer solicitation",
            3.0
        ),
        (
            r"\bconfidently\s+receive\s+and\s+manage\b",
            "Fund manager / money mule solicitation trope",
            3.5
        ),
        (
            r"\brevert\s+back\s+to\s+me\b",
            "Advance-fee scam solicitation phrase ('revert back to me')",
            2.0
        ),
        (
            r"\b(?:next\s+of\s+kin|unclaimed\s+(?:inheritance|estate|consignment|contract\s+sum)|beneficiary)\b",
            "Inheritance / next-of-kin scam indicator",
            4.0
        ),
        (
            r"\bdire\s+need\s+of\s+(?:an?\s+)?(?:entrepreneur|partner|investor|manager)\b",
            "Dire need fund manager plea",
            3.5
        ),

        # --- 2. DMCA & Copyright Extortion / Malware Phishing ---
        (
            r"\b(?:copyright(?:ed)?\s+(?:images?|photos?|content|assets?)|unauthorized\s+use\s+constitutes\s+a\s+direct\s+violation)\b",
            "Copyright / Intellectual property extortion claim",
            3.0
        ),
        (
            r"\b(?:dmca|digital\s+millennium\s+copyright\s+act)\s+(?:takedown\s+notice)?\b",
            "DMCA takedown legal threat",
            2.5
        ),
        (
            r"\b(?:avoid\s+immediate\s+legal\s+action|lawsuit\s+for\s+statutory\s+damages|pursuing\s+financial\s+damages)\b",
            "Legal lawsuit extortion pressure",
            3.0
        ),
        (
            r"(?:view|download|review|see)\s+(?:the\s+)?(?:specific\s+list|copyright|infringing|evidence|notice|document).*?(?:cloud\s+repository|link\s+below|drive|dropbox|onedrive|pdf)",
            "Malicious document/link solicitation disguised as copyright evidence",
            4.0
        ),
        (
            r"\[\s*[^\]]*?(?:view|download|notice|document|pdf|link)[^\]]*?\]",
            "Bracketed phishing link / fake document download button",
            3.0
        ),
        (
            r"\bwithin\s+(?:24|48|72)\s+hours\b.*?\b(?:legal\s+action|attorney|takedown|suspended|terminated|lawsuit)\b",
            "Urgent legal/suspension deadline threat (24-72h)",
            3.5
        ),

        # --- 3. Fake Invoices & Tech Support Scams ---
        (
            r"\b(?:subscription|renewal|order|invoice)\b.*?\b(?:renewed|charged|debited|billed)\b.*?(?:[$£€¥]\s*\d+|\d+\s*dollars)",
            "Fake renewal / auto-debit invoice scam",
            3.5
        ),
        (
            r"\b(?:did\s+not\s+authorize|didn'?t\s+make\s+this\s+purchase|cancel\s+(?:your\s+)?subscription)\b.*?\bcall\s+(?:our\s+)?(?:toll-free|support|helpdesk|billing)",
            "Fake invoice refund call-center bait",
            4.0
        ),

        # --- 4. Delivery / Courier Phishing ---
        (
            r"\b(?:usps|fedex|dhl|ups|postal\s+service)\b.*?\b(?:package|parcel|delivery)\s+(?:failed|suspended|on\s+hold|pending\s+fee)",
            "Fake parcel delivery failure phishing",
            3.5
        ),
        (
            r"\b(?:reschedule\s+your\s+delivery|confirm\s+your\s+postal\s+address|pay\s+(?:redelivery|customs)\s+fee)\b",
            "Courier phishing call-to-action",
            3.5
        ),

        # --- 5. Account Phishing & Credential Harvest ---
        (
            r"\b(?:account|mailbox|profile|wallet)\s+(?:has\s+been|will\s+be)\s+(?:suspended|disabled|locked|terminated|restricted)\b",
            "Account suspension threat",
            3.0
        ),
        (
            r"\b(?:click\s+here|log\s*in|sign\s*in)\s+to\s+(?:verify|reactivate|unlock|restore|update)\s+your\s+(?:account|banking|password|identity)\b",
            "Credential phishing / verification prompt",
            4.0
        ),

        # --- 6. Prize / Sweepstakes / Lottery Scams ---
        (
            r"\b(?:congratulations|winner)\b.*?\b(?:won|awarded)\b.*?\b(?:lottery|jackpot|prize|sweepstakes)\b",
            "Lottery / Prize winning scam",
            3.5
        ),

        # --- 7. Blackmail / Extortion ---
        (
            r"\b(?:recorded\s+you|compromised\s+your\s+device|pegasus\s+spyware|send\s+(?:bitcoin|btc))\b",
            "Sextortion / malware blackmail",
            4.5
        )
    ]

    THRESHOLD: float = 4.0

    @classmethod
    def evaluate(cls, raw_text: str) -> Dict:
        """Evaluate text against heuristic scam indicators.

        Returns a dictionary with score, triggered rules, and boolean is_spam_suspicious.
        """
        score = 0.0
        triggered_rules = []

        for pattern, description, weight in cls.PATTERNS:
            if re.search(pattern, raw_text, re.IGNORECASE):
                score += weight
                triggered_rules.append(f"{description} (+{weight})")

        return {
            "score": round(score, 2),
            "triggered_rules": triggered_rules,
            "is_spam_suspicious": score >= cls.THRESHOLD
        }
