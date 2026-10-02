BASE_URL=http://localhost:5000

help:
	@echo ""
	@echo "Exemplos de uso da API REST"
	@echo ""
	@echo "make get-all"
	@echo "make get ID=1"
	@echo "make head ID=1"
	@echo "make post NOME='Mouse' PRECO=80"
	@echo "make put ID=1 NOME='Teclado Mecânico' PRECO=250"
	@echo "make patch-nome ID=1 NOME='Teclado Gamer'"
	@echo "make patch-preco ID=1 PRECO=199"
	@echo "make delete ID=1"
	@echo "make raw-get ID=1"
	@echo "make verbose-get ID=1"
	@echo ""

get-all:
	curl -i $(BASE_URL)/itens

get:
	curl -i $(BASE_URL)/itens/$(ID)

head:
	curl -I $(BASE_URL)/itens/$(ID)

post:
	curl -i \
		-X POST \
		-H "Content-Type: application/json" \
		-d '{"nome":"$(NOME)","preco":$(PRECO)}' \
		$(BASE_URL)/itens

put:
	curl -i \
		-X PUT \
		-H "Content-Type: application/json" \
		-d '{"nome":"$(NOME)","preco":$(PRECO)}' \
		$(BASE_URL)/itens/$(ID)

patch-nome:
	curl -i \
		-X PATCH \
		-H "Content-Type: application/json" \
		-d '{"nome":"$(NOME)"}' \
		$(BASE_URL)/itens/$(ID)

patch-preco:
	curl -i \
		-X PATCH \
		-H "Content-Type: application/json" \
		-d '{"preco":$(PRECO)}' \
		$(BASE_URL)/itens/$(ID)

delete:
	curl -i \
		-X DELETE \
		$(BASE_URL)/itens/$(ID)

raw-get:
	curl $(BASE_URL)/itens/$(ID)

verbose-get:
	curl -v $(BASE_URL)/itens/$(ID)

options:
	curl -i -X OPTIONS $(BASE_URL)/itens/$(ID)

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -prune -exec rm -rf {} +