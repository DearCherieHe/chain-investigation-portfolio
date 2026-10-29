# Executive summary — Euler Finance case study

This portfolio investigation examines a bounded set of five Ethereum transactions associated with the March 2023 Euler Finance exploit. It is **not** a complete tracing of the approximately $197 million incident.

Three native ETH transfers have been checked against publicly indexed transaction fields: 100 ETH from an Euler-associated address to an address publicly tagged with the Ronin Bridge exploit on March 17, and 1,000 plus 51,000 ETH from that same sender to the Euler deployer on March 18 and 25. Two additional March 18 return transaction hashes appear in [Coinbase's investigation](https://www.coinbase.com/blog/euler-compromise-investigation-part-2-the-redemption), but their individual amounts and receipts remain unverified here.

The 100 ETH transfer is an investigative lead. It does **not** establish that the Euler and Ronin exploits shared an operator. [Chainalysis explicitly noted](https://www.chainalysis.com/blog/euler-finance-flash-loan-attack/) that the transfer could have been a misdirection attempt. The next step is to verify all five transactions from Ethereum RPC receipts, then connect the exploit transactions to subsequent flows on an asset-by-asset basis.
