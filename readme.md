# Portfolio Builder
![396285156_293743566860622_1321961359243836737_n](https://github.com/willburgir/PortfolioBuilder/assets/68487952/3f7fa114-0c28-47e1-82a7-a9de5ea9a9ea)
<img width="1255" alt="CAL part1" src="https://github.com/willburgir/PortfolioBuilder/assets/68487952/32931f1f-fb53-484f-96d2-535910621001">


This Python program helps you construct an optimal investment portfolio based on historical returns of different asset classes. It uses portfolio optimization techniques to maximize expected returns while minimizing "risk" (standard deviation of returns).

## How it works
This [video](https://www.youtube.com/watch?v=x45D7sIb9Mw) should help you understand how this program works. It explains the basics of modern portfolio theory. 

These drafts (will be improved eventually) can also help you understand:
![370233691_1803280986797805_4980354062441897920_n](https://github.com/willburgir/PortfolioBuilder/assets/68487952/54e9ab93-b222-4377-aa27-25f2af3f613e)


## Features

1. **Input File Type**: You can provide the input with a simple Excel file, or use a .csv if you prefer.

2. **Time Tracking**: You can measure the performance of functions within the program using the TagHeuer module. This will help with reducing time complexity of expensive operations. 

## Note
**This project is under development**

**TODO:**
- Somehow show the Efficient Frontier curve
- Highlight the S&P500 on the scatter plot  
- Let users highlight any portfolio on the curve (from input)
- Replace sample input by real data, maybe with yfinance
- Let users input risk free rate and borrowing interest rate
- Extend Capital Allocation Line beyond 100% into optimal portfolio
- Provide better, more complete explanations of the theory on this page
