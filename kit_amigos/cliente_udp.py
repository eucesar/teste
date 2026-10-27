# =============================================================================
# Atividade Classe 04 — Cliente UDP (adaptação da Prática 8b)
# =============================================================================

# ↓↓↓ COLOQUE O SEU RA AQUI (só troca o texto entre as aspas) ↓↓↓
RA = "SEU_RA"
# ↑↑↑ exemplo: RA = "2403862" ↑↑↑

import socket
import os
import time

HOST = "127.0.0.1"
PORTA = 45405
TAMANHO_DATAGRAMA = 512

# Imagem de exemplo já inclusa neste ZIP (Neymar).
# Se quiser outra foto, coloque o arquivo nesta pasta e mude o nome abaixo.
ARQUIVO_IMAGEM = "neymar.png"


def iniciar_cliente_udp():
    """Lê a imagem, fatia em datagramas de 512 bytes e envia ao servidor."""
    pasta = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(pasta, ARQUIVO_IMAGEM)

    with open(caminho, "rb") as arquivo:
        conteudo = arquivo.read()

    nome_arquivo = os.path.basename(caminho)
    tamanho = len(conteudo)

    print(f"RA {RA} — enviando imagem: {nome_arquivo}")
    print(f"Tamanho         : {tamanho} bytes")
    print(f"Destino         : {HOST}:{PORTA}\n")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
            # 1) Cabeçalho com nome e tamanho do arquivo
            cabecalho = f"INICIO|{nome_arquivo}|{tamanho}"
            cliente.sendto(cabecalho.encode("utf-8"), (HOST, PORTA))

            cliente.settimeout(5)
            resposta, addr = cliente.recvfrom(TAMANHO_DATAGRAMA)
            print(f"Servidor respondeu: {resposta.decode('utf-8')}")
            print(f"IP: {addr[0]}  Porta: {addr[1]}\n")

            # 2) Envia a imagem em pedaços de 512 bytes
            enviados = 0
            pacotes = 0

            while enviados < tamanho:
                pedaco = conteudo[enviados:enviados + TAMANHO_DATAGRAMA]
                cliente.sendto(pedaco, (HOST, PORTA))
                enviados += len(pedaco)
                pacotes += 1
                time.sleep(0.001)

            print(f"Envio concluído: {enviados} bytes em {pacotes} datagramas")

            # 3) Confirmação do servidor
            confirmacao, addr = cliente.recvfrom(TAMANHO_DATAGRAMA)
            print(f"Confirmação: {confirmacao.decode('utf-8')}")

    except OSError as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    iniciar_cliente_udp()
