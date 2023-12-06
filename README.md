# 逐字稿：大量轉譯Ｘ分割
經理人聲音情緒與投資人有限注意：影音轉成逐字稿
---
這是一個將大量逐字稿（資料夾）轉譯成逐字稿的輔助工具，主要提供兩種使用方式，以滿足不同的使用需求。

## 轉譯使用方式

### 1. Google 硬碟（Google Drive）

- 使用 Google Colab 上的 Jupyter Notebook，提供兩種選擇。
  - [**insanely_fast_whisper_colab.ipynb**](https://drive.google.com/file/d/1D381cTluvVbzsHAGFqEbm4yhkHqSOfQi/view?usp=sharing)：這是最快的轉譯方式，適合追求速度的使用者。

### 2. 本地端計算

- 當 Colab 資源用完時，推薦使用本地端運算。
  - 對於 macOS 用戶，推薦下載 [Whisper Transcription App](https://apps.apple.com/us/app/whisper-transcription/id1668083311?mt=12)。
  - 另外，我也提供了自行改良的本地端程式 **local_fastWhisper**，性能堪用。

## 分割逐字稿工作區

- 本專案提供了一個自動化工具 **split_v1.py**，用於處理已轉譯的逐字稿。
- 若逐字稿中包含特定的“職稱”，此工具能自動進行分割。
- 使用者僅需收集所有可能出現的職稱，並在程式中進行相應的設定，即可進行自動檢測與分割。

## 快速開始

1. 選擇使用 Google 硬碟或本地端進行轉譯。
2. 根據選擇的方式，遵循相應的指引來設定和運行轉譯工具。
3. 使用 split_v1.py 對轉譯後的逐字稿進行分割。
