from discord import client, embeds, guild
import discord
from discord.ext import commands
import googletrans
import praw
import random
from discord.utils import get
import os
from dotenv import load_dotenv
import whois

load_dotenv()
bot = commands.Bot(command_prefix="$", case_insensitive=True)
bot.remove_command('help')
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
reddit = praw.Reddit(client_id = "BtRbN9gb3F2Zqg",
                    client_secret = "PsT8pY7vv9oonu2dgJuBVpizaC7LmQ",
                    username = "ahoyden",
                    password = "CQX7577t#^*y55SDxG!",
                    user_agent = "pythonpraw",
                    check_for_async=False)

help_embed = discord.Embed(title = "List Of Commands", inline = True)
help_embed.add_field(name = "Rules", value = "Sends server rules.")
help_embed.add_field(name = "Translate", value = "Usage: $Translate (LANGUAGE) (What you want to translate)")
help_embed.add_field(name = "Dog", value = "Sends random picture of dog.")
help_embed.add_field(name = "Cat", value = "Sends random picture of cat.")
help_embed.add_field(name = "Meme", value = "Sends random meme.")
help_embed.add_field(name = "Kangaroo", value = "Sends random reddit post involving a kangaroo in some way.")
help_embed.add_field(name = "Hello", value = "Says Hello!")
help_embed.add_field(name = "Impersonate", value = "Makes the bot impersonate a user of your choice. \n Usage: $impersonate <@user> <messsage>")
help_embed.add_field(name = "Summon", value = "Summons the man himself...")
help_embed.add_field(name = "Eval", value = "A calculator. \n Usage: <operation> <number 1> <number 2>")
help_embed.add_field(name = "WhoisLookup", value = "Performs a whois lookup of a specified URL.")




# Commands
@bot.command()
async def hello(ctx):
    await ctx.send("Hello" + ctx.author.mention + "!")

@bot.command()
async def rules(ctx):
    with open('rules.txt', 'r', encoding='utf-8') as f:
        rules = f.read()
        await ctx.send(rules)

@bot.command(aliases=['tr'])
async def translate(ctx, lang_to, *args):
    lang_to = lang_to.lower()
    if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
        raise commands.BadArgument("Invalid language to translate to")
    text = ' '.join(args)
    translator = googletrans.Translator()
    text_translated = translator.translate(text, dest=lang_to).text
    await ctx.send(text_translated)    

@bot.command(pass_context=True, aliases=['dogpic', 'dogpics', 'dog'])
@commands.cooldown(1,10,commands.BucketType.user)
async def dogs(ctx):
    subreddit = reddit.subreddit("dogpictures")
    all_subs = []
    top = subreddit.top(limit = 50)

    for submission in top:
        all_subs.append(submission)

    random_post = random.choice(all_subs)

    name = random_post.title
    url = random_post.url
    upvotes = random_post.score
    
    dog_embed = discord.Embed(title = name)
    dog_embed.set_image(url = url)
    dog_embed.set_footer(text = f'r/{subreddit} 👍{upvotes}')
    
    await ctx.send(embed = dog_embed)

@bot.command(pass_context=True, aliases=['catpic', 'catpics', 'cat'])
@commands.cooldown(1,10,commands.BucketType.user)
async def cats(ctx):
    subreddit = reddit.subreddit("catpictures")
    all_subs = []
    top = subreddit.top(limit = 50)

    for submission in top:
        all_subs.append(submission)

    random_post = random.choice(all_subs)

    name = random_post.title
    url = random_post.url
    upvotes = random_post.score

    dog_embed = discord.Embed(title = name)
    dog_embed.set_image(url = url)
    dog_embed.set_footer(text = f'r/{subreddit} 👍{upvotes}')
    await ctx.send(embed = dog_embed)

@bot.command(pass_context=True)
@commands.cooldown(1,10,commands.BucketType.user)
async def kangaroo(ctx):
    subreddit = reddit.subreddit("kangaroo")
    all_subs = []
    top = subreddit.top(limit = 50)

    for submission in top:
        all_subs.append(submission)

    random_post = random.choice(all_subs)

    name = random_post.title
    url = random_post.url
    text = random_post.selftext
    upvotes = random_post.score
    subreddit = random_post.subreddit

    kangaroo_embed = discord.Embed(title = name )
    if text != "":
        kangaroo_embed.add_field(name = text, value = "‎")
    kangaroo_embed.add_field(name = url, value = "‎")
    kangaroo_embed.set_footer(text = f'r/{subreddit} 👍{upvotes}')
    await ctx.send(embed = kangaroo_embed)

@bot.command(pass_context=True, aliases=['memes'])
@commands.cooldown(1,10,commands.BucketType.user)
async def meme(ctx):
    subreddit = reddit.subreddit("memes")
    all_subs = []
    top = subreddit.top(limit = 50)

    for submission in top:
        all_subs.append(submission)

    random_post = random.choice(all_subs)

    name = random_post.title
    url = random_post.url
    text = random_post.selftext
    upvotes = random_post.score
    subreddit = random_post.subreddit

    meme_embed = discord.Embed(title = name)
    meme_embed.set_image(url = url)
    meme_embed.set_footer(text = f'r/{subreddit} 👍{upvotes}')

    await ctx.send(embed = meme_embed)

@bot.command()
async def about(ctx):
    embed = discord.Embed(title = "About The Bot!", description = "Custom coded bot for the Squad Brocolli Server.")
    embed.add_field(name = "Created By Dom.#5539", value="[Add Me To your Server](https://discord.com/api/oauth2/authorize?client_id=862363229908107274&permissions=8&scope=bot)")
    await ctx.channel.send(embed = embed)

@bot.command()
async def help(ctx):
    await ctx.send(embed = help_embed)

@bot.command(name='avatar')
async def dp(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    userAvatar = member.avatar_url
    await ctx.send(userAvatar)

@bot.command()
async def impersonate(ctx, member: discord.Member, *, message=None):

        webhook = await ctx.channel.create_webhook(name=member.name)
        await webhook.send(
            str(message), username=member.name, avatar_url=member.avatar_url)

        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
                await webhook.delete()

@bot.command()
async def summon(ctx):
    webhook = await ctx.channel.create_webhook(name="God")
    await webhook.send("Hello mighty human!", avatar_url='https://i.swncdn.com/media/800w/cms/CCOM/61039-jesus-resurrection-light.1200w.tn.jpg')

@bot.command()
async def eval(ctx, operation, firstnumber, secondnumber):
    if operation == '+':
        answer = int(firstnumber) + int(secondnumber)
        await ctx.send(answer)
    if operation == '-':
        answer = int(firstnumber) - int(secondnumber)
        await ctx.send(answer)
    if operation == 'x':
        answer = int(firstnumber) * int(secondnumber)
        await ctx.send(answer)
    if operation == '/':
        answer = int(firstnumber) / int(secondnumber)
        await ctx.send(answer)
    else:
        await ctx.send("Correct operations are: '+', '-', 'x' and '/'!")

@bot.command()
async def whoislookup(ctx, domainname):
    domain = whois.whois(str(domainname))
    await ctx.send(domain['org'])
    await ctx.send("registrar: " + domain['registrar'])
    await ctx.send("creation date: " + str(domain.creation_date[0]))
    await ctx.send("name server: ")
    for i in domain.name_servers:
        await ctx.send(str(i))
    await ctx.send("emails: ")
    for i in domain.emails:
        await ctx.send(str(i))
    

# Moderation Commands

@bot.command(aliases=['b'])
@commands.cooldown(1,10,commands.BucketType.user)
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason= "No reason provided!"):
    await member.send("You have been banned from a server, because: "+reason)
    await member.ban(reason=reason)

@bot.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
@commands.cooldown(1,10,commands.BucketType.user)
async def kick(ctx,member : discord.Member,*,reason= "No reason provided!"):
    await member.kick(reason = reason)
    await member.send("You have been kicked from a server, because: "+reason)

@bot.command()
async def shutdown(ctx):
    if ctx.author.id == 696119919116288100:
        await ctx.send("Bot is successfully shutting down...")
        await bot.close()
    else:
        await ctx.send("You do not have the correct permissions!")
# Events
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)

@bot.event
async def on_member_join(member):
    # role = get(member.guild.roles, name="ROLE")
    await member.add_roles(833700460975489085)

# Executes the bot with the specified token. Token has been removed and used just as an example.
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name=f"$help | {len(bot.guilds)} servers", url=""))
    print("Bot is ready!")
bot.run(DISCORD_TOKEN)