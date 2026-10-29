from flask import Flask,session,url_for,render_template,request
import random
import json

app=Flask(__name__)
app.secret_key="Temporary_placeholder"

with open("pokemon.json","r") as poke_file:
    info=json.load(poke_file)
poke_dict={item['id']: item for item in info}

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/level_1", methods=['GET','POST'])
def level_1():
    if request.method == 'GET':
        session['poke1_id']=random.randint(1,151)
    poke1_id=session["poke1_id"]

    if request.method=='POST':
        guess=request.form.get("guess","")
        guess=guess.lower().strip()
        pokemon=poke_dict[poke1_id]
        if pokemon["name"]==guess:
            return render_template("reveal.html",pokemon=pokemon)
        else:
            return render_template("play_again.html",pokemon=pokemon)
        
    sprites=poke_dict[poke1_id]["sprite"]
    return render_template("level_1.html",sprite_imag=sprites)

@app.route("/level_2", methods=['GET','POST'])
def level_2 ():
    poke1_id=session["poke1_id"]
    if request.method=='GET':
        session["poke2_id"]=random.randint(1,151)
        session["stat"]=random.choice(["attack","defense","hp","special_attack","special_defense","speed"])
        poke2_id=session["poke2_id"]
        while poke2_id == poke1_id:
            session["poke2_id"]=random.randint(1,151)
            poke2_id=session["poke2_id"]
    stat=session["stat"]
    
    pokemon1=poke_dict[poke1_id]
    poke2_id=session["poke2_id"]
    pokemon2=poke_dict[poke2_id]

    if request.method=='POST':
        selection=request.form.get("select","")
        
        if pokemon1[stat]>pokemon2[stat] and selection==str(poke1_id):
            return render_template("u_win.html",pokemon1=pokemon1,pokemon2=pokemon2,stat_label=stat)
        elif pokemon2[stat]>pokemon1[stat] and selection==str(poke2_id):
            return render_template("u_win.html",pokemon1=pokemon1,pokemon2=pokemon2,stat_label=stat)
        elif pokemon2[stat]==pokemon1[stat] and (selection==str(poke1_id) or selection==str(poke2_id)):
            return render_template("u_win.html",pokemon1=pokemon1,pokemon2=pokemon2,stat_label=stat)
        else:
            return render_template("u_lose.html",pokemon1=pokemon1,pokemon2=pokemon2,stat_label=stat)

    sprite1=pokemon1["sprite"]
    sprite2=pokemon2["sprite"]
    return render_template("level_2.html",pokemon1=pokemon1,pokemon2=pokemon2,stat_label=stat,sprite1_img=sprite1,sprite2_img=sprite2)

if __name__== "__main__":
    app.run(debug=True)