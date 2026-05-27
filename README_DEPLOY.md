# 部署說明 | Deployment Instructions

## 本機執行步驟 | Local Setup

### 1. 安裝相依套件 | Install dependencies
```bash
pip install -r requirements.txt
```

### 2. 預先執行分析腳本 | Run pre-computation script
```bash
python analysis.py
```
此步驟約需 **15–30 分鐘**（視電腦效能而定），完成後會在 `results/` 目錄產生：
- `analysis_results.pkl`：所有模型結果
- `cleaned_data.csv`：清洗後的資料

This step takes approximately **15–30 minutes** depending on your machine. It generates:
- `analysis_results.pkl` — all model results
- `cleaned_data.csv` — cleaned dataset

### 3. 本機啟動 Streamlit | Launch Streamlit locally
```bash
streamlit run app.py
```

---

## 部署至 Streamlit Cloud | Deploy to Streamlit Cloud

> ⚠️ **重要**：`results/analysis_results.pkl` 必須在 push 前已產生，並且**不在 `.gitignore` 排除清單內**才能上傳至 GitHub。
> 
> **Important**: `results/analysis_results.pkl` must be generated locally before pushing. Make sure it is **not excluded by `.gitignore`** when you push to GitHub.

### 步驟 | Steps

1. 在本機執行 `python analysis.py` 產生 `results/analysis_results.pkl`
2. **暫時修改 `.gitignore`**，將 `results/*.pkl` 那行註解掉或刪除
3. Push 整個專案（含 `results/analysis_results.pkl`）至 GitHub
4. 前往 [Streamlit Cloud](https://streamlit.io/cloud)，連結你的 GitHub repo
5. 設定 main file 為 `app.py`
6. Deploy

### 檔案大小提醒 | File Size Note
`analysis_results.pkl` 大小視詞彙模型而定，通常約 **50–200 MB**。
GitHub 單檔上限為 100 MB；若超過，請改用 [Git LFS](https://git-lfs.github.com/) 或將結果拆分儲存。

---

## 專案結構 | Project Structure

```
mbti-lexical-analysis/
├── app.py                  # Streamlit 主程式 | Main Streamlit app
├── analysis.py             # 預先執行的分析腳本 | Pre-computation script
├── requirements.txt        # Python 相依套件 | Python dependencies
├── .gitignore
├── README_DEPLOY.md        # 本檔案 | This file
├── data/
│   └── mbti_1.csv          # 原始資料集 | Raw dataset
├── results/                # analysis.py 的輸出（需本機產生）
│   ├── .gitkeep
│   ├── analysis_results.pkl   ← 由 analysis.py 產生
│   └── cleaned_data.csv       ← 由 analysis.py 產生
└── utils/
    ├── __init__.py
    ├── cleaning.py         # 資料清洗函式 | Data cleaning functions
    ├── modeling.py         # 模型訓練與評估 | Modeling & evaluation
    └── translations.py     # 中英文介面文字 | Bilingual UI text
```
