@echo off
echo Installing sentence-transformers and other dependencies...
call venv\Scripts\activate
pip install sentence-transformers==3.3.1
pip install chromadb==0.5.23
pip install langchain==0.3.13
pip install langchain-community==0.3.13
echo.
echo Installation complete!
pause
