import re


def clean_text(text: str) -> str:
    """Normalize text by expanding glued words/punctuation, standardizing URLs,

    emails, monetary figures, and special characters.
    """
    if not isinstance(text, str):
        return ""

    # Separate punctuation stuck to words, e.g. "response.A" -> "response. A", "Hello,Greetings" -> "Hello, Greetings"
    text = re.sub(r'([.,!?;:"])(?=[a-zA-Z])', r'\1 ', text)
    text = re.sub(r'(?<=[a-zA-Z])(["\'])', r' \1 ', text)

    # Separate camelCase transitions if present, e.g. "AfricanCountries" -> "African Countries"
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

    # Lowercase for consistent feature mapping
    text = text.lower()

    # Repair common glued scam/email typos
    glued_word_repairs = [
        (r'\banentrepreneur\b', 'an entrepreneur'),
        (r'\bthesum\b', 'the sum'),
        (r'\bfundsto\b', 'funds to'),
        (r'\btransactionwill\b', 'transaction will'),
        (r'\basuccessful\b', 'a successful'),
        (r'\byouwould\b', 'you would'),
        (r'\bfundshall\b', 'funds shall'),
        (r'\bfurtherdetails\b', 'further details'),
        (r'\bmeso\b', 'me so'),
        (r'\bkindlyrevert\b', 'kindly revert'),
    ]
    for pattern, replacement in glued_word_repairs:
        text = re.sub(pattern, replacement, text)

    # Normalize URLs
    text = re.sub(r"https?://\S+|www\.\S+", " httpaddr ", text)

    # Normalize email addresses
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", " emailaddr ", text)

    # Normalize monetary values including large sums (e.g. US$5.2 Billion, $10,000, 50 million pounds)
    text = re.sub(
        r"(?:us\$|[$£€¥]|\busd\s*)\s*\d+(?:[.,]\d+)?\s*(?:million|billion|trillion)?|"
        r"\b\d+(?:[.,]\d+)?\s*(?:million|billion|trillion)\s*(?:dollars?|pounds?|euros?|usd)?|"
        r"[$£€¥]\s*\d+(?:[.,]\d+)?|\d+\s*(?:dollars?|pounds?|euros?)",
        " moneytoken ",
        text
    )

    # Normalize phone numbers or long digits (commonly in spam messages)
    text = re.sub(r"\b\d{7,}\b|\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b", " phonenumber ", text)

    # Normalize remaining standalone numbers
    text = re.sub(r"\b\d+\b", " numbertoken ", text)

    # Remove excess punctuation/special characters
    text = re.sub(r"[^\w\s]", " ", text)

    # Collapse multiple whitespaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def load_and_clean_data(csv_path: str = "spam.csv", include_email_samples: bool = True):
    """Load spam.csv with correct encoding, append email domain samples,

    and prepare a clean dataframe with 'label', 'label_text', and 'cleaned_text'.
    """
    import pandas as pd
    from src.email_dataset import EMAIL_SAMPLES

    encodings = ["latin-1", "utf-8", "cp1252", "iso-8859-1"]
    df = None
    for enc in encodings:
        try:
            df = pd.read_csv(csv_path, encoding=enc)
            break
        except UnicodeDecodeError:
            continue

    if df is None:
        raise ValueError(f"Could not decode {csv_path} with supported encodings.")

    # spam.csv uses 'v1' for label and 'v2' for content
    if "v1" in df.columns and "v2" in df.columns:
        df = df[["v1", "v2"]].rename(columns={"v1": "label_text", "v2": "text"})
    else:
        df = df.iloc[:, :2]
        df.columns = ["label_text", "text"]

    df = df.dropna(subset=["label_text", "text"])
    df["label_text"] = df["label_text"].astype(str).str.strip().str.lower()
    df["text"] = df["text"].astype(str)

    # Filter to only valid ham and spam rows
    df = df[df["label_text"].isin(["ham", "spam"])].copy()

    # Append email domain samples to bridge SMS -> full email domain gap
    if include_email_samples and EMAIL_SAMPLES:
        email_df = pd.DataFrame(EMAIL_SAMPLES)
        df = pd.concat([df, email_df], ignore_index=True)

    # Map to binary target: ham -> 0, spam -> 1
    df["label"] = (df["label_text"] == "spam").astype(int)

    # Clean text content
    df["cleaned_text"] = df["text"].apply(clean_text)

    # Remove any empty cleaned text entries
    df = df[df["cleaned_text"].str.strip().str.len() > 0].reset_index(drop=True)

    return df
