"""
utils/cleaning.py
資料清洗函式 | Data cleaning functions
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def download_nltk_data():
    for pkg in ['stopwords', 'wordnet', 'omw-1.4']:
        nltk.download(pkg, quiet=True)


# ── 需移除的 MBTI 相關字詞 ──────────────────────────────────────────────────

MBTI_PHRASES = [
    'personality type', 'personality test',
    'cognitive functions', 'cognitive function',
    'shadow function', 'inferior function',
    'ne dom', 'ni dom', 'se dom', 'si dom',
    'te dom', 'ti dom', 'fe dom', 'fi dom',
    'sexual subtype',
]

_BASE_TYPES = [
    'infj', 'enfp', 'intj', 'intp', 'entj', 'entp', 'enfj',
    'isfj', 'isfp', 'istj', 'istp', 'esfj', 'esfp', 'estj', 'estp', 'infp',
]

MBTI_SINGLE_TERMS = (
    _BASE_TYPES
    + [t + 's' for t in _BASE_TYPES]          # 複數形：enfps, intjs ...
    + ['mbti', 'myers', 'briggs']
    + ['introvert', 'introverted',
       'extrovert', 'extroverted',
       'extravert', 'extraverted',
       'intuitive', 'intuition', 'sensing',
       'thinker', 'feeler',
       'judger', 'perceiver', 'judging', 'perceiving']
    # 認知功能縮寫（兩字母）
    + ['ne', 'ni', 'se', 'si', 'te', 'ti', 'fe', 'fi']
    # 兩字母溫度／態度分組
    + ['nt', 'nf', 'st', 'sf',
       'sp', 'sj', 'np', 'nj',
       'ep', 'ej', 'ip', 'ij']
    # 三字母部分類型代碼
    + ['nfp', 'ntp', 'ntj', 'nfj',
       'sfp', 'sfj', 'stp', 'stj',
       'ifp', 'itp', 'itj', 'ifj',
       'efp', 'efj', 'etj', 'etp',
       'enp', 'enj', 'inp', 'inj']
    # x 萬用字元變體（四字母）
    + ['intx', 'infx', 'inxp', 'inxj', 'inxx',
       'enxp', 'enxj', 'enxx',
       'esxp', 'esxj', 'esxx',
       'isxp', 'isxj', 'isxx',
       'istx', 'isfx', 'esfx', 'estx',
       'entx', 'enfx',
       'xnfp', 'xnfj', 'xntp', 'xntj',
       'xsfp', 'xsfj', 'xstp', 'xstj']
    # 其他
    + ['sx']
)


def clean_text(text: str, lemmatizer: WordNetLemmatizer, stop_words: set) -> str:
    # 1a. 移除多字詞組
    for phrase in MBTI_PHRASES:
        text = re.sub(r'\b' + re.escape(phrase) + r'\b', ' ', text, flags=re.IGNORECASE)

    # 1b. 移除單字 MBTI 術語
    for term in MBTI_SINGLE_TERMS:
        text = re.sub(r'\b' + re.escape(term) + r'\b', ' ', text, flags=re.IGNORECASE)

    # 2. 移除 URL
    text = re.sub(r'http\S+|www\S+|https\S+', ' ', text)

    # 3. 移除 ||| 分隔符
    text = text.replace('|||', ' ')

    # 4. 轉小寫
    text = text.lower()

    # 5. 移除表情符號格式 :word:
    text = re.sub(r':[a-z_]+:', ' ', text)

    # 6. 移除標點與數字
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # 7 & 8. 移除停用詞 + Lemmatization
    tokens = [
        lemmatizer.lemmatize(token)
        for token in text.split()
        if token not in stop_words and len(token) > 1
    ]

    return ' '.join(tokens)


def build_cleaned_corpus(df):
    download_nltk_data()
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    print("正在清洗文本... | Cleaning text...")
    cleaned = df['posts'].astype(str).apply(
        lambda text: clean_text(text, lemmatizer, stop_words)
    )
    print(f"完成 | Done. {len(cleaned)} 筆資料已清洗。")
    return cleaned
