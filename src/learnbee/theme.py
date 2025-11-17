"""Theme and CSS styling for the Gradio interface."""

import gradio as gr

# Beautiful Ocean-inspired theme
# Try to use Ocean theme, fallback to default if not available
try:
    BEAUTIFUL_THEME = gr.themes.Ocean(
        primary_hue="blue",
        secondary_hue="cyan",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"],
    )
except AttributeError:
    # Fallback to default theme if Ocean is not available
    BEAUTIFUL_THEME = gr.themes.Default(
        primary_hue="blue",
        secondary_hue="cyan",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"],
    )

# CLEAN, MODERN CSS - Compatible con modo claro y oscuro
CUSTOM_CSS = """
/* Main container */
.gradio-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
    padding: 1rem !important;
}

/* Beautiful header - siempre visible en ambos modos */
.header-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2.5rem 2rem;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.25);
}

.header-banner h1 {
    color: white !important;
    font-size: 2.5rem;
    font-weight: 800;
    margin: 0 0 0.5rem 0;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.header-banner p {
    color: rgba(255, 255, 255, 0.95) !important;
    font-size: 1.1rem;
    margin: 0.25rem 0;
}

/* Status box - adaptativo */
.status-box {
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border-left: 4px solid #667eea;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* Chat messages - adaptativo para modo claro y oscuro */
.message {
    border-radius: 12px !important;
    padding: 1rem !important;
    margin: 0.5rem 0 !important;
    animation: fadeIn 0.3s ease;
}

/* Bot messages - adaptativo */
.message.bot {
    border-left: 4px solid #667eea !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
}

/* User messages - adaptativo */
.message.user {
    border-left: 4px solid #94a3b8 !important;
}

/* Code blocks - siempre oscuro para legibilidad */
.message pre {
    background: #1e293b !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Input fields - adaptativo */
textarea, input[type="text"], input[type="number"] {
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}

textarea:focus, input[type="text"]:focus, input[type="number"]:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* Dropdowns - adaptativo */
select, .gr-dropdown {
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}

select:focus, .gr-dropdown:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* Buttons */
button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    padding: 0.75rem 1.5rem !important;
}

button:hover:not(:disabled) {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
}

button.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
}

/* Tabs */
.tab-nav {
    border-radius: 12px 12px 0 0 !important;
}

.tab-nav button {
    border-radius: 12px 12px 0 0 !important;
    margin-right: 0.25rem !important;
}

/* Info boxes - adaptativo */
.info-box {
    border-radius: 12px;
    padding: 1.25rem;
    margin-top: 1rem;
    border-left: 4px solid #94a3b8;
    line-height: 1.7;
}

/* Footer - adaptativo */
.footer-text {
    text-align: center;
    padding: 2rem 1rem;
    line-height: 1.8;
}

.footer-text a {
    color: #667eea;
    text-decoration: none;
    font-weight: 600;
}

/* Column styling - adaptativo */
.column-container {
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* Chat interface container - adaptativo */
.chat-container {
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* Asegurar que los textos en markdown sean legibles en ambos modos */
.markdown-text, .markdown p, .markdown h1, .markdown h2, .markdown h3, .markdown h4, .markdown h5, .markdown h6 {
    color: inherit !important;
}

/* Asegurar que los labels sean legibles */
label {
    color: inherit !important;
}

/* Textboxes y áreas de texto - adaptativo */
.gr-textbox textarea, .gr-textbox input {
    color: inherit !important;
    background-color: inherit !important;
}

/* Dropdowns - adaptativo */
.gr-dropdown select, .gr-dropdown {
    color: inherit !important;
    background-color: inherit !important;
}

/* Números - adaptativo */
.gr-number input {
    color: inherit !important;
    background-color: inherit !important;
}

/* Chatbot messages - asegurar legibilidad */
.chatbot {
    color: inherit !important;
}

.chatbot .message {
    color: inherit !important;
}

/* Status markdown - adaptativo */
.gr-markdown {
    color: inherit !important;
}

.gr-markdown p, .gr-markdown h1, .gr-markdown h2, .gr-markdown h3, 
.gr-markdown h4, .gr-markdown h5, .gr-markdown h6, .gr-markdown li, 
.gr-markdown ul, .gr-markdown ol {
    color: inherit !important;
}

/* Asegurar que los textos dentro de las cajas de información sean legibles */
.info-box p, .info-box strong {
    color: inherit !important;
}

/* Inputs dentro de componentes Gradio */
.gr-component input, .gr-component textarea, .gr-component select {
    color: inherit !important;
}

/* Labels de Gradio */
.gr-label {
    color: inherit !important;
}

/* Contenedores principales - usar colores del tema */
.dark .gradio-container {
    background: var(--background-fill-primary) !important;
}

/* Asegurar que los mensajes del chatbot usen colores del tema */
.chatbot .user-message, .chatbot .assistant-message {
    color: inherit !important;
}

/* Welcome Card - Modern and User-Friendly Design (Compact) */
.welcome-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.1);
    border: 1px solid rgba(102, 126, 234, 0.1);
    animation: fadeInUp 0.6s ease-out;
}

.dark .welcome-card {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-color: rgba(102, 126, 234, 0.2);
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.welcome-header {
    text-align: center;
    margin-bottom: 1.25rem;
}

.welcome-icon {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    animation: wave 2s ease-in-out infinite;
    display: inline-block;
}

@keyframes wave {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(10deg); }
    75% { transform: rotate(-10deg); }
}

.welcome-title {
    font-size: 1.5rem;
    font-weight: 800;
    margin: 0.25rem 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.welcome-subtitle {
    font-size: 0.95rem;
    color: #64748b;
    margin: 0.25rem 0 0 0;
}

.dark .welcome-subtitle {
    color: #94a3b8;
}

.getting-started-section {
    margin: 1.25rem 0;
}

.section-title {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #1e293b;
}

.dark .section-title {
    color: #f1f5f9;
}

.section-icon {
    font-size: 1.4rem;
}

.steps-container {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
}

.step-item {
    display: flex;
    align-items: flex-start;
    gap: 0.875rem;
    padding: 0.875rem;
    background: #ffffff;
    border-radius: 12px;
    border: 2px solid #e2e8f0;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.step-item::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    transform: scaleY(0);
    transition: transform 0.3s ease;
}

.step-item:hover {
    transform: translateX(8px);
    border-color: #667eea;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.step-item:hover::before {
    transform: scaleY(1);
}

.dark .step-item {
    background: #1e293b;
    border-color: #334155;
}

.dark .step-item:hover {
    border-color: #667eea;
    background: #1e293b;
}

.step-number {
    min-width: 32px;
    height: 32px;
    border-radius: 10px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.95rem;
    flex-shrink: 0;
    box-shadow: 0 3px 8px rgba(102, 126, 234, 0.25);
}

.step-final .step-number {
    background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
    font-size: 1.2rem;
    box-shadow: 0 3px 8px rgba(245, 158, 11, 0.25);
}

.step-content {
    flex: 1;
    padding-top: 0.125rem;
}

.step-content strong {
    display: block;
    font-size: 0.95rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
    color: #1e293b;
}

.dark .step-content strong {
    color: #f1f5f9;
}

.step-content p {
    margin: 0;
    color: #64748b;
    font-size: 0.85rem;
    line-height: 1.4;
}

.dark .step-content p {
    color: #94a3b8;
}

.info-badge {
    margin-top: 1.25rem;
    padding: 0.875rem;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border-radius: 10px;
    border: 1px solid rgba(102, 126, 234, 0.2);
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: #475569;
}

.dark .info-badge {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
    border-color: rgba(102, 126, 234, 0.3);
    color: #cbd5e1;
}

.badge-icon {
    font-size: 1.2rem;
}

/* Multilingual Support Card - Centered and Beautiful */
.multilingual-card {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
    border-radius: 14px;
    padding: 1.5rem;
    margin-top: 1rem;
    border: 2px solid rgba(102, 126, 234, 0.15);
    text-align: center;
    transition: all 0.3s ease;
}

.multilingual-card:hover {
    border-color: rgba(102, 126, 234, 0.3);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
    transform: translateY(-2px);
}

.dark .multilingual-card {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border-color: rgba(102, 126, 234, 0.25);
}

.multilingual-header {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
}

.multilingual-icon {
    font-size: 2rem;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

.multilingual-title {
    font-size: 1.3rem;
    font-weight: 700;
    margin: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.multilingual-text {
    font-size: 0.95rem;
    color: #475569;
    margin: 0 0 1rem 0;
    line-height: 1.6;
}

.dark .multilingual-text {
    color: #cbd5e1;
}

.multilingual-note {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.75rem;
    background: rgba(102, 126, 234, 0.08);
    border-radius: 10px;
    border: 1px solid rgba(102, 126, 234, 0.2);
    margin-top: 0.75rem;
}

.dark .multilingual-note {
    background: rgba(102, 126, 234, 0.15);
    border-color: rgba(102, 126, 234, 0.3);
}

.note-icon {
    font-size: 1.1rem;
    flex-shrink: 0;
}

.note-text {
    font-size: 0.85rem;
    color: #64748b;
    font-style: italic;
}

.dark .note-text {
    color: #94a3b8;
}

/* Responsive design for welcome card */
@media (max-width: 768px) {
    .welcome-card {
        padding: 1.25rem;
    }
    
    .welcome-title {
        font-size: 1.3rem;
    }
    
    .step-item {
        padding: 0.75rem;
    }
    
    .step-content strong {
        font-size: 0.9rem;
    }
    
    .multilingual-card {
        padding: 1.25rem;
    }
}

/* Multilingual footer (full-width) - centered and high-contrast for dark/light */
.multilingual-footer {
    width: 100%;
    padding: 1rem 1.25rem;
    margin-top: 1.25rem;
    border-top: 1px solid rgba(226,232,240,0.6);
    background: linear-gradient(90deg, #f8fafc 0%, #eef2ff 100%);
    color: #0f172a;
    text-align: center;
}
.multilingual-footer > div {
    max-width: 1100px;
    margin: 0 auto;
}
.multilingual-footer .multilingual-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    flex-wrap: wrap;
}
.multilingual-footer .multilingual-title {
    font-weight: 700;
    font-size: 1.05rem;
}
.multilingual-footer .multilingual-desc {
    opacity: 0.9;
}

/* Dark mode adjustments */
.dark .multilingual-footer {
    background: linear-gradient(90deg, #0b1220 0%, #081226 100%);
    color: #e6eef8;
    border-top-color: rgba(51,65,85,0.6);
}

/* Center the main container content while keeping form inputs left-aligned for usability */
.gradio-container {
    text-align: center !important;
}
.gr-label, .gr-input, .gr-dropdown, .gr-textbox, .gr-number {
    text-align: left !important;
}

/* Ensure cards and containers are centered within the page */
.welcome-card, .info-box, .column-container, .chat-container {
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Footer fine-tuning: center icon + title and unify reset text size */
.multilingual-footer .multilingual-icon {
    font-size: 1.6rem;
    display: inline-block;
}
.multilingual-footer .multilingual-content {
    min-width: 280px;
    text-align: center;
}
.multilingual-footer .multilingual-title {
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 0.15rem;
}
.multilingual-footer .multilingual-desc {
    font-size: 0.95rem;
    opacity: 0.92;
}
.multilingual-footer .multilingual-reset {
    font-size: 0.95rem;
    opacity: 0.92;
}
.multilingual-footer .multilingual-reset-wrap {
    margin-left: 0.5rem;
}
"""

