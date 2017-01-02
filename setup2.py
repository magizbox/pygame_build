import cx_Freeze

executables = [cx_Freeze.Executable("hello.py")]
cx_Freeze.setup(
    name="Hello",
    version="1.0",
    options={"build_exe": {}},
    description="Hello",
    executables=executables
)
