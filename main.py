from discord import client, embeds, guild
import discord
from discord.ext import commands
import googletrans
import praw
import random
from discord.utils import get

bot = commands.Bot(command_prefix="$", case_insensitive=True)
bot.remove_command('help')
DISCORD_TOKEN = "ODYyMzYzMjI5OTA4MTA3Mjc0.YOXQVw.dQ8V9iguw3fe05VrDCkn3PZc9ek"
reddit = praw.Reddit(client_id = "BtRbN9gb3F2Zqg",
                    client_secret = "PsT8pY7vv9oonu2dgJuBVpizaC7LmQ",
                    username = "ahoyden",
                    password = "CQX7577t#^*y55SDxG!",
                    user_agent = "pythonpraw",
                    check_for_async=False)

help_embed = discord.Embed(title = "List Of Commands")
help_embed.add_field(name = "Rules", value = "Sends server rules.")
help_embed.add_field(name = "Translate", value = "Usage: $Translate (LANGUAGE) (What you want to translate)")
help_embed.add_field(name = "Dog", value = "Sends random picture of dog.")
help_embed.add_field(name = "Cat", value = "Sends random picture of cat.")
help_embed.add_field(name = "Kangaroo", value = "Sends random reddit post involving a kangaroo in some way.")
help_embed.add_field(name = "Hello", value = "Says Hello!")




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
@bot.command()
async def about(ctx):
    embed = discord.Embed(title = "About The Bot!", description = "Custom coded bot for the Squad Brocolli Server.")
    embed.add_field(name = "Created By Dom.#5539", value="[Add Me To your Server](https://discord.com/api/oauth2/authorize?client_id=862363229908107274&permissions=8&scope=bot)")
    await ctx.channel.send(embed = embed)

@bot.command()
async def help(ctx):
    await ctx.send(embed = help_embed)

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