# from django.conf.urls import url
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

# from mainapp.consumers import ChatConsumer
# application = ProtocolTypeRouter({
#     # Empty for now (http->django views is added by default)
#     # 'websocket': AllowedHostsOriginValidator(
#     'websocket': AuthMiddlewareStack(
#     	URLRouter(
#     		[
#     			url(r"^mainapp/(?P<username>[\w.@+-]+)$", ChatConsumer),
#     		]
#     	)
#     )
# })

# from django.conf.urls import url
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

# from mainapp.consumers import ChatConsumer
# application = ProtocolTypeRouter({
#     # Empty for now (http->django views is added by default)
#     # 'websocket': AllowedHostsOriginValidator(
#     'websocket': AuthMiddlewareStack(
#     	URLRouter(
#     		[
#     			#url(r"^mainapp/chat/(?P<username>[\w.@+-]+)$", ChatConsumer),
#     			url(r'^ws/mainapp/(?P<room_name>[^/]+)/$', ChatConsumer),
#     		]
#     	)
#     )
# })


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import mainapp.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            mainapp.routing.websocket_urlpatterns
        )
    ),
})