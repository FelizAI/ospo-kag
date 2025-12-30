interface knowledgeData {
  name: string
  folder_id?: string
  desc: string
  embedding_model_id?: string
  documents?: Array<any>
}

interface KnowledgeGraphBindingItem {
  id: string
  knowledge_id: string
  instance_id: string
  create_time: string
  update_time: string
}

export type { knowledgeData, KnowledgeGraphBindingItem }
