"""Postmortem section plan: one focused multi-query retrieval + one short generation per section.

Works with the paper dataset (Suricata alerts, Kerberos, HTTP downloads, domains, certificates, derived findings).
A final 'Answers to Investigation Questions' section is added automatically when the incident provides questions
(see build_sections). Optional keys per section: long (bigger token budget), top_k, max_chars.
"""

SECTIONS = [
    {"name": "Affected Host and User",
     "queries": ["internal client IP address ranked by external connections", "Kerberos hostname source IP",
                 "Kerberos client account human user source IP", "derived Kerberos identity of internal client"],
     "rerank": "Which internal host is affected (IP address, hostname and human user account)?",
     "task": "State the IP address, hostname and human user account (not machine accounts ending in $) of each affected internal host, "
             "as observed. If several hosts are affected, list each separately. Domain controllers and gateways are not affected hosts."},
    {"name": "Timeline", "long": True,
     "queries": ["earliest alert hour alert timeline", "alert timeline hourly Suricata alerts UTC", "first seen last seen timestamp UTC",
                 "first contact external IP first queried domain"],
     "rerank": "Chronological order of key events with UTC timestamps.",
     "task": "Write a chronological list with ONE line per timestamp. Include only events that have their own timestamp in the evidence "
             "(alert-hour counts, first/last seen). Every line MUST start with the exact UTC date and hour from the evidence. Do not attach a "
             "timestamp to facts that have none (host identity, destinations). Merge events that share a timestamp. State the earliest alert hour. "
             "Never write placeholders."},
    {"name": "Detection: IDS Alerts",
     "queries": ["Suricata alert signatures malware CnC", "high severity alerts destinations sources",
                 "ET MALWARE trojan alert signature", "suspicious POST user agent alert"],
     "rerank": "Which Suricata alerts indicate malicious activity, and which hosts do they involve?",
     "task": "List the significant alert signatures with counts and the hosts involved. Separate high-severity malicious signatures "
             "from informational ones (such as connection tests)."},
    {"name": "Initial Infection Indicators",
     "queries": ["suspicious domains fake site download", "HTTP file downloads URI file type", "download domains requests client to server",
                 "TLS certificate self-signed IP-based", "direct IP HTTP connections raw IP"],
     "rerank": "Which domains, URLs or downloads were the likely initial infection vector?",
     "task": "List suspicious domains/URLs and downloaded files (file names, server IP/domain, client). Mark weak indicators as 'possible'. "
             "If no initial vector is visible, write 'Not established from the available artifacts'."},
    {"name": "Command-and-Control and Network Activity",
     "queries": ["most contacted external IP connections", "high severity alert destination C2 check-in",
                 "external destinations top destinations connections", "direct IP connections POST beaconing"],
     "rerank": "Which external IP addresses look like command-and-control servers and why?",
     "task": "Separate OBSERVED facts (connection counts, alert counts) from INFERRED assessment (label it 'Assessment:'; at most 3 assessment bullets, each a different conclusion). "
             "State which external IP received the most connections from the affected host(s) and whether the evidence supports C2 or a legitimate service."},
    {"name": "Impact Assessment",
     "queries": ["data theft stealer credential exfiltration alert", "ransomware encryption availability integrity", "volume of connections external destinations",
                 "number of affected hosts"],
     "rerank": "Which security property (confidentiality, integrity or availability) is targeted, and what is the scale of impact?",
     "task": "State the primary CIA component targeted (confidentiality, integrity or availability) as 'Assessment:' with supporting evidence, "
             "and the number of affected hosts and scale of external activity. Use 'possible' where evidence is indirect."},
    {"name": "Root Cause and Evidence Gaps",
     "queries": ["no matching results query returned nothing", "evidence unavailable shard failed", "initial infection vector unknown",
                 "no results certificates"],
     "rerank": "What is the most likely root cause and what cannot be determined from the evidence?",
     "task": "Give the most likely root cause as 'Assessment:' with confidence (low/medium/high). Then list what is NOT established "
             "(for example initial vector, payload behaviour, data exfiltration, queries that failed or were empty). Do not invent evidence."},
    {"name": "Corrective and Preventive Actions",
     "queries": ["block malicious IP domain", "suspicious external server alert destination", "affected host user account", "malicious download URL"],
     "rerank": "Which concrete containment and prevention actions follow from the observed indicators?",
     "task": "Give 4-6 concrete actions tied to specific observed indicators (e.g. isolate host X, reset account Y, block IP Z). No generic advice."},
]

QUESTIONS_SECTION = {
    "name": "Answers to Investigation Questions", "long": True, "per_query_k": 3, "max_chars": 6500,
    "rerank": "Evidence needed to answer the investigation questions.",
    "task": "Answer EVERY question below, one numbered line each, giving the specific values (IPs, host names, accounts, domains, UTC times) "
            "found in the evidence and a citation. For a time question give 'YYYY-MM-DD HH:MM UTC'. If the evidence does not contain the "
            "answer write 'Not established from the available artifacts'. Do not guess. FORMAT: one line per question, exactly '<number>. <answer> [evidence id]'. "
            "Do NOT repeat the question text.\nQUESTIONS:\n{questions}",
}


def build_sections(questions: list[str] | None = None) -> list[dict]:
    secs = [dict(s) for s in SECTIONS]
    if questions:
        q = dict(QUESTIONS_SECTION)
        q["queries"] = list(questions)
        q["task"] = q["task"].format(questions="\n".join(f"{i}. {t}" for i, t in enumerate(questions, 1)))
        secs.append(q)
    return secs
