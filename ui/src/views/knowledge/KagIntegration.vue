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
              <el-form-item :label="$t('views.knowledge.kag.form.kagUrl')" prop="kag_url">
                <el-input v-model="form.kag_url" :placeholder="$t('views.knowledge.kag.form.kagUrlPlaceholder')" />
              </el-form-item>
              <el-form-item :label="$t('views.knowledge.kag.form.kagToken')" prop="kag_token">
                <el-input v-model="form.kag_token" type="password" show-password :placeholder="$t('views.knowledge.kag.form.kagTokenPlaceholder')" />
              </el-form-item>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item :label="$t('views.knowledge.kag.form.llmConfigId')" prop="llm_config_id">
                    <el-input-number v-model="form.llm_config_id" :min="1" controls-position="right" class="w-full" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                   <el-form-item :label="$t('views.knowledge.kag.form.embeddingConfigId')" prop="embedding_config_id">
                    <el-input-number v-model="form.embedding_config_id" :min="1" controls-position="right" class="w-full" />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row :gutter="20">
                 <el-col :span="12">
                  <el-form-item :label="$t('views.knowledge.kag.form.promptId')" prop="prompt_id">
                    <el-input v-model="form.prompt_id" :placeholder="$t('views.knowledge.kag.form.promptIdPlaceholder')" />
                  </el-form-item>
                 </el-col>
                 <el-col :span="12">
                  <el-form-item :label="$t('views.knowledge.kag.form.extractionRounds')" prop="extraction_rounds">
                    <el-input-number v-model="form.extraction_rounds" :min="1" controls-position="right" class="w-full" />
                  </el-form-item>
                 </el-col>
              </el-row>
            </el-form>
            <div class="text-right mt-16">
              <el-button @click="saveConfig" type="primary">{{ $t('views.knowledge.kag.button.save') }}</el-button>
              <el-button @click="handleExport" type="success" :loading="exportLoading">{{ $t('views.knowledge.kag.button.export') }}</el-button>
            </div>
            
            <div v-if="exportResult" class="mt-16">
                <el-alert
                    :title="exportResult.message || $t('views.knowledge.kag.message.taskComplete')"
                    :type="exportResult.status === 'PENDING' ? 'success' : 'warning'"
                    :description="'Task ID: ' + exportResult.task_id"
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
import { ref, onMounted, reactive, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { MsgSuccess, MsgError } from '@/utils/message'
import { loadSharedApi } from '@/utils/dynamics-api/shared-api'

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

const form = ref<any>({
  kag_url: '',
  kag_token: '',
  llm_config_id: undefined,
  embedding_config_id: undefined,
  prompt_id: '',
  extraction_rounds: 1
})

const rules = reactive({
  kag_url: [{ required: true, message: computed(() => t('views.knowledge.kag.form.kagUrlPlaceholder')), trigger: 'blur' }],
  kag_token: [{ required: true, message: computed(() => t('views.knowledge.kag.form.kagTokenPlaceholder')), trigger: 'blur' }]
})

function getApi() {
    return loadSharedApi({ type: 'knowledge', isShared: isShared.value, systemType: apiType.value })
}

function getConfig() {
  const api = getApi()
  if (api && api.getKagConfig) {
      api.getKagConfig(id, loading).then((res: any) => {
        if (res.data && Object.keys(res.data).length > 0) {
            form.value = { ...form.value, ...res.data }
        }
      })
  }
}

async function saveConfig() {
  if (!await formRef.value.validate()) return
  
  // Ensure optional fields are null if empty
  const payload = { ...form.value }
  if (payload.prompt_id === '') payload.prompt_id = null
  if (payload.llm_config_id === '') payload.llm_config_id = null
  if (payload.embedding_config_id === '') payload.embedding_config_id = null

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
  
  // Ensure optional fields are null if empty
  const payload = { ...form.value }
  if (payload.prompt_id === '') payload.prompt_id = null
  if (payload.llm_config_id === '') payload.llm_config_id = null
  if (payload.embedding_config_id === '') payload.embedding_config_id = null

  const api = getApi()
  
  if (api && api.exportToKag) {
      api.exportToKag(id, payload, exportLoading).then((res: any) => {
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
