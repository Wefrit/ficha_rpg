from flask import Flask, render_template, request, redirect, url_for
from ficha import Player

app = Flask(__name__)
player = None

# Página inicial: login ou ficha do jogador
@app.route("/", methods=["GET", "POST"])
def index():
    global player
    if request.method == "POST":
        # Se estiver logando
        if "name" in request.form:
            name = request.form.get("name")
            if name:
                player = Player.load(name)
                return redirect(url_for("index"))

        # Se estiver fazendo uma ação
        action = request.form.get("action")
        if player and action:
            if action == "damage":
                player.take_damage()
            elif action == "heal":
                player.heal()
            elif action == "use_mana":
                player.mana_use()
            elif action == "recover_mana":
                player.mana_recover()
            elif action == "gain_xp":
                xp_amount = request.form.get("xp_amount", 0)
                try:
                    player.gain_xp(int(xp_amount))
                except ValueError:
                    pass
            player.save()
            return redirect(url_for("index"))

    return render_template("index.html", player=player)

# Ações do jogador
@app.route("/damage", methods=["POST"])
def damage():
    player.take_damage(1)
    player.save()
    return redirect(url_for("index"))

@app.route("/heal", methods=["POST"])
def heal():
    player.heal(1)
    player.save()
    return redirect(url_for("index"))

@app.route("/use_mana", methods=["POST"])
def use_mana():
    player.mana_use(1)
    player.save()
    return redirect(url_for("index"))

@app.route("/recover_mana", methods=["POST"])
def recover_mana():
    player.mana_recover(1)
    player.save()
    return redirect(url_for("index"))

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
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
