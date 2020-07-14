import discord
from discord.ext import commands, tasks
import random
import os
from itertools import cycle
from discord.utils import get
import time
import youtube_dl
import shutil
from youtubesearchpython import searchYoutube
import json

client = commands.Bot(command_prefix = '.f ')
status = cycle(['fL0p b0t aCti4ated', 'gamers are the most oppressed group', 'something funny', 'FlupBot is here',
'duckys? more like suckys', 'KingFlup? more like... dumb head', 'lane stinky', 'sleeping...', 'pee pee poo poo in a shoe shoe'])

@client.event
async def on_ready():
    print('Flupbot Activated. ')
    change_status.start()
@client.remove_command('help')

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.red()
    )

    test_e.set_author(name="FlupBot HelpLine")
    test_e.add_field(name="Current Functionality", value="VERSION 0.1", inline=False)
    test_e.add_field(name="Leave / Join", value="Will display in chat when somebody joins or leaves the server")
    test_e.add_field(name="Ping", value="type [ .f ping ] to show bot latency")
    test_e.add_field(name="Question", value="type [ .f Question (QUESTION) ] and FlupBot will give you an answer")
    test_e.add_field(name="Clear Chat", value="type [ .f clear (Amount) ] and it will clear the chat")
    test_e.add_field(name="Status Loop", value="Changes bot status every 10 seconds")
    test_e.add_field(name="Join", value="type [ .f join ] and FlupBot will join your channel")
    test_e.add_field(name="Leave", value="type [ .f leave ] and FlupBot will leave your channel")
    test_e.add_field(name="play", value="type [ .f play (URL) ] and FlupBot will play the audio of the video")
    test_e.add_field(name="skip", value="type [ .f skip ] and FlupBot will skip the audio of whatever is playing")
    test_e.add_field(name="queue", value="type [ .f queue (URL) ] and Flupbot will queue the given video ")
    test_e.add_field(name="Youtube Search", value="type [ .f YoutubeSearch or yts (NameOfVideo) (How Many Search Results) ] and it will give you the video urls ")
    test_e.add_field(name="help", value="type [ .f helpf ] give you this message ")
    test_e.add_field(name="helpsound", value="tye [ .f helpsound ] to give soundboard help ")

    await author.send(embed=test_e)

@client.command(pass_context=True)
async def helpsound(ctx):
    author = ctx.message.author

    test_s = discord.Embed(
        colour=discord.Colour.red()
    )

    test_s.set_author(name="FlupBot SoundBoard")
    test_s.add_field(name="Current Functionality", value="VERSION 0.1", inline=False)
    test_s.add_field(name="[ .f knock ]", value="Will Play Knocking Sounds")
    test_s.add_field(name="[ .f cornflakes ]", value="I love cornflakes video")
    test_s.add_field(name="[ .f tinymouth ]", value="If I had a tinymouth video")
    test_s.add_field(name="[ .f corn ]", value="I love corn, I hate wheat video")

    await author.send(embed=test_s)



# LEAVE JOIN MESSAGE

@client.event
async def on_member_join(member):
    print(f'(member) has joined the server. ')

@client.event
async def on_member_remove(member):
    print(f'(member) has left the server')

# CHECK PING

@client.command()
async def ping(ctx): 
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

# QUESTION COMMAND

@client.command(aliases=['Question', 'question', 'q','Q'])
async def quest(ctx, *, question):
    responses = ['Stop Asking, idiot', 'stop being so dumb', 'NO!', 'Confirmed, you are mega gay',
    '100%', 'I do not know', 'for someone like you, unlikely', 'why are you asking me?', 'stop being so stupid, stupid', 
    'Go to therapy', 'LEARN TO SPELL', 'Seriously?', 'nope', 'Leave the server.', 'weeb', 'beep boop? No understando made in mexico',
    'Flupbot is confuzzled, ask the question again less gay', 'I will do you one better, anime thighs or french fries?',
    'Man, I am just a robot, I have no idea how to answer that question', 'Without a doubt, that is the dumbest question I have EVER been asked.', 'Valorant, more like valorcant',
    'absolutely', 'yessir', 'you probably like wheat more than corn ya normie', '42', 'absolutely not', "that's just a straight bad question", "do you not understand? I only answer good questions",
    "maybe, but you're not cool enough", "go play fortnite", " for that question back to the 4chan wastelands for you!", "i'm a solo player", "bruh", "I'll answer but buy my onlyfans first", "I'll answer but you have to sub with twitch prime frist", "Look at this loser doesn't even have discord nitro"]

    await ctx.send(random.choice(responses))



#CLEAR CHAT

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

#connecting to voice channel

@client.command(pass_context=True)
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
        await ctx.send(f"already in {channel}")
    else:
        voice = await channel.connect()
        await ctx.send(f"gonna join {channel} now")
    
# leave voice channel
@client.command(pass_context=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left{channel}")
        await ctx.send(f"Leaving {channel} nerd")
    else:
        print("Wasn't in channel")
        await ctx.send(f"I'm not in a channel dummy")

# \\\ AUDIO PLAYING STUFF \\\
# \\\ AUDIO PLAYING STUFF \\\
# \\\ AUDIO PLAYING STUFF \\\

@client.command(pass_context=True)
async def play(ctx, url: str):


    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1 
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued songs(s)")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("song done now playing next one ya numpty")
                print(f"Songs still in queue{still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} finished ya doink"))
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return
        else:
            queues.clear()
            print("Aint no songs in there")




    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.sent("error music playing")
        return

    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
            print("no Queue folder buddy boy")


    await ctx.send("gettin' frickin song ya NUMPTY")

    voice = get(client.voice_clients, guild=ctx.guild)
    
    ydl_opts = {
        'format': 'bestaudio/beat',
        'postprocessors':[{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality':'192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download({url})


    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"renamed file: {file}")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 5)
    await ctx.send(f"Here's ya damn song dummy: {nname}")


@client.command(pass_context=True)
async def skip(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    queues.clear()
    
    if voice and voice.is_playing():
        print("Music Stopping")
        voice.stop()
        await ctx.send("Stopping the beats to relax / study to (if you a nerd)")
    else:
        print("Aint no music playing")
        await ctx.send("Ain't no music playin' ya'll")

queues = []

@client.command(pass_context=True)
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues.append(q_num)

        queue_path = os.path.abspath(os.path.realpath("Queue") + f"song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/beat',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors':[{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality':'192',
        }],
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download({url})
    await ctx.send("adding the damn song to the friggin' queue")

    print("son added to queue")


@client.command()
async def YoutubeSearch(ctx, search_term: str, r_num: int):
    
    
    search = searchYoutube(search_term, offset = 1, mode = "json", max_results = r_num - 1)
    search_result = search.result()
    data = json.loads(search_result)


    for item in data['search_result']:
        await ctx.send(item['link'])
        print(item['link'])


# \\\ SOUNDBOARD STUFF \\\\\\ LEAVE ALONE YOU FRIGGIN LOSER MAn
# \\\ SOUNDBOARD STUFF \\\\\\ LEAVE ALONE YOU FRIGGIN LOSER MAn
# \\\ SOUNDBOARD STUFF \\\\\\ LEAVE ALONE YOU FRIGGIN LOSER MAn


@client.command()
async def knock(ctx):

    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
        voice.play(discord.FFmpegPCMAudio("./sound/corn.mp3"))
    else:
        voice = await channel.connect()
        voice.play(discord.FFmpegPCMAudio("./sound/knock.mp3"))

@client.command()
async def cornflakes(ctx):

    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
        voice.play(discord.FFmpegPCMAudio("./sound/cornflakes.mp3"))
    else:
        voice = await channel.connect()
        voice.play(discord.FFmpegPCMAudio("./sound/cornflakes.mp3"))

@client.command()
async def tinymouth(ctx):

    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
        voice.play(discord.FFmpegPCMAudio("./sound/tinymouth.mp3"))
    else:
        voice = await channel.connect()
        voice.play(discord.FFmpegPCMAudio("./sound/tinymouth.mp3"))

@client.command()
async def corn(ctx):

    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
        voice.play(discord.FFmpegPCMAudio("./sound/corn.mp3"))
    else:
        voice = await channel.connect()
        voice.play(discord.FFmpegPCMAudio("./sound/corn.mp3"))


@client.command()
async def bull(ctx):

    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
        voice.play(discord.FFmpegPCMAudio("./sound/bull.mp3"))
    else:
        voice = await channel.connect()
        voice.play(discord.FFmpegPCMAudio("./sound/bull.mp3"))

@client.command()
async def fyou(ctx, loop: bool):

    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
        voice.play(discord.FFmpegPCMAudio("./sound/fyou.mp3"))
    else:
        voice = await channel.connect()
        voice.play(discord.FFmpegPCMAudio("./sound/fyou.mp3"))

    







   





client.run('')
