import uuid_utils.compat as uuid
from django.db import models
from common.mixins.app_model_mixin import AppModelMixin
from knowledge.models.knowledge import Knowledge

class KnowledgeGraphBinding(AppModelMixin):
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="主键id")
    knowledge = models.ForeignKey(Knowledge, on_delete=models.CASCADE, verbose_name="知识库", related_name='graph_bindings', db_constraint=False)
    instance_id = models.CharField(max_length=255, verbose_name="第三方实例ID")
    
    class Meta:
        db_table = "knowledge_graph_binding"
        verbose_name = "知识图谱关联"
