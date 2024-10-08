from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json
from rest_framework.permissions import AllowAny
from rest_framework import status
from apps.orders.models import TakeAwayOrder
from .serializers import WhatsappWebBotMessageSerializer


class WhatsappReceiver(APIView):
    ''' Autenticacion del webhook en meta '''
   
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Verificar el modo y el token enviados son correctos
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = int(request.GET.get('hub.challenge'))
        print(request)
        if mode == 'subscribe' and token == settings.WHATSAPP[0]['WEBHOOK_VERIFY_TOKEN']:
            # Responder con 200 OK y el token de desafío de la solicitud
            return Response(challenge, status=status.HTTP_200_OK)
        else:
            # Responder con '403 Forbidden' si los tokens de verificación no coinciden
            return Response(status=status.HTTP_403_FORBIDDEN)
        
    ''' Registrar mensajes entrantes '''
    def post(self, request):
        message_entries = request.data.get('entry', [])
        for entry in message_entries:
            changes = entry.get('changes', [])
            if not changes:
                continue
            entry_value = changes[0].get('value', {})
            if entry_value.get('field') != 'messages':
                continue
            messages = entry_value.get('messages', [])
            if not messages:
                continue
            for message in messages:
                if message.get('type') != 'text':
                    continue
                print(f"MENSAJE DE {message.get('from')}: {message.get('text', {}).get('body')}")
                self.handle_message_body(message.get('from'), message.get('text', {}).get('body'))
        return Response(status=status.HTTP_200_OK)
    
    def handle_message_body(self, phone_number, message_body):
        try:
            order = TakeAwayOrder.objects.get(id=message_body)
            order.phone_number = phone_number
            order.save()
        except TakeAwayOrder.DoesNotExist:
            print(f"No se encontró una orden con ID: {message_body}")
        except ValueError:
            print(f"ID de orden inválido: {message_body}")
  
      
class Whatsapp(APIView):
    permission_classes = [AllowAny]
    serializer = WhatsappWebBotMessageSerializer()
    
    def post(self, request):
        order_id = request.data.get('body')
        phone_number = request.data.get('phone_number')
        print(f"Mensaje de WhatsApp: {order_id}")
        handle_message_body_custom(phone_number, order_id)
        return Response(status=status.HTTP_200_OK)
    
def handle_message_body_custom(phone_number, order_id):
    try:
        order = TakeAwayOrder.objects.get(id=order_id)
        order.phone_number = phone_number
        order.save()
    except TakeAwayOrder.DoesNotExist:
        print(f"[DEBUG handle_message_body] No se encontró una orden con ID: {order_id}")
    except ValueError:
        print(f"[DEBUG handle_message_body] ID de orden inválido: {order_id}")


# BEEPERS
class LatestOrderWppUrl(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        branch = self.kwargs.get('branch')
        try:
            wpp_url = f"https://wa.me/{settings.WPP_BOT_API[0]['RECEIVER_PHONE_NUMBER']}?text=Hola!%20Tengo%20el%20pedido:%20{TakeAwayOrder.objects.filter(branch_id=branch).last().id}"
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_200_OK, data=wpp_url)
    
        
def send_whatsapp_message_meta_api(phone_number, body):
    url = f"https://graph.facebook.com/v20.0/{settings.WHATSAPP[0]['PHONE_NUMBER_ID']}/messages"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.WHATSAPP[0]['ACCESS_TOKEN']}"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": "+541158368985",                  #TODO phone_number
        "type": "text",
        "text": {
            "body": body
        }
    }
    
    respuesta = requests.post(url, headers=headers, data=json.dumps(data))
    
    if respuesta.status_code != 200:
        print(f"Error al enviar el mensaje: {respuesta.status_code} - {respuesta.text}")

def send_whatsapp_message(phone_number, message):
    url = f"{settings.WPP_BOT_URL}/send-message"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "phone_number": phone_number,
        "message": message
    }

    requests.post(url, headers=headers, data=json.dumps(data))

def notifyOrderReady(orden):
    msg = f"¡Tu pedido #{orden.id} está listo!"
    send_whatsapp_message(orden.phone_number, msg)