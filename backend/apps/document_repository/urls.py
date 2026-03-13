from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ArtifactViewSet, DocumentViewSet, ProjectPhaseViewSet, 
    ArtifactTypeViewSet, RegistryViewSet, NodeTypeViewSet, 
    NodeViewSet, RepositoryViewSet, ProjectViewSet
)
from .public_views import (
    PublicArtifactViewSet, PublicDocumentViewSet, PublicProjectPhaseViewSet,
    PublicArtifactTypeViewSet, PublicRegistryViewSet, PublicNodeTypeViewSet,
    PublicNodeViewSet
)

app_name = 'document_repository'

router = DefaultRouter()
router.register(r'types', ArtifactTypeViewSet, basename='artifact-type')
router.register(r'artifacts', ArtifactViewSet, basename='artifact')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'phases', ProjectPhaseViewSet, basename='project-phase')
router.register(r'registries', RegistryViewSet, basename='registry')
router.register(r'node-types', NodeTypeViewSet, basename='node-type')
router.register(r'nodes', NodeViewSet, basename='node')
router.register(r'repos', RepositoryViewSet, basename='repository')

public_router = DefaultRouter()
public_router.register(r'types', PublicArtifactTypeViewSet, basename='public-artifact-type')
public_router.register(r'artifacts', PublicArtifactViewSet, basename='public-artifact')
public_router.register(r'documents', PublicDocumentViewSet, basename='public-document')
public_router.register(r'phases', PublicProjectPhaseViewSet, basename='public-project-phase')
public_router.register(r'registries', PublicRegistryViewSet, basename='public-registry')
public_router.register(r'node-types', PublicNodeTypeViewSet, basename='public-node-type')
public_router.register(r'nodes', PublicNodeViewSet, basename='public-node')

urlpatterns = [
    path('', include(router.urls)),
    path('public/', include(public_router.urls)),
]
