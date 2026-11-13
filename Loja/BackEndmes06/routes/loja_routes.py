from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.produto_service import (
    listar_produtos,
    obter_produto,
    criar_produto,
    atualizar_produto,
    adicionar_estoque,
    remover_estoque,
    excluir_produto
)

loja_bp = Blueprint('loja', __name__, url_prefix='/loja', template_folder='templates')

# READ: Listagem e Painel Geral de Estoque
@loja_bp.route('/', methods=['GET'])
@loja_bp.route('/produtos', methods=['GET'])
def index():
    busca = request.args.get('busca', '').strip()
    produtos = listar_produtos(busca=busca if busca else None)
    
    # Métricas Gerenciais de Estoque
    total_produtos = len(produtos)
    total_unidades = sum(p.qtd_produto or 0 for p in produtos)
    valor_total_estoque = sum((p.valor or 0.0) * (p.qtd_produto or 0) for p in produtos)
    disponiveis = sum(1 for p in produtos if p.qtd_produto and p.qtd_produto > 0)
    esgotados = sum(1 for p in produtos if not p.qtd_produto or p.qtd_produto <= 0)
    estoque_baixo = sum(1 for p in produtos if p.qtd_produto and 0 < p.qtd_produto <= 5)
    
    return render_template(
        'loja.html',
        produtos=produtos,
        busca=busca,
        total_produtos=total_produtos,
        total_unidades=total_unidades,
        valor_total_estoque=valor_total_estoque,
        disponiveis=disponiveis,
        esgotados=esgotados,
        estoque_baixo=estoque_baixo
    )

# CREATE: Cadastro de Novo Produto
@loja_bp.route('/cadastrar', methods=['GET', 'POST'])
@loja_bp.route('/adicionar', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        nome_produto = request.form.get('nome_produto')
        valor = request.form.get('valor')
        qtd_produto = request.form.get('qtd_produto')
        descricao_produto = request.form.get('descricao_produto')

        try:
            produto = criar_produto(nome_produto, valor, qtd_produto, descricao_produto)
            flash(f"Produto '{produto.nome_produto}' cadastrado com sucesso no estoque!", 'success')
            return redirect(url_for('loja.index'))
        except ValueError as e:
            flash(str(e), 'danger')
            return render_template(
                'cadastro_produto.html',
                nome_produto=nome_produto,
                valor=valor,
                qtd_produto=qtd_produto,
                descricao_produto=descricao_produto
            )

    return render_template('cadastro_produto.html')

# UPDATE: Edição de Produto Existente
@loja_bp.route('/editar/<int:id_p>', methods=['GET', 'POST'])
def editar_produto(id_p):
    produto = obter_produto(id_p)
    if not produto:
        flash("Produto não encontrado no sistema.", "danger")
        return redirect(url_for('loja.index'))

    if request.method == 'POST':
        nome_produto = request.form.get('nome_produto')
        valor = request.form.get('valor')
        qtd_produto = request.form.get('qtd_produto')
        descricao_produto = request.form.get('descricao_produto')

        try:
            atualizar_produto(id_p, nome_produto, valor, qtd_produto, descricao_produto)
            flash(f"Produto '{produto.nome_produto}' atualizado com sucesso!", 'success')
            return redirect(url_for('loja.index'))
        except ValueError as e:
            flash(str(e), 'danger')
            return render_template('editar_produto.html', produto=produto)

    return render_template('editar_produto.html', produto=produto)

# UPDATE: Entrada Rápida de Estoque (+)
@loja_bp.route('/entrada/<int:id_p>', methods=['POST'])
@loja_bp.route('/repor/<int:id_p>', methods=['POST'])
def entrada_estoque(id_p):
    try:
        quantidade = int(request.form.get('quantidade', 1))
    except (ValueError, TypeError):
        quantidade = 1

    sucesso, mensagem = adicionar_estoque(id_p, quantidade=quantidade)
    flash(mensagem, 'success' if sucesso else 'danger')
    return redirect(url_for('loja.index'))

# UPDATE: Saída / Baixa Rápida de Estoque (-)
@loja_bp.route('/saida/<int:id_p>', methods=['POST'])
@loja_bp.route('/comprar/<int:id_p>', methods=['POST'])
def saida_estoque(id_p):
    try:
        quantidade = int(request.form.get('quantidade', 1))
    except (ValueError, TypeError):
        quantidade = 1

    sucesso, mensagem = remover_estoque(id_p, quantidade=quantidade)
    flash(mensagem, 'success' if sucesso else 'danger')
    return redirect(url_for('loja.index'))

# DELETE: Remoção de Produto do Sistema
@loja_bp.route('/excluir/<int:id_p>', methods=['POST'])
@loja_bp.route('/remover/<int:id_p>', methods=['POST'])
def excluir(id_p):
    sucesso, mensagem = excluir_produto(id_p)
    flash(mensagem, 'success' if sucesso else 'danger')
    return redirect(url_for('loja.index'))
