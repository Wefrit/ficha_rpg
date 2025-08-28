from flask import Flask, render_template, request, redirect, url_for
from ficha import Player

app = Flask(__name__)
player = None

# Página de login
@app.route("/", methods=["GET", "POST"])
def index():
    global player
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            player = Player.load(name)
            return redirect(url_for("dashboard"))
    return render_template("index.html", player=player)

# Dashboard do jogador
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    global player
    if request.method == "POST":
        action = request.form.get("action")
        if action == "damage":
            player.take_damage()
        elif action == "heal":
            player.heal()
        elif action == "use_mana":
            player.mana_use()
        elif action == "recover_mana":
            player.mana_recover()
        elif action == "gain_xp":
            amount = int(request.form.get("xp_amount", 0))
            player.gain_xp(amount)
        player.save()  # salva no SQLite
    return render_template("index.html", player=player)


# Ações do jogador
@app.route("/damage", methods=["POST"])
def damage():
    player.take_damage(1)
    player.save()
    return redirect(url_for("dashboard"))

@app.route("/heal", methods=["POST"])
def heal():
    player.heal(1)
    player.save()
    return redirect(url_for("dashboard"))

@app.route("/use_mana", methods=["POST"])
def use_mana():
    player.mana_use(1)
    player.save()
    return redirect(url_for("dashboard"))

@app.route("/recover_mana", methods=["POST"])
def recover_mana():
    player.mana_recover(1)
    player.save()
    return redirect(url_for("dashboard"))

@app.route("/gain_xp", methods=["POST"])
def gain_xp():
    amount = request.form.get("xp_amount")
    if amount:
        try:
            amount = int(amount)
            player.gain_xp(amount)
            player.save()
        except ValueError:
            pass
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
