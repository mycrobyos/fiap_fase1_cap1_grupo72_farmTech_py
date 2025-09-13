import math
import csv

# ---------------------------
# "Banco de dados" em VETORES
# ---------------------------
parcelas = []  # lista principal
ids, culturas, areas, insumos_litros = [], [], [], []  # vetores auxiliares


# ---------------------------
# Funções principais
# ---------------------------
def adicionar_parcela():
    cultura = escolher_cultura()
    reg = {"id": gerar_id(), "cultura": cultura} #Dicionário para adicionar a lista principal posteriormente

    if cultura == "Café":
        reg.update({
            "largura_m": entrada_float("Largura do talhão (m): ", 0),
            "comprimento_m": entrada_float("Comprimento do talhão (m): ", 0),
            "raio_m": 0.0
        })
    elif cultura == "Soja":  # Soja
        reg.update({
            "raio_m": entrada_float("Raio do pivô (m): ", 0),
            "largura_m": 0.0, "comprimento_m": 0.0
        })
        

    reg.update({
        "produto": input("Produto/insumo (ex: Fosfato): ").strip() or "N/D",
        "dose_ml_m": entrada_float("Dose (mL por metro): ", 0),
        "comp_rua_m": entrada_float("Comprimento médio por rua (m): ", 0),
        "num_ruas": entrada_int("Número de ruas: ", 0),
    })

    reg["area_m2"] = calcular_area(reg)
    reg["insumo_litros"] = calcular_insumo_litros(reg)

    parcelas.append(reg)
    ids.append(reg["id"]); culturas.append(reg["cultura"])
    areas.append(reg["area_m2"]); insumos_litros.append(reg["insumo_litros"])
    print(reg)
    print("\nParcela adicionada com sucesso!")


def listar_parcelas():
    if not parcelas:
        print("\nNenhuma parcela cadastrada."); return
    print("\n--- PARCELAS ---")
    for p in parcelas:
        print(f"ID {p['id']:02d} | Cultura: {p['cultura']:<4} | Área: {p['area_m2']:.2f} m² " f"| Insumo: {p['insumo_litros']:.2f} L | Produto: {p['produto']}")
        if p["cultura"] == "Café":
            print(f"   Largura: {p['largura_m']} m | Comprimento: {p['comprimento_m']} m | " f"Ruas: {p['num_ruas']} | Comp/Rua: {p['comp_rua_m']} m | Dose: {p['dose_ml_m']} mL/m")
        else:
            print(f"   Raio: {p['raio_m']} m | Ruas: {p['num_ruas']} | " f"Comp/Rua: {p['comp_rua_m']} m | Dose: {p['dose_ml_m']} mL/m")


def atualizar_parcela():
    if not parcelas:
        print("\nNada para atualizar.")
        return

    pid = entrada_int("Digite o ID da parcela a atualizar: ", 1)
    idx = localizar_indice_por_id(pid)

    if idx is None:
        print("ID não encontrado.")
        return

    p = parcelas[idx]
    print(f"\nAtualizando parcela ID {p['id']} ({p['cultura']})")

    # Café -> largura/comprimento | Soja -> raio
    if p["cultura"] == "Café":
        novo = entrada_float(f"Largura (m) [{p['largura_m']}]: ")
        if novo: p["largura_m"] = novo

        novo = entrada_float(f"Comprimento (m) [{p['comprimento_m']}]: ")
        if novo: p["comprimento_m"] = novo
    elif p["cultura"] == "Soja":
        novo = entrada_float(f"Raio (m) [{p['raio_m']}]: ")
        if novo: p["raio_m"] = novo

    # Produto
    prod = input(f"Produto [{p['produto']}]: ").strip()
    if prod:
        p["produto"] = prod

    # Outros atributos numéricos
    for campo, msg, entrada in [
        ("dose_ml_m", f"Dose (mL/m) [{p['dose_ml_m']}]: ", entrada_float),
        ("comp_rua_m", f"Comp/Rua (m) [{p['comp_rua_m']}]: ", entrada_float),
        ("num_ruas", f"Nº de ruas [{p['num_ruas']}]: ", entrada_int),
    ]:
        novo = entrada(msg)
        if novo:
            p[campo] = novo

    # Recalcular
    p["area_m2"] = calcular_area(p)
    p["insumo_litros"] = calcular_insumo_litros(p)

    # Atualizar vetores auxiliares
    i2 = ids.index(p["id"])
    culturas[i2] = p["cultura"]
    areas[i2] = p["area_m2"]
    insumos_litros[i2] = p["insumo_litros"]

    print("\n✅ Parcela atualizada.")




def deletar_parcela():
    if not parcelas:
        print("\nNada para deletar."); return
    pid, idx = entrada_int("Digite o ID da parcela a deletar: ", 1), None
    idx = localizar_indice_por_id(pid)
    if idx is None: print("ID não encontrado."); return

    rem = parcelas.pop(idx)
    i2 = ids.index(rem["id"])
    for v in (ids, culturas, areas, insumos_litros): v.pop(i2)
    print("\n🗑️  Parcela deletada.")


def escolher_cultura():
    print("\nEscolha a cultura:\n1) Café (área = largura x comprimento)\n2) Soja (área = π r²)")
    return "Café" if entrada_int("Opção: ", 1, 2) == 1 else "Soja"


def exportar_csv(caminho="parcelas.csv"):
    campos = ["id","cultura","largura_m","comprimento_m","raio_m","produto",
              "dose_ml_m","comp_rua_m","num_ruas","area_m2","insumo_litros"]
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos); w.writeheader()
        for p in parcelas:
            w.writerow({c: p.get(c, 0) if p.get(c, "") == "" else p[c] for c in campos})
    print(f"\n💾 Exportado para {caminho}")


# ---------------------------
# Funções matemáticas
# ---------------------------
def calcular_area(p): return p["largura_m"]*p["comprimento_m"] if p["cultura"]=="Café" else math.pi*(p["raio_m"]**2)

def calcular_insumo_litros(p): return (p["dose_ml_m"]*p["comp_rua_m"]*p["num_ruas"])/1000

def calcular_areas_por_cultura():
    tot_cafe = sum(p["area_m2"] for p in parcelas if p["cultura"]=="Café")
    tot_soja = sum(p["area_m2"] for p in parcelas if p["cultura"]=="Soja")
    print("\n--- ÁREA POR CULTURA (m²) ---")
    print(f"Café: {tot_cafe:.2f}\nSoja: {tot_soja:.2f}\nTOTAL: {tot_cafe+tot_soja:.2f}")

def calcular_insumos():
    if not parcelas: print("\nNenhuma parcela cadastrada."); return
    total = sum(p["insumo_litros"] for p in parcelas)
    print("\n--- INSUMOS (litros) ---")
    [print(f"ID {p['id']:02d} | {p['cultura']} | {p['produto']} | {p['insumo_litros']:.2f} L") for p in parcelas]
    print(f"TOTAL: {total:.2f} L")


# ---------------------------
# Funções auxiliares
# ---------------------------
def gerar_id(): return len(parcelas)+1

def entrada_float(msg, min=None, max=None):
    while True:
        try:
            v = float(input(msg).replace(",", "."))
            if min is not None and v < min: print(f"Valor >= {min}."); continue
            if max is not None and v > max: print(f"Valor <= {max}."); continue
            return v
        except: print("Número inválido.")

def entrada_int(msg, min=None, max=None):
    while True:
        try:
            v = int(input(msg))
            if min is not None and v < min: print(f"Valor >= {min}."); continue
            if max is not None and v > max: print(f"Valor <= {max}."); continue
            return v
        except: print("Número inválido.")

def localizar_indice_por_id(pid): 
    return next((i for i,p in enumerate(parcelas) if p["id"]==pid), None)
