# Beitar Jerusalem Ticket Bots ⚽🎫

An automated, robust dual-bot system designed to monitor the Leaan ticketing platform for Beitar Jerusalem matches. Built with a clean, modular **Object-Oriented Programming (OOP)** architecture, the project includes two specialized scripts: a **General Scanner** for discovering new games, and a **Sniper Bot** for securing tickets to a specific high-demand match.

## 🏛️ Architecture Highlights
The project is built following strict software engineering practices:
* **Separation of Concerns:** Dedicated classes handle distinct responsibilities (e.g., `TelegramNotifier` for communications, `ChromeDriverFactory` for browser lifecycle management, and `PageStatusChecker` for DOM validation).
* **Self-Healing Mechanics:** Resilient loops designed to recover gracefully from network timeouts, WebDriver crashes, or unexpected session drops.
* **Stealth Operations:** Headless Chrome execution utilizing tailored User-Agents and optimized flags to avoid bot detection.

## 🛠️ The Tools

### 1. General Scanner (`generalScanner.py`) - The "Radar"
Use this during quiet periods when you are waiting for a new game to be listed on the site.
* **How it works:** Scans the main Leaan page periodically.
* **What it does:** Filters out season tickets and unwanted keywords. If a brand-new match appears on the site, it instantly sends a Telegram alert with the direct link.

### 2. Sniper Bot (`sniperScanner.py`) - The "Sniper"
Use this when you have a specific URL for a match and you are waiting for the sale to open, or for "Sold Out" tickets to become available again. 
* **How it works:** Sits inside the specific event page and refreshes it continuously.
* **What it does:** Bypasses dynamic statuses like "Sold out", "Sale starts soon", or user-specific account restrictions. The exact millisecond the button changes to **"Buy tickets"** or **"הוסף לעגלה"**, it fires immediate Telegram alerts and pops open your browser so you can grab the tickets instantly.

## ⚙️ Prerequisites
* Python 3.8+
* Google Chrome browser installed
* A Telegram Bot Token and Chat ID

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/ticket-finder.git](https://github.com/yourusername/ticket-finder.git)
   cd ticket-finder

  
