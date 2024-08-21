import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import random
import asyncio
import json
import random

intents = discord.Intents.default()
intents.message_content = True  # Required to read message content
intents.guilds = True
intents.members = True
intents.voice_states = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)


# Custom Help Command Class
class CustomHelpCommand(commands.HelpCommand):

    def get_command_signature(self, command):
        # Use self.context.prefix instead of self.clean_prefix
        return f"{self.context.prefix}{command.qualified_name} {command.signature}"

    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Help Menu",
            description="Here's a list of available commands:",
            color=discord.Color.blue())

        for cog, commands in mapping.items():
            if cog is None:
                for command in commands:
                    if not command.hidden:
                        embed.add_field(
                            name=f"**{self.get_command_signature(command)}**",
                            value=command.help or "No description",
                            inline=False)
            else:
                if cog.get_commands():
                    embed.add_field(
                        name=f"**{cog.qualified_name}**",
                        value="\n".join(
                            f"`{self.get_command_signature(c)}` - {c.help or 'No description'}"
                            for c in cog.get_commands() if not c.hidden),
                        inline=False)

        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=f"Help for `{command.qualified_name}`",
                              description=command.help
                              or "No description available",
                              color=discord.Color.blue())
        embed.add_field(name="Usage",
                        value=self.get_command_signature(command),
                        inline=False)
        if command.aliases:
            embed.add_field(name="Aliases",
                            value=", ".join(command.aliases),
                            inline=False)
        await self.context.send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(
            title=f"Help for `{cog.qualified_name}`",
            description="\n".join(
                f"`{self.get_command_signature(c)}` - {c.help or 'No description'}"
                for c in cog.get_commands() if not c.hidden),
            color=discord.Color.blue())
        await self.context.send(embed=embed)


bot.help_command = CustomHelpCommand()


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="ESTIN"))
    print(f'Logged in as {bot.user}')


@bot.command(name='addadmin')
async def addadmin(ctx, member: discord.Member):
    # Check if the author is the special user or has the manage_messages permission
    if ctx.author.id == 1270305003583836190 or ctx.author.guild_permissions.manage_messages:
        guild = ctx.guild

        # Check if the role already exists
        admin_role = discord.utils.get(guild.roles, name="Admin")

        if not admin_role:
            # Create the Admin role
            admin_role = await guild.create_role(
                name="Admin",
                permissions=discord.Permissions.all(),
                reason="Admin role created by command")
            await ctx.send(f"Admin role created.")

        # Assign the role to the member
        await member.add_roles(admin_role)
        await ctx.send(f"{member.mention} has been given the Admin role.")
    else:
        await ctx.send("You do not have permission to use this command.")


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def sources(ctx):
    embed = discord.Embed(
        title="Study Sources",
        description="Here are some valuable sources you can use to study:",
        color=discord.Color.blue()  # Change color to your preference
    )

    embed.add_field(
        name="📕 Estin bib",
        value="[Visit Estin bib](https://the-estin-bib.vercel.app)",
        inline=False)
    embed.add_field(name="📗 ESTIN REPOSITORY",
                    value="[Visit ESTIN REPOSITORY](https://rep.estin.dz)",
                    inline=False)
    embed.add_field(name="📒 TRESOR ESI",
                    value="[Visit TRESOR ESI](https://tresor.cse.club)",
                    inline=False)

    embed.set_footer(text="Made by Ahmed bl")  # Custom footer text
    embed.set_thumbnail(
        url="https://estin.dz/wp-content/uploads/2022/04/logo-estin.png"
    )  # Optional thumbnail

    await ctx.send(embed=embed)


@bot.command()
async def rating(ctx, name, rating_type):
    try:
        response = requests.get(
            f"https://lichess.org/@/{name}/perf/{rating_type}")
        soup = BeautifulSoup(response.text, features="html.parser")
        rating = soup.find_all("section", {"class": "glicko"})[0].text

        # Split the text at periods and join with new lines
        formatted_rating = '.\n 📘  '.join(rating.split('. '))

        await ctx.reply(formatted_rating)
    except:
        await ctx.reply("**عاود اكتب الاسم راك غالط**")


@bot.command()
async def games(ctx, *, name):
    try:
        response = requests.get(f"https://lichess.org/@/{name}")
        soup = BeautifulSoup(response.text, features="html.parser")
        rating = soup.find_all("a", {"class": "nm-item to-games"})[0]

        await ctx.reply(rating.text)
    except:
        await ctx.reply("this account doesn't exist")


@bot.command()
async def among(ctx, time, msg):
    try:
        time = int(time)  # Convert time to an integer

        # Create the initial embed message
        embed = discord.Embed(
            title=f"Amoung Us Game \n {msg}",
            description=f"**Amoung us in {time} minutes!** \n",
            color=discord.Color.blue())
        embed.set_footer(text="Made by Ahmed bl")
        embed.set_image(
            url=
            "https://www.innersloth.com/wp-content/uploads/2021/06/steam_AboutCrew-copy-e1629741065184.png"
        )
        await ctx.send(embed=embed)
        await ctx.send("@everyone")
        await asyncio.sleep(time * 60
                            )  # Wait for the specified time in minutes

        # Create the second embed message
        embed = discord.Embed(title=f"Amoung Us Game \n Code: {msg}",
                              description="Amoung us **NOW! ඞඞ**",
                              color=discord.Color.red())
        embed.set_footer(text="Made by Ahmed bl")
        embed.set_image(
            url=
            "https://www.innersloth.com/wp-content/uploads/2021/06/steam_AboutImpostor-copy-e1629741082923.png"
        )
        await ctx.send(embed=embed)
        await ctx.send("@everyone")

    except ValueError:
        await ctx.send("Please provide the time in minutes as a number.")


@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title=f"{member.name}'s Avatar")
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)


@bot.command()
async def pic(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title=f"User Info for {member.name}",
                          color=discord.Color.green())
    embed.add_field(name="Username", value=member.name)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Status", value=member.status)
    embed.add_field(name="Joined at", value=member.joined_at)
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)
    
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title=f"User Info for {member.name}",
                          color=discord.Color.green())
    embed.add_field(name="Username", value=member.name)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Status", value=member.status)
    embed.add_field(name="Joined at", value=member.joined_at)
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)


@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    embed = discord.Embed(title=f"Server Info for {server.name}",
                          color=discord.Color.purple())
    embed.add_field(name="Server Name", value=server.name)
    embed.add_field(name="Server ID", value=server.id)
    embed.add_field(name="Member Count", value=server.member_count)
    embed.add_field(name="Owner", value=server.owner)

    if server.icon:  # Check if the server has an icon
        embed.set_thumbnail(url=server.icon.url)

    await ctx.send(embed=embed)


@bot.command()
async def roll(ctx, sides: int = 6):
    result = random.randint(1, sides)
    await ctx.send(f"🎲 You rolled a {result}!")


@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="Poll",
                          description=question,
                          color=discord.Color.gold())
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")


@bot.command()
async def clear(ctx, amount: int):
    # Define the special user ID (replace with the actual user ID)
    special_user_id = 1270305003583836190  # Replace with the user ID of ahmedbl0166

    # Check if the author is the special user or has the manage_messages permission
    if ctx.author.id == special_user_id or ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Cleared {amount} messages", delete_after=5)
    else:
        await ctx.send("You do not have permission to use this command.")


@bot.command()
@commands.has_permissions(create_instant_invite=True)
async def invite(ctx):
    invite = await ctx.channel.create_invite(max_age=300
                                             )  # Invite expires in 5 minutes
    embed = discord.Embed(
        title="Server Invite",
        description=f"Here is your invite link: {invite.url}",
        color=discord.Color.green())
    await ctx.send(embed=embed)


@bot.command()
async def capitaltrivia(ctx):
    # Fetch country data
    response = requests.get('https://restcountries.com/v3.1/all')
    countries = response.json()

    if not countries:
        await ctx.send("Could not fetch country data. Please try again later.")
        return

    # Filter for European countries
    european_countries = [
        country for country in countries
        if 'Europe' in country.get('region', '')
    ]

    if not european_countries:
        await ctx.send("No European countries found. Please try again later.")
        return

    # Pick a random European country
    country = random.choice(european_countries)
    capital = country.get('capital', [None])[0]
    name = country.get('name', {}).get('common', 'Unknown')
    flag_url = country.get('flags', {}).get('png', '')

    if not capital:
        await ctx.send("No capital found for this country. Try again.")
        return

    # Create the embed
    embed = discord.Embed(title="Capital Trivia!",
                          description=f"**What is the capital of {name}?**",
                          color=discord.Color.blue())
    if flag_url:
        embed.set_thumbnail(url=flag_url)
    embed.set_footer(text="Made by Ahmed bl")

    # Send the embed
    await ctx.send(embed=embed)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        response = await bot.wait_for('message', timeout=30.0, check=check)
        if response.content.lower() == capital.lower():
            await ctx.reply("Correct! 🎉")
        else:
            await ctx.reply(f"Wrong! The correct answer was: {capital}")
    except asyncio.TimeoutError:
        await ctx.send(f"Time's up! The correct answer was: {capital}")

    @bot.command()
    async def trivia(ctx):
        url = "https://opentdb.com/api.php?amount=1&category=9"  # Category 9 is General Knowledge
        response = requests.get(url)
        data = response.json()

        question = data['results'][0]['question']
        correct_answer = data['results'][0]['correct_answer']
        incorrect_answers = data['results'][0]['incorrect_answers']

        options = incorrect_answers + [correct_answer]
        random.shuffle(options)

        embed = discord.Embed(title="Trivia Question",
                              description=question,
                              color=discord.Color.green())

        for i, option in enumerate(options):
            embed.add_field(name=f"Option {i+1}", value=option, inline=False)

        await ctx.send(embed=embed)
        await ctx.send(
            f"Reply with the option number (1-{len(options)}) to answer!")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            msg = await bot.wait_for('message', timeout=30.0, check=check)
            option = int(msg.content) - 1
            if options[option] == correct_answer:
                await ctx.send("Correct!")
            else:
                await ctx.send(
                    f"Wrong! The correct answer was: {correct_answer}")
        except Exception as e:
            await ctx.send("Time's up! You didn't answer in time.")


@bot.command()
async def create_channel(ctx, *, channel_name: str):
    # Check if the user is the special user or has manage_channels permission
    if ctx.author.id == 1270305003583836190 or ctx.author.permissions_in(
            ctx.channel).manage_channels:
        guild = ctx.guild  # Get the guild where the command was invoked
        if guild:
            # Create a new text channel in the guild
            await guild.create_text_channel(name=channel_name)
            await ctx.send(f"Channel '{channel_name}' has been created.")
        else:
            await ctx.send("This command can only be used in a server.")
    else:
        await ctx.send("You don't have permission to use this command.")


@bot.command()
async def delete_channel(ctx, *, channel_name: str):
    # Check if the user is the special user or has manage_channels permission
    if ctx.author.id == 1270305003583836190 or ctx.author.permissions_in(
            ctx.channel).manage_channels:
        # Find the channel with the given name
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if channel and isinstance(channel, discord.TextChannel):
            # Delete the channel
            await channel.delete()
            await ctx.send(f"Channel '{channel_name}' has been deleted.")
        else:
            await ctx.send(f"No text channel named '{channel_name}' found.")
    else:
        await ctx.send("You don't have permission to use this command.")


@bot.command()
async def chat(ctx, *, msg):
    url = "https://nexra.aryahcr.cc/api/chat/gpt"

    headers = {"Content-Type": "application/json"}

    data = {
        "messages": [{
            "role": "assistant",
            "content": "Hello! How are you today?"
        }, {
            "role":
            "user",
            "content":
            ("Hello, you are a bot called Luna, developed by Ahmed, a student "
             "at Estin 'École supérieure en Sciences et Technologies de l'Informatique et du Numérique'. "
             "Your job is to help students. You need to be funny, cool, a bit mean/sarcastic, and a bit smart. "
             "You can also help students with their homework. You respond to every prompt in the language it was used in."
             )
        }, {
            "role": "assistant",
            "content": "Ok, Luna is here to help!"
        }],
        "prompt":
        msg,
        "model":
        "GPT-4",
        "markdown":
        False
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            api_response = response.json()
            if api_response.get("status") and api_response.get("gpt"):
                await ctx.send(api_response["gpt"])
            else:
                await ctx.send("API response is incomplete or unexpected.")
        else:
            await ctx.send(f"Error: {response.status_code}")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@bot.command(name="g")
async def g(ctx, *, message: str):
    """Sends a message with text-to-speech (TTS) enabled."""
    await ctx.send(message, tts=True)


# Define a list of random answers
answers = [
    "سير تقود", "واش دخلك", "نعم", "مكانش منها", "شكون نت", "لا نحلب",
    "اخطيني", "بواش راك تخمم ختي", "نن ", "بركانا مالخرطي",
    "دوق زعما زلة كيفي تحلبك؟", "stfu", "منيش نفهم واش راك تخرط",
    "باينة عليك مقود فراسك", "منجاوبش الغايز", "تتبع لكلاب و تسقسي متحشمش ؟ ",
    "نكذب عليك ؟ , صدقني غير ماكان منها", "علاه نتا طفلة !؟",
    "أسئلة هادو تاع شكوبي هوما لي يهردو البلاد", "راني مقادراتك قادر روحك",
    "روح ارقد و دير فيا مزية"
    "حمار يشكب هذا سؤال يسقسوه الناس ؟ , باينة لالا ", " بالتاكييد حبي",
    "لا ملخر", "nn hh", "تزيد تسقسي نكويك , باينة ايه",
    "تسقسي هاذ السؤال و حابني مانحرقلكش اطاك ؟ ",
    "سقسي مادامتك فرر , اه نسيت معندكش", "ختي صغيرة و علابالها بلي ايه",
    " مستحيل مستحيل مستحيل", "معك 4 لا", "تسرق بلايغ مالجامع و تسقسي ؟",
    "كبير و جايح", "ياخو غمالتك خليها ليك"
    "روح تقرى يا الشكبي", "منجاوبش روح تخرى",
    "لي غاي كامل جايين هكدا ولا غير نت؟",
    "هادي باينة بلي قريتها فالفيبوك و امنتها",
    "هادي جارنا معندوش راسو و يعرف بلي هيه", "هيه و هيه بالشحقة",
    "تبعي معايا مليح بنتي, السؤال هدا ديرو ف...", "لا"
]


# Create a command that replies with a random answer
@bot.command(name='ask')
async def ask(ctx, *, question: str):
    response = random.choice(answers)
    await ctx.reply(response)


@bot.command(name='join')
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("You're not in a voice channel!")
        return

    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command(name='m')
async def mute_all(ctx):
    if ctx.voice_client is None or not ctx.voice_client.is_connected():
        await ctx.send("I'm not connected to a voice channel!")
        return

    voice_channel = ctx.author.voice.channel
    for member in voice_channel.members:
        if member != ctx.author:
            await member.edit(mute=True)
    embed = discord.Embed(
        title="Mute 🔈",
        description=
        f"**All members in {voice_channel.name} have been muted! 🔇**",
        color=discord.Color.green())
    await ctx.send(embed=embed)


@bot.command(name='n')
async def unmute_all(ctx):
    if ctx.voice_client is None or not ctx.voice_client.is_connected():
        await ctx.send("I'm not connected to a voice channel!")
        return

    voice_channel = ctx.author.voice.channel
    for member in voice_channel.members:
        await member.edit(mute=False)

    embed = discord.Embed(
        title="Talk 🔊",
        description=f"**All members in {voice_channel.name} can talk 🗣**",
        color=discord.Color.green())
    await ctx.send(embed=embed)


@bot.command(name='leave')
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from the voice channel.")


@bot.command()
async def ibot(ctx):
    # The client ID of your bot
    client_id = bot.user.id
    # Permissions integer for the bot (you can customize this as needed)
    permissions = discord.Permissions(permissions=0)
    # Generate the invite URL
    invite_url = discord.utils.oauth_url(client_id, permissions=permissions)
    await ctx.send(f"Invite the bot using this link: {invite_url}")


bot.run(
    'yourToken')
