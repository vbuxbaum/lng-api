BAD_MESSAGES = [
    (
        "os estudantes",
        (
            "Olá mundo! *ESSA* é uma mensagem de exemplo"
            "considerando o uso do seguinte termo: os estudantes."
        ),
    ),
    (
        "muitos estudantes",
        (
            "Olá mundo! *ESSA* é uma mensagem de exemplo"
            "considerando o uso do seguinte termo: muitos estudantes."
        ),
    ),
    (
        "poucos estudantes",
        (
            "Olá mundo! *ESSA* é uma mensagem de exemplo"
            "considerando o uso do seguinte termo: *_poucos_* estudantes."
        ),
    ),
    (
        "tranquilos e tranquilas",
        (
            "Olá mundo! ~ESSA~ é uma mensagem de exemplo"
            "considerando o uso do seguinte termo: tranquilos e tranquilas."
        ),
    ),
]

GOOD_MESSAGES = [
    (
        "Olá mundo! *ESSA* é uma mensagem de exemplo"
        "considerando o uso do seguinte termo: identificarmos estudantes."
    ),
    (
        "Olá mundo! *ESSA* é uma mensagem de exemplo"
        "considerando o uso do seguinte termo: comunicamos estudantes."
    ),
    ("Olá mundo! ~ESSA~ é uma mensagem de exemplo"),
    ("Olá mundo! ~ESSA~ é uma mensagem de exemplo"),
]
