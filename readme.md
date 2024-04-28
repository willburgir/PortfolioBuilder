# Portfolio Builder

## How to use
1. Provide input into the Excel file input.xlsx
2. Run the program:
   ~~~
   # Format
   python3 PortfolioBuilder.py [path to input file] [--time]

   # Example
   python3 PortfolioBuilder.py .\input\input.xlsx --time 
   ~~~

   Optional Flags:
   - '--time': Displays the time tracking report 


## How it works
This [video](https://www.youtube.com/watch?v=x45D7sIb9Mw) should help you understand how this program works. It explains the basics of modern portfolio theory. 

![396285156_293743566860622_1321961359243836737_n](https://github.com/willburgir/PortfolioBuilder/assets/68487952/3f7fa114-0c28-47e1-82a7-a9de5ea9a9ea)
<img width="1255" alt="CAL part1" src="https://github.com/willburgir/PortfolioBuilder/assets/68487952/32931f1f-fb53-484f-96d2-535910621001">
This Python program helps you construct an optimal investment portfolio based on historical returns of different asset classes. It uses portfolio optimization techniques to maximize expected returns while minimizing "risk" (standard deviation of returns).

These drafts (will be improved eventually) can also help you understand:
![370233691_1803280986797805_4980354062441897920_n](https://github.com/willburgir/PortfolioBuilder/assets/68487952/54e9ab93-b222-4377-aa27-25f2af3f613e)


## Complementary Modules

1. **TickerLootLlama**:
   
   Helps users gather historical returns using ticker symbols (with automated API calls through yfinance.)

2. **TagHeuer**:
   
   Measures the performance of functions within the program. Gives users a rough idea of the time complexity as inputs get larger. To use it, simply run the program with the flag: --time

   

## Note
**This project is under development**

**All images shown on this page are drafts and will be replaced with better ones soon.**

**TODO:** 
- Show % as $ for composition implementation
- Let users highlight any portfolio on the curve (from input)
- Extend Capital Allocation Line beyond 100% into optimal portfolio (for investors with leverage)
- Output a PDF report
- Provide better, more complete explanations of the theory on this page
- Given a desired standard deviation, show users the required percentage of their holdings must be composed of:
    1. The optimal portfolio
    2. Risk free assets (AAA government bonds)
- Implement the option to use target downside deviation to measure risk
- Show historical returns distribution (skewness graph)
