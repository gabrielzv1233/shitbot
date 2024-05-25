from flask import Flask, request, redirect, url_for
import shelve
import time
import os

FLAG_FILE = "restart_flag.txt"

app = Flask(__name__)

def get_config():
    db = shelve.open("databases/settings/config")
    if not "configkey" in db.keys:
        data = {
    "allowed_purge_roles": [""],
    "purge_aliases": ["clear", "cls"],
    "watching_status": "you",
"roasts": """{person_to_roast}, If I had a dollar for every brain cell you have, I'd have one dollar.
{person_to_roast}, Roses are red, violets are blue, I was looking for a joke, and then I found you.
{person_to_roast}, you're as useless as a screen door on a submarine.
Hey {person_to_roast}, I'm not saying you're ugly, but if you were a scarecrow, the birds would be laughing at you.
Roses are red, violets are blue, I'm sorry {person_to_roast}, but your IQ is lower than my shoe.
You should kill yourself {person_to_roast}
Hey {person_to_roast}, are you a magician? Because it seems like you made your dad disappear
{person_to_roast} If you were any more inbred, you'd be a sandwich.
{person_to_roast} You have the personality of a wet mop.
{person_to_roast} You're the reason why aliens won't talk to us.
{person_to_roast} Are you a parking ticket? Because you've got "fine" written all over you... and also, everyone hates you.
{person_to_roast} I'd call you a tool, but that implies you're useful in some way.
{person_to_roast} I'm jealous of all the people who haven't met you.
{person_to_roast} Roses are red, violets are blue, God made us beautiful, what happened to you?
{person_to_roast} You're the human equivalent of a participation trophy.
{person_to_roast} I bet your brain feels as good as new, seeing that you never use it.
{person_to_roast} If you were any more irrelevant, you'd be a white crayon.
{person_to_roast} I'd say you're dumb as a rock, but that would be an insult to rocks.
{person_to_roast} You're proof that evolution can go in reverse.
{person_to_roast} If ignorance is bliss, you must be the happiest person on Earth.
{person_to_roast} If stupidity was a crime, you'd be serving multiple life sentences.
{person_to_roast} I've met door knobs with more personality than you.
{person_to_roast} Did you fall from heaven? Because it looks like you landed on your face.
{person_to_roast} Even the Bermuda Triangle wouldn't swallow your ego.
{person_to_roast} I'd say you're a waste of oxygen, but I'm worried you'd take that as a compliment.
{person_to_roast} Is your personality a result of being dropped on your head as a child, or is it natural talent?
{person_to_roast} You're like a broken pencil - pointless.
{person_to_roast} Even an expired carton of milk has more potential than you.
{person_to_roast} Everyone who has ever loved you was wrong.
{person_to_roast} your mother's a whore.
{person_to_roast} your dad left you.
{person_to_roast} You are the best argument for post-term abortion.
{person_to_roast} I would explain it to you but I don't have the time or crayons.
{person_to_roast} Your birth certificate is an apology letter from the condom factory.
{person_to_roast} Everyone has the right to be stupid, but you're just abusing the privilege.
{person_to_roast} In any given situation, you are either correct or stupid. You are yet to be correct.
{person_to_roast} I'd call you a cunt, but you lack the warmth and depth.
{person_to_roast} Why don't you slip into something more comfortable, like a coma.
{person_to_roast} is a fucking pleb.
{person_to_roast} I'd call you an asshole but they serve a purpose.
{person_to_roast} I wish you were retarded. Then you'd have a valid excuse for your incompetence.
I may be drunk, {person_to_roast}, but in the morning I will be sober and you will still be ugly.
{person_to_roast} is a fuckstick"""
        }
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
