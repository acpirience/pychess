echo off

@echo === Ruff Format  ===
ruff format .
@echo.
@echo === Ruff Lint  ===
ruff check .  
@echo.
@echo === MYPY  ===
mypy .
@echo.
