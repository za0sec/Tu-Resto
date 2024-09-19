from rest_framework import serializers

class TextMessageSerializer(serializers.Serializer):
    from_ = serializers.CharField(source='from')
    id = serializers.CharField()
    timestamp = serializers.CharField()
    type = serializers.CharField()
    text = serializers.DictField()
    
    def to_representation(self, instance):
        # Ajusta la clave 'text' para que coincida con 'body'
        ret = super().to_representation(instance)
        ret['text'] = ret['text'].get('body')
        return ret

class ContactSerializer(serializers.Serializer):
    profile = serializers.DictField()
    wa_id = serializers.CharField()

class MetadataSerializer(serializers.Serializer):
    display_phone_number = serializers.CharField()
    phone_number_id = serializers.CharField()

class WhatsappMessageValueSerializer(serializers.Serializer):
    messaging_product = serializers.CharField()
    metadata = MetadataSerializer()
    contacts = ContactSerializer(many=True)
    messages = TextMessageSerializer(many=True)

class WhatsappMessageSerializer(serializers.Serializer):
    object = serializers.CharField()
    entry = serializers.ListField(child=serializers.DictField())
    
    def to_internal_value(self, data):
        # Ajusta la estructura para reflejar los datos anidados
        entry = data.get('entry', [{}])[0]
        changes = entry.get('changes', [{}])[0]
        value = changes.get('value', {})
        
        return {
            'messaging_product': value.get('messaging_product'),
            'metadata': value.get('metadata', {}),
            'contacts': value.get('contacts', []),
            'messages': value.get('messages', [])
        }

    def validate(self, data):
        # Validaciones globales si es necesario
        if not data.get('metadata') or not data.get('contacts') or not data.get('messages'):
            raise serializers.ValidationError("Faltan datos necesarios")
        return data
