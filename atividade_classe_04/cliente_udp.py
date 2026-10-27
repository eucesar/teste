# =============================================================================
# Atividade Classe 04 — RA 2403862
# Adaptação da Prática 8b (Cliente UDP)
#
# O cliente original só enviava a string "Pacote via UDP!".
# Agora ele lê um arquivo de IMAGEM, fatia em datagramas de 512 bytes
# e envia cada pedaço ao servidor.
# =============================================================================

import socket
import os
import time

# Mesmo host e porta da Prática 8 / do servidor.
HOST = "127.0.0.1"
PORTA = 45405

# Mesmo tamanho de buffer da prática (recvfrom(512)).
TAMANHO_DATAGRAMA = 512

# Imagem de exemplo da atividade (Neymar — última imagem enviada).
ARQUIVO_IMAGEM = "neymar.png"


def iniciar_cliente_udp():
    """
    Lê a imagem de exemplo, avisa o servidor (cabeçalho) e envia o arquivo
    pedaço a pedaço via UDP.
    """
    pasta = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(pasta, ARQUIVO_IMAGEM)

    # Abre a imagem em modo binário — UDP carrega bytes, não texto.
    with open(caminho, "rb") as arquivo:
        conteudo = arquivo.read()

    nome_arquivo = os.path.basename(caminho)
    tamanho = len(conteudo)

    print(f"Enviando imagem : {nome_arquivo}")
    print(f"Tamanho         : {tamanho} bytes")
    print(f"Destino         : {HOST}:{PORTA}\n")

    try:
        # Cria o socket UDP sem vincular a uma porta fixa
        # (o SO escolhe uma porta livre, igual à prática).
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
            # ------------------------------------------------------------------
            # 1) Primeiro datagrama: metadados (nome + tamanho)
            # ------------------------------------------------------------------
            cabecalho = f"INICIO|{nome_arquivo}|{tamanho}"
            cliente.sendto(cabecalho.encode("utf-8"), (HOST, PORTA))

            # Espera o "PRONTO" do servidor antes de mandar os bytes da imagem.
            cliente.settimeout(5)
            resposta, addr = cliente.recvfrom(TAMANHO_DATAGRAMA)
            print(f"Servidor respondeu: {resposta.decode('utf-8')}")
            print(f"IP: {addr[0]}  Porta: {addr[1]}\n")

            # ------------------------------------------------------------------
            # 2) Fatia o arquivo e envia cada fatia como um datagrama UDP
            # ------------------------------------------------------------------
            enviados = 0
            pacotes = 0

            while enviados < tamanho:
                pedaco = conteudo[enviados:enviados + TAMANHO_DATAGRAMA]
                cliente.sendto(pedaco, (HOST, PORTA))
                enviados += len(pedaco)
                pacotes += 1

                # Pausa mínima para o buffer do SO não descartar datagramas.
                # (UDP não garante entrega; no localhost isso evita overflow.)
                time.sleep(0.001)

            print(f"Envio concluído: {enviados} bytes em {pacotes} datagramas")

            # ------------------------------------------------------------------
            # 3) Aguarda a confirmação final do servidor
            # ------------------------------------------------------------------
            confirmacao, addr = cliente.recvfrom(TAMANHO_DATAGRAMA)
            print(f"Confirmação: {confirmacao.decode('utf-8')}")

    except OSError as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    iniciar_cliente_udp()
