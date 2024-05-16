import discord
from discord.ext import commands
import pytz
from datetime import datetime, timedelta
import os
import random
import requests
import asyncio
from bot_logic import gen_pass

description = '''An example bot to showcase the discord.ext.commands extension module. There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Membuat klien bot
bot = commands.Bot(command_prefix='>', description=description, intents=intents)

# Menambahkan perintah untuk mendapatkan waktu berdasarkan zona waktu tertentu
@bot.command()
async def waktu(ctx, zona_waktu: str):
    try:
        timezone = pytz.timezone(zona_waktu)
        waktu_sekarang = datetime.now(timezone)
        waktu_format = waktu_sekarang.strftime('%H:%M')
        await ctx.send(f"Waktu saat ini di {zona_waktu} adalah {waktu_format}")
    except pytz.UnknownTimeZoneError:
        await ctx.send("Zona waktu tidak valid. Silakan coba lagi.")

# Menambahkan perintah untuk menetapkan pengingat waktu
@bot.command()
async def ingat(ctx, waktu: str, zona_waktu: str):
    try:
        timezone = pytz.timezone(zona_waktu)
        waktu_ingat = datetime.strptime(waktu, '%H:%M')
        waktu_ingat = timezone.localize(waktu_ingat)
        # Menghitung selisih waktu untuk pengingat
        now = datetime.now(timezone)
        selisih_waktu = waktu_ingat - now
        if selisih_waktu.total_seconds() <= 0:
            # Jika waktu sudah lewat, tambahkan 1 hari ke waktu yang diminta
            waktu_ingat += timedelta(days=1)
            selisih_waktu = waktu_ingat - now
        # Mengatur pengingat
        await asyncio.sleep(selisih_waktu.total_seconds())
        await ctx.send(f"Waktu yang diingatkan! Saat ini adalah {waktu_ingat.strftime('%H:%M')} di zona waktu {zona_waktu}.")
    except ValueError:
        await ctx.send("Format waktu tidak valid. Gunakan format HH:MM (misalnya, 10:30)")

# adding two numbers
@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

# spamming word
@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)
        
# password generator        
@bot.command()
async def pw(ctx):
    await ctx.send(f'Kata sandi yang dihasilkan: {gen_pass(10)}')

# coinflip
@bot.command()
async def coinflip(ctx):
    num = random.randint(1,2)
    if num == 1:
        await ctx.send('It is Head!')
    if num == 2:
        await ctx.send('It is Tail!')

# rolling dice
@bot.command()
async def dice(ctx):
    nums = random.randint(1,6)
    if nums == 1:
        await ctx.send('It is 1!')
    elif nums == 2:
        await ctx.send('It is 2!')
    elif nums == 3:
        await ctx.send('It is 3!')
    elif nums == 4:
        await ctx.send('It is 4!')
    elif nums == 5:
        await ctx.send('It is 5!')
    elif nums == 6:
        await ctx.send('It is 6!')

# overwriting kalimat.txt
@bot.command()
async def tulis(ctx, *, my_string: str):
    with open('kalimat.txt', 'w', encoding='utf-8') as t:
        text = ""
        text += my_string
        t.write(text)

# append kalimat.txt
@bot.command()
async def tambahkan(ctx, *, my_string: str):
    with open('kalimat.txt', 'a', encoding='utf-8') as t:
        text = "\n"
        text += my_string
        t.write(text)

# reading kalimat.txt
@bot.command()
async def baca(ctx):
    with open('kalimat.txt', 'r', encoding='utf-8') as t:
        document = t.read()
        await ctx.send(document)

# random local meme image
@bot.command()
async def meme(ctx):
    img_name = random.choice(os.listdir('meme'))
    with open(f'meme/{img_name}', 'rb') as f:
    # with open(f'meme/enemies-meme.jpg', 'rb') as f:
        # Mari simpan file perpustakaan/library Discord yang dikonversi dalam variabel ini!
        picture = discord.File(f)
    await ctx.send(file=picture)

# API to get random dog and duck image 
def get_dog_image_url():
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']
@bot.command('dog')
async def dog(ctx):
    '''Setiap kali permintaan dog (anjing) dipanggil, program memanggil fungsi get_dog_image_url'''
    image_url = get_dog_image_url()
    await ctx.send(image_url)
def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']
@bot.command('duck')
async def duck(ctx):
    '''Setiap kali permintaan duck (bebek) dipanggil, program memanggil fungsi get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)
def get_cat_image_url():
    url = 'https://api.thecatapi.com/v1/images/search'
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        if data:  # Memastikan data tidak kosong
            return data[0]['url']
    return None
@bot.command('cat')
async def cat(ctx):
    '''Setiap kali permintaan Cat (Kucing) dipanggil, program memanggil fungsi get_cat_image_url'''
    image_url = get_cat_image_url()
    if image_url:
        await ctx.send(image_url)
    else:
        await ctx.send("Maaf, gagal mendapatkan gambar kucing.")
def get_memeabsurd_image_url():
    url = 'https://api.imgflip.com/get_memes'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        memes = data['data']['memes']
        meme = random.choice(memes)
        return meme['url']
    else:
        return None
@bot.command()
async def memeabsurd(ctx):
    """Sends a random absurd meme."""
    absurd_meme_url = get_memeabsurd_image_url()
    if absurd_meme_url:
        await ctx.send(absurd_meme_url)
    else:
        await ctx.send("Failed to fetch absurd meme.")

# welcome message
@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

bot.run('Token')
