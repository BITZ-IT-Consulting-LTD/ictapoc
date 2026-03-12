from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ArtifactViewSet, DocumentViewSet, ProjectPhaseViewSet, 
    ArtifactTypeViewSet, RegistryViewSet, NodeTypeViewSet, 
    NodeViewSet, RepositoryViewSet
)

app_name = 'document_repository'

router = DefaultRouter()
router.register(r'types', ArtifactTypeViewSet, basename='artifact-type')
router.register(r'artifacts', ArtifactViewSet, basename='artifact')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'projects/phases', ProjectPhaseViewSet, basename='project-phase')
router.register(r'registries', RegistryViewSet, basename='registry')
router.register(r'node-types', NodeTypeViewSet, basename='node-type')
router.register(r'nodes', NodeViewSet, basename='node')
router.register(r'repos', RepositoryViewSet, basename='repository')

urlpatterns = [
    path('', include(router.urls)),
]
