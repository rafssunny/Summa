# Importações de Librarys e APIs
import google.generativeai as genai
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from customtkinter import *

# Funções
def centralizar(largura, altura, janela):
    largura_janela = largura
    altura_janela = altura
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = int((largura_tela/2) - int(largura_janela/2))
    pos_y = int((altura_tela/2) - int(altura_janela/2))
    janela.geometry(f'{largura_janela}x{altura_janela}+{pos_x}+{pos_y}')
def entrada_usuario():
    global texto_resumo_label, frame_conteudo, texto_resumo
    texto_resumo = ''
    texto_resumo_label.destroy()
    prompt_usuario = botao_inserir.get()
    #Checagem se é um ID do youtube ou não.
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        yt = YouTubeTranscriptApi().fetch(prompt_usuario, languages=['pt', 'en'])
    except:
        pass
    else:
        for entry in yt:
            texto_resumo += entry.text
        prompt_usuario = texto_resumo
    response = model.generate_content(f'Faça um resumo sobre {prompt_usuario}. Na hora da criação do Resumo não utilize asterisco ou hashtags, Utilize SOMENTE setas ou •. Caso você receba o link de um vídeo do youtube, diga a seguinte frase: "Mande o ID do vídeo, não o link."')
    texto_resumo_label = CTkLabel(frame_conteudo, text=response.text, wraplength=600)
    texto_resumo_label.pack()
    botao_inserir.delete(0, END)

# Configuração modelo da AI e KEY
load_dotenv()
client = genai.configure(api_key=os.getenv("GENAI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Janela Principal
janela = CTk()
janela.title('Summa')
centralizar(700,400, janela)

botao_inserir = CTkEntry(janela, placeholder_text='Conteúdo para ser resumido', width=500, height=50)
botao_inserir.pack(side='bottom')
janela.bind('<Return>', lambda event: entrada_usuario())

frame_conteudo = CTkScrollableFrame(janela, width=600, height=300)
frame_conteudo.pack()

texto_resumo_label = CTkLabel(frame_conteudo, text='', wraplength=600)
texto_resumo_label.pack()


janela.mainloop()