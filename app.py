"""Two public, bounded blockchain investigation case studies in one app."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).parent
st.set_page_config(page_title="On-chain Investigations | 链上调查", page_icon="🔎", layout="wide")
st.markdown("""<style>
.block-container{max-width:1080px;padding-top:1.3rem;padding-bottom:3rem}
h1{letter-spacing:-.04em;font-size:2rem!important}
h2{letter-spacing:-.03em;font-size:1.55rem!important;margin-top:.3rem!important}
.case-kicker{font-size:.76rem;font-weight:700;letter-spacing:.14em;color:#5eead4;text-transform:uppercase;margin:.25rem 0 .35rem}
.case-sub{color:#9aabc0;font-size:.94rem;line-height:1.5;margin:0 0 1rem}
.stat-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:1rem 0 1.3rem}
.stat-card{background:#142238;border:1px solid #30415a;border-radius:14px;padding:1rem 1.1rem;min-width:0}
.stat-label{color:#9fb1c8;font-size:.82rem;font-weight:600;margin-bottom:.4rem}
.stat-value{color:#f5f8fc;font-size:1.55rem;font-weight:750;letter-spacing:-.04em;white-space:nowrap}
.stat-value small{font-size:.69rem;font-weight:600;letter-spacing:0;color:#9fb1c8;margin-left:4px}
div[data-testid="stTabs"] button{font-weight:600}
@media(max-width:640px){
 .block-container{padding:1rem 1rem 2.5rem}
 h1{font-size:1.55rem!important}
 h2{font-size:1.32rem!important;line-height:1.35!important}
 .stat-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}
 .stat-card{padding:.8rem .85rem}
 .stat-card:first-child{grid-column:1 / -1}
 .stat-value{font-size:1.38rem}
 .stat-card:first-child .stat-value{font-size:1.7rem}
}
</style>""", unsafe_allow_html=True)


def cards(items: list[tuple[str, str, str]]) -> None:
    html = '<div class="stat-grid">'
    for label, value, unit in items:
        html += f'<div class="stat-card"><div class="stat-label">{label}</div><div class="stat-value">{value}<small>{unit}</small></div></div>'
    st.markdown(html + '</div>', unsafe_allow_html=True)

COPY = {
    "中文": {
        "title": "链上调查案例集", "tagline": "公开数据 · 可核查证据 · 调查边界",
        "near_sub": "BNB Chain 金库提现 · 2026 年 9 月 30 日至 10 月 1 日<br>范围：七笔 USDT 转账",
        "major": "五笔大额提现", "tests": "两笔测试提现", "near_total": "七笔合计",
        "unit_tx": "笔", "timeline": "时间线", "evidence": "逐笔证据", "findings": "判断与局限", "path": "资金路径",
        "category": "类别", "near_chart_note": "测试交易在这个金额比例下接近不可见；完整数字见逐笔证据。",
        "open_tx": "打开交易", "near_download": "下载 NEAR 证据 CSV",
        "near_evidence_note": "每笔交易已通过主网 RPC 回执中的 BSC USDT Transfer 日志核对发送地址、接收地址与金额。",
        "near_fact": "链上已核对：七笔成功交易从同一金库向同一接收钱包转移，合计 3,865,021 USDT。",
        "near_external": "外部研究结论：Bitquery 追踪了后续 BNB、ETH、BTC 和交易所路径；本项目尚未独立逐笔复核这些跨链段。",
        "near_unknown": "无法由这些交易确认：接收钱包的现实控制人、完整漏洞根因和最终资金归属。",
        "near_more": "[Bitquery 研究](https://www.bitquery.io/investigations/near-intents-hack)提供后续路径参考；本项目中文报告见仓库 `NEAR_REPORT_ZH.md`。事件涉及 NEAR Intents 服务，不等于 NEAR 公链被攻破。",
        "euler_sub": "攻击后 ETH 流向 · 2023 年 3 月<br>范围：五笔公开引用交易",
        "checked_return": "已核对返还", "in_scope": "范围内交易", "pending": "待逐笔核对",
        "euler_chart_note": "只绘制金额已由公开交易索引核对的三笔原生 ETH 转账。",
        "euler_download": "下载 Euler 证据 CSV",
        "euler_fact": "公开交易索引可核对：100 ETH 转向 Ronin 事件关联地址；另外两笔向 Euler deployer 转出 1,000 与 51,000 ETH。",
        "euler_external": "Chainalysis 与 Coinbase 将发送地址关联 Euler 攻击；地址标签与媒体分析是调查线索。",
        "euler_unknown": "100 ETH 转账不能证明 Euler 与 Ronin 攻击由同一人或组织实施。",
        "euler_more": "[Chainalysis 案例](https://www.chainalysis.com/blog/euler-finance-flash-loan-attack/) · [Coinbase 调查](https://www.coinbase.com/blog/euler-compromise-investigation-part-2-the-redemption)。完整报告见仓库 `EULER_REPORT_ZH.md`。",
        "footer": "作品集演示 · 使用公开链上资料 · 非 Chainalysis 官方调查成果",
        "near_nodes": ["Euler 事件关联地址", "Ronin 事件关联地址", "Euler deployer"],
        "dates": ["3 月 17 日", "3 月 18 日", "3 月 25 日"],
    },
    "English": {
        "title": "On-chain Investigations", "tagline": "Public data · Verifiable evidence · Clear limitations",
        "near_sub": "BNB Chain vault withdrawals · 30 Sep–1 Oct 2026<br>Scope: seven USDT transfers",
        "major": "Five major withdrawals", "tests": "Two test withdrawals", "near_total": "Seven-transfer total",
        "unit_tx": "txs", "timeline": "Timeline", "evidence": "Transaction evidence", "findings": "Findings & limits", "path": "Fund flows",
        "category": "Category", "near_chart_note": "The two test withdrawals are nearly invisible at this scale; see the transaction table for their amounts.",
        "open_tx": "Open transaction", "near_download": "Download NEAR evidence CSV",
        "near_evidence_note": "Each transfer was checked against a mainnet RPC receipt and the BSC USDT Transfer event for sender, recipient, and amount.",
        "near_fact": "On-chain verified: seven successful transfers from one vault to one receiving wallet, totalling 3,865,021 USDT.",
        "near_external": "External research: Bitquery traced subsequent BNB, ETH, BTC, and exchange routes. This project has not independently verified those cross-chain legs.",
        "near_unknown": "These transfers do not identify the wallet's real-world controller, the full root cause, or the ultimate ownership of later funds.",
        "near_more": "[Bitquery's investigation](https://www.bitquery.io/investigations/near-intents-hack) describes later routes. The repository contains `NEAR_EXECUTIVE_EN.md`. This incident involved the NEAR Intents service, not a compromise of the NEAR blockchain itself.",
        "euler_sub": "Post-exploit ETH movements · March 2023<br>Scope: five publicly cited transactions",
        "checked_return": "Checked returns", "in_scope": "Transactions in scope", "pending": "Pending verification",
        "euler_chart_note": "Only three native ETH transfers with amounts checked against public transaction indexes are shown.",
        "euler_download": "Download Euler evidence CSV",
        "euler_fact": "Public transaction indexes show 100 ETH sent to a Ronin-associated address and two transfers of 1,000 and 51,000 ETH to the Euler deployer.",
        "euler_external": "Chainalysis and Coinbase associate the sending address with the Euler exploit. Address labels and published analyses are investigative leads.",
        "euler_unknown": "The 100 ETH transfer does not prove that the Euler and Ronin exploits shared an operator or organization.",
        "euler_more": "[Chainalysis case](https://www.chainalysis.com/blog/euler-finance-flash-loan-attack/) · [Coinbase investigation](https://www.coinbase.com/blog/euler-compromise-investigation-part-2-the-redemption). The repository contains `EULER_EXECUTIVE_EN.md`.",
        "footer": "Portfolio demonstration · Public blockchain data · Not an official Chainalysis investigation",
        "near_nodes": ["Euler-associated address", "Ronin-associated address", "Euler deployer"],
        "dates": ["17 March", "18 March", "25 March"],
    },
}

language = st.radio("Language / 语言", ["中文", "English"], horizontal=True, label_visibility="collapsed")
t = COPY[language]

st.title(t["title"])
st.caption(t["tagline"])

near_tab, euler_tab = st.tabs(["NEAR Intents · 2026", "Euler Finance · 2023"])

with near_tab:
    st.markdown('<div class="case-kicker">CASE 01 · RPC VERIFIED</div>', unsafe_allow_html=True)
    st.header("NEAR Intents")
    st.markdown(f'<p class="case-sub">{t["near_sub"]}</p>', unsafe_allow_html=True)
    df = pd.read_csv(ROOT / "data" / "near_withdrawals.csv")
    df["time"] = pd.to_datetime(df["date_utc"], utc=True)
    major = int(df.loc[df.phase == "major", "amount_usdt"].sum())
    tests = int(df.loc[df.phase == "test", "amount_usdt"].sum())
    cards([(t["major"], f"{major:,}", "USDT"),
           (t["tests"], f"{tests:,}", "USDT"),
           (t["near_total"], f"{major + tests:,}", "USDT")])
    n1, n2, n3 = st.tabs([t["timeline"], t["evidence"], t["findings"]])
    with n1:
        chart = px.bar(df, x="time", y="amount_usdt", color="phase", text="amount_usdt",
                       color_discrete_map={"major": "#e45756", "test": "#64748b"},
                       labels={"time": "UTC", "amount_usdt": "USDT", "phase": t["category"]})
        chart.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        chart.update_layout(template="plotly_dark", height=350, yaxis_range=[0, 1800000],
                            margin=dict(l=5, r=5, t=35, b=5), paper_bgcolor="#0b1220",
                            plot_bgcolor="#0b1220", showlegend=False)
        st.plotly_chart(chart, use_container_width=True)
        st.caption(t["near_chart_note"])
    with n2:
        view = df.drop(columns=["time"])
        shown = view.rename(columns={"id": "编号" if language == "中文" else "ID", "date_utc": "UTC 时间" if language == "中文" else "UTC time", "tx_hash": "交易哈希" if language == "中文" else "Transaction hash", "amount_usdt": "金额 (USDT)" if language == "中文" else "Amount (USDT)", "phase": "类型" if language == "中文" else "Type", "verification": "核查状态" if language == "中文" else "Verification", "source": "交易链接" if language == "中文" else "Transaction link"})
        link_col = "交易链接" if language == "中文" else "Transaction link"
        st.dataframe(shown, hide_index=True, use_container_width=True,
                     column_config={link_col: st.column_config.LinkColumn("BscScan", display_text=t["open_tx"])})
        st.download_button(t["near_download"], view.to_csv(index=False).encode("utf-8-sig"),
                           "near_withdrawals.csv", "text/csv", key="near_csv")
        st.caption(t["near_evidence_note"])
    with n3:
        st.success(t["near_fact"])
        st.warning(t["near_external"])
        st.error(t["near_unknown"])
        st.markdown(t["near_more"])

with euler_tab:
    st.markdown('<div class="case-kicker">CASE 02 · PUBLIC INDEX</div>', unsafe_allow_html=True)
    st.header("Euler Finance")
    st.markdown(f'<p class="case-sub">{t["euler_sub"]}</p>', unsafe_allow_html=True)
    edf = pd.read_csv(ROOT / "data" / "euler_cases.csv")
    checked = edf[(edf.verification == "explorer_index") & (edf.kind == "return")]
    checked_sum = int(checked.amount.sum())
    cards([(t["checked_return"], f"{checked_sum:,}", "ETH"),
           (t["in_scope"], str(len(edf)), t["unit_tx"]),
           (t["pending"], str(int((edf.verification != "explorer_index").sum())), t["unit_tx"])])
    e1, e2, e3 = st.tabs([t["path"], t["evidence"], t["findings"]])
    with e1:
        chart = go.Figure(go.Sankey(
            node=dict(label=t["near_nodes"],
                      color=["#334155", "#ef4444", "#10b981"], pad=20, thickness=22),
            link=dict(source=[0, 0, 0], target=[1, 2, 2], value=[100, 1000, 51000],
                      color=["rgba(239,68,68,.35)", "rgba(16,185,129,.35)", "rgba(16,185,129,.35)"],
                      customdata=t["dates"],
                      hovertemplate="%{customdata}: %{value:,.0f} ETH<extra></extra>")))
        chart.update_layout(template="plotly_dark", height=300,
                            paper_bgcolor="#0b1220", font=dict(color="#edf3fb", size=12),
                            margin=dict(l=5, r=5, t=20, b=5))
        st.plotly_chart(chart, use_container_width=True)
        st.caption(t["euler_chart_note"])
    with e2:
        edf["transaction_url"] = edf.tx_hash.map(lambda h: f"https://etherscan.io/tx/{h}")
        eview = edf[["id", "date_utc", "amount", "asset", "kind", "verification", "from_address", "to_address", "transaction_url"]].rename(columns={"id": "编号" if language == "中文" else "ID", "date_utc": "UTC 时间" if language == "中文" else "UTC time", "amount": "金额" if language == "中文" else "Amount", "asset": "资产" if language == "中文" else "Asset", "kind": "类型" if language == "中文" else "Type", "verification": "核查状态" if language == "中文" else "Verification", "from_address": "转出地址" if language == "中文" else "From", "to_address": "接收地址" if language == "中文" else "To", "transaction_url": "交易链接" if language == "中文" else "Transaction link"})
        link_col = "交易链接" if language == "中文" else "Transaction link"
        st.dataframe(eview,
                     hide_index=True, use_container_width=True,
                     column_config={link_col: st.column_config.LinkColumn("Etherscan", display_text=t["open_tx"])})
        st.download_button(t["euler_download"], edf.to_csv(index=False).encode("utf-8-sig"),
                           "euler_cases.csv", "text/csv", key="euler_csv")
    with e3:
        st.success(t["euler_fact"])
        st.warning(t["euler_external"])
        st.error(t["euler_unknown"])
        st.markdown(t["euler_more"])

st.divider()
st.caption(t["footer"])
