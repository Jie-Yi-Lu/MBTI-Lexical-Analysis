"""
utils/modeling.py
模型訓練與評估函式 | Model training and evaluation functions
"""

import warnings
import numpy as np
from itertools import combinations
from scipy import stats
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import balanced_accuracy_score, accuracy_score

warnings.filterwarnings('ignore', category=FutureWarning, module='sklearn')

FACTORS = ['IE', 'NS', 'TF', 'JP']
DIM_INDEX = {'IE': 0, 'NS': 1, 'TF': 2, 'JP': 3}
CHANCE_BASELINE = {1: 0.5, 2: 0.25, 3: 0.125, 4: 0.0625}
N_CLASSES = {1: 2, 2: 4, 3: 8, 4: 16}


def get_all_factor_combinations():
    """
    回傳所有 15 種因子組合（1 到 4 個因子）
    Returns all 15 factor combinations (1 to 4 factors)
    """
    combos = []
    for n in range(1, 5):
        for combo in combinations(FACTORS, n):
            combos.append(combo)
    return combos


def make_combined_labels(df, factor_combo: tuple):
    """
    依指定因子組合建立複合標籤（因子間無順序關係）
    Build composite labels from a factor combination (order-independent)

    e.g., ('IE', 'TF') → 'IT', 'IF', 'ET', 'EF'
    """
    def get_label(mbti_type):
        return ''.join(mbti_type[DIM_INDEX[f]] for f in factor_combo)
    return df['type'].apply(get_label)


def get_tfidf_vectorizer():
    return TfidfVectorizer(
        max_features=10000,
        min_df=5,
        max_df=0.7,
        ngram_range=(1, 1),
        stop_words='english',
    )


def compute_confidence_interval(scores: list, confidence: float = 0.95):
    """t 分布信賴區間（自由度 = n-1）"""
    n = len(scores)
    mean = np.mean(scores)
    se = stats.sem(scores)
    t_val = stats.t.ppf((1 + confidence) / 2, df=n - 1)
    return mean, mean - t_val * se, mean + t_val * se


def run_dimension_cv(X: list, y: np.ndarray, penalty: str = 'l2', n_splits: int = 5):
    """單維度 Stratified 5-Fold CV"""
    solver = 'liblinear' if penalty == 'l1' else 'lbfgs'
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

    cv_balanced_accs = []
    fold_per_class_accs = {0: [], 1: []}
    n_iters = []
    X_arr = np.array(X)

    for train_idx, test_idx in skf.split(X_arr, y):
        X_train = X_arr[train_idx].tolist()
        X_test  = X_arr[test_idx].tolist()
        y_train = y[train_idx]
        y_test  = y[test_idx]

        vectorizer = get_tfidf_vectorizer()
        X_train_tf = vectorizer.fit_transform(X_train)
        X_test_tf  = vectorizer.transform(X_test)

        model = LogisticRegression(
            penalty=penalty, solver=solver,
            class_weight='balanced', max_iter=1000, random_state=42,
        )
        model.fit(X_train_tf, y_train)
        y_pred = model.predict(X_test_tf)

        cv_balanced_accs.append(balanced_accuracy_score(y_test, y_pred))
        for cls in [0, 1]:
            mask = y_test == cls
            if mask.sum() > 0:
                fold_per_class_accs[cls].append(accuracy_score(y_test[mask], y_pred[mask]))

        n_iters.append(int(model.n_iter_[0]))

    mean_bal, ci_lower, ci_upper = compute_confidence_interval(cv_balanced_accs)

    return {
        'cv_scores':         cv_balanced_accs,
        'mean_balanced_acc': mean_bal,
        'ci_lower':          ci_lower,
        'ci_upper':          ci_upper,
        'per_class_acc': {
            0: float(np.mean(fold_per_class_accs[0])),
            1: float(np.mean(fold_per_class_accs[1])),
        },
        'n_iters': n_iters,
    }


def train_final_vocab_model(X: list, y: np.ndarray):
    """L1 全資料訓練，取非零係數詞彙"""
    vectorizer = get_tfidf_vectorizer()
    X_tfidf = vectorizer.fit_transform(X)

    model = LogisticRegression(
        penalty='l1', solver='liblinear',
        class_weight='balanced', max_iter=1000, random_state=42,
    )
    model.fit(X_tfidf, y)

    feature_names = vectorizer.get_feature_names_out()
    coefs = model.coef_[0]

    word_coef_pairs = [
        (feature_names[i], float(coefs[i]))
        for i in range(len(coefs)) if coefs[i] != 0.0
    ]
    word_coef_pairs.sort(key=lambda x: abs(x[1]), reverse=True)

    return {
        'words':     word_coef_pairs,
        'n_nonzero': len(word_coef_pairs),
        'n_iter':    int(model.n_iter_[0]),
    }


def run_factor_combo_cv(X: list, y_series, n_splits: int = 5):
    """
    多元分類 Stratified 5-Fold CV（用於因子組合分析）
    Multiclass Stratified 5-Fold CV for factor combination analysis
    """
    y = y_series.values
    X_arr = np.array(X)
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    cv_scores = []

    for train_idx, test_idx in skf.split(X_arr, y):
        X_train = X_arr[train_idx].tolist()
        X_test  = X_arr[test_idx].tolist()
        y_train = y[train_idx]
        y_test  = y[test_idx]

        vectorizer = get_tfidf_vectorizer()
        X_train_tf = vectorizer.fit_transform(X_train)
        X_test_tf  = vectorizer.transform(X_test)

        model = LogisticRegression(
            penalty='l2', solver='saga',
            class_weight='balanced', max_iter=2000, random_state=42,
        )
        model.fit(X_train_tf, y_train)
        y_pred = model.predict(X_test_tf)
        cv_scores.append(balanced_accuracy_score(y_test, y_pred))

    mean_bal, ci_lower, ci_upper = compute_confidence_interval(cv_scores)

    return {
        'cv_scores':         cv_scores,
        'mean_balanced_acc': mean_bal,
        'ci_lower':          ci_lower,
        'ci_upper':          ci_upper,
    }
