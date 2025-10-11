# Importações de Librarys e APIs
import CTkMessagebox
import google.generativeai as genai
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from customtkinter import *
from PIL import Image
from CTkMessagebox import ctkmessagebox
import webbrowser

# Funções
def abrirgithub():
    navegador = webbrowser.get()
    navegador.open('https://github.com/rafssunny')
def ajuda():
    CTkMessagebox.CTkMessagebox(title='Ajuda', message='• Utilize links como este: https://www.youtube.com/watch?v=UcLoXF8N_No\n\n• Não use links que incluam o tempo do vídeo no final do link ou que estejam em um formato diferente. Exemplos de links incorretos:\nhttps://www.youtube.com/watch?v=iD5y-oZOFAM&t=132s\nhttps://youtu.be/uenpi3MW8pQ?si=BXIxQAWy2LcuHGgi')
def copiar(texto):
    janela.clipboard_clear()
    janela.clipboard_append(texto)
    janela.update()
    CTkMessagebox.CTkMessagebox(title='Copiar texto', message='Copiado com sucesso.', icon='check', option_1='Ok.')
def centralizar(largura, altura, janela):
    largura_janela = largura
    altura_janela = altura
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = int((largura_tela/2) - int(largura_janela/2))
    pos_y = int((altura_tela/2) - int(altura_janela/2))
    janela.geometry(f'{largura_janela}x{altura_janela}+{pos_x}+{pos_y}')
def entrada_usuario():
    global texto_resumo_label, frame_conteudo, texto_resumo, response, frame_gato
    texto_resumo = ''
    texto_resumo_label.destroy()
    prompt_usuario = botao_inserir.get()
    if prompt_usuario.strip() == '':
        pass
    else:
        #Checagem se é um ID do youtube ou não.
        try:
            youtube_id = prompt_usuario[32:]
            from youtube_transcript_api import YouTubeTranscriptApi
            yt = YouTubeTranscriptApi().fetch(youtube_id, languages=['pt', 'en'])
        except:
            CTkMessagebox.CTkMessagebox(title='ERRO', message='Insira o link do vídeo corretamente.', icon='cancel', option_1='Ok.')
        else:
            for entry in yt:
                texto_resumo += entry.text
            prompt_usuario = texto_resumo
            response = model.generate_content(f'Faça um resumo sobre {prompt_usuario}. Na hora da criação do Resumo não utilize ** ou hashtags, Utilize SOMENTE setas ou pequenos pontos brancos flutuantes.')
            texto_resumo_label = CTkLabel(frame_conteudo, text=response.text, wraplength=600)
            texto_resumo_label.pack()
            frame_gato.destroy()
    botao_inserir.delete(0, END)

# Configuração modelo da AI e KEY
load_dotenv()
client = genai.configure(api_key=os.getenv("GENAI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Janela Principal
janela = CTk(fg_color='#1E1E1E')
janela.iconbitmap('icone.ico')
janela.title('Summa')
janela.resizable(False, False)
centralizar(700,425, janela)

#Botão inserir conteúdo
botao_inserir = CTkEntry(janela, placeholder_text='Cole aqui o link do vídeo para resumir 📝', width=500, height=50, fg_color='#333333', border_width=2, border_color='#A78BFA')
botao_inserir.pack(side='top')
janela.bind('<Return>', lambda event: entrada_usuario())

#Frame scrollavel com resumo
frame_conteudo = CTkScrollableFrame(janela, width=700, height=300)
frame_conteudo.pack(side='top', pady=10)
frame_conteudo.configure(scrollbar_button_color="gray14",scrollbar_button_hover_color="gray14", fg_color='#2c2f33')

img_gato = CTkImage(dark_image=Image.open('gato.png'), size=(350,350))
frame_gato = CTkLabel(frame_conteudo, image=img_gato, text='')
frame_gato.pack()

#Frame Rodapé
frame_rodape = CTkFrame(janela, width=700, height=50, fg_color='transparent')
frame_rodape.pack(side='bottom')

#Botões do Rodapé
img_copiar = CTkImage(dark_image=Image.open('botao_copiar.png'), size=(25,25))
botao_copiar = CTkButton(frame_rodape, width=25, height=25, text='Copiar', image=img_copiar, fg_color='#A78BFA', text_color='black', hover_color='#C2A5FF', command= lambda: copiar(response.text))
botao_copiar.place(relx=0.5, rely=0.45, anchor='center')

img_github = CTkImage(dark_image=Image.open('github.png'), size=(30, 30))
botao_github = CTkButton(frame_rodape, width=15, height=15, image=img_github, text='', fg_color='#A78BFA', hover_color='#C2A5FF', corner_radius=50, command= lambda: abrirgithub())
botao_github.place(relx=0.02, rely=0)

botao_duvida = CTkButton(frame_rodape, text='?', width=40, height=15, font=('comic sans ms', 25), text_color='black', fg_color='#A78BFA', corner_radius=10, hover_color='#C2A5FF', command=lambda: ajuda())
botao_duvida.place(relx=0.93, rely=0)

#Texto de Resumo
texto_resumo_label = CTkLabel(frame_conteudo, text='', wraplength=600)
texto_resumo_label.pack()


janela.mainloop()