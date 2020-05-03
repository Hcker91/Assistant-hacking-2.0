import json

# on importe le module discord.py
import discord

from discord.utils import get

from discord.ext.commands import has_permissions

# ajouter un composant de discord.py
from discord.ext import commands


"""
 command_prefix="!/"
    - !/regles affiche les règles du serveur Discord
    - !/amm affiche l'heure de maintenançe de mise à jour
    - !/help affiche l'ensemble des commandes
    - !/hello affiche Bonjour si la personne est toute seule sur le serveur
    - !/bienvenue affiche bienvenue et la demande de l'execution de la commande regles
    - !/pr affiche la présentation du site
"""
# créer le bot
bot = commands.Bot(command_prefix='!/')
warnings = {}


with open('warnings.json', 'r') as outfile:
    warnings = json.load(outfile)

print(warnings)

# détecter quand le bot est pret
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game("Le serveur est en maintenance..."))

    print("Bot en ligne, pret et en cours d'execution...")

# detecter quand quelqun ajoute un emoji sur un message
@bot.event
async def on_raw_reaction_add(payload):

    #recuperer l'emoji
    emoji = payload.emoji.name
    # recupere le canal dans lequel la personne a mis sa réaction
    canal = payload.channel_id
    # recupere le numéro du message
    message = payload.message_id
    roles = bot.get_guild(payload.guild_id).roles
    # Role eleves basiques
    html_basic_role = get(roles, name="html/css eleve basique")
    js_basic_role = get(roles, name="javascript eleve basique")
    python_basic_role = get(roles, name="python eleve basique")

    membre = bot.get_guild(payload.guild_id).get_member(payload.user_id)

    print(membre)

    # verifier que l'emoji ajouté est Python
    if canal == 706154283061477469 and message == 706165093678710885 and emoji == "Python":
        print("Python = Grade ajouté!")
        await membre.add_roles(python_basic_role)
        await membre.send("Tu obtiens le grade Python eleve basique")





    # verifier que l'emoji ajouté est JAVASCRIPT
    if canal == 706154283061477469 and message == 706165195231330335 and emoji == "JAVASCRIPT":
        print("Javascript = Grade ajouté!")
        await membre.add_roles(js_basic_role)
        await membre.send("Tu obtiens le grade Javascript eleve basique")





    # verifier que l'emoji ajouté est HTML
    if canal == 706154283061477469 and message == 706164964095688844 and emoji == "HTML":
        print("Html/Css = Grade ajouté!")
        await membre.add_roles(html_basic_role)
        await membre.send("Tu obtiens le grade html/css eleve basique")






@bot.event
async def on_raw_reaction_remove(payload):

    #recuperer l'emoji
    emoji = payload.emoji.name
    # recupere le canal dans lequel la personne a mis sa réaction
    canal = payload.channel_id
    #recupere le numéro  du message
    message = payload.message_id
    roles = bot.get_guild(payload.guild_id).roles
    # Role eleves basiques
    html_basic_role = get(roles, name="html/css eleve basique")
    js_basic_role = get(roles, name="javascript eleve basique")
    python_basic_role = get(roles, name="python eleve basique")
    membre = bot.get_guild(payload.guild_id).get_member(payload.user_id)

    print(membre)
    # verifier que l'emoji ajouté est Python
    if canal == 706154283061477469 and message == 706165093678710885 and emoji == "Python":
        print("Python = Grade supprimé!")
        await membre.remove_roles(python_basic_role)
        await membre.send("Tu perds le grade python eleve basique")

    # verifier que l'emoji ajouté est JAVASCRIPT
    if canal == 706154283061477469 and message == 706165195231330335 and emoji == "JAVASCRIPT":
        print("Javascript = Grade supprimé!")
        await membre.remove_roles(js_basic_role)
        await membre.send("Tu perds le grade javascript eleve basique")

    # verifier que l'emoji ajouté est HTML
    if canal == 706154283061477469 and message == 706164964095688844 and emoji == "HTML":
        print("Html/Css = Grade supprimé!")
        await membre.remove_roles(html_basic_role)
        await membre.send("Tu perds le grade html/css eleve basique")

# créer la commande !regles
@bot.command()
async def regles(ctx):
    await ctx.send("Les regles: \n1. Pas d'insultes \n2. Pas de double compte \n3. Pas de spams sauf dans l'onglet #pub")

# créer la commande warning
@bot.command()
@commands.has_role("Bot by Aydan et Éditeur de bot et Administrateur supreme et Professeur")
async def warning(ctx, membre: discord.Member):
    pseudo = membre.mention
    id = membre.id

    print(warnings)

    # si la personne n'a pas de warnings
    if id not in warnings:
        warnings[id] = 0
        print(f"Le membre {pseudo} ne possède aucun avertissement")

    warnings[id] += 1
    print(f"Avertissement ajouter au membre {pseudo}", warnings[id], "/3")

    # verifier le nombre d'avertissements
    if warnings[id] == 3:
        # remets les warnings à 0
        warnings[id] = 0
        # message
        await membre.send("Vous avez été banni du serveur pour cause d'avertissement trop nombreux !")
        # ejecter la personne
        await membre.kick()

    # mettre à jour le fichier json
    with open('warnings.json', 'w') as outfile:
        json.dump(warnings, outfile)

    await ctx.send(f"Le membre {pseudo} a reçu une alerte ! Attention à bien respecter les règles !!!")


# verifier l'erreur
@warning.error
async def on_command_error(ctx, error):
    # detecter cette erreur
    if isinstance(error, commands.MissingRequiredArgument):
        # envoyer un message
        await ctx.send("Tu dois faire la commande !/warning @lepseudo")

@bot.command()
async def hello(ctx):
    await ctx.send("Bonjour et bienvenue ! Si tu as tapé cette commande c'est qu'il n'y a personne sur le serveur ! \nVu qu'il n'y a personne je te propose 2 choses: \n-sois tu pars et tu reviens plus tard \n-sois tu apprends les cours !!!")

@bot.command()
async def pr(ctx):
    await ctx.send("Bonjour à toute la communauté ce soir présentation de la version 2.1 du serveur Discord Cours Hacking 2.0.")
# créer la commande !/amm
@bot.command()
async def amm(ctx):
    await ctx.send("Le serveur est en maintenance...")

# créer la commande !/bienvenue
@bot.command()
async def bienvenue(ctx, member: discord.Member):

    #recupere le nom
    pseudo = member.mention

    # executer le message de bienvenue
    await ctx.send(f"Souhaitons la bienvenue à {pseudo} sur le serveur discord ! N'oublie pas de: \n-te rendre sur le site du serveur \n-checker la liste des commandes pour communiquer avec l'Assistant Hacking 2.0 \n-taper !/regles pour connaitre les regles de ce serveur")

# verifier l'erreur
@bienvenue.error
async def on_command_error(ctx, error):
    # detecter cette erreur
    if isinstance(error, commands.MissingRequiredArgument):
        # envoyer un message
        await ctx.send("La commande n'est pas valide |!Warning| vérifier la liste des commandes \nPetit +: VERIFIER EN PARTICULIER la commade !/bienvenue |Warning|")


# donner le jeton pour qu'il se connecte
jeton = "NzA1ODMwNDg4NTUxNzE5MDc0.XqxaTg.eQYN_DhbiRMEcbdEpaTJqrETIYw"

# phrase
print("Lançement du bot...")


































































# connecter au serveur
bot.run(jeton)

