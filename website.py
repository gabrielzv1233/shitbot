from flask import Flask, request, redirect, url_for
import shelve
import time
import os

FLAG_FILE = "restart_flag.txt"

app = Flask(__name__)

def get_config():
    db = shelve.open("databases/settings/config")
    data = db["configkey"]
    db.close()
    return data

def save_config(config):
    db = shelve.open("databases/settings/config")
    db["configkey"] = config
    db.close()

@app.route("/restart_discord_bot")
def restart_discord_bot():
    open(FLAG_FILE, 'a').close()
    time.sleep(1)
    if os.path.exists(FLAG_FILE):
        os.remove(FLAG_FILE)
    return redirect(url_for("config"))



@app.route("/config", methods=["GET", "POST"], strict_slashes=False)
def config():
    if request.method == "POST":
        new_config = request.form["Config"]
        save_config(new_config)
        return redirect(url_for("restart_discord_bot"))
    
    config = get_config()
    
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset='UTF-8'>
<meta name='description' content='Config pannel for Shitbot'>
<meta name='author' content='Gabrielzv1233, desu23'>
<title>Shitbot - Config</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
    textarea {{
        resize: both;
        width: 100%;
        height: 100vh;
        background-color: #1C2333;
        color: white;
        border-radius: 10px;
        border: 1px solid white;
    }}

    body {{
        background-color: #1C2333;
        color: white;
        margin:0;
        padding:0;
        overflow:hidden;
    }}
</style>
<script>
    document.addEventListener("keydown", function(event) {{
        if (event.ctrlKey && event.key === "s") {{
            event.preventDefault();
            document.querySelector('input[type="submit"]').click();
        }}
    }});
</script>
</head>
<body>
<form method="POST" action="/config">
    <textarea name="Config">{config}</textarea><br>
    <input type="submit" value="Save" hidden>
</form>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
