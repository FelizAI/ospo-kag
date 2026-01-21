<template>
  <div class="item-content mb-16 lighter">
    <template v-for="(answer_text, index) in answer_text_list" :key="index">
      <div class="avatar mr-8" v-if="showAvatar">
        <img v-if="application.avatar" :src="application.avatar" height="28px" width="28px" />
        <LogoIcon v-else height="28px" width="28px" />
      </div>
      <div
        class="content"
        @mouseup="openControl"
        :style="{
          'padding-right': showUserAvatar ? 'var(--padding-left)' : '0',
        }"
      >
        <el-card shadow="always" class="mb-8 border-r-8" style="--el-card-padding: 6px 16px">
          <MdRenderer
            v-if="
              (chatRecord.write_ed === undefined || chatRecord.write_ed === true) &&
              answer_text.length == 0
            "
            :source="$t('chat.tip.answerMessage')"
          ></MdRenderer>
          <template v-else-if="answer_text.length > 0">
            <MdRenderer
              v-for="(answer, index) in answer_text"
              :key="index"
              :chat_record_id="answer.chat_record_id"
              :child_node="answer.child_node"
              :runtime_node_id="answer.runtime_node_id"
              :reasoning_content="answer.reasoning_content"
              :disabled="loading || type == 'log'"
              :source="answer.content"
              :send-message="chatMessage"
            ></MdRenderer>
          </template>
          <p v-else-if="chatRecord.is_stop" shadow="always" style="margin: 0.5rem 0">
            {{ $t('chat.tip.stopAnswer') }}
          </p>
          <p v-else shadow="always" style="margin: 0.5rem 0">
            {{ $t('chat.tip.answerLoading') }} <span class="dotting"></span>
          </p>
          <!-- 知识来源 -->
          <KnowledgeSourceComponent
            :data="chatRecord"
            :application="application"
            :type="type"
            :appType="application.type"
            :executionIsRightPanel="props.executionIsRightPanel"
            @open-execution-detail="emit('openExecutionDetail')"
            @openParagraph="emit('openParagraph')"
            @openParagraphDocument="(val: string) => emit('openParagraphDocument', val)"
            v-if="showSource(chatRecord) && index === chatRecord.answer_text_list.length - 1"
          />
        </el-card>
      </div>
    </template>
    <div
      class="content"
      :style="{
        'padding-left': showAvatar ? 'var(--padding-left)' : '0',
        'padding-right': showUserAvatar ? 'var(--padding-left)' : '0',
      }"
    >
      <OperationButton
        :type="type"
        :application="application"
        :chatRecord="chatRecord"
        @update:chatRecord="(event: any) => emit('update:chatRecord', event)"
        :loading="loading"
        :start-chat="startChat"
        :stop-chat="stopChat"
        :regenerationChart="regenerationChart"
        :hasPathGraphData="hasPathGraphData"
        :pathGraphExpanded="pathGraphExpanded"
        @togglePathGraph="togglePathGraph"
      ></OperationButton>
    </div>
    <el-collapse-transition>
      <div
        v-show="pathGraphExpanded && hasPathGraphData"
        class="content"
        :style="{
          'padding-left': showAvatar ? 'var(--padding-left)' : '0',
          'padding-right': showUserAvatar ? 'var(--padding-left)' : '0',
        }"
      >
        <el-card shadow="always" class="mb-8 border-r-8" style="--el-card-padding: 12px 16px">
          <div class="flex align-center flex-between w-full mb-8">
            <span class="path-graph-title ellipsis-1">路径图</span>
            <el-button
              class="path-graph-button"
              size="small"
              type="primary"
              link
              @click="toggleForceLayout"
            >
              {{ forceLayoutEnabled ? '固定布局' : '自动布局' }}
            </el-button>
          </div>
          <div class="path-graph-inline-container">
            <div ref="pathGraphRef" class="path-graph-canvas" v-resize="resizePathGraph"></div>
          </div>
        </el-card>
      </div>
    </el-collapse-transition>
  </div>
</template>
<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import KnowledgeSourceComponent from '@/components/ai-chat/component/knowledge-source-component/index.vue'
import MdRenderer from '@/components/markdown/MdRenderer.vue'
import OperationButton from '@/components/ai-chat/component/operation-button/index.vue'
import { type chatType, type PathToolResultConcept, type PathToolResultData } from '@/api/type/application'
import bus from '@/bus'
import * as echarts from 'echarts'

const props = defineProps<{
  chatRecord: chatType
  application: any
  loading: boolean
  sendMessage: (question: string, other_params_data?: any, chat?: chatType) => Promise<boolean>
  chatManagement: any
  type: 'log' | 'ai-chat' | 'debug-ai-chat'
  executionIsRightPanel?: boolean
}>()

const emit = defineEmits([
  'update:chatRecord',
  'openExecutionDetail',
  'openParagraph',
  'openParagraphDocument',
])

const showAvatar = computed(() => {
  return props.application.show_avatar == undefined ? true : props.application.show_avatar
})
const showUserAvatar = computed(() => {
  return props.application.show_user_avatar == undefined ? true : props.application.show_user_avatar
})
const chatMessage = (question: string, type: 'old' | 'new', other_params_data?: any) => {
  if (type === 'old') {
    add_answer_text_list(props.chatRecord.answer_text_list)
    props.sendMessage(question, other_params_data, props.chatRecord).then(() => {
      props.chatManagement.open(props.chatRecord.id)
      props.chatManagement.write(props.chatRecord.id)
    })
  } else {
    props.sendMessage(question, other_params_data)
  }
}
const add_answer_text_list = (answer_text_list: Array<any>) => {
  answer_text_list.push([])
}

const openControl = (event: any) => {
  if (props.type !== 'log') {
    bus.emit('open-control', event)
  }
}

const answer_text_list = computed(() => {
  return props.chatRecord.answer_text_list.map((item) => {
    if (typeof item == 'string') {
      return [
        {
          content: item,
          chat_record_id: undefined,
          child_node: undefined,
          runtime_node_id: undefined,
          reasoning_content: undefined,
        },
      ]
    } else if (item instanceof Array) {
      return item
    } else {
      return [item]
    }
  })
})

type ArrowToken = '->' | '<-'
type ConceptMap = Map<string, string>
type ConceptItem = PathToolResultConcept

interface GraphNodeData {
  id: string
  name: string
  description: string
  value: number
  symbolSize: number
  category: number
  x?: number
  y?: number
  fixed?: boolean
  itemStyle: {
    color: string
    shadowBlur: number
    shadowColor: string
  }
  label: {
    show: boolean
    color: string
    fontSize: number
  }
}

interface GraphLinkData {
  source: string
  target: string
  labelText: string
  lineStyle: {
    color: string
    width: number
    opacity: number
  }
  label: {
    show: boolean
    formatter: string
    color: string
    fontSize: number
    backgroundColor: string
    borderRadius: number
    padding: number[]
  }
}

const pathToolResultData = computed<PathToolResultData | null>(() => {
  const result = props.chatRecord.path_tool_result
  if (!result) {
    return null
  }
  if ('data' in result) {
    return result.data ?? null
  }
  if ('concept' in result && 'path' in result) {
    return result
  }
  return null
})

const conceptList = computed<ConceptItem[]>(() => {
  const list = pathToolResultData.value?.concept
  if (!Array.isArray(list)) {
    return []
  }
  return list.filter((v) => v.name.trim().length > 0)
})

const pathList = computed<string[]>(() => {
  const list = pathToolResultData.value?.path
  return Array.isArray(list) ? list.filter((v) => typeof v === 'string' && v.length > 0) : []
})

const baseNodeSet = computed<Set<string>>(() => {
  const list = pathToolResultData.value?.base_node
  if (!Array.isArray(list)) {
    return new Set()
  }
  return new Set(list.filter((v) => typeof v === 'string' && v.length > 0))
})

const hasPathGraphData = computed(() => {
  return conceptList.value.length > 0 || pathList.value.length > 0
})

const pathGraphExpanded = ref(false)
const pathGraphRef = ref<HTMLElement>()
const activeChart = ref<echarts.EChartsType | null>(null)

function buildConceptMap(concepts: ConceptItem[]): ConceptMap {
  const map: ConceptMap = new Map()
  for (const c of concepts) {
    const name = c.name.trim()
    if (name.length > 0 && !map.has(name)) {
      map.set(name, c.description.trim())
    }
  }
  return map
}

function splitByArrows(raw: string): string[] {
  return raw
    .split(/(->|<-)/)
    .map((s) => s.trim())
    .filter((s) => s.length > 0)
}

function isArrowToken(v: string): v is ArrowToken {
  return v === '->' || v === '<-'
}

function buildLinksFromPaths(paths: string[]): Array<{ source: string; target: string; labelText: string }> {
  const links: Array<{ source: string; target: string; labelText: string }> = []
  const seen = new Set<string>()

  for (const p of paths) {
    const parts = splitByArrows(p)
    if (parts.length < 5) {
      continue
    }
    let i = 0
    while (i + 4 < parts.length) {
      const leftNode = parts[i]
      const arrow1 = parts[i + 1]
      const labelText = parts[i + 2]
      const arrow2 = parts[i + 3]
      const rightNode = parts[i + 4]

      if (!leftNode || !rightNode || !isArrowToken(arrow1) || !isArrowToken(arrow2) || !labelText) {
        i += 1
        continue
      }

      let source = leftNode
      let target = rightNode

      if (arrow1 === '<-' && arrow2 === '<-') {
        source = rightNode
        target = leftNode
      } else if (arrow1 === '<-' && arrow2 === '->') {
        source = rightNode
        target = leftNode
      } else if (arrow1 === '->' && arrow2 === '<-') {
        source = leftNode
        target = rightNode
      }

      const key = `${source}||${labelText}||${target}`
      if (!seen.has(key)) {
        seen.add(key)
        links.push({ source, target, labelText })
      }

      i += 4
    }
  }

  return links
}

function collectNodes(conceptMap: ConceptMap, links: Array<{ source: string; target: string }>): string[] {
  const names = new Set<string>()
  for (const name of conceptMap.keys()) {
    if (name.length > 0) {
      names.add(name)
    }
  }
  for (const link of links) {
    if (link.source) {
      names.add(link.source)
    }
    if (link.target) {
      names.add(link.target)
    }
  }
  return Array.from(names)
}

function colorForNode(isBaseNode: boolean): string {
  return isBaseNode ? 'rgba(51, 112, 255, 0.98)' : 'rgba(148, 163, 184, 0.98)'
}

function buildGraphData(concepts: ConceptItem[], paths: string[]): { nodes: GraphNodeData[]; links: GraphLinkData[] } {
  const conceptMap = buildConceptMap(concepts)
  const rawLinks = buildLinksFromPaths(paths)
  const nodeNames = collectNodes(conceptMap, rawLinks)

  const degree = new Map<string, number>()
  for (const n of nodeNames) {
    degree.set(n, 0)
  }
  for (const l of rawLinks) {
    degree.set(l.source, (degree.get(l.source) ?? 0) + 1)
    degree.set(l.target, (degree.get(l.target) ?? 0) + 1)
  }

  const nodes: GraphNodeData[] = nodeNames.map((name) => {
    const value = degree.get(name) ?? 0
    const isolated = value === 0
    const isBaseNode = baseNodeSet.value.has(name)
    const color = colorForNode(isBaseNode)
    const size = Math.min(60, Math.max(24, 24 + value * 4))
    const description = conceptMap.get(name) ?? ''

    return {
      id: name,
      name,
      description,
      value,
      symbolSize: size,
      category: isolated ? 0 : 1,
      itemStyle: {
        color,
        shadowBlur: isolated ? 5 : 15,
        shadowColor: isolated ? 'rgba(0, 0, 0, 0.1)' : color,
        borderColor: '#fff',
        borderWidth: 2,
      },
      label: {
        show: true,
        color: '#334155',
        fontSize: isolated ? 11 : 13,
        fontWeight: isolated ? 400 : 600,
        textBorderColor: '#fff',
        textBorderWidth: 2,
      },
    }
  })

  const links: GraphLinkData[] = rawLinks.map((l) => {
    const labelText = l.labelText.trim()
    return {
      source: l.source,
      target: l.target,
      labelText,
      lineStyle: {
        color: '#cbd5e1',
        width: 1.5,
        opacity: 0.8,
        curveness: 0.1,
      },
      label: {
        show: labelText.length > 0,
        formatter: labelText,
        color: '#475569',
        fontSize: 11,
        backgroundColor: '#f1f5f9',
        borderColor: '#e2e8f0',
        borderWidth: 1,
        borderRadius: 4,
        padding: [4, 8],
        shadowBlur: 2,
        shadowColor: 'rgba(0,0,0,0.05)',
      },
    }
  })

  return { nodes, links }
}

const forceLayoutEnabled = ref(true)
const lockedGraphNodes = ref<GraphNodeData[] | null>(null)

function buildGraphOption(
  concepts: ConceptItem[],
  paths: string[],
  isForceLayoutEnabled: boolean,
  fixedNodes?: GraphNodeData[],
): echarts.EChartsOption {
  const { nodes, links } = buildGraphData(concepts, paths)
  const graphNodes = fixedNodes && fixedNodes.length > 0 ? fixedNodes : nodes

  return {
    backgroundColor: {
      type: 'radial',
      x: 0.5,
      y: 0.5,
      r: 0.8,
      colorStops: [
        { offset: 0, color: '#f8fafc' },
        { offset: 1, color: '#f1f5f9' },
      ],
    },
    tooltip: {
      confine: true,
      borderWidth: 1,
      borderColor: '#e2e8f0',
      backgroundColor: 'rgba(255, 255, 255, 0.98)',
      textStyle: { color: '#334155', fontSize: 13 },
      extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); border-radius: 6px;',
      formatter: (params) => {
        const p = Array.isArray(params) ? params[0] : params
        const name = typeof p?.name === 'string' ? p.name : ''
        const dataType = typeof p?.dataType === 'string' ? p.dataType : ''
        const data = (p && typeof p === 'object' && 'data' in p ? (p as any).data : {}) as Record<
          string,
          unknown
        >

        if (dataType === 'node') {
          const description = typeof data.description === 'string' ? data.description : ''
          return description.length > 0
            ? `<div style="font-weight:600; color: #1e293b; margin-bottom: 4px;">${name}</div><div style="color: #64748b; line-height: 1.4;">${description}</div>`
            : name
        }
        if (dataType === 'edge') {
          const labelText = typeof data.labelText === 'string' ? data.labelText : ''
          const source = typeof data.source === 'string' ? data.source : ''
          const target = typeof data.target === 'string' ? data.target : ''
          return `<div style="font-weight:600; color: #1e293b; margin-bottom: 4px;">${source} → ${target}</div><div style="color: #64748b;">${labelText}</div>`
        }
        return name
      },
    },
    animationDuration: 1000,
    animationEasingUpdate: 'quinticInOut',
    series: [
      {
        type: 'graph',
        layout: isForceLayoutEnabled ? 'force' : 'none',
        data: graphNodes,
        links,
        roam: true,
        draggable: true,
        focusNodeAdjacency: true,
        edgeSymbol: ['none', 'arrow'],
        edgeSymbolSize: [4, 12],
        label: {
          position: 'right',
          formatter: '{b}',
        },
        edgeLabel: {
          show: true,
        },
        lineStyle: {
          curveness: 0.1,
        },
        force: isForceLayoutEnabled
          ? {
              repulsion: 1000,
              edgeLength: [120, 350],
              gravity: 0.08,
              layoutAnimation: true,
            }
          : {
              repulsion: 0,
              edgeLength: [0, 0],
              gravity: 0,
              layoutAnimation: false,
            },
        emphasis: {
          scale: true,
          focus: 'adjacency',
          label: { show: true },
          lineStyle: { width: 3, opacity: 1 },
        },
      },
    ],
  }
}

function disposePathGraph() {
  if (activeChart.value) {
    activeChart.value.dispose()
    activeChart.value = null
  }
}

function renderPathGraph() {
  if (!pathGraphRef.value) {
    return
  }
  const concepts = conceptList.value
  const paths = pathList.value

  let chart = echarts.getInstanceByDom(pathGraphRef.value)
  if (!chart) {
    chart = echarts.init(pathGraphRef.value)
  }
  activeChart.value = chart
  const optionNodes = forceLayoutEnabled.value ? undefined : lockedGraphNodes.value ?? undefined
  chart.setOption(buildGraphOption(concepts, paths, forceLayoutEnabled.value, optionNodes), true)
}

function resizePathGraph() {
  if (activeChart.value) {
    activeChart.value.resize()
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null
}

function hasGetModel(value: unknown): value is { getModel: () => unknown } {
  return isRecord(value) && typeof value.getModel === 'function'
}

function hasGetSeriesByIndex(value: unknown): value is { getSeriesByIndex: (index: number) => unknown } {
  return isRecord(value) && typeof value.getSeriesByIndex === 'function'
}

function hasGetData(value: unknown): value is { getData: () => unknown } {
  return isRecord(value) && typeof value.getData === 'function'
}

function hasSeriesDataMethods(
  value: unknown,
): value is { count: () => number; getItemLayout: (index: number) => unknown } {
  return (
    isRecord(value) &&
    typeof value.count === 'function' &&
    typeof value.getItemLayout === 'function'
  )
}

function getGraphNodesWithLayout(): GraphNodeData[] {
  if (!activeChart.value) {
    return []
  }
  const option = activeChart.value.getOption()
  const seriesOption = Array.isArray(option.series) ? option.series[0] : option.series
  if (!seriesOption || !('data' in seriesOption) || !Array.isArray((seriesOption as any).data)) {
    return []
  }

  const baseData = (seriesOption as any).data as unknown[]
  const nodes: GraphNodeData[] = []

  const chartUnknown: unknown = activeChart.value
  const modelUnknown: unknown = hasGetModel(chartUnknown) ? chartUnknown.getModel() : null
  const seriesUnknown: unknown = hasGetSeriesByIndex(modelUnknown)
    ? modelUnknown.getSeriesByIndex(0)
    : null
  const seriesDataUnknown: unknown = hasGetData(seriesUnknown) ? seriesUnknown.getData() : null
  const seriesData = hasSeriesDataMethods(seriesDataUnknown) ? seriesDataUnknown : null

  const itemCount =
    seriesData ? Math.min(seriesData.count(), baseData.length) : 0

  for (let i = 0; i < itemCount; i += 1) {
    const raw = baseData[i]
    if (!isRecord(raw)) {
      continue
    }
    const layout = seriesData ? seriesData.getItemLayout(i) : null

    let x: number | undefined
    let y: number | undefined
    if (Array.isArray(layout) && layout.length >= 2) {
      const lx = layout[0]
      const ly = layout[1]
      if (typeof lx === 'number' && Number.isFinite(lx) && typeof ly === 'number' && Number.isFinite(ly)) {
        x = lx
        y = ly
      }
    } else if (isRecord(layout)) {
      const lx = layout.x
      const ly = layout.y
      if (typeof lx === 'number' && Number.isFinite(lx) && typeof ly === 'number' && Number.isFinite(ly)) {
        x = lx
        y = ly
      }
    }

    const node = { ...(raw as unknown as GraphNodeData) }
    if (x !== undefined && y !== undefined) {
      node.x = x
      node.y = y
    }
    nodes.push(node)
  }

  return nodes
}

function toggleForceLayout() {
  if (!activeChart.value) {
    forceLayoutEnabled.value = !forceLayoutEnabled.value
    return
  }
  const nextState = !forceLayoutEnabled.value

  const currentNodes = getGraphNodesWithLayout()
  if (nextState) {
    lockedGraphNodes.value = null
  } else {
    lockedGraphNodes.value = currentNodes.map((node) => ({ ...node, fixed: true }))
  }

  forceLayoutEnabled.value = nextState

  const optionNodes = nextState
    ? currentNodes.map((node) => {
        const { fixed, ...rest } = node
        return rest
      })
    : lockedGraphNodes.value ?? undefined

  activeChart.value.setOption(
    buildGraphOption(conceptList.value, pathList.value, nextState, optionNodes),
    true,
  )
}

const togglePathGraph = async () => {
  if (!hasPathGraphData.value) {
    return
  }
  if (pathGraphExpanded.value) {
    if (!forceLayoutEnabled.value) {
      const currentNodes = getGraphNodesWithLayout()
      lockedGraphNodes.value = currentNodes.map((node) => ({ ...node, fixed: true }))
    }
    disposePathGraph()
    pathGraphExpanded.value = false
    return
  }

  pathGraphExpanded.value = true
  await nextTick()
  renderPathGraph()
}

watch(
  () => pathToolResultData.value,
  async () => {
    if (pathGraphExpanded.value) {
      await nextTick()
      renderPathGraph()
    }
  },
)

function showSource(row: any) {
  if (props.type === 'log') {
    return true
  } else if (row.write_ed && 500 !== row.status) {
    return true
  }
  return false
}

const regenerationChart = (chat: chatType) => {
  const container = props.chatRecord?.upload_meta
    ? props.chatRecord.upload_meta
    : props.chatRecord.execution_details?.find((detail) => detail.type === 'start-node')

  props.sendMessage(chat.problem_text, {
    re_chat: true,
    image_list: container?.image_list || [],
    document_list: container?.document_list || [],
    audio_list: container?.audio_list || [],
    video_list: container?.video_list || [],
    other_list: container?.other_list || [],
  })
}
const stopChat = (chat: chatType) => {
  props.chatManagement.stop(chat.id)
}
const startChat = (chat: chatType) => {
  props.chatManagement.write(chat.id)
}

onMounted(() => {
  bus.on('chat:stop', () => {
    stopChat(props.chatRecord)
  })
})

onBeforeUnmount(() => {
  disposePathGraph()
})
</script>
<style lang="scss" scoped>
.path-graph-inline-container {
  height: clamp(420px, 60vh, 760px);
  width: 100%;
}

.path-graph-canvas {
  height: 100%;
  width: 100%;
  border-radius: 10px;
  overflow: hidden;
}

.path-graph-title {
  font-weight: 600;
  max-width: 70vw;
}

.path-graph-button {
  font-weight: 600;
}
</style>
