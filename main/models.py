from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

class Colaborador(models.Model):
    OPCOES_DEPARTAMENTOS = [
        ("FINACEIRO","FINACEIRO"),
        ("CENTRAL_ATENDIMENTO","CENTRAL DE ATENDIMENTO"),
        ("CENTRAL_INADIMPLENCIA","CENTRAL DE INADIMPLENCIA"),
        ("COBRANCA","COBRANÇA"),
        ("CONTROLE_QUALIDADE","CONTROLE DE QUALIDADE"),
        ("REAL_CREDIT","REAL CREDIT"),
        ("RELACIONAMENTO","RELACIONAMENTO"),
        ("COMERCIAL","COMERCIAL"),
        ("RH","RH"),
        ("DEP_PESSOAL","DEPARTAMENTO PESSOAL"),
        ("JURIDICO","JURIDICO"),
        ("CONTABIL","CONTABIL"),
        ("CENTRAL_VENDAS","CENTRAL DE VENDAS"),
        ("SUPORTE_ADM","SUPORTE ADM"),
        ("FRANQUIAS_DISTRIBUIDORES","FRANQUIAS / DISTRIBUIDORES"),
        ("GERENCIA_CORPORATIVA","GERENCIA CORPORATIVA"),
        ("DIRETORIA_EXECUTIVA","DIRETORIA EXECUTIVA"),
        ("INFORMATICA","INFORMÁTICA"),
    ]

    OPCOES_CLASSIFICACAO = [
        ("ESTAGIARIO","ESTAGIARIO"),
        ("FUNCIONARIO","FUNCIONARIO"),
        ("MEI","MEI"),
        ]
    OPCOES_ESTADO_CIVIL = [
        ("SOLTEIRO","SOLTEIRO(a)"),
        ("CASADO","CASADO(a)"),
        ("DIVORCIADO","DIVORCIADO(a)"),
        ("SEPARADO","SEPARADO(a)"),
        ("VIUVO","VIUVO(a)"),
        ]
    OPCOES_SEXO = (
        ("MASCULINO", "MASCULINO"),
        ("FEMININO", "FEMININO"),
        ("OUTRO", "OUTRO"),
        ("PREFERE_NAO_INFORMAR", "PREFERE NAO INFORMAR"),
    )
    matricula = models.IntegerField()
    nome = models.CharField(max_length=254, blank=False)
    nome_mae = models.CharField(max_length=254, blank=False)
    nome_pai = models.CharField(max_length=254, blank=False)
    nome_conjuge = models.CharField(max_length=254, blank=False)
    cpf = models.CharField(max_length=14, blank=False)
    cpf_mae = models.CharField(max_length=14, blank=False)
    cpf_pai = models.CharField(max_length=14, blank=False)
    data_nascimento = models.DateField(blank=False)
    estado_civil = models.CharField(max_length=20,choices=OPCOES_ESTADO_CIVIL,default='')
    naturalidade = models.CharField(max_length=50)
    estado_naturalidade = models.CharField(max_length=50)
    sexo = models.CharField(max_length=20,choices=OPCOES_SEXO,default='')
    email = models.EmailField()
    foto = models.ImageField(upload_to="fotos/%Y/%m/%d/", blank=True)
    telefone = models.CharField(blank=True,max_length=15)
    tel_auxiliar = models.CharField(blank=True,max_length=15)
    profissao = models.CharField(max_length=100)
    profissao_pai = models.CharField(max_length=100)
    profissao_mae = models.CharField(max_length=100)
    profissao_conjuge = models.CharField(max_length=100)
    departamento = models.TextField(max_length=150, choices=OPCOES_DEPARTAMENTOS, default='')
    classificacao = models.TextField(max_length=150, choices=OPCOES_CLASSIFICACAO, default='')
    data_entrada = models.DateField(default=datetime.now,blank=False)
    data_saida = models.DateField(blank=True, null=True)
    observacao = models.TextField()
    ativo_inativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="colaborador")

    def __str__(self):
        return self.nome
    
class Contrato(models.Model):
    PERIODO_CHOICES = (
        ("1", "PRIMEIRO"),
        ("2", "SEGUNDO"),
        ("3", "TERCEIRO"),
        ("4", "QUARTO"),
    )
    num_contrato = models.CharField(max_length=50,blank=False, null=False)
    periodo = models.CharField(max_length=1,choices=PERIODO_CHOICES, blank=False, null=False)
    data_inicio = models.DateField(default=datetime.now,blank=False)
    data_termino = models.DateField(blank=True, null=True)
    contrato = models.FileField(upload_to ="contratos")
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE,related_name="contrato")

    def __str__(self):
        return self.periodo
    
class Endereco(models.Model):
    OPCOES_ESTADOS = (
        ("AC", "Acre"),
        ("AL", "Alagoas"),
        ("AP", "Amapá"),
        ("AM", "Amazonas"),
        ("BA", "Bahia"),
        ("CE", "Ceará"),
        ("DF", "Distrito Federal"),
        ("ES", "Espírito Santo"),
        ("GO", "Goiás"),
        ("MA", "Maranhão"),
        ("MT", "Mato Grosso"),
        ("MS", "Mato Grosso do Sul"),
        ("MG", "Minas Gerais"),
        ("PA", "Pará"),
        ("PB", "Paraíba"),
        ("PR", "Paraná"),
        ("PE", "Pernambuco"),
        ("PI", "Piauí"),
        ("RJ", "Rio de Janeiro"),
        ("RN", "Rio Grande do Norte"),
        ("RS", "Rio Grande do Sul"),
        ("RO", "Rondônia"),
        ("RR", "Roraima"),
        ("SC", "Santa Catarina"),
        ("SP", "São Paulo"),
        ("SE", "Sergipe"),
        ("TO", "Tocantins"),
    )
    logradouro = models.CharField(max_length=50,blank=False, null=False)
    cep = models.CharField(max_length=8,blank=False, null=False)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2,choices=OPCOES_ESTADOS)
    colaborador = models.ForeignKey(Colaborador,on_delete=models.CASCADE,related_name="endereco")

    def __str__(self):
        return self.cep
    
class Documentacao(models.Model):
    TIPO_PIX = (
        ('CPF','CPF'),
        ('EMAIL','EMAIL'),
        ('NUM_TELEFONE','NUM_TELEFONE'),
        ('CHAVE_ALEATORIA','CHAVE ALEATORIA')
    )
    num_carteira_profissional = models.CharField(max_length=50)
    serie = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    rg = models.CharField(max_length=50)
    orgao_exp = models.CharField(max_length=50)
    data_exp = models.DateField()
    num_reservista = models.CharField(max_length=50)
    serie_reservista = models.CharField(max_length=50)
    reg_militar = models.CharField(max_length=100)
    titulo_eleitor = models.CharField(max_length=50)
    zona_eleitoral = models.CharField(max_length=50)
    secao_eleitoral = models.CharField(max_length=50)
    pis_pasep = models.CharField(max_length=50)
    habilitacao = models.CharField(max_length=50)
    data_emissao_habilitacao = models.DateField()
    categoria_habilitacao = models.CharField(max_length=5)
    banco = models.CharField(max_length=50)
    agencia = models.CharField(max_length=50)
    conta = models.CharField(max_length=50)
    tipo_pix = models.CharField(max_length=50,choices=TIPO_PIX)
    pix = models.CharField(max_length=50)
    colaborador = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)

    def __str__(self):
        return self.rg

class Desenvolvimento_Profissional(models.Model):
    OPCOES_FUNDAMENTAL = (
        ('COMPLETO','COMPLETO'),
        ('INCOMPLETO','INCOMPLETO')
    )
    NIVEIS_INFORMATICA = (
        ('BASICO','BASICO'),
        ('INTERMEDIARIO','INTERMEDIARIO'),
        ('AVANCADO','AVANCADO'),
    )
    ensino_fundamental = models.CharField(max_length=50,choices=OPCOES_FUNDAMENTAL)
    fundamental_instituicao = models.CharField(max_length=100)
    fundamental_ano_conclusao = models.CharField(max_length=4)
    ensino_medio = models.CharField(max_length=50,choices=OPCOES_FUNDAMENTAL)
    medio_instituicao = models.CharField(max_length=100)
    medio_ano_conclusao = models.CharField(max_length=4)
    informatica_nivel = models.CharField(max_length=50,choices=NIVEIS_INFORMATICA)
    informatica_instituicao = models.CharField(max_length=100)
    informatica_ano_conclusao = models.CharField(max_length=4)
    contabilidade_nivel = models.CharField(max_length=100)
    contabilidade_instituicao = models.CharField(max_length=100)
    contabilidade_ano_conclusao = models.CharField(max_length=4)
    administracao_nivel = models.CharField(max_length=100)
    administracao_instituicao = models.CharField(max_length=100)
    administracao_ano_conclusao = models.CharField(max_length=4)
    colaborador = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)

    def __str__(self):
        return self.ensino_fundamental

class Exp_Profissional(models.Model):
    empresa = models.CharField(max_length=100)
    logradouro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    telefone = models.CharField(blank=True,max_length=15)
    funcao_inicial = models.CharField(max_length=100)
    funcao_final = models.CharField(max_length=100)
    salario_inicial = models.CharField(max_length=50)
    salario_final = models.CharField(max_length=50)
    data_admissao = models.DateField()
    data_recisao = models.DateField()
    motivo_recisao = models.TextField()
    colaborador = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    
    def __str__(self):
        return self.empresa
    
class Referencias_Pessoais(models.Model):
    nome = models.CharField(max_length=100)
    logradouro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    telefone = models.CharField(blank=True,max_length=15)
    profissao = models.CharField(max_length=100)
    colaborador = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome

class Canal_Divulgacao(models.Model):
    CANAIS = (
        ('INSTITUICAO_ENSINO','INSTITUICAO DE ENSINO'),
        ('AGENCIA_EMPREGO','AGENCIA DE EMPREGO'),
        ('INDICACAO','INDICACAO'),
        ('JORNAL','JORNAL'),
        ('OUTROS','OUTROS'),
    )
    canal_divulgacao = models.CharField(max_length=100,choices=CANAIS)
    colaborador = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    
    def __str__(self):
        return self.canal_divulgacao


#TODO:verificar dados obrigatorios e depois terminar os formularios