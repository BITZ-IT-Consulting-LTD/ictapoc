import base64
import uuid
import hashlib
from django.core.files.base import ContentFile
from .models import Document, DocumentVersion, ArtifactType, Artifact

def create_document_from_base64(user, title, base64_content, document_type='personal', classification='internal', metadata=None):
    """
    Utility to create a Document and its first version from a base64 string.
    """
    if not base64_content:
        return None

    mime_type = 'application/pdf' # Default
    # Handle data:uri format if present
    if ';base64,' in base64_content:
        header, content = base64_content.split(';base64,')
        if ':' in header:
            mime_type = header.split(':')[1]
    else:
        content = base64_content

    # Determine extension from mime_type
    import mimetypes
    ext = mimetypes.guess_extension(mime_type) or '.pdf'

    decoded_file = base64.b64decode(content)
    
    # Generate a filename
    from django.utils.text import slugify
    filename = f"{slugify(title)}{ext}"
        
    file_content = ContentFile(decoded_file, name=filename)
    file_size = len(decoded_file)
    checksum = hashlib.sha256(decoded_file).hexdigest()
    
    doc = Document.objects.create(
        title=title,
        document_type=document_type,
        classification_level=classification,
        uploaded_by=user,
        owner_mda=user.mda if hasattr(user, 'mda') and user.mda else None,
        metadata=metadata or {},
        current_version_number=1,
        linked_entity=user # Link directly to User via GFK
    )
    
    DocumentVersion.objects.create(
        document=doc,
        version_number=1,
        file=file_content,
        file_size=file_size,
        mime_type=mime_type,
        checksum=checksum,
        uploaded_by=user,
        change_summary="Initial capture from Citizen Interface"
    )
    
    return doc
