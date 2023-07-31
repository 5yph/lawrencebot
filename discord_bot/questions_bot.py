import discord
import q_generator as questions
import db
import json
import requests

client = discord.Client()
asking = False # is the bot asking a question and waiting for response?

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global asking

    print(asking)
    print(message.content)

    if message.author == client.user:
        return

    if message.content.startswith('!ask') and not asking:
        asking = True

        # keep asking until reply given
        while True:
            # ask question
            print('Getting question...')
            q, cat = questions.get_question()
            print('Got question, sending...')
            await message.channel.send(q)    
        
            # wait for reply
            # user needs to end their answer with a '$' to be considered a reply
            # or the user can simply skip it
            def check(m):
                msg = m.content
                return msg[-1] == '$' or msg == '!skip'
            
            msg = await client.wait_for('message', check=check)
            
            if msg.content == '!skip':
                await message.channel.send('Getting new question...')
                # ask another question (restarts loop)
            else:
                await message.channel.send('Reply received: {}'.format(msg.content[:-1]))
                
                # store answer
                answer = msg.content[:-1]
                
                try: 
                    db.send_to_database(q, answer, cat)
                    await message.channel.send('Answer successfully stored in database!')
                except:
                    await message.channel.send('Failed to store answer in database!')
                
                # end question asking
                asking = False
                break

    elif message.content == '!skip' and not asking:
        await message.channel.send('No message to skip')
    elif not asking and message.content.startswith('!'):
        await message.channel.send('Invalid command')

f = open('TOKEN.txt', 'r')
token = f.read()
f.close()

client.run(token)