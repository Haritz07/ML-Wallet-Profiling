# 🛡️ Solana Wallet Risk Profiler Dashboard

This Streamlit dashboard provides real-time, data-driven wallet risk analysis on the Solana blockchain, powered by machine learning and a FastAPI Backend. It helps investors, researchers, and security analysts like me assess the likelihood that a wallet is involved in fraudulent or scam-like behaviour. Happy Testing!🎉

## 🚀 What It Does

 Accepts a Solana wallet address input
 Pulls transaction history and metadata using the Helius API
 Extracts 9 behavioural features per wallet (e.g. inflow/outflow, mint patterns)
 Feeds features into a trained XGBoost classifier
 Returns a risk label (Safe or High-Risk) with model confidence
 Displays a clean visual summary of the wallet's behaviour

## 💡 How It Works
This dashboard connects to a deployed FastAPI backend that:
  1. Loads our trained model from disk using ```joblib```

  2. Computes features from raw transaction data

  3. Returns a prediction to the dashboard via an API call

The ML model was trained on labelled on-chain data collected via Helius, using 9 core features (see paper or section 7 of this repo for details). Accuracy on test data: 92%, F1 Score: 0.91.

# 📊 Example Use Case

Enter a Solana wallet address like:
```F84Ba...9342z```

And see:
  Risk classification: High Risk 🚨 or Safe ✅
  
  Confidence score (0.0 – 1.0)
  
  Behavioural breakdown (tx volume, mint history, suspicious patterns)

# ⚠️ Limitations
  1. The system only supports wallet addresses already found in our training dataset(for now).
  2. Newly observed wallets will not return predictions until data is collected and processed.
  3. This prototype was built to showcase the potential of machine learning in enhancing wallet intelligence and scam detection on Solana.

# ⚙ Tech Stack

Frontend: Streamlit

Backend: FastAPI

ML: XGBoost (trained with pandas & scikit-learn)

Data: Solana blockchain via Helius API

# 🧪Try It Out (Coming Soon)

Streamlit App: https://ml-wallet-profiling-gpxt8tkpb8pt2tcmpdpqug.streamlit.app/

API Endpoint: 
