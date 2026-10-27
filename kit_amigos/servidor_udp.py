# =============================================================================
# Atividade Classe 04 — Servidor UDP (adaptação da Prática 8a)
# =============================================================================

# ↓↓↓ COLOQUE O SEU RA AQUI (só troca o texto entre as aspas) ↓↓↓
RA = "SEU_RA"
# ↑↑↑ exemplo: RA = "2403862" ↑↑↑

import socket
import os

HOST = "127.0.0.1"
PORTA = 45405
TAMANHO_DATAGRAMA = 512


def iniciar_servidor_udp():
    """Recebe a imagem fatiada em datagramas UDP e salva no disco."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor:
        servidor.bind((HOST, PORTA))
        print(f"RA {RA} — Servidor UDP Ativo, aguardando imagem...\n")

        # 1) Primeiro datagrama: INICIO|nome_do_arquivo|tamanho_em_bytes
        cabecalho, addr = servidor.recvfrom(TAMANHO_DATAGRAMA)
        texto = cabecalho.decode("utf-8")

        if not texto.startswith("INICIO|"):
            print(f"Cabeçalho inválido recebido de {addr}: {texto}")
            servidor.sendto("ERRO: cabecalho invalido".encode("utf-8"), addr)
            return

        _, nome_arquivo, tamanho_str = texto.split("|")
        tamanho_total = int(tamanho_str)

        print("Cabeçalho recebido")
        print(f"Arquivo : {nome_arquivo}")
        print(f"Tamanho : {tamanho_total} bytes")
        print(f"Cliente : {addr[0]}:{addr[1]}\n")

        servidor.sendto("PRONTO".encode("utf-8"), addr)

        # 2) Recebe os pedaços da imagem até completar o tamanho
        pedacos = []
        bytes_recebidos = 0

        while bytes_recebidos < tamanho_total:
            dados, addr = servidor.recvfrom(TAMANHO_DATAGRAMA)
            pedacos.append(dados)
            bytes_recebidos += len(dados)

            if len(pedacos) % 20 == 0 or bytes_recebidos >= tamanho_total:
                print(f"Recebidos {bytes_recebidos}/{tamanho_total} bytes "
                      f"({len(pedacos)} datagramas)")

        imagem = b"".join(pedacos)

        # 3) Grava o arquivo recebido na mesma pasta do script
        pasta = os.path.dirname(os.path.abspath(__file__))
        caminho_saida = os.path.join(pasta, f"recebido_{nome_arquivo}")

        with open(caminho_saida, "wb") as arquivo:
            arquivo.write(imagem)

        print(f"\nImagem salva em: {caminho_saida}")
        print(f"Bytes gravados : {len(imagem)}")

        confirmacao = f"Arquivo {nome_arquivo} recebido com {len(imagem)} bytes"
        servidor.sendto(confirmacao.encode("utf-8"), addr)


if __name__ == "__main__":
    try:
        iniciar_servidor_udp()
    except OSError as e:
        print(f"Erro: {e}")
