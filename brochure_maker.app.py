import os
import tempfile
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 1. API Client Setup
MODEL = "openai/gpt-oss-20b"
open_api = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=open_api,
    base_url="https://api.groq.com/openai/v1"
)

# 2. Advanced CSS (Sunset Amber & Coral Palette)
custom_css = """
/* Target the custom gradio-app element alongside the body */
gradio-app, body { 
    background-image: linear-gradient(rgba(12, 10, 9, 0.85), rgba(12, 10, 9, 0.85)), 
                      url('https://images.unsplash.com/photo-1432405972618-fc40814d2a10?q=80&w=2000&auto=format&fit=crop') !important; 
    background-size: cover !important;
    background-position: center center !important;
    background-attachment: fixed !important; 
    background-repeat: no-repeat !important;
    background-color: transparent !important;
}

/* Force the main container to let the image show through */
.gradio-container {
    background: transparent !important;
    background-color: transparent !important;
    max-width: 850px !important;
    margin: 0 auto !important;
    font-family: 'Inter', system-ui, sans-serif !important;
}
/* Glassmorphic Container */
.main-card {
    background: #1c1917 !important;
    border: 1px solid #292524 !important;
    border-radius: 16px !important;
    padding: 25px 30px !important;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5) !important;
}

/* Clean up labels */
.main-card span, .output-card span {
    background: transparent !important;
    border: none !important;
    color: #a8a29e !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    padding-left: 0 !important;
}

/* Text Input Styling */
input[type="text"] {
    background-color: #292524 !important;
    border: 1.5px solid #44403c !important;
    border-radius: 10px !important;
    color: #f5f5f4 !important;
    padding: 12px 16px !important;
    font-size: 1rem !important;
    transition: all 0.2s ease !important;
}

input[type="text"]:focus {
    border-color: #f97316 !important; /* Orange accent */
    box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.15) !important;
}

/* Main Generate Button - Warm Sunset Gradient */
#generate-btn {
    background: linear-gradient(135deg, #ea580c 0%, #dc2626 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    padding: 12px !important;
    box-shadow: 0 6px 20px rgba(234, 88, 12, 0.3) !important;
    transition: all 0.3s ease !important;
    margin-top: 15px !important;
}

#generate-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 25px rgba(234, 88, 12, 0.5) !important;
}

/* Secondary Download Button */
#download-btn {
    background: #292524 !important;
    border: 1px solid #44403c !important;
    color: #f5f5f4 !important;
    transition: all 0.2s ease !important;
    margin-top: 15px !important;
    border-radius: 8px !important;
}

#download-btn:hover {
    background: #44403c !important;
    border-color: #fbbf24 !important; /* Amber accent */
}

/* Output Area Card */
.output-card {
    background: #1c1917 !important;
    border: 1px solid #292524 !important;
    border-radius: 16px !important;
    padding: 30px !important;
    margin-top: 25px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
}

/* Executive Summary Badge */
.summary-badge {
    background: rgba(249, 115, 22, 0.08) !important;
    border-left: 4px solid #f97316 !important;
    padding: 15px 20px !important;
    border-radius: 0 8px 8px 0 !important;
    margin-bottom: 20px !important;
}

/* Custom Title with Amber to Orange Gradient */
#custom-title {
    font-size: 2.6rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #fde047 0%, #f97316 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin-bottom: 8px !important;
}

/* Hide default Gradio footer to use our custom one */
footer { visibility: hidden !important; }
"""


# 3. Streaming Generator Function
def create_brochure_gradio(url):

    system_prompt = (
        "You are a professional corporate content strategist. "
        "First, write a 2-sentence 'Executive Summary' of the company. "
        "Then, add exactly this separator on a new line: '---'. "
        "After the separator, generate the full structured brochure in Markdown with sections for Overview, Key Products, and Company Culture. "
        "CRITICAL INSTRUCTION: You must use a wide variety of relevant emojis generously throughout brochure to make the brochure highly visual, modern, and engaging."
    )

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Create a brochure for this website: {url}"}
        ],
        stream=True
    )

    full_response = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content or ''
        full_response += content

        parts = full_response.split('---', 1)
        summary = parts[0].strip()
        brochure = parts[1].strip() if len(parts) > 1 else "Generating body..."

        yield summary, brochure, full_response, gr.update(visible=False)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".md", mode="w", encoding="utf-8") as f:
        f.write(full_response.replace('---', '\n\n'))
        temp_file_path = f.name

    yield summary, brochure, full_response, gr.update(value=temp_file_path, visible=True)


# 4. UI Layout
with gr.Blocks(theme=gr.themes.Base(), css=custom_css, title="AI Brochure Generator") as demo:
    gr.HTML(
        """
        <div style="text-align: center; padding: 30px 0 20px 0;">
            <h1 id="custom-title">AI Brochure Generator</h1>
            <p style="color: #a8a29e; font-size: 1.05rem; margin-top: 4px;">
                Transform any company URL into an engaging, structured brochure instantly.
            </p>
        </div>
        """
    )

    with gr.Column(elem_classes="main-card"):
        url_input = gr.Textbox(
            label="Company Website URL",
            placeholder="e.g., https://huggingface.co",
            lines=1,
            max_lines=1
        )
        generate_btn = gr.Button("🔥 Generate Brochure", elem_id="generate-btn")

    with gr.Column(elem_classes="output-card"):
        gr.Markdown("<h3 style='color: #fdba74; margin-top: 0;'>💡 Executive Summary</h3>")
        summary_display = gr.Markdown(elem_classes="summary-badge")

        with gr.Tabs():
            with gr.Tab("📄 Formatted Brochure"):
                output_display = gr.Markdown()

            with gr.Tab("📋 Raw Source (Copy)"):
                # Notice I removed the 'show_copy_button' parameter to avoid your previous error!
                raw_display = gr.Textbox(show_label=False, lines=15)

        download_btn = gr.DownloadButton("📥 Download as Markdown (.md)", visible=False, elem_id="download-btn")

    # 5. Custom Acknowledgement Footer
    gr.HTML(
        """
        <div style="text-align: center; padding: 25px 0 10px 0; margin-top: 40px; border-top: 1px solid #292524;">
            <p style="color: #78716c; font-size: 0.9rem; margin: 0;">
                Designed and developed with Python by <strong>Thevindu Dilmith A.K.</strong>
            </p>
            <p style="color: #78716c; font-size: 0.85rem; margin: 5px 0 0 0;">
                © 2026 All Rights Reserved.
            </p>
        </div>
        """
    )

    generate_btn.click(
        fn=create_brochure_gradio,
        inputs=url_input,
        outputs=[summary_display, output_display, raw_display, download_btn]
    )

if __name__ == "__main__":
    import os
    # Render assigns a dynamic port. If running locally, it defaults to 7860.
    port = int(os.environ.get("PORT", 7860))
    demo.queue().launch(server_name="0.0.0.0", server_port=port)