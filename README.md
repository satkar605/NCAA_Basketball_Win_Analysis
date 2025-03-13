# NCAA Hoops Analysis

## Overview

This project analyzes the NCAA Men's Division I Basketball Tournament data to determine the probability of a team winning if they were leading at half-time. The dataset was extracted from an Azure SQL Database, cleaned, and processed for statistical analysis and visualization.

## Objectives

- Extract and clean NCAA basketball game data.
- Analyze the probability of a team winning when leading at half-time.
- Conduct exploratory data analysis (EDA) to identify trends.
- Use regression analysis to explore the relationship between total points and winning percentage.

## Data Source

- Data was obtained from an **Azure SQL Database** storing NCAA basketball statistics.
- The dataset includes game results, team scores, and overtime details.

## Tools & Technologies Used

- **Python** (pandas, pyodbc, matplotlib, statsmodels)
- **SQL** (Extracting data from Azure SQL Database)
- **Jupyter Notebook / Spyder** (for code execution & analysis)
- **CSV** (Exporting cleaned data for further analysis)

## Project Structure

```
📂 NCAA-Hoops-Analysis/
 ├── 📜 README.md  # Project documentation
 ├── 📜 .gitignore  # Ignored files configuration
 ├── 📜 LICENSE  # (Optional) Open-source license
 ├── 📜 NCAA_Hoops_Analysis_Report.pdf  # Detailed analysis report
 ├── 📜 ncaa_hoops_analysis.py  # Main Python script
 ├── 📜 ncaa_hoops_analysis.ipynb  # Jupyter Notebook (optional)
 ├── 📜 gameresults.csv  # Cleaned dataset output
```

## Installation & Dependencies

Ensure you have the following libraries installed:

```bash
pip install pandas pyodbc matplotlib statsmodels
```

## How to Run the Code

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/NCAA-Hoops-Analysis.git
   ```
2. Navigate to the project directory:
   ```bash
   cd NCAA-Hoops-Analysis
   ```
3. Run the Python script:
   ```bash
   python ncaa_hoops_analysis.py
   ```
4. Open `gameresults.csv` to view the cleaned data.

## Key Findings

- **Winning Probability**: Teams leading at half-time had a `XX%` chance of winning.
- **Highest Scoring Team**: `Providence` scored the most points across all games.
- **Lowest Scoring Team**: `Stanislaus St.` had the fewest points in total.
- **Regression Analysis**: There is a strong correlation between total points scored and winning percentage.

## Visualizations

1. **Win vs Loss Probability for 1st Half Leaders**2. **Comparison of Total Points: Fewest vs. Most**
## Future Improvements

- Enhance model prediction using machine learning.
- Incorporate real-time game data.
- Add player-level statistics for deeper analysis.

## Author

**Satkar Karki**[LinkedIn](https://www.linkedin.com/in/satkarkarki)[GitHub](https://github.com/satkar605)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
