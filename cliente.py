import socket
import threading
import datetime

# Endereço IP e porta do servidor
host = '192.168.56.1'  # substitua pelo IP do servidor
porta = 8080

# Criar socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar ao servidor
sock.connect((host, porta))

# Nome do usuário
usuario = input("Digite seu nome: ")

def receber_mensagens():
    while True:
        try:
            # Receber mensagem do servidor
            mensagem = sock.recv(1024)
            if not mensagem:  # Se a mensagem estiver vazia, a conexão foi fechada
                break
            # Exibir a mensagem com um timestamp
            print(f"\r{mensagem.decode()}\n> ", end="")
        except:
            print("Erro ao receber mensagem.")
            break

# Iniciar thread para receber mensagens
threading.Thread(target=receber_mensagens, daemon=True).start()

while True:
    # Enviar mensagem
    mensagem = input("> ")
    if mensagem.strip() == "":  # Ignorar mensagens vazias
        continue
    if mensagem.lower() == "sair":
        break
    
    # Formatar a mensagem com o nome do usuário
    mensagem_formatada = f"\033[32m{usuario}\033[0m: {mensagem}"
    sock.sendall(mensagem_formatada.encode())

# Fechar conexão
sock.close()
