from rest_framework import serializers
from .models import Folder, FolderImage

class FolderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderImage
        fields = ('id', 'image')

class FolderSerializer(serializers.ModelSerializer):
    # Serializa las imágenes actuales
    images = FolderImageSerializer(many=True, read_only=True)
    # Para subir nuevas imágenes
    image_files   = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        help_text="Sube aquí una o más imágenes."
    )
    # Para eliminar imágenes existentes por su ID
    remove_images = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text="IDs de imágenes a eliminar."
    )

    class Meta:
        model = Folder
        fields = [
            'id', 'name', 'description',
            'start_date', 'end_date', 'created_at',
            'images', 'image_files', 'remove_images'
        ]
        read_only_fields = ['created_at']

    def create(self, validated_data):
        files_to_add = validated_data.pop('image_files', [])
        folder = super().create(validated_data)
        for img in files_to_add:
            FolderImage.objects.create(folder=folder, image=img)
        return folder

    def update(self, instance, validated_data):
        # Extraemos listas de archivos a añadir y IDs a eliminar
        files_to_add = validated_data.pop('image_files', [])
        ids_to_remove = validated_data.pop('remove_images', [])

        # Actualizamos los campos básicos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Eliminamos imágenes marcadas
        if ids_to_remove:
            FolderImage.objects.filter(folder=instance, id__in=ids_to_remove).delete()

        # Añadimos nuevas imágenes
        for img in files_to_add:
            FolderImage.objects.create(folder=instance, image=img)

        return instance