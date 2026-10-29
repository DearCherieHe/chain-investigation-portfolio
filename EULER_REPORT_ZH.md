# Euler Finance 攻击后资金流：限定范围调查报告

**调查范围：**2023 年 3 月 17–25 日，以太坊地址 `0xb66cd966670d962C227B3EABA30a872DbFb995db` 的五笔公开引用交易。这里调查的是攻击后的部分资金流，不是完整攻击路径或全部资产的最终去向。

## 结论

该地址在 3 月 17 日向被公开标记为 Ronin Bridge 攻击关联地址的钱包发送 100 ETH；3 月 18 日和 25 日向 Euler deployer 地址发送已核对的 1,000 与 51,000 ETH。另有两笔 3 月 18 日的交易哈希由 Coinbase 报告列出，但本项目尚未逐笔核对回执，因此不计入“已核对返还额”。交易明细见 [证据台账](data/cases.csv)。

从资金流可以提出“为什么向 Ronin 关联地址发送 100 ETH”的调查问题，但不能据此确认两个事件由同一人或组织实施。Chainalysis 对此也保留了误导调查的可能解释。[来源](https://www.chainalysis.com/blog/euler-finance-flash-loan-attack/)

## 分析方法

1. 以 Coinbase 报告中的交易哈希建立初始清单。[来源](https://www.coinbase.com/blog/euler-compromise-investigation-part-2-the-redemption)
2. 对 Etherscan 可检索的交易记录核对哈希、时间、发送方、接收方、金额和成功状态。无法直接读取完整页面或 RPC 回执的项目降级标记为 `secondary_report`。
3. 仅对 `explorer_index` 且金额已核对的记录做数值汇总。图表不纳入金额未知的记录。
4. 把地址的公开标签、调查者假设和可直接观察的转账分开表述。

## 限制

- 本报告未建立攻击交易与各笔后续转账之间的逐资产成本流。地址收到多笔资产时，不能把全部余额直接称为赃款。
- 没有验证代币转移、合约内部转账或跨链桥事件；图表只显示三笔原生 ETH 转账。
- Etherscan 标签不是身份认证。100 ETH 转账本身不证明共同控制、组织关系或主观动机。
- 这是公开数据作品集案例，不是 Chainalysis 官方调查成果，也未使用其专有数据或产品。

## 后续验证任务

运行 `fetch_rpc.py`，核对所有五笔交易的原始 JSON、回执和 wei 数值；随后扩展到攻击交易及 ERC-20 `Transfer` 日志，建立逐资产路径和时间窗。
