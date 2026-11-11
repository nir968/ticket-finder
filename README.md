# Ticket Scanner & Monitor ⚽🎫

An automated monitoring system that tracks ticketing platforms for high-demand events and sends real-time Telegram alerts. Built with a clean, modular **Object-Oriented Programming (OOP)** architecture, the project includes two scripts: a **General Scanner** that discovers newly listed events, and a **Targeted Monitor** that watches a specific event page for availability changes.

## 🏛️ Architecture Highlights

* **Separation of Concerns:** Dedicated classes handle distinct responsibilities, such as `TelegramNotifier` for notifications, `ChromeDriverFactory` for browser lifecycle management, and `PageStatusChecker` for DOM validation.
* **Self-Healing Mechanics:** Resilient loops that recover gracefully from network timeouts, WebDriver crashes, or unexpected session drops.
* **Headless Execution:** Runs Chrome in headless mode for lightweight, continuous monitoring.

## 🛠️ The Tools

### 1. General Scanner (`generalScanner.py`)
Use this when you are waiting for a new event to be listed on the site.

* **How it works:** Periodically scans the main events page.
* **What it does:** Filters out season tickets and unwanted keywords. When a new event appears, it sends a Telegram alert with a direct link.

### 2. Targeted Monitor (`sniperScanner.py`)
Use this when you have a specific event URL and are waiting for the sale to open, or for sold-out tickets to become available again.

* **How it works:** Monitors the specific event page and refreshes it periodically.
* **What it does:** Detects status changes such as "Sold out" or "Sale starts soon". As soon as the button changes to "Buy tickets" or "הוסף לעגלה", it sends a Telegram alert and opens the event page in your browser.

## ⚙️ Prerequisites

* Python 3.8+
* Google Chrome
* A Telegram bot token and chat ID

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/nir968/ticket-finder.git
cd ticket-finder
```

2. Install the dependencies:
```bash
pip install selenium webdriver-manager python-dotenv requests beautifulsoup4 python-bidi
```

3. Create a `.env` file in the root directory with your Telegram credentials:
```bash
TELEGRAM_TOKEN=your_telegram_api_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

## ▶️ Usage

Run the General Scanner:
```bash
python generalScanner.py
```

Run the Targeted Monitor: open `sniperScanner.py`, set `TARGET_EVENT_URL` at the top to your event link, and run:
```bash
python sniperScanner.py
```

## ⚠️ Disclaimer

This project is for educational and personal use only. Use responsibly and comply with the ticketing platform's Terms of Service.
