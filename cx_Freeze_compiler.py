import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
	name="Pixel Brawl v0.2-a2",
	options={"build": {"packages":["pygame"]}},
	executables = executables

	)