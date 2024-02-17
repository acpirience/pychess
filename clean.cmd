echo off

@echo === Ruff Format  ===
ruff format .
@echo.
@echo === Ruff Lint  ===
ruff check --fix .
@echo.
@echo === MYPY  ===
mypy .
@echo.
