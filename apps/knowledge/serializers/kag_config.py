from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from knowledge.models.knowledge import KnowledgeKagConfig


class ExtractionPipelineConfigSerializer(serializers.Serializer):
    prompt_id = serializers.CharField(required=False, allow_blank=True, default='')
    extraction_rounds = serializers.IntegerField(default=3)
    llm_config_id = serializers.IntegerField(required=False, allow_null=True)
    embedding_config_id = serializers.IntegerField(required=False, allow_null=True)


class DisambiguationPipelineConfigSerializer(serializers.Serializer):
    algorithm_type = serializers.CharField(default='hdbscan')
    hdbscan_min_cluster_size = serializers.IntegerField(default=2)
    hdbscan_min_samples = serializers.IntegerField(default=1)
    hdbscan_cluster_selection_epsilon = serializers.FloatField(default=0.0)
    birch_threshold = serializers.FloatField(default=0.5)
    birch_branching_factor = serializers.IntegerField(default=50)
    k_neighbors = serializers.IntegerField(default=10)
    resolution = serializers.FloatField(default=500)
    faiss_prompt = serializers.CharField(required=False, allow_blank=True, default='')
    name_weight = serializers.FloatField(default=0.5)
    prompt_id = serializers.CharField(required=False, allow_blank=True, default='')
    llm_config_id = serializers.IntegerField(required=False, allow_null=True)
    embedding_config_id = serializers.IntegerField(required=False, allow_null=True)


class RelationExtractionPipelineConfigSerializer(serializers.Serializer):
    prompt_id = serializers.CharField(required=False, allow_blank=True, default='')
    extraction_rounds = serializers.IntegerField(default=1)
    llm_config_id = serializers.IntegerField(required=False, allow_null=True)
    embedding_config_id = serializers.IntegerField(required=False, allow_null=True)


class TripleRefinementPipelineConfigSerializer(serializers.Serializer):
    llm_config_id = serializers.IntegerField(required=False, allow_null=True)
    embedding_config_id = serializers.IntegerField(required=False, allow_null=True)


class PredicateRefinementPipelineConfigSerializer(serializers.Serializer):
    confidence_threshold = serializers.FloatField(default=0.7)
    clustering_method = serializers.CharField(default='dbscan')
    prompt_id = serializers.CharField(required=False, allow_blank=True, default='')
    llm_config_id = serializers.IntegerField(required=False, allow_null=True)
    embedding_config_id = serializers.IntegerField(required=False, allow_null=True)


class GraphDBPipelineConfigSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    description = serializers.CharField(default="Created via External API", required=False)
    embedding_config_id = serializers.IntegerField(required=False, allow_null=True)


class KGPipelineConfigSerializer(serializers.Serializer):
    llm_config_id = serializers.IntegerField(required=True)
    embedding_config_id = serializers.IntegerField(required=True)
    extraction_config = ExtractionPipelineConfigSerializer(required=False)
    disambiguation_config = DisambiguationPipelineConfigSerializer(required=False)
    relation_extraction_config = RelationExtractionPipelineConfigSerializer(required=False)
    triple_refinement_config = TripleRefinementPipelineConfigSerializer(required=False)
    predicate_refinement_config = PredicateRefinementPipelineConfigSerializer(required=False)
    graph_db_config = GraphDBPipelineConfigSerializer(required=True)


class KnowledgeKagConfigSerializer(serializers.ModelSerializer):
    task_name = serializers.CharField(required=False, help_text=_("任务名称"))
    kag_pipeline_config = serializers.JSONField(required=False, help_text=_("KAG Pipeline配置"))

    class Meta:
        model = KnowledgeKagConfig
        fields = '__all__'
        read_only_fields = ['id', 'knowledge']


class ExportToKAGSerializer(serializers.Serializer):
    kag_url = serializers.URLField(required=True, help_text=_("KAG系统地址"))
    kag_token = serializers.CharField(required=True, help_text=_("KAG Token"))
    task_name = serializers.CharField(required=False, help_text=_("任务名称"))
    config = KGPipelineConfigSerializer(required=True, help_text=_("Pipeline配置"))
