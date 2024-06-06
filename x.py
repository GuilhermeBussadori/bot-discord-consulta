import disnake
import aiosqlite
import pandas as pd
from disnake.ext import commands

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned, intents=disnake.Intents.default())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

async def buscar_por_nome(nome: str):
    async with aiosqlite.connect('brasil.db') as db:
        query = f"SELECT * FROM pessoas WHERE LOWER(`Nome Completo`) LIKE LOWER('%{nome}%')"
        async with db.execute(query) as cursor:
            columns = [col[0] for col in cursor.description]
            rows = await cursor.fetchall()
            df = pd.DataFrame(rows, columns=columns)
    return df

async def buscar_por_cpf(cpf: str):
    async with aiosqlite.connect('brasil.db') as db:
        query = f"SELECT * FROM pessoas WHERE `CPF` = '{cpf}'"
        async with db.execute(query) as cursor:
            columns = [col[0] for col in cursor.description]  # Obtém os nomes das colunas
            rows = await cursor.fetchall()  # Obtém todas as linhas da consulta
            df = pd.DataFrame(rows, columns=columns)  # Cria o DataFrame com os resultados
    return df

bot = MyBot()

@bot.slash_command(name='buscar_nome', description='Busca por nome no banco de dados.')
async def buscar_nome(
    interaction: disnake.ApplicationCommandInteraction,
    nome: str = disnake.Option("nome", description="Nome completo da pessoa")  # Corrigido aqui
):
    await interaction.response.defer(ephemeral=True)
    df = await buscar_por_nome(nome)
    if df.empty:
        await interaction.edit_original_response('Nenhum registro encontrado.')
    else:
        await interaction.edit_original_response(f'```{df.to_string(index=False)}```')


@bot.slash_command(name='buscar_cpf', description='Busca por CPF no banco de dados.')
async def buscar_cpf(interaction: disnake.ApplicationCommandInteraction, cpf: str = disnake.Option("cpf", description="CPF da pessoa")):
    await interaction.response.defer(ephemeral=True)
    df = await buscar_por_cpf(cpf)
    if df.empty:
        await interaction.edit_original_response('Nenhum registro encontrado.')
    else:
        await interaction.edit_original_response(f'```{df.to_string(index=False)}```')

bot.run('adquira o token em: discord.dev/')  