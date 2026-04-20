import json
import re
import os
from datetime import datetime

# ==========================================
# 📥 战术情报源 (你过去四天的邮件通讯记录)
# ==========================================
raw_email_text = r"""
On Fri, Apr 17, 2026 at 5:19 PM edward xin <edwardxin@gmail.com> wrote:
📊 [PLTR] Consensus: 6 Runs | 🟢 Long: 6 | 🔴 Short: 0 | ⚖️ Net Score: +6
📊 [RSP] Consensus: 6 Runs | 🟢 Long: 6 | 🔴 Short: 0 | ⚖️ Net Score: +6
📊 [LEN] Consensus: 6 Runs | 🟢 Long: 5 | 🔴 Short: 0 | ⚖️ Net Score: +5
📊 [RSPG] Consensus: 6 Runs | 🟢 Long: 5 | 🔴 Short: 0 | ⚖️ Net Score: +5
📊 [XPEV] Consensus: 6 Runs | 🟢 Long: 4 | 🔴 Short: 0 | ⚖️ Net Score: +4
📊 [TLT] Consensus: 6 Runs | 🟢 Long: 4 | 🔴 Short: 0 | ⚖️ Net Score: +4
📊 [OPEN] Consensus: 6 Runs | 🟢 Long: 5 | 🔴 Short: 1 | ⚖️ Net Score: +4
📊 [BABA | 阿里巴巴 (BABA)] Consensus: 6 Runs | 🟢 Long: 4 | 🔴 Short: 1 | ⚖️ Net Score: +3
📊 [TSLA] Consensus: 6 Runs | 🟢 Long: 4 | 🔴 Short: 1 | ⚖️ Net Score: +3
📊 [SMH] Consensus: 6 Runs | 🟢 Long: 3 | 🔴 Short: 0 | ⚖️ Net Score: +3
📊 [SPY] Consensus: 6 Runs | 🟢 Long: 4 | 🔴 Short: 1 | ⚖️ Net Score: +3
📊 [QQQ] Consensus: 6 Runs | 🟢 Long: 3 | 🔴 Short: 0 | ⚖️ Net Score: +3
📊 [XLP] Consensus: 6 Runs | 🟢 Long: 4 | 🔴 Short: 1 | ⚖️ Net Score: +3
📊 [EWJ] Consensus: 6 Runs | 🟢 Long: 4 | 🔴 Short: 1 | ⚖️ Net Score: +3
📊 [IWM] Consensus: 6 Runs | 🟢 Long: 3 | 🔴 Short: 1 | ⚖️ Net Score: +2
📊 [RSPF] Consensus: 6 Runs | 🟢 Long: 3 | 🔴 Short: 1 | ⚖️ Net Score: +2
📊 [PDD | 拼多多 (PDD)] Consensus: 6 Runs | 🟢 Long: 4 | 🔴 Short: 2 | ⚖️ Net Score: +2
📊 [KWEB | 中概互联网ETF (KWEB)] Consensus: 6 Runs | 🟢 Long: 3 | 🔴 Short: 2 | ⚖️ Net Score: +1
📊 [ETH-USD] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 1 | ⚖️ Net Score: +1
📊 [META] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 2 | ⚖️ Net Score: 0
📊 [XLV] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 2 | ⚖️ Net Score: 0
📊 [AMZN] Consensus: 6 Runs | 🟢 Long: 3 | 🔴 Short: 3 | ⚖️ Net Score: 0
📊 [ASHR | A股ETF(沪深300口径) (ASHR)] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 1 | ⚖️ Net Score: 0
📊 [^VIX] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 2 | ⚖️ Net Score: 0
📊 [EWI] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 1 | ⚖️ Net Score: 0
📊 [DBB] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 2 | ⚖️ Net Score: 0
📊 [AAPL] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 2 | ⚖️ Net Score: -1
📊 [XLB] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 2 | ⚖️ Net Score: -1
📊 [STX] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 2 | ⚖️ Net Score: -1
📊 [000300.SS | 沪深300 (000300.SS)] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 3 | ⚖️ Net Score: -1
📊 [MAGS] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 3 | ⚖️ Net Score: -1
📊 [COPX] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 3 | ⚖️ Net Score: -1
📊 [NFLX] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 2 | ⚖️ Net Score: -2
📊 [XLE] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 4 | ⚖️ Net Score: -2
📊 [EWP] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 4 | ⚖️ Net Score: -2
📊 [RSPT] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 4 | ⚖️ Net Score: -2
📊 [ASTS] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 4 | ⚖️ Net Score: -2
📊 [XLF] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 3 | ⚖️ Net Score: -3
📊 [GOOGL] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [AMD] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 5 | ⚖️ Net Score: -4
📊 [NVDA] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [ORCL] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [ILF] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [CIFR] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [EZA] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [ASEA] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [EWG] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [IBB] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 5 | ⚖️ Net Score: -4
📊 [SLV] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 5 | ⚖️ Net Score: -4
📊 [VNET] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 5 | ⚖️ Net Score: -4
📊 [TSM] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [CL=F] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [^VXN] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [UBER] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [MSFT] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [IGV] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [XLI] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [KRE] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [MU] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [SNDK] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [KBE] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [WDC] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [EEM] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [ETN] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [VRT] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [PWR] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [TAN] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [BTC-USD] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [COIN] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [CSCO] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [AVGO] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [EWZ] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [ECH] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [EWW] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [AIA] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [EWT] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [EWY] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [ENOR] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [KLAC] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [LRCX] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [ASML] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [AMAT] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [ROK] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [SE] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [RKLB] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [QBTS] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [RVLV] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [KC] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [URA] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [IRM] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [DLR] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [SATS] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [XBI] Consensus: 12 Runs | 🟢 Long: 0 | 🔴 Short: 12 | ⚖️ Net Score: -12

On Thu, Apr 16, 2026 at 2:36 PM edward xin <edwardxin@gmail.com> wrote:
📊 [AAPL] Consensus: 6 Runs | 🟢 Long: 6 | 🔴 Short: 0 | ⚖️ Net Score: +6
📊 [XLP] Consensus: 6 Runs | 🟢 Long: 6 | 🔴 Short: 0 | ⚖️ Net Score: +6
📊 [^VXN] Consensus: 6 Runs | 🟢 Long: 6 | 🔴 Short: 0 | ⚖️ Net Score: +6
📊 [KWEB | 中概互联网ETF (KWEB)] Consensus: 5 Runs | 🟢 Long: 5 | 🔴 Short: 0 | ⚖️ Net Score: +5
📊 [XPEV] Consensus: 6 Runs | 🟢 Long: 5 | 🔴 Short: 0 | ⚖️ Net Score: +5
📊 [XLV] Consensus: 6 Runs | 🟢 Long: 5 | 🔴 Short: 0 | ⚖️ Net Score: +5
📊 [QQQ] Consensus: 6 Runs | 🟢 Long: 5 | 🔴 Short: 0 | ⚖️ Net Score: +5
📊 [PLTR] Consensus: 6 Runs | 🟢 Long: 4 | 🔴 Short: 0 | ⚖️ Net Score: +4
📊 [META] Consensus: 6 Runs | 🟢 Long: 4 | 🔴 Short: 0 | ⚖️ Net Score: +4
📊 [ETH-USD] Consensus: 6 Runs | 🟢 Long: 5 | 🔴 Short: 1 | ⚖️ Net Score: +4
📊 [^VIX] Consensus: 6 Runs | 🟢 Long: 4 | 🔴 Short: 0 | ⚖️ Net Score: +4
📊 [TSLA] Consensus: 5 Runs | 🟢 Long: 4 | 🔴 Short: 1 | ⚖️ Net Score: +3
📊 [TSM] Consensus: 6 Runs | 🟢 Long: 3 | 🔴 Short: 0 | ⚖️ Net Score: +3
📊 [LEN] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 0 | ⚖️ Net Score: +2
📊 [XLF] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 0 | ⚖️ Net Score: +2
📊 [SMH] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 0 | ⚖️ Net Score: +2
📊 [SPY] Consensus: 6 Runs | 🟢 Long: 4 | 🔴 Short: 2 | ⚖️ Net Score: +2
📊 [XLE] Consensus: 6 Runs | 🟢 Long: 3 | 🔴 Short: 1 | ⚖️ Net Score: +2
📊 [NVDA] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 1 | ⚖️ Net Score: +1
📊 [XLB] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 2 | ⚖️ Net Score: 0
📊 [IWM] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 2 | ⚖️ Net Score: 0
📊 [SLV] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 2 | ⚖️ Net Score: 0
📊 [AVGO] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 3 | ⚖️ Net Score: -1
📊 [CIFR] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 3 | ⚖️ Net Score: -1
📊 [EWW] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 3 | ⚖️ Net Score: -2
📊 [EWG] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 2 | ⚖️ Net Score: -2
📊 [RSPT] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 3 | ⚖️ Net Score: -2
📊 [RSPF] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 3 | ⚖️ Net Score: -2
📊 [BABA | 阿里巴巴 (BABA)] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 3 | ⚖️ Net Score: -3
📊 [NFLX] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 4 | ⚖️ Net Score: -3
📊 [000300.SS | 沪深300 (000300.SS)] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 4 | ⚖️ Net Score: -3
📊 [TAN] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 3 | ⚖️ Net Score: -3
📊 [EZA] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 3 | ⚖️ Net Score: -3
📊 [RSP] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 3 | ⚖️ Net Score: -3
📊 [MSFT] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [GOOGL] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [ENOR] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [RSPG] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [IGV] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [AMD] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [MU] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [WDC] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [STX] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [ASHR | A股ETF(沪深300口径) (ASHR)] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [CL=F] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [CSCO] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [ILF] Consensus: 5 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [EWT] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [UBER] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [ROK] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [AMZN] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [XLI] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [KRE] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [KBE] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [SNDK] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [EEM] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [ETN] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [PWR] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [VRT] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [BTC-USD] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [COIN] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [ORCL] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [MAGS] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [EWZ] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [COPX] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [ECH] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [AIA] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [EWY] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [ASEA] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [EWJ] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [EWP] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [EWI] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [IBB] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [AMAT] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [LRCX] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [KLAC] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [ASML] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [XBI] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6 

On Wed, Apr 15, 2026 at 11:43 PM edward xin <edwardxin@gmail.com> wrote:
📊 [TSLA] Consensus: 4 Runs | 🟢 Long: 4 | 🔴 Short: 0 | ⚖️ Net Score: +4
📊 [TSM] Consensus: 4 Runs | 🟢 Long: 4 | 🔴 Short: 0 | ⚖️ Net Score: +4
📊 [ASHR | A股ETF(沪深300口径) (ASHR)] Consensus: 4 Runs | 🟢 Long: 4 | 🔴 Short: 0 | ⚖️ Net Score: +4
📊 [^VIX] Consensus: 4 Runs | 🟢 Long: 4 | 🔴 Short: 0 | ⚖️ Net Score: +4
📊 [IWM] Consensus: 4 Runs | 🟢 Long: 4 | 🔴 Short: 0 | ⚖️ Net Score: +4
📊 [UBER] Consensus: 4 Runs | 🟢 Long: 4 | 🔴 Short: 0 | ⚖️ Net Score: +4
📊 [SLV] Consensus: 4 Runs | 🟢 Long: 4 | 🔴 Short: 0 | ⚖️ Net Score: +4
📊 [NVDA] Consensus: 4 Runs | 🟢 Long: 3 | 🔴 Short: 0 | ⚖️ Net Score: +3
📊 [TAN] Consensus: 4 Runs | 🟢 Long: 3 | 🔴 Short: 0 | ⚖️ Net Score: +3
📊 [XLP] Consensus: 4 Runs | 🟢 Long: 3 | 🔴 Short: 0 | ⚖️ Net Score: +3
📊 [EZA] Consensus: 4 Runs | 🟢 Long: 3 | 🔴 Short: 0 | ⚖️ Net Score: +3
📊 [PLTR] Consensus: 4 Runs | 🟢 Long: 2 | 🔴 Short: 0 | ⚖️ Net Score: +2
📊 [XLF] Consensus: 4 Runs | 🟢 Long: 2 | 🔴 Short: 0 | ⚖️ Net Score: +2
📊 [SMH] Consensus: 4 Runs | 🟢 Long: 2 | 🔴 Short: 0 | ⚖️ Net Score: +2
📊 [SPY] Consensus: 4 Runs | 🟢 Long: 3 | 🔴 Short: 1 | ⚖️ Net Score: +2
📊 [^VXN] Consensus: 4 Runs | 🟢 Long: 2 | 🔴 Short: 0 | ⚖️ Net Score: +2
📊 [XLE] Consensus: 4 Runs | 🟢 Long: 2 | 🔴 Short: 0 | ⚖️ Net Score: +2
📊 [XPEV] Consensus: 4 Runs | 🟢 Long: 2 | 🔴 Short: 1 | ⚖️ Net Score: +1
📊 [AAPL] Consensus: 4 Runs | 🟢 Long: 2 | 🔴 Short: 1 | ⚖️ Net Score: +1
📊 [BTC-USD] Consensus: 4 Runs | 🟢 Long: 2 | 🔴 Short: 1 | ⚖️ Net Score: +1
📊 [GOOGL] Consensus: 4 Runs | 🟢 Long: 2 | 🔴 Short: 2 | ⚖️ Net Score: 0
📊 [XBI] Consensus: 8 Runs | 🟢 Long: 2 | 🔴 Short: 2 | ⚖️ Net Score: 0
📊 [AMD] Consensus: 4 Runs | 🟢 Long: 1 | 🔴 Short: 1 | ⚖️ Net Score: 0
📊 [XLI] Consensus: 4 Runs | 🟢 Long: 1 | 🔴 Short: 1 | ⚖️ Net Score: 0
📊 [QQQ] Consensus: 4 Runs | 🟢 Long: 2 | 🔴 Short: 2 | ⚖️ Net Score: 0
📊 [ETH-USD] Consensus: 4 Runs | 🟢 Long: 2 | 🔴 Short: 2 | ⚖️ Net Score: 0
📊 [COIN] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 0 | ⚖️ Net Score: 0
📊 [COPX] Consensus: 2 Runs | 🟢 Long: 1 | 🔴 Short: 1 | ⚖️ Net Score: 0
📊 [EWG] Consensus: 4 Runs | 🟢 Long: 2 | 🔴 Short: 2 | ⚖️ Net Score: 0
📊 [RSPT] Consensus: 4 Runs | 🟢 Long: 2 | 🔴 Short: 2 | ⚖️ Net Score: 0
📊 [IBB] Consensus: 4 Runs | 🟢 Long: 2 | 🔴 Short: 2 | ⚖️ Net Score: 0
📊 [RSPG] Consensus: 4 Runs | 🟢 Long: 1 | 🔴 Short: 1 | ⚖️ Net Score: 0
📊 [MAGS] Consensus: 4 Runs | 🟢 Long: 1 | 🔴 Short: 2 | ⚖️ Net Score: -1
📊 [ASEA] Consensus: 4 Runs | 🟢 Long: 1 | 🔴 Short: 2 | ⚖️ Net Score: -1
📊 [RSP] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 1 | ⚖️ Net Score: -1
📊 [EWI] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 1 | ⚖️ Net Score: -1
📊 [BABA | 阿里巴巴 (BABA)] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 2 | ⚖️ Net Score: -2
📊 [MSFT] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 2 | ⚖️ Net Score: -2
📊 [NFLX] Consensus: 4 Runs | 🟢 Long: 1 | 🔴 Short: 3 | ⚖️ Net Score: -2
📊 [IGV] Consensus: 4 Runs | 🟢 Long: 1 | 🔴 Short: 3 | ⚖️ Net Score: -2
📊 [META] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 2 | ⚖️ Net Score: -2
📊 [XLB] Consensus: 4 Runs | 🟢 Long: 1 | 🔴 Short: 3 | ⚖️ Net Score: -2
📊 [000300.SS | 沪深300 (000300.SS)] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 2 | ⚖️ Net Score: -2
📊 [EWW] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 2 | ⚖️ Net Score: -2
📊 [CL=F] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 3 | ⚖️ Net Score: -3
📊 [AVGO] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 3 | ⚖️ Net Score: -3
📊 [CSCO] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 3 | ⚖️ Net Score: -3
📊 [ILF] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 3 | ⚖️ Net Score: -3
📊 [EWZ] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 3 | ⚖️ Net Score: -3
📊 [ECH] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 3 | ⚖️ Net Score: -3
📊 [KWEB | 中概互联网ETF (KWEB)] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [LEN] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [AMZN] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [KRE] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [MU] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [SNDK] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [XLV] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [STX] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [KBE] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [WDC] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [EEM] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [VRT] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [ETN] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [PWR] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [CIFR] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [ORCL] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [EWY] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [AIA] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [EWT] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [EWJ] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [EWP] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [ENOR] Consensus: 4 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4

On Tue, Apr 14, 2026 at 3:48 PM edward xin <edwardxin@gmail.com> wrote:
📊 [^VIX] Consensus: 6 Runs | 🟢 Long: 6 | 🔴 Short: 0 | ⚖️ Net Score: +6
📊 [BABA] Consensus: 6 Runs | 🟢 Long: 5 | 🔴 Short: 0 | ⚖️ Net Score: +5
📊 [BTC-USD] Consensus: 6 Runs | 🟢 Long: 5 | 🔴 Short: 0 | ⚖️ Net Score: +5
📊 [COPX] Consensus: 6 Runs | 🟢 Long: 5 | 🔴 Short: 0 | ⚖️ Net Score: +5
📊 [TSLA] Consensus: 6 Runs | 🟢 Long: 4 | 🔴 Short: 0 | ⚖️ Net Score: +4
📊 [XLV] Consensus: 6 Runs | 🟢 Long: 5 | 🔴 Short: 1 | ⚖️ Net Score: +4
📊 [XLE] Consensus: 6 Runs | 🟢 Long: 4 | 🔴 Short: 0 | ⚖️ Net Score: +4
📊 [PLTR] Consensus: 6 Runs | 🟢 Long: 3 | 🔴 Short: 0 | ⚖️ Net Score: +3
📊 [MSFT] Consensus: 6 Runs | 🟢 Long: 4 | 🔴 Short: 1 | ⚖️ Net Score: +3
📊 [TAN] Consensus: 6 Runs | 🟢 Long: 4 | 🔴 Short: 1 | ⚖️ Net Score: +3
📊 [LEN] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 0 | ⚖️ Net Score: +2
📊 [SMH] Consensus: 6 Runs | 🟢 Long: 4 | 🔴 Short: 2 | ⚖️ Net Score: +2
📊 [AVGO] Consensus: 6 Runs | 🟢 Long: 3 | 🔴 Short: 1 | ⚖️ Net Score: +2
📊 [XPEV] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 0 | ⚖️ Net Score: +1
📊 [QQQ] Consensus: 6 Runs | 🟢 Long: 3 | 🔴 Short: 2 | ⚖️ Net Score: +1
📊 [000300.SS] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 2 | ⚖️ Net Score: 0
📊 [CL=F] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 2 | ⚖️ Net Score: 0
📊 [^VXN] Consensus: 6 Runs | 🟢 Long: 2 | 🔴 Short: 2 | ⚖️ Net Score: 0
📊 [GOOGL] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 2 | ⚖️ Net Score: -1
📊 [KWEB] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 2 | ⚖️ Net Score: -2
📊 [IGV] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 2 | ⚖️ Net Score: -2
📊 [AAPL] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 4 | ⚖️ Net Score: -3
📊 [CIFR] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 4 | ⚖️ Net Score: -3
📊 [IWM] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 4 | ⚖️ Net Score: -3
📊 [ORCL] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 4 | ⚖️ Net Score: -3
📊 [NFLX] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 5 | ⚖️ Net Score: -4
📊 [XBI] Consensus: 12 Runs | 🟢 Long: 2 | 🔴 Short: 6 | ⚖️ Net Score: -4
📊 [NVDA] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 5 | ⚖️ Net Score: -4
📊 [AMZN] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [XLB] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [WDC] Consensus: 6 Runs | 🟢 Long: 1 | 🔴 Short: 5 | ⚖️ Net Score: -4
📊 [EEM] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [CSCO] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 4 | ⚖️ Net Score: -4
📊 [TSM] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [KBE] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [SPY] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [XLP] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 5 | ⚖️ Net Score: -5
📊 [XLF] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [AMD] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [META] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [KRE] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [MU] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [XLI] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [STX] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [ASHR] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [SNDK] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [ETN] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [PWR] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
📊 [VRT] Consensus: 6 Runs | 🟢 Long: 0 | 🔴 Short: 6 | ⚖️ Net Score: -6
"""

# 2. 执行终端
import os
import json
import re
from datetime import datetime

def inject_history():
    print("🚀 启动战术数据注入程序...")
    
    # 切分区块
    blocks = re.split(r'On\s+', raw_email_text)
    new_snapshots = []

    for block in blocks:
        if not block.strip(): continue
        
        # 提取时间 (兼容你的狭义空格)
        date_match = re.search(r'([A-Z][a-z]{2},\s+[A-Z][a-z]{2}\s+\d{1,2},\s+\d{4}\s+at\s+\d{1,2}:\d{2}.{0,2}[AP]M)', block)
        if not date_match: continue
        
        date_str = date_match.group(1).replace('\u202f', ' ').replace(' ', ' ')
        dt = datetime.strptime(date_str, "%a, %b %d, %Y at %I:%M %p")
        formatted_date = dt.strftime("%Y-%m-%d %H:%M:%S")
        
        signals = []
        for line in block.split('\n'):
            if '📊' not in line: continue
            
            sig_match = re.search(r'\[(.*?)\].*?Consensus:\s*(\d+).*?Long:\s*(\d+).*?Short:\s*(\d+).*?Net Score:\s*([+-]?\d+)', line)
            if sig_match:
                raw_ticker = sig_match.group(1).split('|')[0].strip()
                
                
                    
                signals.append({
                    "ticker": raw_ticker,
                    "timestamp": formatted_date,
                    "total_runs": int(sig_match.group(2)),
                    "long_votes": int(sig_match.group(3)),
                    "short_votes": int(sig_match.group(4)),
                    "net_score": int(sig_match.group(5)),
                    "final_action": "HISTORICAL_RECORD",
                    "reason": "Tactical Import from Email Logs"
                })
                
        if signals:
            new_snapshots.append({
                "timestamp": formatted_date,
                "signals": signals
            })

    if not new_snapshots:
        print("❌ 未提取到任何有效历史记录，请检查文本格式。")
        return

    # 3. 读取现有历史库 (修改为你正确的物理路径)
    history_file = r"F:\mx_radar_web\history_1d.json"
    existing_data = []
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            existing_data = json.load(f)

    # 4. 数据融合与去重
    existing_timestamps = {x["timestamp"] for x in existing_data}
    added_count = 0
    for snap in new_snapshots:
        if snap["timestamp"] not in existing_timestamps:
            existing_data.append(snap)
            added_count += 1

    # 按时间强制排序
    existing_data.sort(key=lambda x: x["timestamp"])

    # 5. 覆写保存
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
    print(f"✅ 战术数据注入完毕！成功将 {added_count} 个历史交易日汇入全息沙盘。")

if __name__ == "__main__":
    inject_history()