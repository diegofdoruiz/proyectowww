from rolepermissions.roles import AbstractUserRole

class Cliente(AbstractUserRole):
    available_permissions = {
        'pedir_turno': True,
        'ver_pantalla': True,
    }

class Administrador(AbstractUserRole):
    available_permissions = {
        'edit_patient_file': True,
    }


class Cajero_G(AbstractUserRole):
    available_permissions = {
        'consignaciones': True,
        'retiros': True,
        'pagos': True,
        'importaciones': True,
        'exportaciones': True,
        'seguros': True,
        'dolares': True,
        'vip': True,
    }

class Cajero_IE(AbstractUserRole):
    available_permissions = {
        'consignaciones': True,
        'retiros': True,
        'pagos': True,
        'importaciones': True,
        'exportaciones': True,
        'seguros': True,
        'dolares': True,
        'vip': True,
    }

class Cajero_S(AbstractUserRole):
    available_permissions = {
        'consignaciones': True,
        'retiros': True,
        'pagos': True,
        'importaciones': True,
        'exportaciones': True,
        'seguros': True,
        'dolares': True,
        'vip': True,
    }

class Cajero_D(AbstractUserRole):
    available_permissions = {
        'consignaciones': True,
        'retiros': True,
        'pagos': True,
        'importaciones': True,
        'exportaciones': True,
        'seguros': True,
        'dolares': True,
        'vip': True,
    }

class Cajero_VIP(AbstractUserRole):
    available_permissions = {
        'consignaciones': True,
        'retiros': True,
        'pagos': True,
        'importaciones': True,
        'exportaciones': True,
        'seguros': True,
        'dolares': True,
        'vip': True,
    }