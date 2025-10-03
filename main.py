# Importações de Librarys e APIs
import google.generativeai as genai
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from customtkinter import *
from PIL import Image

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
    if prompt_usuario.strip() == '':
        pass
    else:
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
        response = model.generate_content(f'Faça um resumo sobre {prompt_usuario}. Na hora da criação do Resumo não utilize asterisco ou hashtags, Utilize SOMENTE setas ou pequenos pontos brancos flutuantes. Caso você receba o link de um vídeo do youtube antes do "Faça um resumo sobre...", você mandará SOMENTE a seguinte frase: "Mande o ID do vídeo, não o link."')
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
janela.resizable(False, False)
centralizar(700,425, janela)

#Botão inserir conteúdo
botao_inserir = CTkEntry(janela, placeholder_text='Insira o assunto ou ID do vídeo para ser resumido...', width=500, height=50)
botao_inserir.pack(side='top')
janela.bind('<Return>', lambda event: entrada_usuario())

#Frame scrollavel com resumo
frame_conteudo = CTkScrollableFrame(janela, width=700, height=300)
frame_conteudo.pack(side='top', pady=10)
frame_conteudo.configure(scrollbar_button_color="gray14",scrollbar_button_hover_color="gray14")

#Frame Rodapé
frame_rodape = CTkFrame(janela, width=700, height=50, fg_color='transparent')
frame_rodape.pack(side='bottom')

#Botões do Rodapé
img_copiar = CTkImage(dark_image=Image.open('botao_copiar.png'), size=(25,25))
botao_copiar = CTkButton(frame_rodape, width=25, height=25, text='Copiar', image=img_copiar, fg_color='white', text_color='black', hover_color='#b5b5b5')
botao_copiar.place(relx=0.5, rely=0.45, anchor='center')

botao_cor = CTkSwitch(frame_rodape, text='Mudar cor')
botao_cor.place(relx=0.95, rely=0.5, anchor='e')

img_github = CTkImage(dark_image=Image.open('github.png'), size=(30, 30))
botao_github = CTkButton(frame_rodape, width=15, height=15, image=img_github, text='', fg_color='white', hover_color='#b5b5b5', corner_radius=50)
botao_github.place(relx=0.02, rely=0)

botao_duvida = CTkButton(frame_rodape, text='?', width=40, height=15, font=('comic sans ms', 25), text_color='black', fg_color='white', corner_radius=10, hover_color='#b5b5b5')
botao_duvida.place(relx=0.1, rely=0)

#Texto de Resumo
texto_resumo_label = CTkLabel(frame_conteudo, text='', wraplength=600)
texto_resumo_label.pack()


janela.mainloop()