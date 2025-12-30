from rest_framework import serializers

from knowledge.models.knowledge import KnowledgeKagConfig


class KnowledgeKagConfigSerializer(serializers.ModelSerializer):
    task_name = serializers.CharField(required=False, help_text="任务名称")

    class Meta:
        model = KnowledgeKagConfig
        fields = '__all__'
        read_only_fields = ['id', 'knowledge']


class ExportToKAGSerializer(serializers.Serializer):
    kag_url = serializers.URLField(required=True, help_text="KAG系统地址")
    kag_token = serializers.CharField(required=True, help_text="KAG Token")
    task_name = serializers.CharField(required=False, help_text="任务名称")
    llm_config_id = serializers.IntegerField(required=False, allow_null=True, help_text="LLM配置ID")
    embedding_config_id = serializers.IntegerField(required=False, allow_null=True, help_text="Embedding配置ID")
    prompt_id = serializers.CharField(required=False, allow_null=True, allow_blank=True, help_text="Prompt ID")
    extraction_rounds = serializers.IntegerField(default=1, help_text="抽取轮数")
