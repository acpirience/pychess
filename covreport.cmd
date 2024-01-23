echo off
@echo This has to run in venv (poetry shell)
@echo.
@echo === pytest  ===
coverage run -m pytest
@echo.
@echo === Coverage text  ===
coverage report -m
@echo.
@echo === Coverage html  ===
coverage html
@echo.
