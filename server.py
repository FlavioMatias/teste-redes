try:
    import socket
    import threading
    import subprocess

    # Configurações do servidor
    host = '0.0.0.0'  # Escutar em todas as interfaces
    porta = 8080

    # Lista para armazenar conexões de clientes
    clientes = []

    def liberar_porta(porta):
        try:
            # Comando do PowerShell para liberar a porta no firewall
            comando = f"New-NetFirewallRule -DisplayName 'Servidor Python' -Direction Inbound -Protocol TCP -LocalPort {porta} -Action Allow"
            subprocess.run(["powershell", "-Command", comando], check=True)
            print(f"Porta {porta} liberada no firewall.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao liberar a porta {porta}: {e}")

    def handle_client(conn, addr):
        print(f"Conexão estabelecida com {addr}")
        while True:
            try:
                # Receber mensagem do cliente
                mensagem = conn.recv(1024)
                if not mensagem:  # Se a mensagem estiver vazia, a conexão foi fechada
                    break
                
                print(f"Mensagem de {addr}: {mensagem.decode()}")

                # Encaminhar a mensagem para todos os clientes conectados
                broadcast(mensagem, conn)
            except:
                break
        
        conn.close()
        clientes.remove(conn)
        print(f"Conexão encerrada com {addr}")

    def broadcast(mensagem, sender_conn):
        # Enviar a mensagem para todos os clientes, exceto o remetente
        for cliente in clientes:
            if cliente != sender_conn:
                try:
                    cliente.sendall(mensagem)
                except:
                    cliente.close()
                    clientes.remove(cliente)

    # Criar socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind do socket à porta
    sock.bind((host, porta))
    liberar_porta(porta)

    # Escutar conexões
    sock.listen(5)
    print(f"Aguardando conexões em {host}:{porta}")

    while True:
        # Aceitar nova conexão
        conn, addr = sock.accept()
        clientes.append(conn)  # Adicionar à lista de clientes
        threading.Thread(target=handle_client, args=(conn, addr)).start()
except:
    input()
