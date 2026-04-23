import os
import csv
from sqlalchemy.orm import Session
from app.models import Contrato
from unidecode import unidecode

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "contratos", "BASEFINAL.csv")


def normalizar(texto: str) -> str:
    return unidecode(str(texto)).upper().strip()


def importar_contratos(db: Session):
    try:
        if not os.path.exists(CSV_PATH):
            return {
                "ok": False,
                "msg": "Arquivo contracts.csv não encontrado"
            }

        # Detecta delimitador automaticamente
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            amostra = f.read(2048)

        delimitador = ";" if ";" in amostra else ","

        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=delimitador)

            # Normaliza nomes de colunas
            colunas_originais = reader.fieldnames or []
            colunas_normalizadas = [
                normalizar(c).replace(" ", "_")
                for c in colunas_originais
            ]

            mapa_colunas = dict(zip(colunas_normalizadas, colunas_originais))

            # ✅ MAPEAMENTO EXPLÍCITO
            coluna_cliente = "CESSIONARIO_1"
            coluna_contrato = "CODIGO"
            coluna_status = "STATUS"   # 👈 NOVA COLUNA

            if coluna_cliente not in mapa_colunas or coluna_contrato not in mapa_colunas:
                return {
                    "ok": False,
                    "msg": (
                        "Não foi possível identificar CLIENTE/CONTRATO. "
                        f"Colunas encontradas: {colunas_normalizadas}"
                    )
                }

            col_cliente_real = mapa_colunas[coluna_cliente]
            col_contrato_real = mapa_colunas[coluna_contrato]
            col_status_real = mapa_colunas.get(coluna_status)  # pode ou não existir

            db.query(Contrato).delete()

            total = 0
            for row in reader:
                cliente = normalizar(row.get(col_cliente_real))
                contrato = normalizar(row.get(col_contrato_real))

                status = (
                    normalizar(row.get(col_status_real))
                    if col_status_real and row.get(col_status_real)
                    else None
                )

                if cliente and contrato:
                    db.add(
                        Contrato(
                            cliente_nome=cliente,
                            numero_contrato=contrato,
                            status=status
                        )
                    )
                    total += 1

            db.commit()

        return {
            "ok": True,
            "msg": f"{total} contratos importados com sucesso"
        }

    except Exception as e:
        return {
            "ok": False,
            "msg": f"Erro ao importar CSV: {str(e)}"
        }
