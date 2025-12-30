from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.views import APIView

from common.auth import TokenAuth
from common.auth.authentication import has_permissions
from common.constants.permission_constants import CompareConstants, PermissionConstants, RoleConstants, ViewPermission
from common.result import result
from knowledge.models import KnowledgeGraphBinding


class KnowledgeGraphBindingRequest(serializers.Serializer):
    instance_id = serializers.CharField(required=True, allow_blank=False, max_length=255)


class KnowledgeGraphBindingSerializer(serializers.ModelSerializer):
    knowledge_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = KnowledgeGraphBinding
        fields = ['id', 'knowledge_id', 'instance_id', 'create_time', 'update_time']


class KnowledgeGraphBindingView(APIView):
    authentication_classes = [TokenAuth]

    @extend_schema(
        methods=['GET'],
        summary='List knowledge graph bindings',
        description='List third-party instance bindings for a knowledge base',
        responses=KnowledgeGraphBindingSerializer(many=True),
        tags=['Knowledge Base'],
    )
    @has_permissions(
        PermissionConstants.KNOWLEDGE_READ.get_workspace_knowledge_permission(),
        PermissionConstants.KNOWLEDGE_READ.get_workspace_permission_workspace_manage_role(),
        RoleConstants.WORKSPACE_MANAGE.get_workspace_role(),
        ViewPermission(
            [RoleConstants.USER.get_workspace_role()],
            [PermissionConstants.KNOWLEDGE.get_workspace_knowledge_permission()],
            CompareConstants.AND,
        ),
    )
    def get(self, request: Request, workspace_id: str, knowledge_id: str):
        bindings = QuerySet(KnowledgeGraphBinding).filter(knowledge_id=knowledge_id).order_by('-update_time')
        return result.success(KnowledgeGraphBindingSerializer(bindings, many=True).data)

    @extend_schema(
        methods=['POST'],
        summary='Bind third-party instance',
        description='Bind a third-party instance to a knowledge base',
        request=KnowledgeGraphBindingRequest,
        responses=serializers.BooleanField(),
        tags=['Knowledge Base'],
    )
    @has_permissions(
        PermissionConstants.KNOWLEDGE_EDIT.get_workspace_knowledge_permission(),
        PermissionConstants.KNOWLEDGE_EDIT.get_workspace_permission_workspace_manage_role(),
        RoleConstants.WORKSPACE_MANAGE.get_workspace_role(),
        ViewPermission(
            [RoleConstants.USER.get_workspace_role()],
            [PermissionConstants.KNOWLEDGE.get_workspace_knowledge_permission()],
            CompareConstants.AND,
        ),
    )
    def post(self, request: Request, workspace_id: str, knowledge_id: str):
        req = KnowledgeGraphBindingRequest(data=request.data)
        req.is_valid(raise_exception=True)

        instance_id: str = req.validated_data['instance_id']
        QuerySet(KnowledgeGraphBinding).get_or_create(
            knowledge_id=knowledge_id,
            instance_id=instance_id,
            defaults={},
        )
        return result.success(True)

    @extend_schema(
        methods=['DELETE'],
        summary='Unbind third-party instance',
        description='Unbind one or all third-party instances from a knowledge base',
        parameters=[],
        responses=serializers.BooleanField(),
        tags=['Knowledge Base'],
    )
    @has_permissions(
        PermissionConstants.KNOWLEDGE_EDIT.get_workspace_knowledge_permission(),
        PermissionConstants.KNOWLEDGE_EDIT.get_workspace_permission_workspace_manage_role(),
        RoleConstants.WORKSPACE_MANAGE.get_workspace_role(),
        ViewPermission(
            [RoleConstants.USER.get_workspace_role()],
            [PermissionConstants.KNOWLEDGE.get_workspace_knowledge_permission()],
            CompareConstants.AND,
        ),
    )
    def delete(self, request: Request, workspace_id: str, knowledge_id: str):
        instance_id = request.query_params.get('instance_id')

        qs = QuerySet(KnowledgeGraphBinding).filter(knowledge_id=knowledge_id)
        if instance_id:
            qs = qs.filter(instance_id=instance_id)
        qs.delete()
        return result.success(True)
