import os

import aiohttp
import nextcord
from nextcord.ext import commands

bot = commands.Bot(command_prefix="$", intents=nextcord.Intents.all())


@bot.event
async def on_ready():
  print(f"{bot.user} has successfully joined the club!")


@bot.command()
async def weather(ctx: commands.Context, *, city):
  url = "http://api.weatherapi.com/v1/current.json"
  par = {"key": os.environ['WEATHER_API_KEY'], "q": city}

  async with aiohttp.ClientSession() as session, session.get(url, params=par) as res:
    data = await res.json()

    location = data["location"]["name"]
    temp_cel = data["current"]["temp_c"]
    temp_far = data["current"]["temp_f"]
    humidity = data["current"]["humidity"]
    condition = data["current"]["condition"]["text"]
    uv = data["current"]["uv"]
    image_url = "http:" + data["current"]["condition"]["icon"]

    embed = nextcord.Embed(
        title=f"{location}'s Current Weather:",
        description=f"The condition in {location} is currently {condition}",
        color=nextcord.Color.random())
    embed.add_field(name="Temperature", value=f"{temp_cel}°C | {temp_far}°F")
    embed.add_field(name="Humidity", value=f"{humidity}%")
    embed.add_field(name="UV Index", value=f"{uv}")
    embed.set_thumbnail(url=image_url)

    await ctx.send(embed=embed)
    
"""Work In Progress
@bot.command()
async def forecast(ctx: commands.Context, *, city, days):
  days = 3
  url = "http://api.weatherapi.com/v1/forecast.json"
  par = {"key": os.environ['WEATHER_API_KEY'], "q": city, "days": days}

  async with aiohttp.ClientSession() as session, session.get(url, params=par) as res:
    data = await res.json()
    
    location = data["location"]["name"]
    temp_cel_max = data["day"]["maxtemp_c"]
    temp_cel_min = data["day"]["mintemp_c"]
    temp_far_max = data["day"]["maxtemp_f"]
    temp_far_min = data["day"]["mintemp_f"]
    humidity = data["humidity"]
    image_url = "http:" + data["day"]["condition"]["icon"]

    embed = nextcord.Embed(
      title=f"{location}'s Forecasted Weather:",
      description=f"The 3 day forecast for {location} is:",
      color=nextcord.Color.random())
    embed.add_field(name="Max Temperature", value=f"{temp_cel_max}°C | {temp_far_max}°F")
    embed.add_field(name="Min Temperature", value=f"{temp_cel_min}°C | {temp_far_min}°F")
    embed.add_field(name="Humidity", value=f"{humidity}%")
    embed.set_thumbnail(url=image_url)

    await ctx.send(embed=embed)
"""

bot.run(os.environ['TOKEN'])
