# Importações de Librarys e APIs
import CTkMessagebox
import google.generativeai as genai
from dotenv import load_dotenv
from customtkinter import *
from PIL import Image
import webbrowser
from youtube_transcript_api import YouTubeTranscriptApi
import threading

# Funções
def forcar_cursor_click(event):
    """
    :param event:
    :return: Forçar mudança do ponteiro do mouse em botão de clicar
    """
    event.widget.configure(cursor="@click.cur")
def forcar_cursor_tipo(event):
    """

    :param event:
    :return: Forçar aparição do ponteiro do mouse em botão de escrever
    """
    event.widget.configure(cursor="@tipo.cur")
def abrirgithub():
    navegador = webbrowser.get()
    navegador.open('https://linktr.ee/rafssunny')
def ajuda():
    CTkMessagebox.CTkMessagebox(title='Ajuda', message='• Utilize links como este: https://www.youtube.com/watch?v=UcLoXF8N_No\n\n• Não use links que incluam o tempo do vídeo no final do link ou que estejam em um formato diferente. Exemplos de links incorretos:\nhttps://www.youtube.com/watch?v=iD5y-oZOFAM&t=132s\nhttps://youtu.be/uenpi3MW8pQ?si=BXIxQAWy2LcuHGgi',bg_color='#0d0d0d', fg_color='#240046', text_color='white', button_color='#ff66c4', button_hover_color='#e055ad')
def copiar(texto):
    if not texto or str(texto).strip() == '':
        return
    else:
        janela.clipboard_clear()
        janela.clipboard_append(texto)
        janela.update()
        CTkMessagebox.CTkMessagebox(title='Copiar texto', message='Copiado com sucesso.', icon='check', option_1='Ok.',bg_color='#0d0d0d', fg_color='#240046', text_color='white', button_color='#ff66c4', button_hover_color='#e055ad')
def centralizar(largura, altura, janela):
    largura_janela = largura
    altura_janela = altura
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = int((largura_tela/2) - int(largura_janela/2))
    pos_y = int((altura_tela/2) - int(altura_janela/2))
    janela.geometry(f'{largura_janela}x{altura_janela}+{pos_x}+{pos_y}')
def entrada_usuario():
    global texto_resumo_label, frame_conteudo, texto_resumo, response, gatoenter_label, gatoenter_img
    texto_resumo = ''
    texto_resumo_label.destroy()
    gatoenter_label.destroy()
    prompt_usuario = botao_inserir.get()
    progress_bar = CTkProgressBar(frame_conteudo, progress_color='#cb6ce6')
    progress_label = CTkLabel(frame_conteudo, text='Gerando resumo...', font=('Lexent', 30, 'bold'), text_color='#5c0078')
    progress_label.pack()
    progress_bar.start()
    progress_bar.pack()
    gato_deitadoimg = CTkImage(dark_image=Image.open('imgs/gato_deitado.png'), size=(150,150))
    gato_deitadolabel = CTkLabel(frame_conteudo, text='', image=gato_deitadoimg)
    gato_deitadolabel.pack()
    if prompt_usuario.strip() == '':
        pass
    else:
        #Checagem se é um ID do youtube ou não.
        try:
            youtube_id = prompt_usuario[32:]
            ytt_api = YouTubeTranscriptApi()
            yt = ytt_api.fetch(youtube_id, languages=['pt'])
        except:
            CTkMessagebox.CTkMessagebox(title='ERRO', message='Insira o link do vídeo corretamente.', icon='cancel', option_1='Ok.',bg_color='#0d0d0d', fg_color='#240046', text_color='white', button_color='#ff66c4', button_hover_color='#e055ad')
            gatoenter_label = CTkLabel(frame_conteudo, text='Após colar seu link, pressione ENTER\n no teclado para gerar o resumo',compound='bottom', image=gatoenter_img, font=('Arial', 20), text_color='#5c0078')
            gatoenter_label.pack(side='top')
        else:
            for entry in yt:
                texto_resumo += entry.text
            prompt_usuario = texto_resumo
            response = model.generate_content(f'Faça um resumo sobre {prompt_usuario}. Na hora da criação do Resumo não utilize ** ou hashtags, Utilize SOMENTE setas ou pequenos pontos brancos flutuantes.')
            texto_resumo_label = CTkLabel(frame_conteudo, text=response.text, wraplength=300, text_color='#5c0078')
            texto_resumo_label.pack()
    botao_inserir.delete(0, END)
    janela.after(0, progress_bar.destroy)
    janela.after(0, progress_label.destroy)
    janela.after(0, gato_deitadolabel.destroy)

def limpar_texto():
    global texto_resumo_label, response, gatoenter_label
    gatoenter_label = CTkLabel(frame_conteudo, text='Após colar seu link, pressione ENTER\n no teclado para gerar o resumo', compound='bottom', image=gatoenter_img, font=('Arial', 20), text_color='#5c0078')
    gatoenter_label.pack(side='top')
    texto_resumo_label.destroy()

# Configuração modelo da AI e KEY
load_dotenv()
client = genai.configure(api_key=os.getenv("GENAI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Janela Principal
janela = CTk(fg_color='#cb6ce6')
janela.iconbitmap('icone.ico')
janela.configure(cursor='@cursor.cur')
janela.title('Summa')
janela.resizable(False, False)
centralizar(700,425, janela)

#Botão inserir conteúdo
botao_inserir = CTkEntry(janela, placeholder_text='Cole seu link', width=400, height=40, fg_color='#5c0078', corner_radius=50, border_color='#5c0078')
botao_inserir.place(relx=0.215, rely=0.18)
janela.bind('<Return>', lambda event: threading.Thread(target=entrada_usuario).start())
botao_inserir.bind('<Enter>', forcar_cursor_tipo)

#Frame scrollavel com resumo
frame_conteudo = CTkScrollableFrame(janela, width=365, height=0, corner_radius=15, fg_color='#d6b2e0')
frame_conteudo.place(relx=0.5, rely=0.55, anchor='center')
frame_conteudo.configure(scrollbar_button_color="#d6b2e0",scrollbar_button_hover_color="#d6b2e0")

#Imagem e Label gato Pressionando Enter
gatoenter_img = CTkImage(dark_image=Image.open('imgs/gato_enter.png'), size=(150, 150))
gatoenter_label = CTkLabel(frame_conteudo, text='Após colar seu link, pressione ENTER\n no teclado para gerar o resumo', compound='bottom', image=gatoenter_img, font=('Arial', 20), text_color='#5c0078')
gatoenter_label.pack(side='top')

#Frame Rodapé
frame_rodape = CTkFrame(janela, width=700, height=50, fg_color='transparent')
frame_rodape.pack(side='bottom')

#Botões do Rodapé
img_copiar = CTkImage(dark_image=Image.open('imgs/botao_copiar.png'), size=(30,30))
botao_copiar = CTkButton(frame_rodape, width=50, height=25, text='Copiar', image=img_copiar, fg_color='white', text_color='black', hover_color='#b5b5b5', corner_radius=20, command=lambda: copiar(texto_resumo_label.cget('text')))
botao_copiar.place(relx=0.02, rely=0)
botao_copiar.bind('<Enter>', forcar_cursor_click)

img_github = CTkImage(dark_image=Image.open('imgs/github.png'), size=(30, 30))
botao_github = CTkButton(frame_rodape, width=15, height=15, image=img_github, text='', fg_color='white', hover_color='#b5b5b5', corner_radius=50, command= lambda: abrirgithub())
botao_github.place(relx=0.9, rely=0)
botao_github.bind("<Enter>", forcar_cursor_click)

# Botão com messagebox explicando como usar programa
botao_duvida = CTkButton(frame_rodape, text='?', width=40, height=15, font=('Lexend', 25, 'bold'), text_color='black', fg_color='white', corner_radius=10, hover_color='#b5b5b5', command=lambda: ajuda())
botao_duvida.place(relx=0.18, rely=0.03)
botao_duvida.bind('<Enter>', forcar_cursor_click)

# Botão Limpar texto que apaga o texto resumo label
botao_lixeira = CTkButton(janela, text='Limpar texto', width=40, height=15, text_color='black', fg_color='white', corner_radius=10, hover_color='#b5b5b5', command=limpar_texto)
botao_lixeira.place(relx=0.437, rely=0.85)
botao_lixeira.bind('<Enter>', forcar_cursor_click)

# Logo do Programa no topo
gato_img = CTkImage(dark_image=Image.open('imgs/gato_icone.png'), size=(70,70))
gato_label = CTkLabel(janela, text='S U M M A', image=gato_img, compound='left', font=('Lexend', 30, 'bold'), fg_color='transparent')
gato_label.place(relx=0, rely=0)

# Label do Resumo dentro do Frame Conteúdo
texto_resumo_label = CTkLabel(frame_conteudo, text='', wraplength=600)
texto_resumo_label.pack()


janela.mainloop()