"""
analysis.py — 預先執行的分析腳本 | Pre-computation script
執行方式: python analysis.py
"""

import os, pickle, sys
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))

from utils.cleaning import build_cleaned_corpus
from utils.modeling import run_dimension_cv, train_final_vocab_model

RESULTS_DIR = os.path.join(os.path.dirname(__file__), 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)


def main():
    print("=" * 60)
    print("MBTI Lexical Analysis — 預先分析腳本")
    print("=" * 60)

    print("\n[1/4] 載入資料...")
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'mbti_1.csv'))
    print(f"      {len(df)} 筆")

    print("\n[2/4] 清洗文本...")
    df['cleaned'] = build_cleaned_corpus(df)

    print("\n[3/4] 建立維度標籤...")
    dim_configs = {
        'IE': {'index': 0, 'pos': 'I', 'neg': 'E'},
        'NS': {'index': 1, 'pos': 'N', 'neg': 'S'},
        'TF': {'index': 2, 'pos': 'T', 'neg': 'F'},
        'JP': {'index': 3, 'pos': 'J', 'neg': 'P'},
    }
    for dim, cfg in dim_configs.items():
        df[dim] = df['type'].apply(lambda t, c=cfg: 1 if t[c['index']] == c['pos'] else 0)
        c = df[dim].value_counts()
        print(f"      {dim}: {cfg['pos']}={c.get(1,0)}, {cfg['neg']}={c.get(0,0)}")

    X = df['cleaned'].tolist()

    print("\n[4/4] 單維度分析...")
    dimension_results = {}

    for dim, cfg in dim_configs.items():
        print(f"\n  ── {dim} ──")
        y = df[dim].values

        print("      L1 CV...")
        l1_cv = run_dimension_cv(X, y, penalty='l1')
        print(f"      L1 Balanced Acc: {l1_cv['mean_balanced_acc']:.4f} "
              f"[{l1_cv['ci_lower']:.4f}, {l1_cv['ci_upper']:.4f}]")

        print("      L2 CV...")
        l2_cv = run_dimension_cv(X, y, penalty='l2')
        print(f"      L2 Balanced Acc: {l2_cv['mean_balanced_acc']:.4f} "
              f"[{l2_cv['ci_lower']:.4f}, {l2_cv['ci_upper']:.4f}]")

        print("      詞彙模型...")
        vocab = train_final_vocab_model(X, y)
        print(f"      非零詞彙：{vocab['n_nonzero']}，迭代：{vocab['n_iter']}")

        dimension_results[dim] = {
            'pos_label': cfg['pos'],
            'neg_label': cfg['neg'],
            'l1':  l1_cv,
            'l2':  l2_cv,
            'vocab': vocab,
        }

    print("\n儲存結果...")
    results = {
        'dimension_results': dimension_results,
        'sample_stats': {
            'total':       len(df),
            'type_counts': df['type'].value_counts().to_dict(),
            'dim_counts': {
                dim: {
                    cfg['pos']: int((df[dim] == 1).sum()),
                    cfg['neg']: int((df[dim] == 0).sum()),
                }
                for dim, cfg in dim_configs.items()
            },
        },
    }

    with open(os.path.join(RESULTS_DIR, 'analysis_results.pkl'), 'wb') as f:
        pickle.dump(results, f)

    df[['type', 'cleaned', 'IE', 'NS', 'TF', 'JP']].to_csv(
        os.path.join(RESULTS_DIR, 'cleaned_data.csv'), index=False
    )

    print("\n" + "=" * 60)
    print("分析完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
