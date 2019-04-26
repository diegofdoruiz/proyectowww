from rolepermissions.roles import AbstractUserRole

class Cliente(AbstractUserRole):
    available_permissions = {
        'pedir_turno': True,
        'ver_pantalla': True,
    }

class Administrador(AbstractUserRole):
    available_permissions = {
        'consignaciones': True,
        'retiros': True,
        'pagos': True,
        'importaciones': True,
        'exportaciones': True,
        'seguros': True,
        'dolares': True,
        'vip': True,
        'pedir_turno': True,
        'ver_pantalla': True,
    }


class Cajero(AbstractUserRole):
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