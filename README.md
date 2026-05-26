# AI Gig Hunter

An autonomous AI-powered lead generation system for finding web development gigs, scoring opportunities, storing leads, and automating outreach.

Built with Python, SQLite, modular scrapers, and n8n automation.

---

## 🚀 Features

- Multi-source lead scraping
- Intelligent lead scoring
- SQLite lead database
- Automated outreach pipeline
- Modular agent architecture
- Duplicate prevention
- Extensible scraper system

## 🧠 Current Agents

### Marketing Agent

Responsible for:
- collecting leads from scrapers
- filtering relevant opportunities
- scoring leads
- saving qualified leads into the database


### Sales Agent

Responsible for:
- retrieving uncontacted leads
- sending outreach via n8n webhook
- marking leads as contacted


## 🌐 Current Scrapers

### RemoteOK

Scrapes remote developer jobs from RemoteOK.

### Reddit

Scrapes hiring-related posts from Reddit.

Supports filtering buyer vs seller posts.

### WeWorkRemotely

Scrapes remote developer opportunities from We Work Remotely.


## 🏗️ Project Structure

```text
ai-gig-hunter/
│
├── agents/
│   ├── marketing_agent.py
│   ├── sales_agent.py
│
├── sources/
│   ├── remoteok.py
│   ├── reddit.py
│   ├── weworkremotely.py
│
├── tools/
│   ├── scraper_manager.py
│
├── memory/
│   ├── db.py
│
├── config/
│   ├── settings.py
│
├── test_scraper.py
├── run.py
├── requirements.txt
│
└── README.md
```


## ⚙️ Tech Stack

- Python 3
- SQLite
- Requests
- BeautifulSoup
- n8n


## 📦 Installation

1. **Clone the repository:**
   ```bash
   git git clone https://github.com/yourusername/ai-gig-hunter.git

2. **Navigate to the project directory:**
   ```bash
   cd ai-gig-hunter

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

```


### Contributing

Contributions are welcome! Feel free to submit pull requests or raise issues to improve the app.

1. **Fork the repository.**

2. **Create your feature branch (git checkout -b feature/new-feature).**

3. **Commit your changes (git commit -am 'Add new feature').**

4. **Push to the branch (git push origin feature/new-feature).**

5. **Open a pull request.**

### 📜 License

MIT License