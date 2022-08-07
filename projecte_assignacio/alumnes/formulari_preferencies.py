"""Form object declaration."""
from wtforms import Form, SelectField

seleccio = [
    ("1","1"),
    ("2","2"),
    ("3","3"),
    ("4","4"),
    ("5","5"),
    ("6","6"),
    ("7","7"),
    ("8","8"),
    ("9","9"),
    ("10","10")
]

class PreferenciesASIR(Form):
    administrador_de_sistemes = SelectField(
        "Administrador de Sistemes",
        choices=seleccio
    )
    administrador_de_base_de_dades = SelectField(
        "Administrador de Base de Dades",
        choices=seleccio
    )
    administrador_de_xarxes = SelectField(
        "Administrador de Xarxes",
        choices=seleccio
    )
    ciberseguretat = SelectField(
        "Ciberseguretat",
        choices=seleccio
    )
    administrador_de_sistemes = SelectField(
        "Administrador de Sistemes",
        choices=seleccio
    )
    consultor_tic = SelectField(
        "Consultor TIC",
        choices=seleccio
    )
    tecnic_de_hardware = SelectField(
        "Tècnic de Hardware",
        choices=seleccio
    )
    tecnic_de_soport_helpdesk_l2 = SelectField(
        "Tècnic de Soport HelpDesk L2",
        choices=seleccio
    )
    auditor_tic = SelectField(
        "Auditor TIC",
        choices=seleccio
    )
    tecnic_de_monitoritzacio_de_xarxes = SelectField(
        "Tècnic de Monitorització de Xarxes",
        choices=seleccio
    )

class PreferenciesTSMR(Form):
    tecnic_de_microinformatica = SelectField(
        "Tècnic de Microinformàtica",
        choices=seleccio
    )
    asesor_de_microinformatica = SelectField(
        "Asesor/Venedor de Microinformàtica",
        choices=seleccio
    )
    tecnic_de_soport_helpdesk_l1 = SelectField(
        "Tècnic de Soport HelpDesk L1",
        choices=seleccio
    )
    instalador_de_xarxes_i_infraestructura_it = SelectField(
        "Instal·lador de Xarxes i Infraestructura IT",
        choices=seleccio
    )

class PreferenciesDAW(Form):
    desenvolupador_backend = SelectField(
        "Desenvolupador BackEnd",
        choices=seleccio
    )
    desenvolupador_frontend = SelectField(
        "Desenvolupador FrontEnd",
        choices=seleccio
    )
    desenvolupador_fullstack = SelectField(
        "Desenvolupador Fullstack",
        choices=seleccio
    )
    dissenyador = SelectField(
        "Dissenyador",
        choices=seleccio
    )
    tecnic_qa_i_documentacio = SelectField(
        "Tècnic QA i Documentació",
        choices=seleccio
    )
    devops = SelectField(
        "Devops",
        choices=seleccio
    )
    desenvolupador_de_aplicacions_movils = SelectField(
        "Desenvolupador d'Aplicacions Mòvils",
        choices=seleccio
    )
class PreferenciesDAW(Form):
    desenvolupador_backend = SelectField(
        "Desenvolupador BackEnd",
        choices=seleccio
    )
    desenvolupador_frontend = SelectField(
        "Desenvolupador FrontEnd",
        choices=seleccio
    )
    desenvolupador_fullstack = SelectField(
        "Desenvolupador Fullstack",
        choices=seleccio
    )
    dissenyador = SelectField(
        "Dissenyador",
        choices=seleccio
    )
    tecnic_qa_i_documentacio = SelectField(
        "Tècnic QA i Documentació",
        choices=seleccio
    )
    devops = SelectField(
        "Devops",
        choices=seleccio
    )
    desenvolupador_de_aplicacions_mobils = SelectField(
        "Desenvolupador d'Aplicacions Mòbils",
        choices=seleccio
    )

class PreferenciesDAM(Form):
    desenvolupador_backend = SelectField(
        "Desenvolupador BackEnd",
        choices=seleccio
    )
    desenvolupador_software_multiplataforma = SelectField(
        "Desenvolupador Software Multiplataforma",
        choices=seleccio
    )
    desenvolupador_de_videojocs = SelectField(
        "Desenvolupador de Videojocs",
        choices=seleccio
    )
    desenvolupador_de_aplicacions_mobils = SelectField(
        "Desenvolupador d'Aplicacions Mòbils",
        choices=seleccio
    )
    robotica_automocio_i_informatica_tradicional = SelectField(
        "Robòtica, Automoció i Informàtica Industrial",
        choices=seleccio
    )
    tecnic_qa_i_documentacio = SelectField(
        "Tècnic QA i Documentació",
        choices=seleccio
    )
    consultor_erp = SelectField(
        "Consultor ERP",
        choices=seleccio
    )