from cx_Freeze import setup, Executable

if __name__ == "__main__":
    # Nome e versão do aplicativo
    app_name = "Summa"
    app_version = "1.0"

    include_files = [
        "icone.ico",
        "click.cur",
        "cursor.cur",
        "tipo.cur",
        "imgs/"
    ]

    build_exe_options = {
        "include_files": include_files,
        "include_msvcr": True,
    }

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