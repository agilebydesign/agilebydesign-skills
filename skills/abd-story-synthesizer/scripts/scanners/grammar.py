"""Optional grammar support via NLTK. Falls back to None when NLTK unavailable (nerfed mode)."""
from typing import Any

_GRAMMAR_AVAILABLE = False
_pos_tag: Any = None
_word_tokenize: Any = None

try:
    import nltk
    from nltk import pos_tag as _pt, word_tokenize as _wt

    for resource, subpath in [
        ("punkt_tab", "tokenizers/punkt_tab"),
        ("averaged_perceptron_tagger_eng", "taggers/averaged_perceptron_tagger_eng"),
        ("wordnet", "corpora/wordnet"),
    ]:
        try:
            nltk.data.find(subpath)
        except LookupError:
            nltk.download(resource, quiet=True)

    _pos_tag = _pt
    _word_tokenize = _wt
    _GRAMMAR_AVAILABLE = True
except (ImportError, OSError, Exception):
    pass


def has_grammar_support() -> bool:
    return _GRAMMAR_AVAILABLE


def get_pos_tags(text: str) -> list[tuple[str, str]]:
    """Return [(word, tag), ...]. Empty list when grammar unavailable."""
    if not _GRAMMAR_AVAILABLE or not _word_tokenize or not _pos_tag:
        return []
    try:
        tokens = _word_tokenize(text)
        tokens = [t for t in tokens if t.isalnum() or any(c.isalnum() for c in t)]
        return _pos_tag(tokens) if tokens else []
    except Exception:
        return []


def is_verb(tag: str) -> bool:
    verb_tags = ("VB", "VBP", "VBZ", "VBD", "VBG", "VBN")
    return tag in verb_tags


def is_noun(tag: str) -> bool:
    noun_tags = ("NN", "NNS", "NNP", "NNPS")
    return tag in noun_tags
