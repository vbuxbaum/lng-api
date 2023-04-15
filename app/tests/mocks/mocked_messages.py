from src.data_model import LNGReport

BAD_MESSAGES = [
    (
        LNGReport(used_expression="muitooos estudantes ativos"),
        "Sobre isso que são muitooos estudantes ativos e algo mais.",
    ),
    (
        LNGReport(used_expression="estudantes aprovados"),
        "Sobre estudantes aprovados e algo mais.",
    ),
    (
        LNGReport(used_expression="muitos usuários"),
        "Sobre termos muitos _usuarios_. e algo mais",
    ),
    (
        LNGReport(used_expression="poucos usuários"),
        "Sobre termos *poucos* usuarios e algo mais.",
    ),
    (
        LNGReport(used_expression="usuários desligados"),
        "Sobre [usuários] desligados e algo mais.",
    ),
    (
        LNGReport(used_expression="poucos estudantes"),
        "Sobre *_poucos estudantes_* e algo mais.",
    ),
    (
        LNGReport(used_expression="alguns estudantes"),
        "Sobre alguns estudantes e algo mais.",
    ),
    (
        LNGReport(used_expression="instrutores"),
        "Sobre somente instrutores e algo mais.",
    ),
    (
        LNGReport(used_expression="trabalhadores"),
        "Sobre somente serem trabalhadores e algo mais.",
    ),
    (
        LNGReport(used_expression="estudantes campeões"),
        "Estudantes campeões testando no início.",
    ),
    (
        LNGReport(used_expression="aos estudantes"),
        "Sobre agradecer aos estudantes.",
    ),
]

GOOD_MESSAGES = [
    ("Sobre identificarmos estudantes."),
    ("Sobre dizer que nós comunicamos estudantes."),
    ("Sobre estudantes ativas não há problema"),
    ("Sobre muitos. Estudantes não deveriam ser problema"),
    ("Sobre Estudantes. Ativos não deveriam ser problema"),
    ("Sobre emoji :green_heart: e pessoas instrutoras"),
    ("Sobre pessoas estudantes campeãs"),
    ("Sobre observar estudantes nos jornais"),
    ("Sobre grupo das pessoas estudantes nos escritórios"),
    ("Sobre disponibilizar para estudantes uns benefícios"),
    ("Estudantes não podem ter prejuízo com essa mensagem"),
]
