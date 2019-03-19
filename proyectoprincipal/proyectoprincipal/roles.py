from rolepermissions.roles import AbstractUserRole

class Cliente(AbstractUserRole):
    available_permissions = {
        'create_medical_record': True,
        'can_add_user': True,
    }

class Cajero(AbstractUserRole):
    available_permissions = {
        'edit_patient_file': True,
    }

class Administrador(AbstractUserRole):
    available_permissions = {
        'edit_patient_file': True,
    }