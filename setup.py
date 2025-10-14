from cx_Freeze import setup, Executable

# Nome e versão do aplicativo
app_name = "Summa"
app_version = "1.0"

# Arquivos extras que devem ir junto com o executável
include_files = [
    "icone.ico",
    "click.cur",
    "cursor.cur",
    "tipo.cur",
    "imgs/"
]

# Opções de build (compilação)
build_exe_options = {
    "include_files": include_files,
    "include_msvcr": True,
}

# Configuração principal
setup(
    name=app_name,
    version=app_version,
    description="Aplicativo Summa - resumo de vídeos e textos",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            script="main.py",
            base="Win32GUI",
            icon="icone.ico"
        )
    ]
)
