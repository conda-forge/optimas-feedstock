@echo on

:: Python
%PYTHON% examples\dummy\run_example.py
if errorlevel 1 exit 1

:: Python: pytest
%PYTHON% -m pytest -s -vvvv tests\
if errorlevel 1 exit 1
