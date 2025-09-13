import functions as func
import sys

def menu():
    while True:
        print("\n===== FarmTech Solutions | Menu =====")
        print("1) Inserir parcela")
        print("2) Listar parcelas")
        print("3) Atualizar parcela (por ID)")
        print("4) Deletar parcela (por ID)")
        print("5) Calcular áreas por cultura")
        print("6) Calcular manejo de insumos")
        print("7) Exportar CSV para R")
        print("8) Sair")
        op = input("Escolha: ").strip()
        if op == "1":
            func.adicionar_parcela()
        elif op == "2":
            func.listar_parcelas()
        elif op == "3":
            func.atualizar_parcela()
        elif op == "4":
            func.deletar_parcela()
        elif op == "5":
            func.calcular_areas_por_cultura()
        elif op == "6":
            func.calcular_insumos()
        elif op == "7":
            caminho = input("Arquivo CSV (padrão: parcelas.csv): ").strip() or "parcelas.csv"
            func.exportar_csv(caminho)
        elif op == "8":
            print("Encerrando...")
            sys.exit(0)
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
