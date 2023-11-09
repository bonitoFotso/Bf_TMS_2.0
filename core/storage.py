from django.core.files.storage import FileSystemStorage
from django.conf import settings

class CustomStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None):
        if location is None:
            location = settings.MEDIA_ROOT
        if base_url is None:
            base_url = settings.MEDIA_URL
        super().__init__(location, base_url)

    def _save(self, name, content):
        # Gérez ici le téléchargement de l'image et l'utilisation de l'image d'avatar par défaut si l'image n'est pas définie
        # Par exemple, vous pouvez vérifier si `name` est vide et utiliser l'image d'avatar par défaut à la place.
        if not name:
            # Utilisez l'image d'avatar par défaut ici
            name = 'avatars/img.png'
        return super()._save(name, content)
