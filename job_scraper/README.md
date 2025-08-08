# Pakistan Job Market Analyzer

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

An automated tool to scrape and analyze job listings from Rozee.pk, Pakistan's leading job portal. Perfect for HR analysts, job seekers, and market researchers.

## ✨ Features

- **Comprehensive Data Extraction**:
  - Job Titles
  - Company Names 
  - Salary Ranges (when available)
- **Smart Pagination Handling**: Automatically scrapes across multiple pages
- **Customizable Search**: Filter by job title and city
- **Automated Scheduling**: Daily runs via Windows Task Scheduler
- **Structured Output**: Clean CSV files with standardized naming:
  ```python
  "rozee_{job_title}_{city}_jobs.csv"  # Example: rozee_software_engineer_karachi_jobs.csv

## 🛠️ Technologies Used

- **Python 3.10+**
- **Selenium WebDriver** – Browser automation
- **Pandas** – Data export
- **ChromeDriver** – Browser control

## 🚀 Getting Started

### Prerequisites
- Chrome browser installed
- Python 3.10 or newer

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/pakistan-job-analyzer.git
   cd pakistan-job-analyzer

2. **Set up a virtual environment (Recommended):**
    python -m venv venv
    venv\Scripts\activate  # Windows

3. **Install dependencies:**
    pip install -r requirements.txt

4. **Download ChromeDriver:**
    Get the version matching your Chrome browser from chromedriver.chromium.org

    Place it in the project folder or add to PATH

## 🖥️ Usage

### **Interactive Mode (Manual Run)**
    python main.py

You'll be prompted for:
    Enter job title (press Enter for default): Data Scientist
    Enter City (press Enter for default): Lahore

# ⏰ Scheduling Automated Runs (Windows)

### **Open Task Scheduler (Win + R → taskschd.msc)**

**Create a new task with:**

- **Trigger:** Daily at your preferred time  
- **Action:**  
  - **Program:** `python.exe`  
  - **Arguments:** `"C:\path\to\main.py"`  
  - **Start in:** `"C:\path\to\project\folder"`  
- Check **"Run whether user is logged on or not"**

---

## 📊 Sample Output

**rozee_software_engineer_karachi_jobs.csv**:

| Title               | Company                       | Salary             |
|---------------------|--------------------------------|--------------------|
| AI Engineer         | PixelFyre Code Labs,          | Not listed         |
| Planning Engineer   | Exide,                        | Not listed         |
| IT Security Engineer| Contour Software,             | Not listed         |
| Data Engineer       | Horizon Technologies,         | 200K - 200K        |

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository  
2. Create a feature branch:

```bash
git checkout -b feature/your-feature

## 🐞 Reporting Issues

Please include the following when reporting issues:

- **Steps to reproduce**
- **Screenshots** (if applicable)
- **Expected vs actual behavior**

---

## 📜 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.



