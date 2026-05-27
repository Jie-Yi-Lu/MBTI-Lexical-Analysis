"""
app.py — MBTI Lexical Analysis Streamlit 主程式
"""

import os, pickle
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats

from utils.translations import TRANSLATIONS, DIM_DISPLAY, DIM_SHORT, EFFECT_SIZE_LABELS

st.set_page_config(
    page_title='MBTI Lexical Analysis',
    page_icon='🧠',
    layout='wide',
    initial_sidebar_state='expanded',
)

# ── 資料載入 ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_results():
    path = os.path.join(os.path.dirname(__file__), 'results', 'analysis_results.pkl')
    if not os.path.exists(path): return None
    with open(path, 'rb') as f: return pickle.load(f)

@st.cache_data
def load_raw_data():
    return pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'mbti_1.csv'))

# ── 統計工具 ──────────────────────────────────────────────────────────────────
def one_sample_ttest(cv_scores, chance=0.5):
    n      = len(cv_scores)
    mean   = np.mean(cv_scores)
    std    = np.std(cv_scores, ddof=1)
    t_stat = (mean - chance) / (std / np.sqrt(n))
    p_val  = stats.t.sf(t_stat, df=n - 1)
    cohens_d = (mean - chance) / std if std > 0 else 0.0
    return float(t_stat), float(p_val), float(cohens_d)

def effect_size_label(d, lang):
    d = abs(d)
    lab = EFFECT_SIZE_LABELS[lang]
    if d < 0.2:   return lab['negligible']
    elif d < 0.5: return lab['small']
    elif d < 0.8: return lab['medium']
    else:          return lab['large']

# ── 側邊欄 ────────────────────────────────────────────────────────────────────
with st.sidebar:
    lang_choice = st.radio('🌐 Language / 語言', ['中文', 'English'], index=0)
    lang = 'zh' if lang_choice == '中文' else 'en'
    T = TRANSLATIONS[lang]

    st.divider()
    st.markdown(f"**{T['sidebar']['nav_label']}**")
    nav_opts = T['sidebar']['nav_options']
    page_display = st.radio('navigation', list(nav_opts.values()), label_visibility='collapsed')
    page_key = [k for k, v in nav_opts.items() if v == page_display][0]

    st.divider()
    with st.expander(T['sidebar']['instructions_title'], expanded=False):
        st.markdown(T['sidebar']['instructions'])

# ── 載入結果 ──────────────────────────────────────────────────────────────────
results      = load_results()
df_raw       = load_raw_data()

if results is None:
    st.error('找不到分析結果。請先執行 `python analysis.py`。\nAnalysis results not found. Please run `python analysis.py` first.')
    st.stop()

dim_results  = results['dimension_results']
sample_stats = results['sample_stats']
DIMS         = ['IE', 'NS', 'TF', 'JP']


# ════════════════════════════════════════════════════════════════
# 首頁
# ════════════════════════════════════════════════════════════════
def show_home():
    T_p = T['home']
    st.title(T_p['title'])
    st.markdown(f"##### {T_p['subtitle']}")
    st.divider()

    st.subheader(T_p['intro_header'])
    st.info(T_p['intro_q1'])

    st.divider()
    st.subheader(T_p['mbti_header'])
    st.markdown(T_p['mbti_intro'])
    st.warning(T_p['mbti_caveat'])

    st.divider()
    st.subheader(T_p['dataset_header'])
    st.markdown(T_p['dataset_text'])
    st.download_button(
        T_p['dataset_download_btn'],
        df_raw.to_csv(index=False).encode('utf-8'),
        file_name='mbti_1.csv', mime='text/csv',
    )
    st.warning(T_p['imbalance_warning'])

    st.divider()
    st.subheader(T_p['dims_header'])
    st.markdown(T_p['dims_intro'])
    st.markdown('')
    for dim_key, dim_info in T_p['dims'].items():
        with st.expander(dim_info['name'], expanded=True):
            st.markdown(dim_info['desc'])
            st.caption(f"📊 {dim_info['dist']}")

    st.divider()
    st.subheader(T_p['method_header'])
    st.markdown(T_p['method_text'])
    mt = T_p['method_terms']
    for tk, dk in [('tfidf_title','tfidf_desc'), ('lr_title','lr_desc'),
                   ('cv_title','cv_desc'), ('ba_title','ba_desc')]:
        with st.expander(f"📌 {mt[tk]}", expanded=False):
            st.markdown(mt[dk])


# ════════════════════════════════════════════════════════════════
# 樣本分布
# ════════════════════════════════════════════════════════════════
def show_sample():
    T_p = T['sample']
    st.title(T_p['title'])
    st.divider()

    tc    = sample_stats['type_counts']
    most  = max(tc, key=tc.get)
    least = min(tc, key=tc.get)

    st.subheader(T_p['stats_header'])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(T_p['total_records'], f"{sample_stats['total']:,}")
    c2.metric(T_p['n_types'],       len(tc))
    c3.metric(T_p['most_common'],   f"{most} ({tc[most]})")
    c4.metric(T_p['least_common'],  f"{least} ({tc[least]})")

    st.divider()
    st.subheader(T_p['dist_header'])
    tdf = (pd.DataFrame.from_dict(tc, orient='index', columns=[T_p['count_label']])
           .reset_index().rename(columns={'index': 'type'})
           .sort_values(T_p['count_label'], ascending=False))
    fig = px.bar(tdf, x='type', y=T_p['count_label'],
                 title=T_p['chart_title_type'],
                 color=T_p['count_label'], color_continuous_scale='Blues')
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader(T_p['dim_dist_header'])
    rows = []
    for dim, counts in sample_stats['dim_counts'].items():
        for label, count in counts.items():
            rows.append({'dimension': DIM_SHORT[lang][dim], 'type': label,
                         T_p['count_label']: count})
    fig2 = px.bar(pd.DataFrame(rows), x='dimension', y=T_p['count_label'],
                  color='type', barmode='group', title=T_p['chart_title_dim'],
                  color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader(T_p['preview_header'])
    st.dataframe(df_raw.head(20), use_container_width=True)
    st.download_button(T_p['download_btn'],
                       df_raw.to_csv(index=False).encode('utf-8'),
                       file_name=T_p['download_name'], mime='text/csv')


# ════════════════════════════════════════════════════════════════
# 維度詞彙分析與差異檢定（合併頁）
# ════════════════════════════════════════════════════════════════
def show_main():
    T_p = T['main']
    st.title(T_p['title'])
    st.divider()

    # ── 上半部：跨維度總覽 ────────────────────────────────────
    st.subheader(T_p['overview_header'])
    st.info(T_p['chance_note'])
    st.caption(T_p['l2_note'])

    dim_labels = [DIM_DISPLAY[lang][d] for d in DIMS]
    bal_accs   = [dim_results[d]['l2']['mean_balanced_acc'] for d in DIMS]
    ci_lowers  = [dim_results[d]['l2']['ci_lower']          for d in DIMS]
    ci_uppers  = [dim_results[d]['l2']['ci_upper']          for d in DIMS]

    # CI half-width（對稱）
    ci_half = [(u - l) / 2 for u, l in zip(ci_uppers, ci_lowers)]

    # Balanced Accuracy 圖表（簡單長條圖，y 軸 0–100%）
    fig = go.Figure()
    ci_half = [(u - l) / 2 for u, l in zip(ci_uppers, ci_lowers)]
    fig.add_trace(go.Bar(
        x=dim_labels, y=bal_accs,
        error_y=dict(type='data', symmetric=True, array=ci_half),
        marker_color='steelblue',
        hovertemplate='%{x}<br>Balanced Accuracy: %{y:.2f} ± %{error_y.array:.2f}<extra></extra>',
    ))
    fig.add_hline(y=0.5, line_dash='dash', line_color='red',
                  annotation_text='Chance (50%)', annotation_position='top right')
    fig.update_layout(
        title=T_p['chart_title'],
        yaxis=dict(range=[0, 1], title=T_p['balanced_acc_col'],
                   tickformat='.0%'),
        height=420, showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    # 總覽表格（欄位順序：維度 → 高於隨機猜測 → Balanced Accuracy → 95% CI）
    overview_rows = []
    for dim in DIMS:
        l2 = dim_results[dim]['l2']
        overview_rows.append({
            T_p['dim_label']:        DIM_DISPLAY[lang][dim],
            T_p['above_chance_col']: T_p['yes'] if l2['mean_balanced_acc'] > 0.5 else T_p['no'],
            T_p['balanced_acc_col']: f"{l2['mean_balanced_acc']:.4f}",
            T_p['ci_col']:           f"[{l2['ci_lower']:.4f}, {l2['ci_upper']:.4f}]",
        })
    st.dataframe(pd.DataFrame(overview_rows), use_container_width=True, hide_index=True)

    st.divider()

    # ── 結果摘要與研究問題回應（含統計檢定表格）────────────────
    st.subheader(T_p['result_header'])
    st.markdown(T_p['ttest_note'])
    st.warning(T_p['ttest_limitation'])

    # 統計檢定表格
    ttest_stats = {}
    ttest_rows  = []
    for dim in DIMS:
        scores = dim_results[dim]['l2']['cv_scores']
        t_stat, p_val, d = one_sample_ttest(scores, chance=0.5)
        sig = p_val < 0.05
        ttest_stats[dim] = {'t': t_stat, 'p': p_val, 'd': d, 'sig': sig}
        ttest_rows.append({
            T_p['dim_label']:       DIM_DISPLAY[lang][dim],
            T_p['t_col']:           f"{t_stat:.3f}",
            T_p['p_col']:           f"{p_val:.4f}",
            T_p['sig_col']:         T_p['sig_yes'] if sig else T_p['sig_no'],
            T_p['cohens_d_col']:    f"{d:.3f}",
            T_p['effect_size_col']: effect_size_label(d, lang),
        })
    st.dataframe(pd.DataFrame(ttest_rows), use_container_width=True, hide_index=True)

    st.divider()
    _render_interpretation(ttest_stats, T_p)

    st.divider()

    # ── 下半部：單一維度深入分析 ──────────────────────────────
    st.subheader(T_p['drilldown_header'])

    dim_choice = st.selectbox(
        T_p['dim_select_label'],
        options=DIMS,
        format_func=lambda k: DIM_DISPLAY[lang][k],
    )

    res   = dim_results[dim_choice]
    l2    = res['l2']
    vocab = res['vocab']
    pos   = res['pos_label']
    neg   = res['neg_label']

    if dim_choice == 'IE':   st.warning(T_p['imbalance_note_IE'])
    elif dim_choice == 'NS': st.warning(T_p['imbalance_note_NS'])

    # 各折準確率（L2）+ 各類別之準確率
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(f"**{T_p['accuracy_header']}**")
        st.metric(T_p['mean_balanced_acc'], f"{l2['mean_balanced_acc']:.4f}")
        st.caption(f"{T_p['ci_header']}：[{l2['ci_lower']:.4f}, {l2['ci_upper']:.4f}]")
        fd = {T_p['fold_label'].format(i+1): [f"{s:.4f}", f"{n}"]
              for i, (s, n) in enumerate(zip(l2['cv_scores'], l2['n_iters']))}
        fold_df = pd.DataFrame.from_dict(
            fd, orient='index',
            columns=[T_p['mean_balanced_acc'], T_p['n_iter_label']]
        )
        st.table(fold_df)

    with col_right:
        st.markdown(f"**{T_p['per_class_header']}**")
        st.caption(T_p['per_class_note'])
        pc_rows = [
            {T_p['dim_label']: pos, T_p['balanced_acc_col']: f"{l2['per_class_acc'][1]:.4f}"},
            {T_p['dim_label']: neg, T_p['balanced_acc_col']: f"{l2['per_class_acc'][0]:.4f}"},
        ]
        st.table(pd.DataFrame(pc_rows).set_index(T_p['dim_label']))

        st.markdown("---")
        st.markdown(f"**{T_p['l1_vocab_title']}**")
        st.caption(T_p['l1_vocab_note'])

    st.divider()

    # 詞彙分析
    all_words = vocab['words']
    if not all_words:
        st.warning(T_p['no_words'])
        return

    max_coef = max(abs(c) for _, c in all_words)
    min_coef = min(abs(c) for _, c in all_words if c != 0)
    st.markdown(f"**{T_p['slider_label']}**")
    st.caption(T_p['slider_explain'])
    threshold = st.slider(
        T_p['slider_label'],
        min_value=float(round(min_coef, 4)),
        max_value=float(round(max_coef, 4)),
        value=float(round(max_coef * 0.1, 4)),
        step=float(round((max_coef - min_coef) / 200, 4)),
    )
    words_above = [(w, c) for w, c in all_words if abs(c) >= threshold]
    st.markdown(T_p['n_words_above'].format(len(words_above)))

    # 係數分布圖
    coef_abs = sorted([abs(c) for _, c in all_words], reverse=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=list(range(1, len(coef_abs)+1)), y=coef_abs,
        mode='lines', line=dict(color='steelblue'),
        name=T_p['coef_abs_label'],
    ))
    fig2.add_hline(y=threshold, line_dash='dash', line_color='red',
                   annotation_text=T_p['threshold_line'],
                   annotation_position='top right')
    fig2.update_layout(
        title=T_p['dist_chart_title'],
        xaxis_title=T_p['n_words_label'],
        yaxis_title=T_p['coef_abs_label'],
        height=350,
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 代表詞彙一覽
    st.subheader(T_p['vocab_header'])
    st.caption(
        T_p['direction_pos'].format(pos) + '　　' +
        T_p['direction_neg'].format(neg)
    )
    if not words_above:
        st.info(T_p['no_words'])
    else:
        vdf = pd.DataFrame(words_above, columns=[T_p['word_col'], T_p['coef_col']])
        vdf[T_p['direction_col']] = vdf[T_p['coef_col']].apply(
            lambda c: pos if c > 0 else neg
        )
        vdf[T_p['coef_col']] = vdf[T_p['coef_col']].round(6)
        st.dataframe(vdf, use_container_width=True, hide_index=True)


# ── 結果解讀（動態生成）────────────────────────────────────────────────────────
def _render_interpretation(ttest_stats, T_p):
    sig_dims    = [d for d in DIMS if ttest_stats[d]['sig']]
    nonsig_dims = [d for d in DIMS if not ttest_stats[d]['sig']]
    fmt         = lambda d: DIM_SHORT[lang][d]
    fmt_stat    = lambda d: (f"t(4) = {ttest_stats[d]['t']:.3f}, "
                             f"p = {ttest_stats[d]['p']:.4f}, "
                             f"d = {ttest_stats[d]['d']:.3f}")
    best_dim    = max(DIMS, key=lambda d: abs(ttest_stats[d]['d']))
    worst_dim   = min(DIMS, key=lambda d: abs(ttest_stats[d]['d']))

    if lang == 'zh':
        st.markdown("#### 研究問題回應")

        if len(sig_dims) == 4:
            st.success(
                "四個 MBTI 人格維度的詞彙分類結果均顯著高於隨機猜測水準（α = 0.05），"
                "支持「各維度的自然語言用詞風格存在可觀察差異」的研究假設。"
                "這意味著，詞彙特徵確實在一定程度上反映了個人在各 MBTI 維度上的人格傾向。"
            )
        elif len(sig_dims) == 0:
            st.error(
                "四個維度的檢定結果均未達統計顯著水準（α = 0.05），"
                "現有資料不足以支持用詞風格存在系統性差異的假設。"
                "考量到本檢定自由度僅為 4，型二錯誤風險較高，"
                "建議增加交叉驗證折數以提升檢定力後再做結論。"
            )
        else:
            sig_str    = "、".join(fmt(d) for d in sig_dims)
            nonsig_str = "、".join(fmt(d) for d in nonsig_dims)
            st.warning(
                f"**{sig_str}** 的分類結果達統計顯著（α = 0.05），"
                f"支持這些維度存在可觀察的用詞風格差異；"
                f"**{nonsig_str}** 則未達顯著，現有證據不足以支持該維度存在系統性詞彙差異。"
            )

        st.markdown("**效應量分析**")
        st.markdown(
            f"效應量（Cohen's d）反映了模型表現超越隨機基準的程度。"
            f"**{fmt(best_dim)}** 效應量最大（d = {ttest_stats[best_dim]['d']:.3f}，"
            f"{effect_size_label(ttest_stats[best_dim]['d'], lang)}效應），"
            f"代表此維度的詞彙特徵最具鑑別力；"
            f"**{fmt(worst_dim)}** 效應量最小（d = {ttest_stats[worst_dim]['d']:.3f}，"
            f"{effect_size_label(ttest_stats[worst_dim]['d'], lang)}效應），"
            f"兩類型間的詞彙使用差異相對不明顯。"
        )

        st.markdown("**研究限制**")
        st.markdown(
            "本研究有兩項主要限制需要說明：\n\n"
            "1. **統計檢定力**：每個 t 檢定僅以 5 折的準確率分數為樣本（df = 4），"
            "檢定力偏低，小效應量可能因此未能達到顯著水準（型二錯誤風險較高）。\n\n"
            "2. **樣本代表性**：資料集來源為 MBTI 討論社群，I 與 N 類型過度集中，"
            "分析結果反映的是特定社群的語言風格，不宜直接推論至一般母群體。"
        )

    else:  # English
        st.markdown("#### Response to Research Question")

        if len(sig_dims) == 4:
            st.success(
                "All four MBTI dimensions showed classification performance significantly above chance (α = 0.05), "
                "supporting the hypothesis that observable lexical differences exist across dimensions. "
                "Lexical features appear to reflect, to some extent, individuals' personality preferences on each MBTI dimension."
            )
        elif len(sig_dims) == 0:
            st.error(
                "None of the four dimensions reached statistical significance (α = 0.05). "
                "The current evidence does not support systematic lexical differences across dimensions. "
                "Given the low degrees of freedom (df = 4), the risk of Type II error is elevated; "
                "increasing the number of CV folds may improve statistical power."
            )
        else:
            sig_str    = ", ".join(fmt(d) for d in sig_dims)
            nonsig_str = ", ".join(fmt(d) for d in nonsig_dims)
            st.warning(
                f"**{sig_str}** reached statistical significance (α = 0.05), "
                f"supporting observable lexical differences for these dimensions. "
                f"**{nonsig_str}** did not reach significance; "
                f"current evidence is insufficient to claim systematic lexical differences for these dimensions."
            )

        st.markdown("**Effect Size Analysis**")
        st.markdown(
            f"Cohen's d reflects the magnitude of model performance above the chance baseline. "
            f"**{fmt(best_dim)}** showed the largest effect (d = {ttest_stats[best_dim]['d']:.3f}, "
            f"{effect_size_label(ttest_stats[best_dim]['d'], lang).lower()} effect), "
            f"indicating the most discriminative lexical signal. "
            f"**{fmt(worst_dim)}** showed the smallest effect (d = {ttest_stats[worst_dim]['d']:.3f}, "
            f"{effect_size_label(ttest_stats[worst_dim]['d'], lang).lower()} effect), "
            f"suggesting more modest lexical differences between its two types."
        )

        st.markdown("**Limitations**")
        st.markdown(
            "Two key limitations should be noted:\n\n"
            "1. **Statistical power**: Each t-test uses only 5 fold-level accuracy scores (df = 4), "
            "resulting in low power. Small true effects may fail to reach significance (elevated Type II error risk).\n\n"
            "2. **Sample representativeness**: The dataset overrepresents I and N types due to its forum origin. "
            "Findings reflect the linguistic patterns of this specific community and should not be generalized to the broader population."
        )


# ── 路由 ──────────────────────────────────────────────────────────────────────
if   page_key == 'home':   show_home()
elif page_key == 'sample': show_sample()
elif page_key == 'main':   show_main()
