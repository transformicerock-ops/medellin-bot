import discord
from discord.ext import commands
import asyncio

TOKEN = "MTQxMDczOTEwMzA5MTI2MTYyMA.GYvUH5.yWuxIwTGi8Ij2yP0psMUhxcEV7QsNu4gtneK1s"  # Substitua pelo seu token

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Ao iniciar o bot
@bot.event
async def on_ready():
    print(f"🤖 Bot logado como {bot.user}")
    try:
        if bot.user.name != "Medellin Roleplay":
            await bot.user.edit(username="Medellin Roleplay")
    except Exception as e:
        print(f"⚠️ Não foi possível mudar o nome: {e}")

# View para abrir ticket
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎟️ Abrir Ticket", style=discord.ButtonStyle.primary, custom_id="abrir_ticket")
    async def abrir_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        # Verifica se o usuário já tem ticket
        for channel in guild.channels:
            if channel.name == f"ticket-{user.name.lower()}":
                await interaction.response.send_message("⚠️ Você já possui um ticket aberto!", ephemeral=True)
                return

        # Verifica se existe a categoria "Tickets"
        categoria = discord.utils.get(guild.categories, name="Tickets")
        if not categoria:
            categoria = await guild.create_category("Tickets")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        # Cria canal do ticket
        canal = await guild.create_text_channel(
            name=f"ticket-{user.name}",
            overwrites=overwrites,
            category=categoria
        )

        # Adiciona botão para fechar ticket
        view = FecharTicketView()
        await canal.send(
            "🎬 Quer ser Streamer Oficial do Medellin?\n\n"
            "E aí, tudo certo? 🚀\n"
            "Se você manda bem nas transmissões e quer representar o Medellin Roleplay como streamer, chegou a sua chance! "
            "Para participar, basta preencher o formulário abaixo com suas informações:\n\n"
            "✨ Nome do seu personagem\n"
            "✨ Plataformas onde você faz stream\n"
            "✨ Links dos seus perfis\n\n"
            "⚠️ Ao preencher o formulário, você garante que todas as informações são reais e corretas. "
            "Isso é essencial para que a nossa equipe possa avaliar você da melhor forma.\n\n"
            "Depois de enviar, é só aguardar a análise.\n"
            "✨ Boa sorte e nos vemos em Medellin! 🌆",
            view=view
        )

        await interaction.response.send_message(f"✅ Seu ticket foi criado em {canal.mention}", ephemeral=True)

# View para fechar ticket
class FecharTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Fechar Ticket", style=discord.ButtonStyle.danger, custom_id="fechar_ticket")
    async def fechar_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.channel.name.startswith("ticket-"):
            await interaction.response.send_message("⏳ Fechando ticket em 5 segundos...", ephemeral=True)
            await asyncio.sleep(5)
            await interaction.channel.delete()
        else:
            await interaction.response.send_message("⚠️ Este comando só pode ser usado dentro de um ticket.", ephemeral=True)

# Comando para enviar o painel de ticket
@bot.command()
async def ticket(ctx):
    view = TicketView()
    await ctx.send(
        "👋 Seja Bem Vindo!\n\n"
        "🎟️ Gere um ticket para realizar o cadastro e ser aprovado pela nossa equipe:",
        view=view
    )

bot.run("MTQxMDczOTEwMzA5MTI2MTYyMA.GYvUH5.yWuxIwTGi8Ij2yP0psMUhxcEV7QsNu4gtneK1s")
