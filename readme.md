Script para geração automática de tabela para controle de ações

Utiliza as seguintes informações com base na biblioteca yfinance (Yahoo Finances) : 
 - TrailingEps (Earnings Per Share - 12M), 
 - BookValue, 
 - DividendYield,
 - CurrentPrice

Os preços-teto são calculados da seguinte forma : 
 - Preço teto Bazin : (Dividend Yield * CurrentPrice) / 0.07
 - Preço teto Graham : (TrailingEps * BookValue * 22.5) ** 0.5