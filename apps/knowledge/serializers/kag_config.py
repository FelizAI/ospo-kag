from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from knowledge.models.knowledge import KnowledgeKagConfig


class KnowledgeKagConfigSerializer(serializers.ModelSerializer):
    task_name = serializers.CharField(required=False, help_text=_("任务名称"))

    class Meta:
        model = KnowledgeKagConfig
        fields = '__all__'
        read_only_fields = ['id', 'knowledge']


class ExportToKAGSerializer(serializers.Serializer):
    kag_url = serializers.URLField(required=True, help_text=_("KAG系统地址"))
    kag_token = serializers.CharField(required=True, help_text=_("KAG Token"))
    task_name = serializers.CharField(required=False, help_text=_("任务名称"))
    llm_config_id = serializers.IntegerField(required=False, allow_null=True, help_text=_("LLM配置ID"))
    embedding_config_id = serializers.IntegerField(required=False, allow_null=True, help_text=_("Embedding配置ID"))
    prompt_id = serializers.CharField(required=False, allow_null=True, allow_blank=True, help_text=_("Prompt ID"))
    extraction_rounds = serializers.IntegerField(default=1, help_text=_("抽取轮数"))
