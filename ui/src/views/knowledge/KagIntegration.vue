<template>
  <div class="p-16-24">
    <h2 class="mb-16">{{ $t('views.knowledge.kag.title') }}</h2>
    <el-card style="--el-card-padding: 0">
      <div class="knowledge-setting main-calc-height">
        <el-scrollbar>
          <div class="p-24" v-loading="loading">
            <h4 class="title-decoration-1 mb-16">
              {{ $t('views.knowledge.kag.configInfo') }}
            </h4>
            <el-form
              ref="formRef"
              :rules="rules"
              :model="form"
              label-position="top"
              require-asterisk-position="right"
            >
              <!-- Global Config -->
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item :label="$t('views.knowledge.kag.form.kagUrl')" prop="kag_url">
                    <el-input v-model="form.kag_url" :placeholder="$t('views.knowledge.kag.form.kagUrlPlaceholder')" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item :label="$t('views.knowledge.kag.form.kagToken')" prop="kag_token">
                    <el-input v-model="form.kag_token" type="password" show-password :placeholder="$t('views.knowledge.kag.form.kagTokenPlaceholder')" />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item :label="$t('views.knowledge.kag.form.llmConfigId')" prop="llm_config_id">
                    <el-select v-model="form.llm_config_id" :placeholder="$t('views.knowledge.kag.form.llmConfigIdPlaceholder')" clearable class="w-full">
                      <el-option
                        v-for="item in llmOptions"
                        :key="item.id"
                        :label="item.name"
                        :value="item.id"
                      />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                   <el-form-item :label="$t('views.knowledge.kag.form.embeddingConfigId')" prop="embedding_config_id">
                    <el-select v-model="form.embedding_config_id" :placeholder="$t('views.knowledge.kag.form.embeddingConfigIdPlaceholder')" clearable class="w-full">
                      <el-option
                        v-for="item in embeddingOptions"
                        :key="item.id"
                        :label="item.name"
                        :value="item.id"
                      />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-divider content-position="left">{{ $t('views.knowledge.kag.pipelineConfig') }}</el-divider>

              <el-tabs type="border-card" class="mb-16">
                <!-- Extraction Config -->
                <el-tab-pane :label="$t('views.knowledge.kag.tab.extraction')">
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <el-form-item :label="$t('views.knowledge.kag.form.promptId')" prop="kag_pipeline_config.extraction_config.prompt_id">
                        <el-select v-model="form.kag_pipeline_config.extraction_config.prompt_id" :placeholder="$t('views.knowledge.kag.form.promptIdPlaceholder')" clearable class="w-full">
                          <el-option
                            v-for="item in extractionPromptOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id"
                          />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item :label="$t('views.knowledge.kag.form.extractionRounds')" prop="kag_pipeline_config.extraction_config.extraction_rounds">
                        <el-input-number v-model="form.kag_pipeline_config.extraction_config.extraction_rounds" :min="1" :max="5" controls-position="right" class="w-full" />
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <el-form-item :label="$t('views.knowledge.kag.form.llmConfigIdOverride')">
                        <el-select v-model="form.kag_pipeline_config.extraction_config.llm_config_id" placeholder="Default (Global)" clearable class="w-full">
                          <el-option v-for="item in llmOptions" :key="item.id" :label="item.name" :value="item.id" />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item :label="$t('views.knowledge.kag.form.embeddingConfigIdOverride')">
                        <el-select v-model="form.kag_pipeline_config.extraction_config.embedding_config_id" placeholder="Default (Global)" clearable class="w-full">
                          <el-option v-for="item in embeddingOptions" :key="item.id" :label="item.name" :value="item.id" />
                        </el-select>
                      </el-form-item>
                    </el-col>
                  </el-row>
                </el-tab-pane>

                <!-- Disambiguation Config -->
                <el-tab-pane :label="$t('views.knowledge.kag.tab.disambiguation')">
                  <el-form-item :label="$t('views.knowledge.kag.form.algorithmType')">
                    <el-radio-group v-model="form.kag_pipeline_config.disambiguation_config.algorithm_type">
                      <el-radio label="hdbscan">HDBSCAN</el-radio>
                      <el-radio label="birch">BIRCH</el-radio>
                      <el-radio label="faiss">FAISS</el-radio>
                    </el-radio-group>
                  </el-form-item>

                  <!-- HDBSCAN Specific -->
                  <div v-if="form.kag_pipeline_config.disambiguation_config.algorithm_type === 'hdbscan'">
                    <el-row :gutter="20">
                      <el-col :span="8">
                        <el-form-item label="Min Cluster Size">
                          <el-input-number v-model="form.kag_pipeline_config.disambiguation_config.hdbscan_min_cluster_size" :min="2" controls-position="right" class="w-full" />
                        </el-form-item>
                      </el-col>
                      <el-col :span="8">
                        <el-form-item label="Min Samples">
                          <el-input-number v-model="form.kag_pipeline_config.disambiguation_config.hdbscan_min_samples" :min="1" controls-position="right" class="w-full" />
                        </el-form-item>
                      </el-col>
                      <el-col :span="8">
                        <el-form-item label="Cluster Selection Epsilon">
                          <el-input-number v-model="form.kag_pipeline_config.disambiguation_config.hdbscan_cluster_selection_epsilon" :step="0.1" controls-position="right" class="w-full" />
                        </el-form-item>
                      </el-col>
                    </el-row>
                  </div>

                  <!-- BIRCH Specific -->
                  <div v-if="form.kag_pipeline_config.disambiguation_config.algorithm_type === 'birch'">
                    <el-row :gutter="20">
                      <el-col :span="12">
                        <el-form-item label="Threshold">
                          <el-input-number v-model="form.kag_pipeline_config.disambiguation_config.birch_threshold" :step="0.1" controls-position="right" class="w-full" />
                        </el-form-item>
                      </el-col>
                      <el-col :span="12">
                        <el-form-item label="Branching Factor">
                          <el-input-number v-model="form.kag_pipeline_config.disambiguation_config.birch_branching_factor" :min="10" controls-position="right" class="w-full" />
                        </el-form-item>
                      </el-col>
                    </el-row>
                  </div>

                  <!-- FAISS Specific -->
                  <div v-if="form.kag_pipeline_config.disambiguation_config.algorithm_type === 'faiss'">
                    <el-row :gutter="20">
                      <el-col :span="8">
                        <el-form-item label="K Neighbors">
                          <el-input-number v-model="form.kag_pipeline_config.disambiguation_config.k_neighbors" :min="1" controls-position="right" class="w-full" />
                        </el-form-item>
                      </el-col>
                      <el-col :span="8">
                        <el-form-item label="Resolution">
                          <el-input-number v-model="form.kag_pipeline_config.disambiguation_config.resolution" :step="10" controls-position="right" class="w-full" />
                        </el-form-item>
                      </el-col>
                      <el-col :span="8">
                        <el-form-item label="Name Weight">
                          <el-input-number v-model="form.kag_pipeline_config.disambiguation_config.name_weight" :min="0" :max="1" :step="0.1" controls-position="right" class="w-full" />
                        </el-form-item>
                      </el-col>
                    </el-row>
                      <el-form-item label="FAISS Prompt">
                        <el-select 
                            v-model="form.kag_pipeline_config.disambiguation_config.faiss_prompt" 
                            :placeholder="$t('views.knowledge.kag.form.promptIdPlaceholder')" 
                            clearable 
                            class="w-full"
                        >
                          <el-option v-for="item in disambiguationPromptOptions" :key="item.id" :label="item.name" :value="item.id" />
                        </el-select>
                      </el-form-item>
                  </div>

                   <el-divider content-position="left">Common</el-divider>
                   <el-row :gutter="20">
                      <el-col :span="8">
                        <el-form-item :label="$t('views.knowledge.kag.form.promptId')">
                          <el-select v-model="form.kag_pipeline_config.disambiguation_config.prompt_id" :placeholder="$t('views.knowledge.kag.form.promptIdPlaceholder')" clearable class="w-full">
                            <el-option v-for="item in disambiguationPromptOptions" :key="item.id" :label="item.name" :value="item.id" />
                          </el-select>
                        </el-form-item>
                      </el-col>
                      <el-col :span="8">
                         <el-form-item :label="$t('views.knowledge.kag.form.llmConfigIdOverride')">
                            <el-select v-model="form.kag_pipeline_config.disambiguation_config.llm_config_id" placeholder="Default (Global)" clearable class="w-full">
                              <el-option v-for="item in llmOptions" :key="item.id" :label="item.name" :value="item.id" />
                            </el-select>
                          </el-form-item>
                      </el-col>
                      <el-col :span="8">
                          <el-form-item :label="$t('views.knowledge.kag.form.embeddingConfigIdOverride')">
                            <el-select v-model="form.kag_pipeline_config.disambiguation_config.embedding_config_id" placeholder="Default (Global)" clearable class="w-full">
                              <el-option v-for="item in embeddingOptions" :key="item.id" :label="item.name" :value="item.id" />
                            </el-select>
                          </el-form-item>
                      </el-col>
                   </el-row>
                </el-tab-pane>

                <!-- Relation Extraction Config -->
                <el-tab-pane :label="$t('views.knowledge.kag.tab.relationExtraction')">
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <el-form-item :label="$t('views.knowledge.kag.form.promptId')">
                        <el-select v-model="form.kag_pipeline_config.relation_extraction_config.prompt_id" :placeholder="$t('views.knowledge.kag.form.promptIdPlaceholder')" clearable class="w-full">
                          <el-option v-for="item in relationExtractionPromptOptions" :key="item.id" :label="item.name" :value="item.id" />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item :label="$t('views.knowledge.kag.form.extractionRounds')">
                         <el-input-number v-model="form.kag_pipeline_config.relation_extraction_config.extraction_rounds" :min="1" controls-position="right" class="w-full" />
                      </el-form-item>
                    </el-col>
                  </el-row>
                   <el-row :gutter="20">
                      <el-col :span="12">
                        <el-form-item :label="$t('views.knowledge.kag.form.llmConfigIdOverride')">
                          <el-select v-model="form.kag_pipeline_config.relation_extraction_config.llm_config_id" placeholder="Default (Global)" clearable class="w-full">
                            <el-option v-for="item in llmOptions" :key="item.id" :label="item.name" :value="item.id" />
                          </el-select>
                        </el-form-item>
                      </el-col>
                      <el-col :span="12">
                        <el-form-item :label="$t('views.knowledge.kag.form.embeddingConfigIdOverride')">
                          <el-select v-model="form.kag_pipeline_config.relation_extraction_config.embedding_config_id" placeholder="Default (Global)" clearable class="w-full">
                            <el-option v-for="item in embeddingOptions" :key="item.id" :label="item.name" :value="item.id" />
                          </el-select>
                        </el-form-item>
                      </el-col>
                   </el-row>
                </el-tab-pane>

                <!-- Refinement Config -->
                <el-tab-pane :label="$t('views.knowledge.kag.tab.tripleRefinement')">
                  <el-row :gutter="20">
                      <el-col :span="12">
                        <el-form-item :label="$t('views.knowledge.kag.form.llmConfigIdOverride')">
                          <el-select v-model="form.kag_pipeline_config.triple_refinement_config.llm_config_id" placeholder="Default (Global)" clearable class="w-full">
                            <el-option v-for="item in llmOptions" :key="item.id" :label="item.name" :value="item.id" />
                          </el-select>
                        </el-form-item>
                      </el-col>
                      <el-col :span="12">
                        <el-form-item :label="$t('views.knowledge.kag.form.embeddingConfigIdOverride')">
                          <el-select v-model="form.kag_pipeline_config.triple_refinement_config.embedding_config_id" placeholder="Default (Global)" clearable class="w-full">
                            <el-option v-for="item in embeddingOptions" :key="item.id" :label="item.name" :value="item.id" />
                          </el-select>
                        </el-form-item>
                      </el-col>
                   </el-row>
                </el-tab-pane>

                <el-tab-pane :label="$t('views.knowledge.kag.tab.predicateRefinement')">
                   <el-row :gutter="20">
                     <el-col :span="8">
                        <el-form-item :label="$t('views.knowledge.kag.form.promptId')">
                          <el-select v-model="form.kag_pipeline_config.predicate_refinement_config.prompt_id" :placeholder="$t('views.knowledge.kag.form.promptIdPlaceholder')" clearable class="w-full">
                            <el-option v-for="item in predicateRefinementPromptOptions" :key="item.id" :label="item.name" :value="item.id" />
                          </el-select>
                        </el-form-item>
                      </el-col>
                      <el-col :span="8">
                        <el-form-item :label="$t('views.knowledge.kag.form.llmConfigIdOverride')">
                          <el-select v-model="form.kag_pipeline_config.predicate_refinement_config.llm_config_id" placeholder="Default (Global)" clearable class="w-full">
                            <el-option v-for="item in llmOptions" :key="item.id" :label="item.name" :value="item.id" />
                          </el-select>
                        </el-form-item>
                      </el-col>
                      <el-col :span="8">
                        <el-form-item :label="$t('views.knowledge.kag.form.embeddingConfigIdOverride')">
                          <el-select v-model="form.kag_pipeline_config.predicate_refinement_config.embedding_config_id" placeholder="Default (Global)" clearable class="w-full">
                            <el-option v-for="item in embeddingOptions" :key="item.id" :label="item.name" :value="item.id" />
                          </el-select>
                        </el-form-item>
                      </el-col>
                   </el-row>
                </el-tab-pane>

                <!-- Graph DB Config -->
                <el-tab-pane :label="$t('views.knowledge.kag.tab.graphDb')">
                  <el-form-item label="Password" prop="kag_pipeline_config.graph_db_config.password" :rules="[{ required: true, message: 'Password is required', trigger: 'blur' }]">
                    <el-input v-model="form.kag_pipeline_config.graph_db_config.password" type="password" show-password />
                  </el-form-item>
                   <el-form-item label="Description">
                    <el-input v-model="form.kag_pipeline_config.graph_db_config.description" type="textarea" />
                  </el-form-item>
                   <el-form-item :label="$t('views.knowledge.kag.form.embeddingConfigIdOverride')">
                      <el-select v-model="form.kag_pipeline_config.graph_db_config.embedding_config_id" placeholder="Default (Global)" clearable class="w-full">
                        <el-option v-for="item in embeddingOptions" :key="item.id" :label="item.name" :value="item.id" />
                      </el-select>
                    </el-form-item>
                </el-tab-pane>
              </el-tabs>

            </el-form>
            <div class="text-right mt-16">
              <el-upload
                action=""
                :auto-upload="false"
                :show-file-list="false"
                accept=".json"
                :on-change="handleImportFile"
                style="display: inline-block; margin-right: 12px;"
              >
                <el-button>{{ $t('views.knowledge.kag.button.import') }}</el-button>
              </el-upload>
              <el-button @click="saveConfig" type="primary">{{ $t('views.knowledge.kag.button.save') }}</el-button>
              <el-button @click="handleExport" type="success" :loading="exportLoading">{{ $t('views.knowledge.kag.button.export') }}</el-button>
            </div>
            
            <div v-if="exportResult" class="mt-16">
                <el-alert
                    v-if="exportResult.instance_id"
                    :title="$t('views.knowledge.kag.message.taskComplete')"
                    type="success"
                    :description="'Instance ID: ' + exportResult.instance_id"
                    show-icon
                />
                <el-alert
                    v-else
                    :title="exportResult.message || $t('views.knowledge.kag.message.taskComplete')"
                    :type="exportResult.status === 'PENDING' ? 'success' : 'warning'"
                    :description="exportResult.task_id ? 'Task ID: ' + exportResult.task_id : ''"
                    show-icon
                />
            </div>
          </div>
        </el-scrollbar>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { MsgSuccess, MsgError } from '@/utils/message'
import { loadSharedApi } from '@/utils/dynamics-api/shared-api'
import { useDebounceFn } from '@vueuse/core'
import { cloneDeep } from 'lodash'

const route = useRoute()
const { t } = useI18n()
const { params: { id, folderId } } = route as any

const apiType = computed(() => {
  if (route.path.includes('shared')) {
    return 'systemShare'
  } else if (route.path.includes('resource-management')) {
    return 'systemManage'
  } else {
    return 'workspace'
  }
})

const isShared = computed(() => folderId === 'share')

const loading = ref(false)
const exportLoading = ref(false)
const formRef = ref()
const exportResult = ref<any>(null)

// Default config structure
const defaultPipelineConfig = {
  extraction_config: {
    prompt_id: '',
    extraction_rounds: 3,
    llm_config_id: undefined,
    embedding_config_id: undefined
  },
  disambiguation_config: {
    algorithm_type: 'hdbscan',
    hdbscan_min_cluster_size: 2,
    hdbscan_min_samples: 1,
    hdbscan_cluster_selection_epsilon: 0.0,
    birch_threshold: 0.5,
    birch_branching_factor: 50,
    k_neighbors: 10,
    resolution: 500,
    name_weight: 0.5,
    faiss_prompt: '',
    prompt_id: '',
    llm_config_id: undefined,
    embedding_config_id: undefined
  },
  relation_extraction_config: {
    prompt_id: '',
    extraction_rounds: 1,
    llm_config_id: undefined,
    embedding_config_id: undefined
  },
  triple_refinement_config: {
    llm_config_id: undefined,
    embedding_config_id: undefined
  },
  predicate_refinement_config: {
    confidence_threshold: 0.7,
    clustering_method: 'dbscan',
    prompt_id: '',
    llm_config_id: undefined,
    embedding_config_id: undefined
  },
  graph_db_config: {
    password: '',
    description: 'Created via External API',
    embedding_config_id: undefined
  }
}

const form = ref<any>({
  kag_url: '',
  kag_token: '',
  llm_config_id: undefined,
  embedding_config_id: undefined,
  kag_pipeline_config: cloneDeep(defaultPipelineConfig)
})

const promptOptions = ref<any[]>([])
const extractionPromptOptions = computed(() => promptOptions.value.filter(item => item.type === 'EXTRACTION'))
const disambiguationPromptOptions = computed(() => promptOptions.value.filter(item => item.type === 'DISAMBIGUATION'))
const relationExtractionPromptOptions = computed(() => promptOptions.value.filter(item => item.type === 'RELATION_EXTRACTION'))
const predicateRefinementPromptOptions = computed(() => promptOptions.value.filter(item => item.type === 'PREDICATE_REFINEMENT'))
const tripleRefinementPromptOptions = computed(() => promptOptions.value.filter(item => item.type === 'TRIPLE_REFINEMENT'))

const llmOptions = ref<any[]>([])
const embeddingOptions = ref<any[]>([])

const rules = reactive({
  kag_url: [{ required: true, message: computed(() => t('views.knowledge.kag.form.kagUrlPlaceholder')), trigger: 'blur' }],
  kag_token: [{ required: true, message: computed(() => t('views.knowledge.kag.form.kagTokenPlaceholder')), trigger: 'blur' }]
})

function getApi() {
    return loadSharedApi({ type: 'knowledge', isShared: isShared.value, systemType: apiType.value })
}

const fetchOptions = useDebounceFn(() => {
    if (form.value.kag_url && form.value.kag_token) {
        loadOptionsData(form.value.kag_url, form.value.kag_token)
    }
}, 500)

watch(() => [form.value.kag_url, form.value.kag_token], () => {
    if (form.value.kag_url && form.value.kag_token) {
        fetchOptions()
    }
})

async function loadOptionsData(url: string, token: string) {
    const api = getApi()
    if (!api || !url || !token) return

    const params = { kag_url: url, kag_token: token }
    
    const promises = []
    
    if (api.getKagPrompts) {
        // Fetch all prompts without task_type filtering
        // The backend will return list of prompts, we can filter them in frontend or request multiple times
        // Given the requirement, we should probably fetch all.
        // But the previous implementation was single fetch.
        // Let's fetch all types in parallel or one by one.
        // To simplify, let's fetch for each type.
        
        const taskTypes = ['EXTRACTION', 'DISAMBIGUATION', 'RELATION_EXTRACTION', 'PREDICATE_REFINEMENT', 'TRIPLE_REFINEMENT']
        const promptPromises = taskTypes.map(type => 
            api.getKagPrompts(id, { ...params, task_type: type }).then((res: any) => {
                if (res.data) {
                    return res.data.map((item: any) => ({ ...item, type }))
                }
                return []
            })
        )
        
        promises.push(Promise.all(promptPromises).then(results => {
            promptOptions.value = results.flat()
        }))
    }
    
    if (api.getKagLlmConfigs) {
        promises.push(api.getKagLlmConfigs(id, { ...params, config_type: 'llm' }).then((res: any) => {
             if (res.data) llmOptions.value = res.data
        }))
        
        promises.push(api.getKagLlmConfigs(id, { ...params, config_type: 'embedding' }).then((res: any) => {
             if (res.data) embeddingOptions.value = res.data
        }))
    }
    
    await Promise.all(promises)
}

function getConfig() {
  const api = getApi()
  if (api && api.getKagConfig) {
      loading.value = true
      api.getKagConfig(id).then(async (res: any) => {
        if (res.data && Object.keys(res.data).length > 0) {
            const data = res.data
            // Remove explicit loadOptionsData call to rely on watch
            // if (data.kag_url && data.kag_token) {
            //      await loadOptionsData(data.kag_url, data.kag_token)
            // }
            
            // Merge loaded data with form, handling kag_pipeline_config separately
            const { kag_pipeline_config, ...rest } = data
            
            form.value = { ...form.value, ...rest }
            
            if (kag_pipeline_config && Object.keys(kag_pipeline_config).length > 0) {
                 // Deep merge to preserve defaults for missing keys
                 form.value.kag_pipeline_config = {
                    ...defaultPipelineConfig,
                    ...kag_pipeline_config,
                    extraction_config: { ...defaultPipelineConfig.extraction_config, ...(kag_pipeline_config.extraction_config || {}) },
                    disambiguation_config: { ...defaultPipelineConfig.disambiguation_config, ...(kag_pipeline_config.disambiguation_config || {}) },
                    relation_extraction_config: { ...defaultPipelineConfig.relation_extraction_config, ...(kag_pipeline_config.relation_extraction_config || {}) },
                    triple_refinement_config: { ...defaultPipelineConfig.triple_refinement_config, ...(kag_pipeline_config.triple_refinement_config || {}) },
                    predicate_refinement_config: { ...defaultPipelineConfig.predicate_refinement_config, ...(kag_pipeline_config.predicate_refinement_config || {}) },
                    graph_db_config: { ...defaultPipelineConfig.graph_db_config, ...(kag_pipeline_config.graph_db_config || {}) },
                 }
            }
            
            // Backward compatibility for root fields if pipeline config is empty
            if (!kag_pipeline_config) {
                if (data.prompt_id) form.value.kag_pipeline_config.extraction_config.prompt_id = data.prompt_id
                if (data.extraction_rounds) form.value.kag_pipeline_config.extraction_config.extraction_rounds = data.extraction_rounds
            }
        }
      }).finally(() => {
          loading.value = false
      })
  }
}

function handleImportFile(file: any) {
  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const result = e.target?.result as string
      const data = JSON.parse(result)

      if (data.llm_config_id !== undefined) form.value.llm_config_id = data.llm_config_id
      if (data.embedding_config_id !== undefined) form.value.embedding_config_id = data.embedding_config_id

      const pipelineKeys = [
        'extraction_config',
        'disambiguation_config',
        'relation_extraction_config',
        'triple_refinement_config',
        'predicate_refinement_config',
        'graph_db_config'
      ]

      pipelineKeys.forEach(key => {
        if (data[key]) {
          form.value.kag_pipeline_config[key] = {
            ...form.value.kag_pipeline_config[key],
            ...data[key]
          }
        }
      })

      MsgSuccess(t('views.knowledge.kag.message.importSuccess'))
    } catch (error) {
      MsgError('Invalid JSON file')
    }
  }
  reader.readAsText(file.raw)
}

async function saveConfig() {
  if (!await formRef.value.validate()) return
  
  const payload = cloneDeep(form.value)
  
  // Clean up empty strings to null for optional ID fields
  const cleanId = (val: any) => (val === '' ? null : val)
  
  payload.llm_config_id = cleanId(payload.llm_config_id)
  payload.embedding_config_id = cleanId(payload.embedding_config_id)
  
  // Clean nested configs
  const pipeline = payload.kag_pipeline_config
  if (pipeline) {
      ['extraction_config', 'disambiguation_config', 'relation_extraction_config', 'triple_refinement_config', 'predicate_refinement_config', 'graph_db_config'].forEach(key => {
          if (pipeline[key]) {
              pipeline[key].llm_config_id = cleanId(pipeline[key].llm_config_id)
              pipeline[key].embedding_config_id = cleanId(pipeline[key].embedding_config_id)
              if (pipeline[key].prompt_id !== undefined) pipeline[key].prompt_id = cleanId(pipeline[key].prompt_id)
          }
      })
  }

  const api = getApi()
  if (api && api.putKagConfig) {
      api.putKagConfig(id, payload, loading).then(() => {
        MsgSuccess(t('views.knowledge.kag.message.saveSuccess'))
      })
  }
}

async function handleExport() {
  if (!await formRef.value.validate()) return
  
  exportLoading.value = true
  exportResult.value = null
  
  const payload = cloneDeep(form.value)
  // Clean logic same as saveConfig, but export might need it
  const cleanId = (val: any) => (val === '' ? null : val)
  
  payload.llm_config_id = cleanId(payload.llm_config_id)
  payload.embedding_config_id = cleanId(payload.embedding_config_id)
  
  const pipeline = payload.kag_pipeline_config
   if (pipeline) {
      ['extraction_config', 'disambiguation_config', 'relation_extraction_config', 'triple_refinement_config', 'predicate_refinement_config', 'graph_db_config'].forEach(key => {
          if (pipeline[key]) {
              pipeline[key].llm_config_id = cleanId(pipeline[key].llm_config_id)
              pipeline[key].embedding_config_id = cleanId(pipeline[key].embedding_config_id)
              if (pipeline[key].prompt_id !== undefined) pipeline[key].prompt_id = cleanId(pipeline[key].prompt_id)
          }
      })
  }

  // The backend now expects 'config' inside the payload which matches the structure of payload.kag_pipeline_config
  // plus global IDs. However, the ExportToKAGSerializer expects 'config' as a nested object.
  // The backend View logic constructs the final payload.
  // We just send the form data, and the backend view handles the rest (merging defaults, etc.)
  
  // Note: The backend view logic for ExportToKAG prioritizes `kag_pipeline_config` from DB if not provided in request.
  // But here we want to export with *current form values*.
  // So we should construct the `config` object here to be safe.
  
  const exportPayload = {
      kag_url: payload.kag_url,
      kag_token: payload.kag_token,
      config: {
          llm_config_id: payload.llm_config_id,
          embedding_config_id: payload.embedding_config_id,
          ...pipeline
      }
  }

  const api = getApi()
  
  if (api && api.exportToKag) {
      api.exportToKag(id, exportPayload, exportLoading).then((res: any) => {
        exportResult.value = res.data
        MsgSuccess(t('views.knowledge.kag.message.exportSent'))
      }).catch((err: any) => {
          // Error is handled by request interceptor usually
      }).finally(() => {
          exportLoading.value = false
      })
  } else {
      exportLoading.value = false
      MsgError(t('views.knowledge.kag.message.apiUnavailable'))
  }
}

onMounted(() => {
  getConfig()
})
</script>

<style lang="scss" scoped>
.knowledge-setting {
  width: 70%;
  margin: 0 auto;
}
.w-full {
    width: 100%;
}
</style>
