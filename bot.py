import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from mapa_astral import gerar_mapa
from conexao_gemini import analisar_pergunta

#Carrega variáveis de ambiente para bot
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

#Inicializa bot e dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher()

#Handler para a inicialização do bot
@dispatcher.message(CommandStart())
async def comando_start(message: types.Message):
    await message.answer(
        "Olá! Sou seu assistente de Astrologia Tradicional e Horária.\n\n"
        "Envie qualquer pergunta que deseja analisar agora (ex: 'Vou conseguir aquela vaga?') "
        "e eu gerarei o mapa horário deste exato momento para responder."
    )

#Handler que captura qualquer mensagem de texto
@dispatcher.message()
async def processar_pergunta(message: types.Message):
    pergunta = message.text

    mensagem_aguarde = await message.answer("🔮 Calculando as efemérides e gerando o mapa horário...")

    try:
        dados_mapa = gerar_mapa()
        await mensagem_aguarde.edit_text("🧠 Enviando mapa para análise do Gemini...")
        
        resposta = analisar_pergunta(dados_mapa, pergunta)
        
        await message.chat.delete_message(mensagem_aguarde.message_id)
        await message.answer(resposta, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"Ocorreu um erro ao processar sua solicitação: {str(e)}")

async def main():
    print("Bot do Telegram iniciado!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())