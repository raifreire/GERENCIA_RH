from rolepermissions.roles import AbstractUserRole

class Admin(AbstractUserRole):
    available_permissions = {
        'add_colaborador': True,       
        'change_colaborador': True,
        'delete_colaborador': True,
        'view_colaborador': True,
        'add_contrato': True,
        'change_contrato': True,
        'delete_contrato': True,
        'view_contrato': True,
    }

class Padrao(AbstractUserRole):
    available_permissions = {
        'view_colaborador': True,
        'view_contrato': True,
    }