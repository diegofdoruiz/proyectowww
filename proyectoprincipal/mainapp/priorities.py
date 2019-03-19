from .models import Turn, LocationOnService


class cola():
	turnos = Turn.objects.get(status='1')
	atendiendo = LocationOnService.objects.get(status='1', is_online = True)
	def contruir_cola(self):
		return self.atendiendo

