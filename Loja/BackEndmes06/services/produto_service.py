from models.models import Produto, db

def listar_produtos(busca: str = None) -> list[Produto]:
    """Retorna a lista de produtos cadastrados no estoque, com suporte a busca."""
    query = db.session.query(Produto)
    if busca:
        termo = f"%{busca.strip()}%"
        query = query.filter(
            Produto.nome_produto.ilike(termo) | Produto.descricao_produto.ilike(termo)
        )
    return query.order_by(Produto.id_p.desc()).all()

def obter_produto(id_p: int) -> Produto:
    """Busca um produto pelo seu ID."""
    return db.session.query(Produto).filter_by(id_p=id_p).first()

def criar_produto(nome_produto: str, valor: str | float, qtd_produto: str | int, descricao_produto: str = "") -> Produto:
    """Cadastra um novo produto no estoque (CREATE)."""
    if not nome_produto or not str(nome_produto).strip():
        raise ValueError("O nome do produto é obrigatório.")
    
    if valor is None or str(valor).strip() == "":
        raise ValueError("O valor unitário do produto é obrigatório.")
    
    if qtd_produto is None or str(qtd_produto).strip() == "":
        raise ValueError("A quantidade de estoque é obrigatória.")

    try:
        valor_limpo = str(valor).strip().replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".") if "," in str(valor) else str(valor).strip().replace("R$", "").replace(" ", "")
        valor_final = float(valor_limpo)
        if valor_final < 0:
            raise ValueError
    except ValueError:
        raise ValueError("Por favor, informe um valor numérico válido para o preço (Ex: 150.00).")

    try:
        qtd_final = int(qtd_produto)
        if qtd_final < 0:
            raise ValueError
    except ValueError:
        raise ValueError("A quantidade de estoque deve ser um número inteiro igual ou maior que zero.")

    produto = Produto(
        nome_produto=nome_produto.strip(),
        valor=valor_final,
        qtd_produto=qtd_final,
        descricao_produto=(descricao_produto or "").strip()
    )
    db.session.add(produto)
    db.session.commit()
    return produto

def atualizar_produto(id_p: int, nome_produto: str, valor: str | float, qtd_produto: str | int, descricao_produto: str = "") -> Produto:
    """Atualiza as informações de um produto existente (UPDATE)."""
    produto = obter_produto(id_p)
    if not produto:
        raise ValueError("Produto não encontrado no sistema.")

    if not nome_produto or not str(nome_produto).strip():
        raise ValueError("O nome do produto é obrigatório.")
    
    if valor is None or str(valor).strip() == "":
        raise ValueError("O valor unitário do produto é obrigatório.")
    
    if qtd_produto is None or str(qtd_produto).strip() == "":
        raise ValueError("A quantidade de estoque é obrigatória.")

    try:
        valor_limpo = str(valor).strip().replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".") if "," in str(valor) else str(valor).strip().replace("R$", "").replace(" ", "")
        valor_final = float(valor_limpo)
        if valor_final < 0:
            raise ValueError
    except ValueError:
        raise ValueError("Por favor, informe um valor numérico válido para o preço.")

    try:
        qtd_final = int(qtd_produto)
        if qtd_final < 0:
            raise ValueError
    except ValueError:
        raise ValueError("A quantidade deve ser um número inteiro igual ou superior a zero.")

    produto.nome_produto = nome_produto.strip()
    produto.valor = valor_final
    produto.qtd_produto = qtd_final
    produto.descricao_produto = (descricao_produto or "").strip()
    db.session.commit()
    return produto

def adicionar_estoque(id_p: int, quantidade: int = 1) -> tuple[bool, str]:
    """Registra entrada de unidades no estoque de um produto."""
    produto = obter_produto(id_p)
    if not produto:
        return False, "Produto não encontrado."
    
    if quantidade <= 0:
        return False, "A quantidade de entrada deve ser maior que zero."

    produto.qtd_produto = (produto.qtd_produto or 0) + quantidade
    db.session.commit()
    return True, f"Entrada de +{quantidade} unidade(s) adicionada a '{produto.nome_produto}'. Novo estoque: {produto.qtd_produto}."

repor_estoque = adicionar_estoque

def remover_estoque(id_p: int, quantidade: int = 1) -> tuple[bool, str]:
    """Registra saída/baixa de unidades do estoque de um produto."""
    produto = obter_produto(id_p)
    if not produto:
        return False, "Produto não encontrado."
    
    if quantidade <= 0:
        return False, "A quantidade para saída deve ser de no mínimo 1 unidade."

    estoque_atual = produto.qtd_produto or 0
    if estoque_atual <= 0:
        return False, f"O item '{produto.nome_produto}' já se encontra com estoque esgotado."

    if estoque_atual < quantidade:
        return False, f"Estoque insuficiente. Restam apenas {estoque_atual} unidade(s) no sistema."

    produto.qtd_produto = estoque_atual - quantidade
    db.session.commit()
    return True, f"Saída de -{quantidade} unidade(s) registrada para '{produto.nome_produto}'. Novo estoque: {produto.qtd_produto}."

baixar_estoque = remover_estoque
comprar_produto = remover_estoque

def excluir_produto(id_p: int) -> tuple[bool, str]:
    """Exclui definitivamente um produto do sistema (DELETE)."""
    produto = obter_produto(id_p)
    if not produto:
        return False, "Produto não encontrado."
    
    nome = produto.nome_produto
    db.session.delete(produto)
    db.session.commit()
    return True, f"Produto '{nome}' excluído com sucesso do estoque."

remover_produto = excluir_produto
