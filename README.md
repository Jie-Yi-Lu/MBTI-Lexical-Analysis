# MBTI Lexical Analysis

## 簡介 | Introduction

本專案以「在 MBTI 的單一人格維度上，自然語言用詞風格是否存在可觀察的差異？」為核心研究問題，對一份包含 8,675 筆社群媒體貼文的資料集進行文本分析，並以 Streamlit 網頁應用程式呈現互動式分析結果。

This project investigates whether observable lexical differences exist across individual MBTI personality dimensions, using a dataset of 8,675 social media posts presented through an interactive Streamlit web application.

---

## 研究問題 | Research Question

在 MBTI 的單一人格維度上，自然語言用詞風格是否存在可觀察的差異？

Across individual MBTI personality dimensions, are there observable differences in natural language word usage?

---

## 資料集 | Dataset

- **來源 Source**：Kaggle — [MBTI Personality Type Dataset](https://www.kaggle.com/datasets/datasnaek/mbti-type)
- **筆數 Records**：8,675
- **欄位 Columns**：
  - `type`：用戶的 MBTI 人格類型代碼（如 INFP）
  - `posts`：該用戶最近 50 則社群媒體貼文，以 `|||` 分隔

**各維度樣本分布 | Class Distribution per Dimension**

| 維度 Dimension | 類型 A | 人數 | 比例 | 類型 B | 人數 | 比例 |
|----------------|--------|------|------|--------|------|------|
| 能量來源 I/E | I | 6,676 | 77.0% | E | 1,999 | 23.0% |
| 資訊收集 N/S | N | 7,478 | 86.2% | S | 1,197 | 13.8% |
| 決策依據 T/F | T | 3,981 | 45.9% | F | 4,694 | 54.1% |
| 生活態度 J/P | J | 3,434 | 39.6% | P | 5,241 | 60.4% |

> ⚠️ **樣本偏差**：資料集來源為 MBTI 討論社群，I 與 N 類型過度集中，不代表真實人口分布（現實中 S 類型約佔 73%）。MBTI 類型為用戶自行申報，非正式評量結果。

---

## 環境設定 | Environment Setup

```bash
pip install -r requirements.txt
```

**requirements.txt 內容：**
```
streamlit>=1.32.0
pandas>=2.0.0
scikit-learn>=1.4.0
nltk>=3.8.0
plotly>=5.18.0
numpy>=1.24.0
scipy>=1.11.0
```

---

## 執行流程 | Workflow

```bash
# 步驟一：預先執行分析（約 15–30 分鐘）
python analysis.py

# 步驟二：啟動 Streamlit 應用
streamlit run app.py
```

`analysis.py` 執行完畢後，`results/` 目錄會產生：
- `analysis_results.pkl`：所有模型結果（詞彙係數、CV 準確率等）
- `cleaned_data.csv`：清洗後的資料集

---

## 資料清洗 | Data Cleaning

### 為何需要清洗？

原始貼文來自社群媒體，包含大量雜訊（URL、表情符號格式、標點符號），以及對本分析至關重要的**資料洩漏（Data Leakage）**問題。

**資料洩漏（Data Leakage）**：訓練資料中直接洩露分類答案的資訊。本資料集的用戶在貼文中頻繁提及自身人格類型（如 "As an INFJ, I tend to..."）或 MBTI 術語。若不移除，模型可能直接學到「看到 INFJ → 預測為 I 維度」，準確率虛高但毫無語言分析意義。

### 清洗步驟（依序執行）

清洗順序至關重要——必須先移除資料洩漏和結構性雜訊，再執行語言學處理，避免步驟間相互干擾。

#### 步驟 1：移除 MBTI 相關字眼（資料洩漏處理）

以下字詞皆以正規表示式 `\b...\b`（word boundary）搭配不分大小寫（`re.IGNORECASE`）進行匹配與移除：

**16 種人格代碼及其複數形**
```
infj, enfp, intj, intp, entj, entp, enfj, isfj, isfp, istj, istp, esfj, esfp, estj, estp, infp
（及加 s 的複數形：infjs, enfps, ...）
```

**MBTI 系統名稱**
```
mbti, myers, briggs, personality type, personality test
```

**認知功能術語**（Cognitive Function Terms）
MBTI 社群常用於描述內在心理運作的術語，非日常用語，直接透露人格類型傾向：
```
cognitive function, cognitive functions, shadow function, inferior function
ne dom, ni dom, se dom, si dom, te dom, ti dom, fe dom, fi dom
ne, ni, se, si, te, ti, fe, fi  （兩字母認知功能縮寫）
```

**氣質分組縮寫**
```
nt, nf, st, sf  （例如 "NT types are..."）
```

**維度標籤**（直接指涉四個維度的用語）
```
introvert, introverted, extrovert, extroverted, extravert, extraverted
intuitive, intuition, sensing
thinker, feeler, judger, perceiver, judging, perceiving
```

**其他社群常見術語**
```
sx（sexual subtype 縮寫）, sexual subtype
```

> **保留**：`thinking`、`feeling` 雖與 MBTI 維度同名，但在日常英文中廣泛作為動詞或名詞使用（"I've been thinking about this"），保留以維持語言分析完整性。

#### 步驟 2：移除 URL

移除所有 `http://`、`https://`、`www.` 開頭的連結。

#### 步驟 3：移除貼文分隔符 `|||`

原始資料以 `|||` 分隔每則貼文，清洗時替換為空格。

#### 步驟 4：轉小寫

統一轉為小寫，使 `Think` 與 `think` 被視為相同詞彙。

#### 步驟 5：移除表情符號格式 `:...:`

社群媒體常見的文字表情符號格式（如 `:wink:`、`:smile:`）以正規表示式 `:[a-z_]+:` 移除。

#### 步驟 6：移除標點符號與數字

僅保留英文字母與空格，其餘字元一律替換為空格。

#### 步驟 7：移除停用詞（Stopwords）

**停用詞（Stopwords）**：在幾乎所有文章中都大量出現、但對分類無幫助的常用字，如 `the`、`a`、`is`、`in`。這些詞無法區分不同人格類型的語言風格，保留只會增加雜訊。

本專案使用 **NLTK 內建英文停用詞表**（`nltk.corpus.stopwords.words('english')`，約 180 個詞）搭配 TF-IDF 的 `stop_words='english'` 進行雙重過濾。

#### 步驟 8：詞形還原（Lemmatization）

**Lemmatization（詞形還原）**：將詞彙的各種變形還原回字典基本型（lemma）。例如 `running`、`runs`、`ran` 均還原為 `run`；`studies`、`studied` 均還原為 `study`。若不處理，電腦會將這些視為不同詞彙，稀釋統計意義。

使用 **NLTK 的 `WordNetLemmatizer`** 實作。相較於直接截斷字尾的 Stemming，Lemmatization 透過查詢語言學字典進行還原，結果更為準確。

> **注意**：本實作以名詞形式（預設值）進行還原。更嚴謹的做法應先進行詞性標注（POS Tagging），再依詞性選擇對應的還原方式，但此項優化已在本專案範疇外。

### 清洗後過濾

長度為 1 的詞彙（單一字母）在還原後可能殘留，一律過濾排除。

---

## 特徵萃取 | Feature Extraction

### TF-IDF（詞頻-逆文件頻率）

**TF-IDF（Term Frequency–Inverse Document Frequency）**：衡量一個詞對某類文件重要性的指標。

- **TF（詞頻）**：詞彙在文件中出現的頻率，越高分數越高
- **IDF（逆文件頻率）**：若詞彙在大多數文件中都出現（如 "the"），給予懲罰降低分數；若只在少數文件出現，給予加分

兩者相乘，能自動過濾無意義的常用詞，凸顯真正具鑑別力的特徵詞彙。

**參數設定（`sklearn.feature_extraction.text.TfidfVectorizer`）：**

| 參數 | 設定值 | 說明 |
|------|--------|------|
| `max_features` | 10,000 | 保留 TF-IDF 分數最高的前 10,000 個詞彙 |
| `min_df` | 5 | 排除出現在少於 5 篇文章中的詞（可能為拼寫錯誤或個人化用語） |
| `max_df` | 0.7 | 排除出現在超過 70% 文章中的詞（過於普遍，無鑑別力） |
| `ngram_range` | (1, 1) | 僅使用單詞（unigrams），專注詞彙層面分析 |
| `stop_words` | `'english'` | 套用 sklearn 內建英文停用詞表進行額外過濾 |

---

## 分類任務設定 | Classification Setup

每個 MBTI 維度獨立進行二元分類。標籤從完整人格代碼中依位置拆解：

| 維度 | 位置 | 標籤 1（pos） | 標籤 0（neg） |
|------|------|--------------|--------------|
| 能量來源 I/E | 第 1 位 | I = 1 | E = 0 |
| 資訊收集 N/S | 第 2 位 | N = 1 | S = 0 |
| 決策依據 T/F | 第 3 位 | T = 1 | F = 0 |
| 生活態度 J/P | 第 4 位 | J = 1 | P = 0 |

---

## 模型 | Model

### Logistic Regression

**參數設定（`sklearn.linear_model.LogisticRegression`）：**

| 參數 | 詞彙分析（L1） | 表現比較（L2） | 說明 |
|------|---------------|---------------|------|
| `penalty` | `'l1'` | `'l2'` | 見下方說明 |
| `solver` | `'liblinear'` | `'lbfgs'` | L1 需使用 liblinear；L2 使用 lbfgs |
| `class_weight` | `'balanced'` | `'balanced'` | 依各類別樣本數自動調整訓練權重，避免偏袒多數類別 |
| `max_iter` | 1,000 | 1,000 | 最大迭代次數；若出現 `ConvergenceWarning` 應調高 |
| `random_state` | 42 | 42 | 確保結果可重現 |

訓練完成後，`model.n_iter_` 輸出實際收斂所需迭代次數，供透明度參考。

### L1 vs L2 Regularization

**Regularization（正則化）**：防止模型過度擬合（Overfitting）的機制。Overfitting 是指模型學到了訓練資料中的個別雜訊（如某位 E 類型用戶特別愛用某個詞），而非真正的類別特徵，導致遇到新資料時表現不佳。Regularization 透過懲罰「係數過大」的詞彙，逼迫模型只依賴真正重要的特徵。

- **L1 Regularization**：將不重要詞彙的係數直接壓為零，自動篩選出少數具鑑別力的詞彙。**用於詞彙分析**，非零係數詞彙即為代表詞彙來源。
- **L2 Regularization**：縮小所有係數但不歸零，整體預測穩定性略優。**用於模型表現報告**，此處目標為最佳化準確率而非詞彙解讀。

---

## 模型評估 | Model Evaluation

### Stratified 5-Fold Cross Validation（分層五折交叉驗證）

**Cross Validation（交叉驗證）**：將資料分為 k 份，輪流以其中 k-1 份訓練、1 份測試，共進行 k 輪，取平均準確率作為最終評估，比單次切割更穩定可靠。

本專案使用 **k = 5**，搭配 **Stratified（分層）** 切割：確保每折中各類別的比例與原始資料一致，避免因不均勻切割影響評估結果（在 N/S 和 I/E 等不平衡維度尤為重要）。

實作：`sklearn.model_selection.StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`

### Balanced Accuracy（平衡準確率）

**Balanced Accuracy**：各類別準確率的平均值，讓每個類別對最終分數的貢獻相等，不受樣本數多寡影響。

> 例：N 準確率 90%，S 準確率 60% → Balanced Accuracy = (90% + 60%) ÷ 2 = **75%**

適用於類別不平衡情境（如本資料集的 N/S 維度），比整體準確率更能反映模型的真實表現。

實作：`sklearn.metrics.balanced_accuracy_score`

### 95% 信賴區間（t 分布）

以 5 折的 Balanced Accuracy 分數計算 95% 信賴區間，採用 **t 分布**（自由度 = 4），係數為 2.776。

使用 t 分布而非常態分布的原因：t 分布適用於小樣本（n = 5），係數較常態分布的 1.96 更大，誠實反映「僅有 5 個數據點」的不確定性。

> **公式**：95% CI = 平均值 ± 2.776 × (標準差 ÷ √5)

實作：`scipy.stats.t.ppf` + `scipy.stats.sem`

### 統計顯著性檢定（單樣本 t 檢定）

對每個維度的 5 折 Balanced Accuracy 分數進行**單樣本單尾 t 檢定**：

- **H₀**：平均 Balanced Accuracy = 0.5（隨機猜測水準）
- **H₁**：平均 Balanced Accuracy > 0.5
- **顯著水準**：α = 0.05

同時計算 **Cohen's d** 作為效應量（Effect Size）：

> d = (平均值 − 0.5) ÷ 標準差

| d 範圍 | 效應量 |
|--------|--------|
| < 0.2 | 可忽略（Negligible） |
| 0.2–0.5 | 小（Small） |
| 0.5–0.8 | 中（Medium） |
| ≥ 0.8 | 大（Large） |

> ⚠️ **檢定力限制**：每個 t 檢定僅有 5 個數據點（df = 4），統計檢定力偏低，偵測小效應量的能力有限，型二錯誤（False Negative）風險較高。

---

## Streamlit 分頁架構 | Streamlit Pages

| 分頁 | 核心內容 |
|------|---------|
| 🏠 首頁 | MBTI 背景說明、研究問題、四個維度介紹、分析方法概覽（含名詞解釋） |
| 📊 樣本分布 | 描述統計、MBTI 類型分布圖、各維度分布圖、資料預覽與 CSV 下載 |
| 🔤 維度詞彙分析與差異檢定 | **上半部**：跨維度 Balanced Accuracy 圖表、統計檢定表（t 值、p 值、Cohen's d）、結果解讀；**下半部**：單一維度選擇、各折準確率、代表詞彙互動探索（係數截點滑桿） |

---

## 專案結構 | Project Structure

```
mbti-lexical-analysis/
├── app.py                  # Streamlit 主程式
├── analysis.py             # 預先執行的分析腳本（需在部署前執行）
├── requirements.txt
├── .gitignore
├── README.md               # 本文件
├── README_DEPLOY.md        # 部署說明
├── data/
│   └── mbti_1.csv          # 原始資料集
├── results/                # analysis.py 的輸出（需本機產生後上傳）
│   ├── .gitkeep
│   ├── analysis_results.pkl
│   └── cleaned_data.csv
└── utils/
    ├── __init__.py
    ├── cleaning.py         # 資料清洗函式
    ├── modeling.py         # 模型訓練與評估
    └── translations.py     # 中英文介面文字
```

---

## 使用語言與套件 | Language & Libraries

- **Python 3**
- `pandas`：資料載入與處理
- `scikit-learn`：TF-IDF、Logistic Regression、StratifiedKFold、Balanced Accuracy
- `nltk`：停用詞表、WordNetLemmatizer
- `scipy`：t 分布信賴區間、單樣本 t 檢定
- `numpy`：數值運算
- `streamlit`：互動式網頁應用
- `plotly`：互動式圖表
