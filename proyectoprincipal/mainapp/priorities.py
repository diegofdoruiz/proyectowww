from .models import Turn


class cola():
	turnos = Turn.objects.all()
	turnos = Turn.objects.get(status='1')
	def contruir_cola():
