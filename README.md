# 链上调查案例集 / Blockchain Investigation Portfolio

一个 Streamlit 页面中的两个独立案例 Tab：**NEAR Intents 2026** 与 **Euler Finance 2023**。每个案例都展示资金路径、证据台账和调查边界。

## 本地运行

```bash
python -m pip install -r requirements.txt
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

## 数据核查等级

- NEAR：七笔 BNB Chain USDT 转账已通过主网 RPC 的交易回执与 `Transfer` 日志核对。复现脚本见 `verification/near/fetch_rpc.py`；设置 `BSC_RPC_URL` 后运行 `python verification/near/fetch_rpc.py`。
- Euler：三笔 ETH 转账已由公开交易搜索索引核对，另两笔来自 Coinbase 调查报告，尚未独立读取 RPC 回执。

源数据与报告随本目录打包；发布到 Streamlit Community Cloud 时，请将本目录设为 GitHub 仓库根目录，入口文件为 `app.py`。

