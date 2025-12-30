# coding=utf-8
"""
    @project: maxkb
    @Author：虎
    @file： base_generate_human_message_step.py.py
    @date：2024/1/10 17:50
    @desc:
"""
import json
from typing import List, Dict

from langchain.schema import BaseMessage, HumanMessage
from langchain_core.messages import SystemMessage

from application.chat_pipeline.I_base_chat_pipeline import ParagraphPipelineModel
from application.chat_pipeline.step.generate_human_message_step.i_generate_human_message_step import \
    IGenerateHumanMessageStep
from application.models import ChatRecord
from common.utils.common import flat_map
from common.utils.http_client import GraphQueryResult


class BaseGenerateHumanMessageStep(IGenerateHumanMessageStep):

    def execute(self, problem_text: str,
                paragraph_list: List[ParagraphPipelineModel],
                history_chat_record: List[ChatRecord],
                dialogue_number: int,
                max_paragraph_char_number: int,
                prompt: str,
                graph_query_result:List[GraphQueryResult],
                padding_problem_text: str = None,
                no_references_setting=None,
                system=None,
                **kwargs) -> List[BaseMessage]:
        prompt = prompt if (paragraph_list is not None and len(paragraph_list) > 0) else no_references_setting.get(
            'value')
        exec_problem_text = padding_problem_text if padding_problem_text is not None else problem_text
        start_index = len(history_chat_record) - dialogue_number
        history_message = [[history_chat_record[index].get_human_message(), history_chat_record[index].get_ai_message()]
                           for index in
                           range(start_index if start_index > 0 else 0, len(history_chat_record))]
        if system is not None and len(system) > 0:
            return [SystemMessage(system), *flat_map(history_message),
                    self.to_human_message(prompt, exec_problem_text, max_paragraph_char_number, paragraph_list,
                                          no_references_setting,graph_query_result)]

        return [*flat_map(history_message),
                self.to_human_message(prompt, exec_problem_text, max_paragraph_char_number, paragraph_list,
                                      no_references_setting,graph_query_result)]

    @staticmethod
    def to_human_message(prompt: str,
                         problem: str,
                         max_paragraph_char_number: int,
                         paragraph_list: List[ParagraphPipelineModel],
                         no_references_setting: Dict,graph_query_result:List[GraphQueryResult]):
        if paragraph_list is None or len(paragraph_list) == 0:
            concept_list = []
            for gqr in graph_query_result:
                for c in gqr.concept:
                    concept_list.append(f"<concept>{c}</concept>")
            concepts = "\n".join(concept_list)
            triple_list = []
            for gqr in graph_query_result:
                for t in gqr.triple:
                    triple_list.append(f"<triple>{t}</triple>")
            triples = "\n".join(triple_list)
            retrieval_content_list = []
            for gqr in graph_query_result:
                for r in gqr.retrieval_content:
                    retrieval_content_list.append(f"<retrieval_content>{r}</retrieval_content>")
            retrieval_contents = "\n".join(retrieval_content_list)
            if no_references_setting.get('status') == 'ai_questioning':
                value = (no_references_setting.get('value')
                    .replace('{question}', problem)
                    .replace('{data}', '')
                    .replace('{concept}', concepts)
                    .replace('{triple}', triples)
                    .replace('{retrieval_content}',retrieval_contents))
                print(f'没有从知识库召回到内容:{value},graph_query_result:{[gqr.model_dump() for gqr in graph_query_result]}')
                return HumanMessage(
                    content=value)
            else:
                value=(prompt.replace('{data}', "")
                                    .replace('{concept}', concepts)
                                    .replace('{triple}', triples)
                                    .replace('{retrieval_content}', retrieval_contents)
                                    .replace('{question}', problem))
                print(f"没有从知识库召回到内容 not ai_questioning:{value},graph_query_result:{[gqr.model_dump() for gqr in graph_query_result]}")
                return HumanMessage(content=value)
        temp_data = ""
        data_list = []
        exist_chunk:set[str] = set()
        for p in paragraph_list:
            exist_chunk.add(p.content)
            content = f"{p.title}:{p.content}"
            temp_data += content
            if len(temp_data) > max_paragraph_char_number:
                row_data = content[0:max_paragraph_char_number - len(temp_data)]
                data_list.append(f"<data>{row_data}</data>")
                break
            else:
                data_list.append(f"<data>{content}</data>")
        data = "\n".join(data_list)
        concept_list = []
        for gqr in graph_query_result:
            for c in gqr.concept:
                concept_list.append(f"<concept>{c}</concept>")
        concepts = "\n".join(concept_list)
        triple_list = []
        for gqr in graph_query_result:
            for t in gqr.triple:
                triple_list.append(f"<triple>{t}</triple>")
        triples = "\n".join(triple_list)
        retrieval_content_list = []
        for gqr in graph_query_result:
            for r in gqr.retrieval_content:
                if r in exist_chunk:
                    continue
                retrieval_content_list.append(f"<retrieval_content>{r}</retrieval_content>")
        retrieval_contents = "\n".join(retrieval_content_list)
        value = (prompt.replace('{data}', data)
                            .replace('{concept}', concepts)
                            .replace('{triple}', triples)
                            .replace('{retrieval_content}', retrieval_contents)
                            .replace('{question}', problem))
        print(f"知识库召回了内容:prompt:{prompt},replace_value:{value},graph_query_result:{[gqr.model_dump() for gqr in graph_query_result]}")
        return HumanMessage(content=value)
