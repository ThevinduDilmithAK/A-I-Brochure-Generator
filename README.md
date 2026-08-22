# 🏢 AI Brochure Generator

The **AI Brochure Generator** is a sleek, high-performance Python web application that instantly transforms any company URL into an engaging, structured Markdown brochure. 

Designed for rapid corporate research, sales profiling, and content strategy, this tool scrapes target websites and leverages large language models (via the Groq API) to synthesize the data into a highly visual, emoji-rich executive summary and comprehensive company overview.

## ✨ Key Features

* **Instant Content Synthesis:** Simply paste a URL, and the AI automatically generates an Executive Summary, Key Products overview, and Company Culture breakdown.
* **Premium Glassmorphic UI:** Built with a custom Gradio interface featuring a striking Sunset Amber & Coral color palette, CSS gradients, and hover animations.
* **Smart Tabbed Layout:** View the beautifully formatted brochure in one tab, or switch to the raw source tab to easily copy the Markdown text.
* **Direct File Export:** Includes a built-in download feature that seamlessly packages the generated response into a ready-to-use `.md` file.
* **Blazing Fast Inference:** Powered by the Groq API to ensure the text streams into the application with near-zero latency.

## 🛠️ Tech Stack

* **Language:** Python
* **Frontend UI:** Gradio (with custom CSS injection)
* **LLM Integration:** OpenAI Python SDK (routed through Groq's endpoint)
* **Deployment:** Designed for seamless hosting on platforms like Render or Hugging Face.

## 🚀 Getting Started

Follow these steps to run the application on your local machine.

### Prerequisites
Make sure you have Python installed, along with an active API key from [Groq](https://console.groq.com/).

### Installation

1. **Clone the repository:**

2. Install the required dependencies:

Bash
pip install -r requirements.txt
Set up your API Key:
Set your Groq API key as an environment variable in your terminal:

Windows: set GROQ_API_KEY=your_api_key_here

Mac/Linux: export GROQ_API_KEY=your_api_key_here

Run the application:

Bash
python app.py
Open your browser and navigate to http://127.0.0.1:7860 to use the tool locally.

##👨‍💻 About the Author
Designed and developed by Thevindu Dilmith A.K., a computer science and engineering student at the University of Moratuwa. This project combines robust Python backend logic with modern, aesthetic web design principles to create a highly functional AI utility.

© 2026 All Rights Reserved.
   ```bash
   git clone [https://github.com/your-username/ai-brochure-generator.git](https://github.com/your-username/ai-brochure-generator.git)
   cd ai-brochure-generator
