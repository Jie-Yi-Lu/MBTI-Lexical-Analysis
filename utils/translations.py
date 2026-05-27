"""
utils/translations.py — 中英文介面文字對照 | Bilingual UI text
"""

DIM_DISPLAY = {
    'zh': {
        'IE': '能量來源：內向 (I) / 外向 (E)',
        'NS': '資訊收集：直覺 (N) / 感官 (S)',
        'TF': '決策依據：思考 (T) / 情感 (F)',
        'JP': '生活態度：判斷 (J) / 感知 (P)',
    },
    'en': {
        'IE': 'Energy Source: Introversion (I) / Extroversion (E)',
        'NS': 'Information Gathering: Intuition (N) / Sensing (S)',
        'TF': 'Decision Making: Thinking (T) / Feeling (F)',
        'JP': 'Lifestyle: Judging (J) / Perceiving (P)',
    },
}

DIM_SHORT = {
    'zh': {'IE': '能量來源', 'NS': '資訊收集', 'TF': '決策依據', 'JP': '生活態度'},
    'en': {'IE': 'Energy Source', 'NS': 'Info. Gathering', 'TF': 'Decision Making', 'JP': 'Lifestyle'},
}

EFFECT_SIZE_LABELS = {
    'zh': {'negligible': '可忽略', 'small': '小', 'medium': '中', 'large': '大'},
    'en': {'negligible': 'Negligible', 'small': 'Small', 'medium': 'Medium', 'large': 'Large'},
}

TRANSLATIONS = {
    'zh': {
        'sidebar': {
            'language_label': '🌐 語言 Language',
            'nav_label': '📄 分頁導覽',
            'nav_options': {
                'home':   '🏠 首頁',
                'sample': '📊 樣本分布',
                'main':   '🔤 維度詞彙分析與差異檢定',
            },
            'instructions_title': '📖 操作說明',
            'instructions': """
**首頁**
了解本專案的研究背景、MBTI 四個維度說明與分析方法概覽。

**樣本分布**
瀏覽資料集的描述統計與樣本預覽，並可下載完整 CSV。

**維度詞彙分析與差異檢定**

*上半部：跨維度總覽*
- 查看四個維度的 Balanced Accuracy 比較圖
- 檢視統計檢定結果（t 值、p 值、Cohen's d）
- 閱讀研究問題回應與結果解讀

*下半部：單一維度深入分析*
1. 從下拉選單選擇要深入分析的維度
2. 查看該維度各折準確率與各類別之準確率
3. 拖動滑桿調整係數截點，數值越高篩選越嚴格，詞彙越少但越具代表性
4. 查看代表詞彙一覽表
""",
        },

        'home': {
            'title':    'MBTI 詞彙分析',
            'subtitle': '自然語言處理 × 人格類型',
            'intro_header': '研究問題',
            'intro_q1': '在各 MBTI 人格維度中，不同類型的個體在詞彙使用偏好上是否存在差異？',
            'dataset_header': '關於資料集',
            'dataset_text': '本分析使用來自 Kaggle 的 MBTI Personality Type Dataset，共包含 **8,675** 名用戶及其在社群媒體上最近的 50 則貼文。',
            'dataset_download_btn': '⬇️ 下載原始資料集 CSV',
            'mbti_header': '什麼是 MBTI？',
            'mbti_intro': 'Myers-Briggs Type Indicator（MBTI，邁爾斯-布里格斯類型指標）是一種基於卡爾·榮格（Carl Gustav Jung）的心理類型理論發展的人格評量工具。它透過四大維度（能量來源、資訊收集、決策依據、生活態度）、八個面向的二分法組合，將人類的人格特質歸納為 **16 型人格**。',
            'mbti_caveat': '然而，MBTI 在學術上的效度存在爭議——許多心理學研究指出它的**重測信度偏低**（同一個人隔段時間再測，結果可能不同）。此外，本資料集中的 MBTI 類型為用戶自行申報，來自網路論壇，用戶可能是做了免費的線上測驗（效度參差不齊）、或根據自我認同填寫，而非經過正式評量，資料本身的準確性存在一定程度的不確定性。',
            'dims_header': 'MBTI 四個維度',
            'dims_intro': 'MBTI 人格類型由四個維度各取一個傾向組合而成，例如 **INFP** 代表 Introversion、Intuition、Feeling、Perceiving。',
            'dims': {
                'IE': {'name': '能量來源：內向 (I) / 外向 (E)', 'desc': 'I（內向）傾向從獨處和內在思考獲取能量；E（外向）傾向從社交互動獲取能量。', 'dist': 'I：6,676 人（77.0%）／ E：1,999 人（23.0%）'},
                'NS': {'name': '資訊收集：直覺 (N) / 感官 (S)', 'desc': 'N（直覺）傾向關注抽象概念與未來可能性；S（感官）傾向關注具體細節與當下現實。', 'dist': 'N：7,478 人（86.2%）／ S：1,197 人（13.8%）'},
                'TF': {'name': '決策依據：思考 (T) / 情感 (F)', 'desc': 'T（思考）傾向以邏輯和客觀標準做決策；F（情感）傾向以人際和諧與價值觀做決策。', 'dist': 'T：3,981 人（45.9%）／ F：4,694 人（54.1%）'},
                'JP': {'name': '生活態度：判斷 (J) / 感知 (P)', 'desc': 'J（判斷）傾向偏好計畫與結構；P（感知）傾向偏好彈性與開放性。', 'dist': 'J：3,434 人（39.6%）／ P：5,241 人（60.4%）'},
            },
            'imbalance_warning': '⚠️ **樣本偏差說明**：本資料集來源為 MBTI 討論社群，I 與 N 類型用戶聚集比例偏高，不代表真實世界的人口分布（現實中 S 類型約佔 73%）。分析結論僅反映此社群媒體樣本，S 與 E 類型樣本較少，其結果不宜過度推論至一般母群體。',
            'method_header': '分析方法概覽',
            'method_text': '本專案以 **TF-IDF** 萃取詞彙特徵，搭配 **Logistic Regression（L1/L2 Regularization）** 對每個 MBTI 維度進行二元分類，並以 **Stratified 5-Fold Cross Validation** 評估模型表現，報告 **Balanced Accuracy** 與 **95% 信賴區間**。',
            'method_terms': {
                'tfidf_title': 'TF-IDF（詞頻-逆文件頻率）',
                'tfidf_desc':  '衡量一個詞對某類文件重要性的指標。詞頻（TF）越高、且在其他類別中越少見（IDF 越高），分數越高，代表該詞越具鑑別力。能自動過濾常見無意義詞彙，凸顯真正能區分類別的特徵詞。',
                'lr_title':    'Logistic Regression with L1/L2 Regularization',
                'lr_desc':     '用於二元分類的統計模型。Regularization 機制透過懲罰過大的詞彙係數防止 overfitting（過度擬合）。L1 Regularization 會將不重要詞彙的係數歸零，自動篩選代表詞彙；L2 Regularization 縮小所有係數，追求整體預測穩定性。\n\n本專案對四個 MBTI 維度各自訓練一個二元分類模型（I vs E、N vs S、T vs F、J vs P）。其中 **L1 模型**用於萃取各維度的代表詞彙（係數不為零的詞即為代表詞），**L2 模型**用於報告 Balanced Accuracy 與統計檢定，各有分工。',
                'cv_title':    'Stratified 5-Fold Cross Validation（分層五折交叉驗證）',
                'cv_desc':     '將資料分為五份輪流訓練與測試，確保每份的類別比例與原始資料一致。比單次訓練測試切割更穩定可靠，不會因偶然的資料切割影響結果。',
                'ba_title':    'Balanced Accuracy（平衡準確率）',
                'ba_desc':     '各類別準確率的平均值，讓每個類別對最終分數的貢獻相等，不受樣本數多寡影響。在類別不平衡的情境下（例如本資料集的 N/S 維度），比整體準確率更能反映模型的真實表現。',
            },
        },

        'sample': {
            'title': '樣本分布', 'stats_header': '描述統計',
            'total_records': '總筆數', 'n_types': 'MBTI 類型數',
            'most_common': '最多人的類型', 'least_common': '最少人的類型',
            'dist_header': 'MBTI 類型分布', 'dim_dist_header': '四個維度分布',
            'preview_header': '資料預覽（前 20 筆）',
            'download_btn': '⬇️ 下載完整 CSV', 'download_name': 'mbti_1.csv',
            'chart_title_type': 'MBTI 類型分布', 'chart_title_dim': '各維度類型分布',
            'count_label': '人數',
        },

        'main': {
            'title':    '維度詞彙分析與差異檢定',
            'overview_header': '跨維度總覽',
            'l2_note':          '以下準確率指標均使用 **L2 Regularization** 模型（最佳化整體預測穩定性）。詞彙代表性分析（下方）另外使用 **L1 Regularization** 模型（自動篩選代表詞彙）。',
            'chart_axis_note':  '⚠️ y 軸為截斷顯示（0–10% 與 40–100%），以凸顯高於隨機基準的差異。',

            # 圖表
            'chance_note':      '二元分類隨機猜測基準為 **50%**',
            'chart_title':      '各維度 Balanced Accuracy（含 95% 信賴區間）',
            'balanced_acc_col': 'Balanced Accuracy',
            'above_chance_col': '高於隨機猜測',
            'ci_col':           '95% CI',
            'yes': '✅ 是', 'no': '❌ 否',

            # 統計檢定
            'ttest_header':     '統計檢定：各維度用詞差異是否顯著？',
            'ttest_note':       '對每個維度的 5 折 Balanced Accuracy 分數進行**單樣本 t 檢定**（單尾），虛無假設 H₀：平均 Balanced Accuracy = 0.5（隨機猜測水準）。',
            'ttest_limitation': '⚠️ **統計檢定力說明**：本檢定以 5 折交叉驗證的 5 個分數為樣本（自由度 = 4），統計檢定力偏低，偵測小效果量的能力有限。',
            'dim_label':        '維度',
            't_col':            't 值',
            'p_col':            'p 值（單尾）',
            'sig_col':          '顯著（α = 0.05）',
            'cohens_d_col':     "Cohen's d",
            'effect_size_col':  '效果量',
            'sig_yes': '✅ 是', 'sig_no': '❌ 否',

            # 結果摘要
            'result_header':    '結果摘要與研究問題回應',

            # 單一維度深入分析
            'drilldown_header':  '單一維度深入分析',
            'dim_select_label':  '選擇維度',
            'accuracy_header':   '模型準確率（L2 Regularization + Stratified 5-Fold）',
            'mean_balanced_acc': '平均 Balanced Accuracy',
            'fold_label':        '第 {} 折',
            'ci_header':         '95% 信賴區間',
            'n_iter_label':      '最終模型收斂迭代次數',
            'per_class_header':  '各類別之準確率',
            'per_class_note':    '各類別準確率為 5 折的平均值',
            'n_iter_label':      '迭代次數',
            'n_iter_note':       '若迭代次數等於 max_iter（1000），代表模型尚未完全收斂，建議調高 max_iter。',
            'l1_vocab_title':    '代表詞彙說明',
            'l1_vocab_note':     '以下代表詞彙由 L1 模型萃取。L1 Regularization 會將不重要詞彙的係數歸零，係數不為零的詞即為代表詞彙。',
            'n_iter_col':        '迭代次數',
            'imbalance_note_IE': '⚠️ 能量來源（I/E）維度樣本不平衡（I：77.0%，E：23.0%），代表詞彙解讀請保持保留態度，結果不宜推論至一般母群體。',
            'imbalance_note_NS': '⚠️ 資訊收集（N/S）維度樣本嚴重不平衡（N：86.2%，S：13.8%），S 類型樣本數偏少，其代表詞彙穩定性較低，結果不宜推論至一般母群體。',
            'slider_label':      '係數截點',
            'slider_explain':    '在「控制其他所有詞彙的情況下」，讓模型將某一詞彙判斷為某一類型的傾向有多強。\n數值越高，篩選越嚴格，詞彙越少而越具代表性。',
            'n_words_above':     '截點以上共 **{}** 個詞彙',
            'dist_chart_title':  '係數絕對值分布',
            'coef_abs_label':    '係數絕對值',
            'n_words_label':     '詞彙數',
            'threshold_line':    '目前截點',
            'vocab_header':      '代表詞彙一覽',
            'direction_pos':     '係數為正 → 傾向 {}',
            'direction_neg':     '係數為負 → 傾向 {}',
            'word_col':          '詞彙',
            'coef_col':          '係數',
            'direction_col':     '方向',
            'no_words':          '目前截點下無詞彙，請降低係數截點。',
        },
    },

    'en': {
        'sidebar': {
            'language_label': '🌐 Language',
            'nav_label': '📄 Navigation',
            'nav_options': {
                'home':   '🏠 Home',
                'sample': '📊 Sample Distribution',
                'main':   '🔤 Vocabulary Analysis & Significance Testing',
            },
            'instructions_title': '📖 Instructions',
            'instructions': """
**Home**
Learn about the research background, the four MBTI dimensions, and the analytical approach.

**Sample Distribution**
Browse descriptive statistics and a data preview. Download the full CSV.

**Vocabulary Analysis & Significance Testing**

*Upper section: Cross-dimension overview*
- Compare Balanced Accuracy across all four dimensions
- View statistical test results (t-value, p-value, Cohen's d)
- Read the response to the research question

*Lower section: Single-dimension deep-dive*
1. Select a dimension from the dropdown
2. View fold-level accuracy and per-class breakdown
3. Drag the slider to adjust the coefficient threshold
4. Explore representative vocabulary
""",
        },

        'home': {
            'title':    'MBTI Lexical Analysis',
            'subtitle': 'Natural Language Processing × Personality Types',
            'intro_header': 'Research Question',
            'intro_q1': 'Do individuals of different personality types within each MBTI dimension differ in their vocabulary usage preferences?',
            'dataset_header': 'About the Dataset',
            'dataset_text': 'This analysis uses the MBTI Personality Type Dataset from Kaggle, comprising **8,675** users and their 50 most recent social media posts.',
            'dataset_download_btn': '⬇️ Download Raw Dataset CSV',
            'mbti_header': 'What is MBTI?',
            'mbti_intro': "The Myers-Briggs Type Indicator (MBTI) is a personality assessment tool developed from Carl Gustav Jung's theory of psychological types. It categorizes human personality traits into **16 personality types** through binary combinations across four dimensions: Energy Source, Information Gathering, Decision Making, and Lifestyle.",
            'mbti_caveat': "However, MBTI's academic validity has been contested — many psychological studies note its **low test-retest reliability** (the same person may receive different results across administrations). Furthermore, the personality types in this dataset are self-reported by users of an online forum, who may have taken free online tests of varying validity or self-identified their type without formal assessment, introducing uncertainty into the data.",
            'dims_header': 'The Four MBTI Dimensions',
            'dims_intro': 'An MBTI personality type is formed by combining one preference from each of four dimensions. For example, **INFP** stands for Introversion, Intuition, Feeling, and Perceiving.',
            'dims': {
                'IE': {'name': 'Energy Source: Introversion (I) / Extroversion (E)', 'desc': 'I (Introversion) types draw energy from solitude and inner reflection; E (Extroversion) types from social interaction.', 'dist': 'I: 6,676 (77.0%) / E: 1,999 (23.0%)'},
                'NS': {'name': 'Information Gathering: Intuition (N) / Sensing (S)', 'desc': 'N (Intuition) types focus on abstract concepts and future possibilities; S (Sensing) types on concrete details and present realities.', 'dist': 'N: 7,478 (86.2%) / S: 1,197 (13.8%)'},
                'TF': {'name': 'Decision Making: Thinking (T) / Feeling (F)', 'desc': 'T (Thinking) types make decisions using logic and objective criteria; F (Feeling) types based on interpersonal harmony and values.', 'dist': 'T: 3,981 (45.9%) / F: 4,694 (54.1%)'},
                'JP': {'name': 'Lifestyle: Judging (J) / Perceiving (P)', 'desc': 'J (Judging) types prefer structure and planning; P (Perceiving) types prefer flexibility and open-endedness.', 'dist': 'J: 3,434 (39.6%) / P: 5,241 (60.4%)'},
            },
            'imbalance_warning': '⚠️ **Sampling Bias**: This dataset originates from an MBTI community where I and N types are overrepresented. It does not reflect the general population (S types ~73% in reality). Findings should not be generalized beyond this sample.',
            'method_header': 'Analytical Approach',
            'method_text': 'This project extracts lexical features using **TF-IDF**, classifies each MBTI dimension as a binary task with **Logistic Regression (L1/L2 Regularization)**, and evaluates models with **Stratified 5-Fold Cross Validation**, reporting **Balanced Accuracy** and **95% confidence intervals**.',
            'method_terms': {
                'tfidf_title': 'TF-IDF (Term Frequency–Inverse Document Frequency)',
                'tfidf_desc':  'Measures the importance of a word to a category of documents. Higher TF combined with high IDF (rare across other categories) yields a higher score, identifying truly discriminative terms.',
                'lr_title':    'Logistic Regression with L1/L2 Regularization',
                'lr_desc':     'A statistical model for binary classification. Regularization prevents overfitting. L1 drives unimportant coefficients to zero (automatic vocabulary selection); L2 shrinks all coefficients for overall stability.\n\nIn this project, one binary classifier is trained per MBTI dimension (I vs E, N vs S, T vs F, J vs P). The **L1 model** is used to extract representative vocabulary for each dimension (words with non-zero coefficients); the **L2 model** is used to report Balanced Accuracy and run statistical tests — each serving a distinct purpose.',
                'cv_title':    'Stratified 5-Fold Cross Validation',
                'cv_desc':     'Splits data into five folds for rotating training and testing, maintaining class proportions in each fold. More stable than a single train-test split.',
                'ba_title':    'Balanced Accuracy',
                'ba_desc':     'The average of per-class accuracies, giving equal weight to each class regardless of sample size. More appropriate than overall accuracy in class-imbalanced settings.',
            },
        },

        'sample': {
            'title': 'Sample Distribution', 'stats_header': 'Descriptive Statistics',
            'total_records': 'Total Records', 'n_types': 'MBTI Types',
            'most_common': 'Most Common Type', 'least_common': 'Least Common Type',
            'dist_header': 'MBTI Type Distribution', 'dim_dist_header': 'Distribution by Dimension',
            'preview_header': 'Data Preview (First 20 Rows)',
            'download_btn': '⬇️ Download Full CSV', 'download_name': 'mbti_1.csv',
            'chart_title_type': 'MBTI Type Distribution', 'chart_title_dim': 'Distribution by Dimension',
            'count_label': 'Count',
        },

        'main': {
            'title':    'Vocabulary Analysis & Significance Testing',
            'overview_header': 'Cross-Dimension Overview',
            'l2_note':          'All accuracy metrics below use the **L2 Regularization** model (optimized for overall prediction stability). Vocabulary analysis (lower section) uses a separate **L1 Regularization** model (automatically selects representative words by zeroing unimportant coefficients).',
            'chart_axis_note':  '⚠️ Y-axis is broken (0–10% and 40–100%) to highlight differences above the chance baseline.',

            'chance_note':      'Chance baseline for binary classification: **50%**',
            'chart_title':      'Balanced Accuracy by Dimension (with 95% CI)',
            'balanced_acc_col': 'Balanced Accuracy',
            'above_chance_col': 'Above Chance',
            'ci_col':           '95% CI',
            'yes': '✅ Yes', 'no': '❌ No',

            'ttest_header':     'Statistical Testing: Are Lexical Differences Significant?',
            'ttest_note':       "A **one-sample t-test** (one-tailed) is conducted on each dimension's 5-fold Balanced Accuracy scores. Null hypothesis H₀: mean Balanced Accuracy = 0.5 (chance level).",
            'ttest_limitation': '⚠️ **Statistical Power Note**: Each test uses only 5 data points (df = 4), resulting in low statistical power. Small effect sizes may not reach significance even if real differences exist.',
            'dim_label':        'Dimension',
            't_col':            't-value',
            'p_col':            'p-value (one-tailed)',
            'sig_col':          'Significant (α = 0.05)',
            'cohens_d_col':     "Cohen's d",
            'effect_size_col':  'Effect Size',
            'sig_yes': '✅ Yes', 'sig_no': '❌ No',

            'result_header':    'Summary & Response to Research Question',

            'drilldown_header':  'Single-Dimension Deep Dive',
            'dim_select_label':  'Select Dimension',
            'accuracy_header':   'Model Accuracy (L2 Regularization, Stratified 5-Fold Cross-Validation)',
            'mean_balanced_acc': 'Mean Balanced Accuracy',
            'fold_label':        'Fold {}',
            'ci_header':         '95% Confidence Interval',
            'n_iter_label':      'Iterations to Convergence (Final Model)',
            'per_class_header':  'Per-Class Accuracy',
            'per_class_note':    'Per-class accuracy averaged across 5 folds',
            'n_iter_label':      'Iterations',
            'n_iter_note':       'If iterations equal max_iter (1000), the model did not fully converge.',
            'l1_vocab_title':    'About representative vocabulary',
            'l1_vocab_note':     'The representative vocabulary below is extracted by the L1 model. L1 Regularization zeroes out unimportant word coefficients — words with non-zero coefficients become the representative vocabulary.',
            'n_iter_col':        'Iterations',
            'imbalance_note_IE': '⚠️ Energy Source (I/E) is imbalanced (I: 77.0%, E: 23.0%). Interpret with caution.',
            'imbalance_note_NS': '⚠️ Information Gathering (N/S) is severely imbalanced (N: 86.2%, S: 13.8%). S-type vocabulary is less stable.',
            'slider_label':      'Coefficient Threshold',
            'slider_explain':    'How strongly a word pushes the model toward classifying it as one type, controlling for all other words.\nHigher values = stricter filter = fewer but more representative words.',
            'n_words_above':     '**{}** words above threshold',
            'dist_chart_title':  'Coefficient Absolute Value Distribution',
            'coef_abs_label':    'Absolute Coefficient',
            'n_words_label':     'Word Count',
            'threshold_line':    'Current Threshold',
            'vocab_header':      'Representative Vocabulary',
            'direction_pos':     'Positive coefficient → associated with {}',
            'direction_neg':     'Negative coefficient → associated with {}',
            'word_col':          'Word',
            'coef_col':          'Coefficient',
            'direction_col':     'Direction',
            'no_words':          'No words above this threshold. Try lowering the value.',
        },
    },
}
