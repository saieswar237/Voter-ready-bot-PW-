# Voter-Ready Bot 🗳️✨

Voter-Ready Bot is a premium, interactive AI assistant designed to guide Indian citizens through the election process. Built with an "agency-style" glassmorphism Single Page Application (SPA) frontend and powered by Google's cutting-edge **Gemini Flash** AI model, it transforms a traditionally tedious process into a stunning, lightning-fast experience.

## ✨ Features

- **Premium UI/UX:** Full-screen radial gradients, dynamic Particles.js backgrounds, and smooth GSAP micro-animations.
- **Interactive State Machine:** A slick, step-by-step wizard that asks for your age and Voter ID status before giving personalized advice.
- **Bi-Directional Streamlit Component:** Bypasses standard Streamlit widgets entirely by injecting a bespoke HTML/CSS/JS interface that communicates flawlessly with the Python backend.
- **Gemini AI Integration:** Utilizes `google-genai` SDK to fetch accurate, context-aware instructions for first-time voters, address changes, and polling day simulations.
- **Continuous AI Chat:** Ask follow-up questions right inside the final assessment card! The bot remembers conversation history and can handle typos and edge-case questions beautifully.
- **Robust Fallbacks:** Implements automatic retries for API high-demand (503) scenarios to ensure users always get an answer.

## 🛠️ Technology Stack

- **Frontend:** HTML5, Vanilla CSS (Glassmorphism), Vanilla JS, Particles.js, GSAP (GreenSock Animation Platform)
- **Backend:** Python, Streamlit (used as a rapid backend router)
- **AI Engine:** Google Gemini (`gemini-flash-latest`) via the `google-genai` SDK

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/voter-ready-bot.git
cd voter-ready-bot
```

### 2. Set up a Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Rename `.env.example` to `.env` and insert your Gemini API Key:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```
*(The app will automatically open in your default browser at `http://localhost:8501`)*

## 📂 Project Structure

- `app.py`: The main Streamlit file that injects the custom HTML frontend and handles session state.
- `bot_logic.py`: Contains the master prompt and conversational flow rules.
- `api_handler.py`: Manages the connection to Google's Gemini API, including retry mechanisms for rate limits.
- `requirements.txt`: Python dependencies.
- `.env.example`: Template for environment variables.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📄 License
This project is open-source and available under the MIT License.
