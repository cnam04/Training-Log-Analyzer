 # 🧗‍♂️ Climbing Workout Analyzer

> *Track, analyze, and visualize your climbing training data with customizable graphs and automated PDF reports.*

## 🌟 Highlights

- 📊 Automatically generates visual performance reports from Excel training logs
- 🧠 Built with object-oriented Python, leveraging pandas and matplotlib
- 📁 Outputs polished PDF reports using Pillow and `fpdf`
- 💡 Designed for climbers seeking insight into their training progress
- 🔁 Modular architecture allows for easy extension and additional graphs

## ℹ️ Overview

**Climbing Workout Analyzer** is a Python-based tool for analyzing and visualizing structured climbing training data. It automates the creation of customized performance graphs and compiles them into professional PDF reports — no manual charting required.

This project was built to automate the entry, planning, and analysis of my personal climbing accessory workout data.

It was developed as a personal project to build skills in data analysis, object-oriented programming, and automated reporting.

### ✍️ Author

I'm Cole Nam, a computer science student and climber. I created this project to combine my passion for training with my growing skills in data science and Python development.

My goal is to improve my technical portfolio while creating a tool I actually use to track and improve my own climbing performance.

## 🚀 Usage Instructions

> The project is still in development, but here’s what it will look like to use:

```bash
python generate_report.py --date 2025-07-01
```

- Automatically parses your climbing log spreadsheet
- Allows for data entry through the CL
- Gives recommendations for workout weights, sets, reps, RPE based on the the current phase of my training
- Cleans and processes workout data using pandas
- Generates multiple matplotlib graphs using class-based design
- Formats and compiles graphs into a downloadable PDF report

## ⬇️ Installation Instructions

1. Clone the repo:

```bash
git clone https://github.com/cnam04/climbing-workout-analyzer.git
cd climbing-workout-analyzer
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Dependencies include:
- `pandas`
- `matplotlib`
- `fpdf`
- `Pillow`
- `openpyxl`

## 🖼️ Example Output

> *Coming soon: screenshots and sample PDF reports*

## 📁 Project Structure

```
climbing-workout-analyzer/
├── README.md
├── .gitignore
├── main.py
└── src/
    ├── graphs/
    ├── reports/
    ├── date_tool.py
    ├── graph_classes.py
    ├── graph_maker.py
    ├── input_module.py
    ├── Training_day.py
    ├── workout_logic.py
    └── Workout.py
```

## 💭 Contributing / Feedback

This project is primarily personal, as it is designed around the format of my personal spreadsheet. I am a beginner so any feedback or contributions are always welcome! I am trying my best to learn how to program conventionally. If you have something to add, just drop me a message on GitHub!



