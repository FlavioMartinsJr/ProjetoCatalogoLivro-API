from Configs import settings
from fastapi import status
from fastapi.exceptions import HTTPException
import smtplib
import random
import string

email = settings.EMAIL
senha = settings.PWD

class Menssage:
    def gerar_nova_senha():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    def send_email(destinatario, token_senha):
        assunto = 'Confirmacao para Alterar Senha'
        mensagem = f"""\
Subject: {assunto}
Content-Type: text/html
<html>
<body style="font-family: Arial, Helvetica, sans-serif;font-size: 14px;display: flex;overflow: hidden;">
    <div class="box" style="width: auto;">
        <div class="header" style="height: 50px;margin-top: 40px;padding: 10px 5px 10px 20px;background-color: #dee2e6;display: flex;justify-content: center;align-items: center;">
            <img src="https://projeto-catalogo-livro.vercel.app/assets/logo-Livro-oiQdaaxN.png" alt="catalogo de livros" style=" height: 43px;width: 50%; margin: 0 auto;">
        </div>
        <div class="main" style="padding: 20px 30px 20px 10px;">
            
            <p>Prezado,</p><br/>
        
            <p>Foi solicitado uma alteracao na senha, caso queira continuar clique em confirmar:</p>
            
            <form action="http://127.0.0.1:7777/ProjetoLivro/Api/V1/Auth/AlteraSenhaLoginByToken/{token_senha}" method="get" style="width:10%; margin: 0px auto; padding: 25px 10px 25px 10px;">
                <input type="submit" value="Confirmar" style="background-color: #cf4b44;color: #dee2e6;padding: 8px 12px;border-radius: 5px;border-color: #cf4b44;">
            </form>
            
            
            <p>Se nao for necessario apenas desconsidere esse email</p><br/>
            
            <p>Atenciosamente,<br/><br/>Projeto Livros</p>    
        </div>
        <div class="footer" style="height: 50px; background-color: #1e1e1e; display: flex; justify-content: center; align-items: center;">
            <div class="copy-text" style="font-size: 10px;letter-spacing: 1.2px;  width: 100%; align-items: center;">
                <a style="color: #dee2e6; align-items: center;width: 50%;margin: 0 auto;">Catalogo de Livro - Todos os Direitos Reservados.</a>
            </div>
        </div>
    </div>
</body>
</html>
"""
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, senha)
            remetente = email
            server.sendmail(remetente, destinatario, mensagem)
            server.quit()

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT, 
                detail="Falha ao enviar o email"
            )