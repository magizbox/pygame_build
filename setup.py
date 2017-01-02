import cx_Freeze

executables = [cx_Freeze.Executable("game.py")]
cx_Freeze.setup(
    name="Slither",
    version="1.0",
    options={"build_exe": {"packages": ["pygame"], "include_files": ["apple.png", "head.png"]}},
    description="Slither",
    executables=executables
)
