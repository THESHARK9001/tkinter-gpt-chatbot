@echo Please be sure you have python 3.13 before building and that you have run "pip install -r requirements.txt" or this will not work
@pause
@pyinstaller --noconsole --clean --onefile --icon=".\ai-build\chatgpt.ico" .\ai-build\gpt.pyw
@pause
