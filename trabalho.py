from random import randint;
import os;

class Data():
	def __init__(self, dia, mes, ano):
		self.dia = dia
		self.mes = mes
		self.ano = ano
	
	def __str__(self):
		return dia + "/" + mes + "/" + ano

class Produto():
	def __init__(self, nome, quant=1):
		self.nome = nome
		self.quant = quant

class Pedido():
	def __init__(self, oferta, demanda, user, grupo):
		self.oferta = oferta
		self.demanda = demanda
		self.user = user
		self.grupo = grupo

class Usuario():
	def __init__(self,ID, nome,cpf,senha):
		self.nome = nome
		self.cpf = cpf
		self.senha = senha
		self.ID = ID
		self.grupos = []
		self.contratos_pendentes = []
		self.contratos_assinados = []
	
	
	def getNome(self):
		return self.nome


class Grupo():
	def __init__(self,ID, nome, senha, subgrupos=[]):
		self.ID = ID
		self.nome = nome
		self.senha = senha
		self.subgrupos = subgrupos
		self.mercado = {"pedidos": [["Abacate"],["Banana"],["Caju"],["Damasco"],["Espada"],["Farofa"]], "valores": []}
	
	def mercadoGetOfertas():
		return mercado[ofertas]
	
	def mercadoGetDemandas():
		return mercado[demandas]

'''Executando mercado'''
'''procura as partes e tenta montar uma cadeia fechada'''
def fazCadeia(mercado,pedido,cadeia):
	'''insere o ultimo pedido na cadeia'''
	cadeia.append(pedido)
	'''Verifica se o final da cadeia (o ultimo pedido inserido, 
	tem uma demanda igual a oferta de uma das partes, se sim, 
	ele encerra'''
	for i in range(len(cadeia)):
		if pedido.demanda.nome == cadeia[i].oferta.nome:
			return cadeia
	'''procura a lista de ofertas que atendem a demanda do pedido'''
	for lista in mercado['pedidos']:
		'''Verifica se o nome do primeiro elemento da lista é o nome da
		oferta'''
		if lista[0] == pedido.demanda.nome:
			'''vai nessa lista e verifica se tem alguma oferta'''
			achou = False
			for i in range(1,len(lista)):
				if lista[i].oferta.nome == pedido.demanda.nome:
					'''se tiver, ele vai pegar o pedido da oferta, e fazer o mesmo processo'''
					cadeia = fazCadeia(mercado,lista[i],cadeia)
					for elemento in cadeia:
						if elemento == lista[i]:
							'''caso a cadeia retornada nao um dos pedidos como sendo igual
							o pedido analisado, quer dizer que ele nao conseguiu entrar na cadeia, entao
							o programa nao vai considera-lo'''
							achou = True
			'''Se nao tiver achado nada que dê para continuar o processo por esse pedido,
			ele será apagado da cadeia, e o proximo do for anterior sera puxado'''
			if not(achou):
				cadeia.remove(pedido)
			return(cadeia)

'''Função para deixar apenas a parte da cadeia que se fecha'''
def lapidaCadeia(cadeia):
	if len(cadeia) > 0:
		ultimo = cadeia[len(cadeia)-1]
		for pedido in cadeia:
			if pedido.oferta.nome != ultimo.demanda.nome:
				cadeia.remove(pedido)
			else:
				return cadeia
	else:
		return False

def executaMercado(mercado,pedido):
	cadeia = []
	cadeia = fazCadeia(mercado,pedido,cadeia)
	cadeia = lapidaCadeia(cadeia)
	if cadeia != False:
		os.system('cls' if os.name == 'nt' else 'clear')
		print("			-=--GERADOR DE TROCAS--=-")
		print("\n			Foi possível encontrar uma cadeia de trocas\n que satisfaz o seu pedido.")
		input("")
		contrato = "			[CADEITA DE TROCAS]\n\n"
		for i in range(len(cadeia)):
			if (i -1) < 0:
				clausula = "			Transação {}: {} dá {} para {}.\n".format(i+1,cadeia[i].user.nome,cadeia[i].oferta.nome,cadeia[len(cadeia)-1].user.nome)
			else:
				clausula = "\n			Transação {}:{} dá {} para {}.\n".format(i+1,cadeia[i].user.nome,cadeia[i].oferta.nome,cadeia[i-1].user.nome)
			contrato = contrato + clausula
		print(contrato)
		input()
		for pedido in cadeia:
			pedido.user.contratos_pendentes.append(contrato)
			for lista in mercado:
				if pedido.oferta.nome == lista[0]:
					lista.remove(pedido)
			del(pedido)
	else:
		input("Não foi possível encontrar uma cadeia de trocas :(  ")
		return False

def cadastraUsuario(nome, usuarios):
	usuario = Usuario(len(usuarios),nome,"123","123")
	usuarios.append(usuario)
	return usuarios

def buscaUsuario(nome,usuarios):
	for usuario in usuarios:
		if (usuario.getNome() == nome):
			return usuario
	return 0

def cadastraPedido(usuario, demanda, oferta, mercado):
	prodOferta = Produto(oferta)
	prodDemanda = Produto(demanda)
	pedido = Pedido(prodOferta,prodDemanda,usuario,Grupo(1,"grupo","123"))
	achou = False
	for lista in mercado["pedidos"]:
		if (lista[0] == pedido.demanda.nome):
			achou = True
	if (not(achou)):
		mercado["pedidos"].append([pedido.demanda.nome])
	for lista in mercado["pedidos"]:
		if (lista[0] == pedido.oferta.nome):
			lista.append(pedido)
			return mercado, pedido
	mercado["pedidos"].append([pedido.oferta.nome])
	mercado["pedidos"][len(mercado["pedidos"])-1].append(pedido)
	return mercado, pedido

def main():
	answ = ""
	cont = 0
	usuarios = []
	mercado = {"pedidos": []}
	pedidos = []
	while answ != "-":
		print("			-=--GERADOR DE TROCAS--=-")
		print("\n			O que você deseja?\n")
		print("			[0] Cadastrar um comerciante")
		print("			[1] Cadastrar um pedido")
		print("			[2] Reset")
		print("			[3] Lista")
		print("			[-] Fechar\n")
		answ = input("			[R] ")
		
		os.system('cls' if os.name == 'nt' else 'clear')
		
		if (answ == "0"):
			print("			-=--GERADOR DE TROCAS--=-")
			nome = input("\n			[0] Nome do comerciante: ")
			usuarios = cadastraUsuario(nome,usuarios)
			print("			[0]Comerciante Cadastrado!")
			input("			")
			os.system('cls' if os.name == 'nt' else 'clear')
		
		elif (answ == "1"):
			print("			-=--GERADOR DE TROCAS--=-")
			nome = input("\n			[1] Nome do comerciante: ")
			usuario = buscaUsuario(nome,usuarios)
			demanda = input("\n			[1] Produto que deseja consumir: ")
			oferta = input("\n			[1] Produto que pode oferecer: ")
			mercado, pedido = cadastraPedido(usuario,demanda,oferta,mercado)
			pedidos.append(pedido)
			print("			[1] Pedido cadastrado!")
			input("			")
			cont += 1
			if cont > 1:
				executaMercado(mercado,pedido)
			os.system('cls' if os.name == 'nt' else 'clear')
		
		elif (answ == "2"):
				usuarios = []
				mercado = {"pedidos": []}
				os.system('cls' if os.name == 'nt' else 'clear')
				input("\n\n\n			DADOS RESETADOS")
				os.system('cls' if os.name == 'nt' else 'clear')
		
		elif (answ == "3"):
			print("			-=--GERADOR DE TROCAS--=-")
			print("Comerciantes:")
			for usuario in usuarios:
				print("	" + usuario.nome)
				cont = 0
				for pedido in pedidos:
					if pedido.user == usuario:
						cont += 1
						print("	" + "Pedido " + str(cont) + ":")
						print("	Oferta: " + pedido.oferta.nome)
						print("	Demanda: " + pedido.demanda.nome)
			input()
			os.system('cls' if os.name == 'nt' else 'clear')
	return 0

main()
