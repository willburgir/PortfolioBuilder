# Portfolio Builder
![396285156_293743566860622_1321961359243836737_n](https://github.com/willburgir/PortfolioBuilder/assets/68487952/3f7fa114-0c28-47e1-82a7-a9de5ea9a9ea)
<img width="1204" alt="first_efficient_frontier" src="https://github.com/willburgir/PortfolioBuilder/assets/68487952/611b8f85-049e-4865-8892-e99e98a7a55c">

This Python program helps you construct an optimal investment portfolio based on historical returns of different asset classes. It uses portfolio optimization techniques to maximize expected returns while minimizing "risk" (standard deviation of returns).

## How it works
This [video](https://www.youtube.com/watch?v=x45D7sIb9Mw) should help you understand how this program works. It explains the basics of modern portfolio theory. 

These drafts (will be improved eventually) can also help you understand:
![370233691_1803280986797805_4980354062441897920_n](https://github.com/willburgir/PortfolioBuilder/assets/68487952/54e9ab93-b222-4377-aa27-25f2af3f613e)


## Features

1. **Input File Type**: You can provide the input with a simple Excel file, or use a .csv if you prefer.

2. **Time Tracking**: You can measure the performance of functions within the program using the TagHeuer module. This will help with reducing time complexity of expensive operations. 

## Note
**This project is still under development**

**TODO:**
- TimeTracker report should show total metrics
- Somehow show the Efficient Frontier curve
- Add to graph: (a) risk free rate (b) line tangent to Eff Front. (c) Optimal portfolio
- Highlight the S&P500 on the scatter plot  
- Let users highlight any portfolio on the curve (from input)
- Replace sample input by real values, maybe with yfinance
