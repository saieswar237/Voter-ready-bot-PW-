import os
import streamlit as st
import streamlit.components.v1 as components
from bot_logic import process_chat

# Hide default Streamlit padding, header, footer to make it full screen
st.set_page_config(page_title="Voter-Ready Bot", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
    .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    /* Remove vertical scrolling from Streamlit main body */
    body, html { overflow: hidden !important; background: #000 !important; }
    iframe { border: none !important; height: 100vh !important; width: 100vw !important; display: block !important; }
</style>
""", unsafe_allow_html=True)

# The Full-Screen HTML/CSS/JS Payload
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600&display=swap" rel="stylesheet">
    <!-- Load Particles.js -->
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <!-- Load GSAP -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <style>
        body, html {
            margin: 0; padding: 0; width: 100%; height: 100vh;
            background: radial-gradient(circle at center, #1a1a2e 0%, #000000 100%);
            color: #fff; font-family: 'Space Grotesk', sans-serif; overflow: hidden;
        }
        #particles-js { position: absolute; width: 100%; height: 100%; z-index: 1; }
        .container {
            position: relative; z-index: 2; width: 100%; height: 100%;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px; padding: 50px; text-align: center;
            max-width: 700px; width: 90%;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
            display: none;
        }
        .glass-card.active { display: block; }
        h1 { font-size: 2.8rem; margin-bottom: 20px; font-weight: 600; letter-spacing: -1px; }
        p { font-size: 1.25rem; color: #b0b0c0; margin-bottom: 40px; line-height: 1.6; }
        .btn-container { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; }
        .btn {
            background: rgba(255,255,255,0.05); color: #fff;
            border: 1px solid rgba(255,255,255,0.2);
            padding: 16px 36px; font-size: 1.1rem; border-radius: 30px;
            cursor: pointer; transition: all 0.3s ease; font-family: 'Space Grotesk', sans-serif;
            backdrop-filter: blur(5px); outline: none;
        }
        .btn:hover { background: #fff; color: #000; transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
        .result-text { font-size: 1.15rem; text-align: left; line-height: 1.7; color: #e2e2e2; }
        .result-text b, .result-text strong { color: #fff; }
        .result-text a { color: #4dabf7; text-decoration: none; }
        .result-text a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div id="particles-js"></div>
    <div class="container">
        
        <!-- Stage 0: Hook -->
        <div id="stage0" class="glass-card active">
            <h1>The Power of Vote</h1>
            <p>The first Indian election took 4 months to complete.<br>Today, the power is in your hands in seconds.</p>
            <div class="btn-container">
                <button class="btn" onclick="nextStage(1)">Enter the Wizard</button>
            </div>
        </div>

        <!-- Stage 1: Age Check -->
        <div id="stage1" class="glass-card">
            <h1>Are you 18 or older?</h1>
            <p>You must be 18 years of age on the qualifying date to be eligible to vote.</p>
            <div class="btn-container">
                <button class="btn" onclick="setAge('yes')">Yes, I am 18+</button>
                <button class="btn" onclick="setAge('no')">No, I'm under 18</button>
            </div>
        </div>

        <!-- Stage 2: Document Check -->
        <div id="stage2" class="glass-card">
            <h1>Do you have a Voter ID?</h1>
            <p>Also known as the EPIC card. It is required to cast your vote.</p>
            <div class="btn-container">
                <button class="btn" onclick="setDoc('yes')">Yes, I have it</button>
                <button class="btn" onclick="setDoc('no')">No, I don't</button>
            </div>
        </div>

        <!-- Stage 3: The Result -->
        <div id="stage3" class="glass-card">
            <h1 id="result-title">Processing...</h1>
            <div id="result-content" class="result-text">
                <!-- A sleek CSS loader while waiting for backend -->
                <div style="text-align:center; padding: 20px;">
                    <svg width="50" height="50" viewBox="0 0 50 50" stroke="#fff">
                        <g fill="none" fill-rule="evenodd" stroke-width="4">
                            <circle cx="25" cy="25" r="20" stroke-opacity=".2"/>
                            <path d="M25 5c0 0 20 0 20 20">
                                <animateTransform attributeName="transform" type="rotate" from="0 25 25" to="360 25 25" dur="1s" repeatCount="indefinite"/>
                            </path>
                        </g>
                    </svg>
                </div>
            </div>
            
            <!-- Chat Interface -->
            <div id="chat-interface" style="display:none; margin-top: 30px; text-align: left;">
                <div id="chat-history" style="max-height: 250px; overflow-y: auto; padding: 15px; border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; margin-bottom: 15px; background: rgba(0,0,0,0.3);">
                    <div id="chat-history-content"></div>
                    <div id="typing-indicator" style="display:none; text-align: left; margin-top: 10px;">
                        <div style="display: inline-block; background: rgba(255, 255, 255, 0.1); padding: 10px 15px; border-radius: 15px; color: #ccc; font-style: italic; font-size: 0.95rem;">Thinking...</div>
                    </div>
                </div>
                
                <div style="display: flex; gap: 10px;">
                    <input type="text" id="chat-input" placeholder="Ask a follow-up question..." onkeypress="handleKeyPress(event)" style="flex: 1; padding: 12px 20px; border-radius: 30px; border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.05); color: #fff; font-family: 'Space Grotesk', sans-serif; font-size: 1rem; outline: none; backdrop-filter: blur(5px);">
                    <button class="btn" style="padding: 10px 25px; margin: 0; font-size: 1rem;" onclick="sendChat()">Send</button>
                </div>
            </div>

            <div class="btn-container" style="margin-top: 20px;">
                <button id="restart-btn" class="btn" style="display:none; font-size: 0.9rem; padding: 10px 20px;" onclick="startOver()">Start Over</button>
            </div>
        </div>
    </div>

    <script>
        // Init Particles
        particlesJS("particles-js", {
          "particles": {
            "number": {"value": 80, "density": {"enable": true, "value_area": 800}},
            "color": {"value": "#ffffff"},
            "shape": {"type": "circle"},
            "opacity": {"value": 0.4, "random": true},
            "size": {"value": 2.5, "random": true},
            "line_linked": {"enable": true, "distance": 150, "color": "#ffffff", "opacity": 0.15, "width": 1},
            "move": {"enable": true, "speed": 1.5, "direction": "none", "out_mode": "out"}
          },
          "interactivity": {
            "events": { "onhover": {"enable": true, "mode": "grab"}, "onclick": {"enable": true, "mode": "push"} },
            "modes": { "grab": {"distance": 200, "line_linked": {"opacity": 0.3}} }
          },
          "retina_detect": true
        });

        // Initial GSAP Animation for Hook
        gsap.from("#stage0 h1", {y: -20, opacity: 0, duration: 0.3, ease: "power3.out"});
        gsap.from("#stage0 p", {y: 10, opacity: 0, duration: 0.3, delay: 0.1});
        gsap.from("#stage0 .btn-container", {y: 10, opacity: 0, duration: 0.3, delay: 0.2});

        let userData = { age: null, has_id: null };

        function transition(fromId, toId) {
            gsap.to(fromId, {
                y: -30, opacity: 0, duration: 0.15, ease: "power2.in", onComplete: () => {
                    document.querySelector(fromId).classList.remove("active");
                    let nextEl = document.querySelector(toId);
                    nextEl.classList.add("active");
                    gsap.fromTo(toId, {y: 30, opacity: 0}, {y: 0, opacity: 1, duration: 0.2, ease: "power3.out"});
                }
            });
        }

        function nextStage(stage) { transition("#stage0", "#stage1"); }

        function setAge(val) {
            userData.age = val;
            if (val === 'no') {
                transition("#stage1", "#stage3");
                sendData();
            } else {
                transition("#stage1", "#stage2");
            }
        }

        function setDoc(val) {
            userData.has_id = val;
            transition("#stage2", "#stage3");
            sendData();
        }

        function sendData() {
            let payload = "I am ";
            if(userData.age === 'no') {
                payload += "under 18 years old and want to know about voting in India.";
            } else {
                payload += "over 18 years old. ";
                if(userData.has_id === 'yes') {
                    payload += "I DO have my Voter ID (EPIC card). Explain briefly what I should do inside the polling booth.";
                } else {
                    payload += "I DO NOT have a Voter ID. How do I get one?";
                }
            }
            // Send payload to Python
            Streamlit.setComponentValue({action: "fetch_result", prompt: payload});
        }
        
        function sendChat() {
            let inputEl = document.getElementById("chat-input");
            let text = inputEl.value.trim();
            if(!text) return;
            
            // Show typing indicator
            document.getElementById("typing-indicator").style.display = "block";
            let historyDiv = document.getElementById("chat-history");
            historyDiv.scrollTop = historyDiv.scrollHeight;
            
            inputEl.value = "";
            Streamlit.setComponentValue({action: "chat", prompt: text});
        }
        
        function handleKeyPress(e) {
            if(e.key === "Enter") sendChat();
        }

        function startOver() {
            userData = {age: null, has_id: null};
            document.getElementById("result-title").innerText = "Processing...";
            document.getElementById("result-content").innerHTML = `
                <div style="text-align:center; padding: 20px;">
                    <svg width="50" height="50" viewBox="0 0 50 50" stroke="#fff">
                        <g fill="none" fill-rule="evenodd" stroke-width="4">
                            <circle cx="25" cy="25" r="20" stroke-opacity=".2"/>
                            <path d="M25 5c0 0 20 0 20 20">
                                <animateTransform attributeName="transform" type="rotate" from="0 25 25" to="360 25 25" dur="1s" repeatCount="indefinite"/>
                            </path>
                        </g>
                    </svg>
                </div>
            `;
            document.getElementById("chat-history-content").innerHTML = "";
            document.getElementById("chat-interface").style.display = "none";
            document.getElementById("restart-btn").style.display = "none";
            transition("#stage3", "#stage0");
            Streamlit.setComponentValue({action: "reset"});
        }

        // Streamlit Component integration via postMessage
        const Streamlit = {
            setComponentReady: function() {
                window.parent.postMessage({isStreamlitMessage: true, type: "streamlit:componentReady", apiVersion: 1}, "*");
            },
            setFrameHeight: function(height) {
                window.parent.postMessage({isStreamlitMessage: true, type: "streamlit:setFrameHeight", height: height}, "*");
            },
            setComponentValue: function(value) {
                window.parent.postMessage({isStreamlitMessage: true, type: "streamlit:setComponentValue", value: value, dataType: "json"}, "*");
            }
        };

        window.addEventListener("message", function(event) {
            if (event.data.type === "streamlit:render") {
                Streamlit.setFrameHeight(window.screen.availHeight || 1000); 
                
                const data = event.data.args;
                if(data && data.messages && data.messages.length > 0) {
                    // Automatically jump to Stage 3 if not already there (handles page refresh)
                    if (!document.getElementById("stage3").classList.contains("active")) {
                        document.querySelectorAll('.glass-card').forEach(el => el.classList.remove('active'));
                        document.getElementById("stage3").classList.add("active");
                        gsap.set("#stage3", {opacity: 1, y: 0});
                    }

                    document.getElementById("result-title").innerText = "Your Path Forward";
                    document.getElementById("typing-indicator").style.display = "none";
                    
                    let assistantMsgs = data.messages.filter(m => m.role === 'assistant');
                    
                    if(assistantMsgs.length > 0) {
                        let formattedFirst = assistantMsgs[0].content
                            .replace(/\\*\\*(.*?)\\*\\*/g, '<b>$1</b>')
                            .replace(/\\*(.*?)\\*/g, '<i>$1</i>')
                            .replace(/\\[(.*?)\\]\\((.*?)\\)/g, '<a href="$2" target="_blank">$1</a>')
                            .replace(/\\n/g, '<br>');
                        
                        let resultContent = document.getElementById("result-content");
                        if(resultContent.innerHTML.includes("svg")) {
                            resultContent.innerHTML = formattedFirst;
                            gsap.fromTo("#result-content", {opacity: 0, y: 10}, {opacity: 1, y: 0, duration: 0.3});
                        } else {
                            resultContent.innerHTML = formattedFirst;
                        }
                        
                        document.getElementById("restart-btn").style.display = "inline-block";
                        document.getElementById("chat-interface").style.display = "block";
                    }

                    if(data.messages.length > 2) {
                        let chatHtml = "";
                        let chatMsgs = data.messages.slice(2);
                        for(let msg of chatMsgs) {
                            let align = msg.role === 'user' ? 'right' : 'left';
                            let color = msg.role === 'user' ? '#4dabf7' : '#e2e2e2';
                            let bg = msg.role === 'user' ? 'rgba(77, 171, 247, 0.2)' : 'rgba(255, 255, 255, 0.1)';
                            let content = msg.content
                                .replace(/\\*\\*(.*?)\\*\\*/g, '<b>$1</b>')
                                .replace(/\\*(.*?)\\*/g, '<i>$1</i>')
                                .replace(/\\[(.*?)\\]\\((.*?)\\)/g, '<a href="$2" target="_blank">$1</a>')
                                .replace(/\\n/g, '<br>');
                            
                            chatHtml += `<div style="text-align: ${align}; margin-bottom: 12px;"><div style="display: inline-block; text-align: left; background: ${bg}; padding: 12px 18px; border-radius: 15px; color: ${color}; max-width: 85%; font-size: 1.05rem; line-height: 1.5; border: 1px solid rgba(255,255,255,0.05);">${content}</div></div>`;
                        }
                        document.getElementById("chat-history-content").innerHTML = chatHtml;
                        let historyDiv = document.getElementById("chat-history");
                        historyDiv.scrollTop = historyDiv.scrollHeight;
                    }
                }
            }
        });
        
        // Notify Streamlit we are ready
        Streamlit.setComponentReady();
        Streamlit.setFrameHeight(window.screen.availHeight || 1000);
    </script>
</body>
</html>
"""

# Initialize session state for response messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Create a frontend directory to serve the component from
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
os.makedirs(frontend_dir, exist_ok=True)
index_path = os.path.join(frontend_dir, "index.html")

# Only write HTML_TEMPLATE if the file doesn't exist or has changed to prevent Streamlit from hot-reloading the iframe unnecessarily
if not os.path.exists(index_path) or open(index_path, "r", encoding="utf-8").read() != HTML_TEMPLATE:
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)

# Declare the custom component using the path
wizard_ui = components.declare_component("wizard_ui", path=frontend_dir)

# Render the component, passing in the current chat messages
result = wizard_ui(messages=st.session_state.messages, key="wizard")

# --- THE FIX: Create a dedicated lock to prevent infinite loops ---
if "last_processed_prompt" not in st.session_state:
    st.session_state.last_processed_prompt = None

# Handle bi-directional communication
if result and isinstance(result, dict):
    if result.get("action") in ["fetch_result", "chat"]:
        prompt = result.get("prompt")
        
        # Check against our dedicated lock, NOT the chat array!
        if prompt and st.session_state.last_processed_prompt != prompt:
            # LOCK IT IN immediately so it doesn't run again on the next refresh
            st.session_state.last_processed_prompt = prompt
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Format history for bot_logic
            history_str = ""
            for m in st.session_state.messages:
                prefix = "User: " if m["role"] == "user" else "Bot: "
                history_str += f"{prefix}{m['content']}\n"
                
            response = process_chat(history_str)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()
            
    elif result.get("action") == "reset":
        if len(st.session_state.messages) > 0:
            st.session_state.messages = []
            st.session_state.last_processed_prompt = None # Reset the lock too!
            st.rerun()