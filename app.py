from flask import Flask, request
import subprocess

app = Flask(__name__)

MODEL = "/data/data/com.termux/files/home/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
LLAMA = "/data/data/com.termux/files/home/llama.cpp/build/bin/llama-simple"

@app.route("/")
def home():
    return """
<html>

<head>
<title>Android AI Server</title>

<style>
body{
    background:#0f1117;
    color:white;
    font-family:sans-serif;
    padding:40px;
}

h1{
    color:#00ff99;
}

input{
    padding:12px;
    width:320px;
    border-radius:10px;
    border:none;
    font-size:16px;
    background:#161b22;
    color:white;
}

button{
    padding:12px 18px;
    border-radius:10px;
    border:none;
    background:#00ff99;
    color:black;
    font-weight:bold;
    font-size:16px;
    cursor:pointer;
}

button:hover{
    opacity:0.9;
}
</style>

</head>

<body>

<h1>Android AI Server</h1>

<form action="/chat">

<input
name="q"
placeholder="Ask something..."
required
>

<button type="submit">
Ask
</button>

</form>

</body>
</html>
"""

@app.route("/chat")
def chat():

    q = request.args.get("q")

    prompt = f"Q: {q}\\nA:"

    result = subprocess.check_output([
        LLAMA,
        "-m", MODEL,
        prompt
    ]).decode()

    cleaned = result.split("A:")[-1]

    return f"""
<html>

<head>
<style>

body{{
    background:#0f1117;
    color:white;
    font-family:sans-serif;
    padding:40px;
}}

pre{{
    white-space:pre-wrap;
    background:#161b22;
    padding:20px;
    border-radius:12px;
    font-size:18px;
    line-height:1.6;
}}

a{{
    color:#00ff99;
    text-decoration:none;
    font-size:18px;
}}

</style>
</head>

<body>

<h2>AI Response</h2>

<pre>{cleaned}</pre>

<br><br>

<a href="/">← Back</a>

</body>
</html>
"""

app.run(host="0.0.0.0", port=5000)
