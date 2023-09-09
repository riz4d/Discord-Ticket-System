import discord
from discord.ext import commands
from config import server_id,user_category_id,discord_bot_token
from intents import intents

intents.message_content = True
bot = commands.Bot(command_prefix="/",intents=intents)
@bot.event
async def on_ready():
    try:
            server = bot.get_guild(server_id)
            if server:
                category = discord.utils.get(server.categories, name="server")
                send_to_channel = discord.utils.get(category.text_channels, name="server-logs")
                await send_to_channel.send("Bot is online in cloud-server")
    except:
            pass


@bot.event
async def on_message(message):
    
    print(bot.user.id)
    userchannelid =str(message.author.id)
    if message.author.id == bot.user.id:
        return
    try:
        
        category_name = "userchat"
        channel_name = message.channel.name
        if (
            message.channel.category and
            message.channel.category.name == category_name
        ):
            try:
                
                user_id = int(channel_name)
                user = await bot.fetch_user(user_id)
                print(user)
                await user.send(message.content)
        
                print(f"Message sent to user {user.name}#{user.discriminator}.")
            except ValueError:
                print("Invalid user ID.")
            except discord.NotFound:
                print("User not found or user is not a member of a shared server.")

            
        await bot.process_commands(message)
    except Exception as e:
        print("error " + str(e))
    try:
        if isinstance(message.channel, discord.DMChannel):
            server = bot.get_guild(server_id)
            if server:
                category = discord.utils.get(server.categories, name=category_name)
                if category:
                    channel_names = [channel.name for channel in category.channels if isinstance(channel, discord.TextChannel)]
                    print(channel_names)
                    if userchannelid in channel_names:
                        send_to_channel = discord.utils.get(category.text_channels, name=userchannelid)
                        await send_to_channel.send(message.content)
                    else:
                        await category.create_text_channel(userchannelid)
                        send_to_channel = discord.utils.get(category.text_channels, name=userchannelid)
                        await send_to_channel.send(message.content)
    except Exception as x:
        try:
            server = bot.get_guild(server_id)
            if server:
                category = discord.utils.get(server.categories, name="staff-channel")
                send_to_channel = discord.utils.get(category.text_channels, name="server-logs")
                await send_to_channel.send(x)
        except:
            pass
        print(x)
        pass           
                        
bot.run()
