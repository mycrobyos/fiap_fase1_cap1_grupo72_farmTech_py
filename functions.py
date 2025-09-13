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
def adicionar_parcela():  #Função para adicionar parcelas (Grupo da cultura)
    cultura = escolher_cultura()
    reg = {"id": gerar_id(), "cultura": cultura} #Dicionário para adicionar a lista principal posteriormente


    # Condicional para verificar a cultura
    if cultura == "Café": # Café
        reg.update({ #Update do dicionário para input do usúario. entrada_float = função para input
            "largura_m": entrada_float("Largura do talhão (m): ", 0),
            "comprimento_m": entrada_float("Comprimento do talhão (m): ", 0),
            "raio_m": 0.0
        })
    elif cultura == "Cana":  # Cana
        reg.update({
            "raio_m": entrada_float("Raio do pivô (m): ", 0),
            "largura_m": 0.0, "comprimento_m": 0.0
        })
        
    # Update do dicionário novamente
    reg.update({ 
        "produto": input("Produto/insumo (ex: Fosfato): ").strip() or "N/D",
        "dose_ml_m": entrada_float("Dose (mL por metro): ", 0),
        "comp_rua_m": entrada_float("Comprimento médio por rua (m): ", 0),
        "num_ruas": entrada_int("Número de ruas: ", 0),
    })

    # Calculo da área e insumo para adicionar no dicionário
    reg["area_m2"] = calcular_area(reg)
    reg["insumo_litros"] = calcular_insumo_litros(reg)

    # Adição do dicionário para a lista de parcelas + adição do id e área  nos vetores de ids e areas.
    parcelas.append(reg)
    ids.append(reg["id"]); culturas.append(reg["cultura"])
    areas.append(reg["area_m2"]); insumos_litros.append(reg["insumo_litros"])
    print(reg)
    print("\nParcela adicionada com sucesso!")


def listar_parcelas(): #Função para listar as parcelas
    if not parcelas: #Condicional para verificar se existem parcelas.
        print("\nNenhuma parcela cadastrada."); return
    print("\n--- PARCELAS ---")

    for p in parcelas: #Loop para printar cada parcela dentro da lista de parcelas, e condicional para identificar o tipo da cultura.
        print(f"ID {p['id']:02d} | Cultura: {p['cultura']:<4} | Área: {p['area_m2']:.2f} m² " f"| Insumo: {p['insumo_litros']:.2f} L | Produto: {p['produto']}")
        if p["cultura"] == "Café":
            print(f"   Largura: {p['largura_m']} m | Comprimento: {p['comprimento_m']} m | " f"Ruas: {p['num_ruas']} | Comp/Rua: {p['comp_rua_m']} m | Dose: {p['dose_ml_m']} mL/m")
        elif p["cultura"] == "Cana":
            print(f"   Raio: {p['raio_m']} m | Ruas: {p['num_ruas']} | " f"Comp/Rua: {p['comp_rua_m']} m | Dose: {p['dose_ml_m']} mL/m")


def atualizar_parcela(): #Função para atualizar as parcelas.
    if not parcelas: #Condicional para verificar se existem parcelas.
        print("\nNada para atualizar.")
        return

    pid = entrada_int("Digite o ID da parcela a atualizar: ", 1) #Input para selecionar o id da parcela.
    idx = localizar_indice_por_id(pid) #Localizar id da parcela.

    if idx is None: #Condicional para verificar se o id da parcela existe.
        print("ID não encontrado.")
        return

    p = parcelas[idx] #Associando o p para o a parcela a ser atualizada
    print(f"\nAtualizando parcela ID {p['id']} ({p['cultura']})")

    #Condicional para verificar o tipo de cultura
    if p["cultura"] == "Café":
        novo = entrada_float(f"Largura (m) [{p['largura_m']}]: ")
        if novo: p["largura_m"] = novo #Verifica se existe a variável e atualiza a lista caso exista

        novo = entrada_float(f"Comprimento (m) [{p['comprimento_m']}]: ")
        if novo: p["comprimento_m"] = novo #Verifica se existe a variável e atualiza a lista caso exista
    elif p["cultura"] == "Cana":
        novo = entrada_float(f"Raio (m) [{p['raio_m']}]: ")
        if novo: p["raio_m"] = novo #Verifica se existe a variável e atualiza a lista caso exista

    # Input para atualizar o produto da parcela
    prod = input(f"Produto [{p['produto']}]: ").strip()
    if prod: #Condicional para associar o produto anterior ao mesmo, caso necessário.
        p["produto"] = prod

    # Outros atributos numéricos
    for campo, msg, entrada in [ #Loop para input da atualização dos componentes da cultura.
        ("dose_ml_m", f"Dose (mL/m) [{p['dose_ml_m']}]: ", entrada_float),
        ("comp_rua_m", f"Comp/Rua (m) [{p['comp_rua_m']}]: ", entrada_float),
        ("num_ruas", f"Nº de ruas [{p['num_ruas']}]: ", entrada_int),
    ]:
        novo = entrada(msg)
        if novo: #Verifica se existe a variável e atualiza a lista caso exista
            p[campo] = novo

    # Recalcular para as novas atualizações
    p["area_m2"] = calcular_area(p)
    p["insumo_litros"] = calcular_insumo_litros(p)

    # Atualizar vetores auxiliares
    i2 = ids.index(p["id"])
    culturas[i2] = p["cultura"]
    areas[i2] = p["area_m2"]
    insumos_litros[i2] = p["insumo_litros"]

    print("\n✅ Parcela atualizada.")




def deletar_parcela(): #Função para deletar parcela
    if not parcelas: #Condicional para verificar se existe parcelas.
        print("\nNada para deletar."); return
    
    pid, idx = entrada_int("Digite o ID da parcela a deletar: ", 1), None #Input para adicionar o id a ser removido.
    idx = localizar_indice_por_id(pid) #Localizar o id digitado.
    if idx is None: print("ID não encontrado."); return #Condicional para dizer se foi encontrado um id.

    rem = parcelas.pop(idx) #Remoção da parcela caso exista, na lista de parcelas
    i2 = ids.index(rem["id"]) #Remoção do id do vetor de ids + associando o id ao i2 para remoção dos outros vetores
    for v in (ids, culturas, areas, insumos_litros): v.pop(i2) #Remoção dos vetores restantes
    print("\n Parcela deletada.")




def exportar_csv(caminho="parcelas.csv"): #Função para exportar a lista de parcelas, para um csv.
    campos = ["id","cultura","largura_m","comprimento_m","raio_m","produto",
              "dose_ml_m","comp_rua_m","num_ruas","area_m2","insumo_litros"] #Os campos para adicionar no arquivo.
    with open(caminho, "w", newline="", encoding="utf-8") as f: #Criação do arquivo.
        w = csv.DictWriter(f, fieldnames=campos); w.writeheader() #Associando o w a criação de um csv a partir dos campos.
        for p in parcelas: #Loop para adicionar cada parcela ao código de acordo com os campos
            w.writerow({c: p.get(c, 0) if p.get(c, "") == "" else p[c] for c in campos})
    print(f"\n Exportado para {caminho}")


# ---------------------------
# Funções matemáticas
# ---------------------------
def calcular_area(p): return p["largura_m"]*p["comprimento_m"] if p["cultura"]=="Café" else math.pi*(p["raio_m"]**2) #Função para calcular a área, dando um return com a expressão matemática.

def calcular_insumo_litros(p): return (p["dose_ml_m"]*p["comp_rua_m"]*p["num_ruas"])/1000 #Função para calcular o insumo, dando um return com a expressão matemática.

def calcular_areas_por_cultura(): #Função para calcular a área por cultura.
    tot_cafe = sum(p["area_m2"] for p in parcelas if p["cultura"]=="Café") #Associando uma váriavel para o total da aréa de café existente.
    tot_cana = sum(p["area_m2"] for p in parcelas if p["cultura"]=="Cana") #Associando uma váriavel para o total da aréa de cana existente.
    print("\n--- ÁREA POR CULTURA (m²) ---")
    print(f"Café: {tot_cafe:.2f}\nCana: {tot_cana:.2f}\nTOTAL: {tot_cafe+tot_cana:.2f}") 

def calcular_insumos(): #Função para printar o insumo e calcular o total necessário.
    if not parcelas: print("\nNenhuma parcela cadastrada."); return #Condicional para existencia de parcelas
    total = sum(p["insumo_litros"] for p in parcelas) #Associando váriavel a soma total dos insumos.
    print("\n--- INSUMOS (litros) ---")
    [print(f"ID {p['id']:02d} | {p['cultura']} | {p['produto']} | {p['insumo_litros']:.2f} L") for p in parcelas]
    print(f"TOTAL: {total:.2f} L")


# ---------------------------
# Funções auxiliares
# ---------------------------
def gerar_id(): return len(parcelas)+1 #Função simples para gerar o id.


def escolher_cultura(): #Função simples para escolha de cultura
    print("\nEscolha a cultura:\n1) Café (área = largura x comprimento)\n2) Cana (área = π r²)")
    return "Café" if entrada_int("Opção: ", 1, 2) == 1 else "Cana"

def entrada_float(msg, min=None, max=None): #Função simples para verifcar o input do usúario, para os cálculos
    while True:
        try:
            v = float(input(msg).replace(",", "."))
            if min is not None and v < min: print(f"Valor >= {min}."); continue
            if max is not None and v > max: print(f"Valor <= {max}."); continue
            return v
        except: print("Número inválido.")

def entrada_int(msg, min=None, max=None): #Função simples para verifcar o input do usúario, para os cálculos
    while True: 
        try:
            v = int(input(msg))
            if min is not None and v < min: print(f"Valor >= {min}."); continue
            if max is not None and v > max: print(f"Valor <= {max}."); continue
            return v
        except: print("Número inválido.")

def localizar_indice_por_id(pid):  #Função simples para localizar o indice no vetor de parcelas.
    return next((i for i,p in enumerate(parcelas) if p["id"]==pid), None)
