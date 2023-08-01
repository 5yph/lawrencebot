import discord
import db
from discord.ext import commands
import q_generator as questions
import askreddit

# set intents and commands
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

asking = False # is the bot asking a question and waiting for response?

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

    # start up reddit session
    global reddit
    reddit = await askreddit.authenticate()

@bot.command()
async def ask(ctx):
    global asking

    if not asking:
        asking = True

        # keep asking until reply given
        while True:
            # ask question
            print('Getting question...')
            q, cat, time = await questions.get_question(reddit, 'askreddit') # set to askreddit for now
            print('Got question, sending...')
            await ctx.send("Category: " + cat)
            await ctx.send("Time posted: " + time)      
            await ctx.send(q)    
        
            # wait for reply
            # user needs to end their answer with a '$' to be considered a reply
            # or the user can simply skip it
            def check(m):
                msg = m.content
                return msg[-1] == '$' or msg == '!skip'
            
            msg = await bot.wait_for('message', check=check)
            
            if msg.content == '!skip':
                await ctx.send('Getting new question...')
                # ask another question (restarts loop)
            else:
                await ctx.send('Reply received: {}'.format(msg.content[:-1]))
                
                # store answer
                answer = msg.content[:-1]
                
                try: 
                    db.send_to_database(q, answer, cat)
                    await ctx.send('Answer successfully stored in database!')
                except:
                    await ctx.send('Failed to store answer in database!')
                
                # end question asking
                asking = False
                break

@bot.command()
async def shutdown(ctx):
    await ctx.send('Shutting down bot...')
    await reddit.close()
    await bot.close()
    print("Successfully closed, exiting...")

f = open('TOKEN.txt', 'r')
token = f.read()
f.close()

bot.run(token)