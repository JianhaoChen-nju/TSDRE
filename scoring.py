from typing import Dict, List, Tuple

import json
from data_process import RawPred, Sentence, Data


def safe_divide(a: float, b: float) -> float:
    if a == 0.0 or b == 0.0:
        return 0.0
    return a / b


class Scorer:
    name: str = ""

    def run(self, pred: List[Sentence], gold: List[Sentence]) -> Dict[str, float]:
        raise NotImplementedError


class StrictScorer:
    name: str = "strict triplet"

    def make_sent_tuples(
        self, s: Sentence
    ) -> List[Tuple[Tuple[int, int, str], Tuple[int, int, str], str]]:
        id_to_entity = {e.span: e for e in s.entities}
        tuples = []
        for r in s.relations:
            head = id_to_entity[r.head]
            tail = id_to_entity[r.tail]
            t = (
                (head.span[0], head.span[1], head.label),
                (tail.span[0], tail.span[1], tail.label),
                r.label,
            )
            tuples.append(t)
        return tuples

    def match_gold_to_pred(
        self, pred: List[Sentence], gold: List[Sentence]
    ) -> List[Sentence]:
        assert self is not None
        text_to_pred = {p.text: p for p in pred}
        empty = RawPred.empty().as_sentence(None)
        matched = [text_to_pred.get(s.text, empty) for s in gold]
        print("\nHow many gold sents have no matching pred?")
        print(dict(num=len([p for p in matched if p == empty])))
        return matched

    def run(self, pred: List[Sentence], gold: List[Sentence]) -> Dict[str, float]:
        pred = self.match_gold_to_pred(pred, gold)
        assert len(pred) == len(gold)
        num_correct = 0
        num_pred = 0
        num_gold = 0
        have_time_sent_cnt_gold=0
        have_time_sent_cnt_pred=0
        f=open("time_qualifier_related_results.tsv","a")
        for p, g in zip(pred, gold):
            tuples_pred = self.make_sent_tuples(p)
            tuples_pred_copy=tuples_pred.copy()
            tuples_gold = self.make_sent_tuples(g)
            tuples_gold_copy= tuples_gold.copy()
            tuples_matched=[]
            num_pred += len(tuples_pred)
            num_gold += len(tuples_gold)

            time_q_pred=0
            time_q_gold=0
            for a in tuples_pred:
                for a_ele in a:
                    if str(a_ele).endswith("time") or str(a_ele).endswith("date"):
                        time_q_pred+=1
                        break
            for a in tuples_gold:
                for a_ele in a:
                    if str(a_ele).endswith("time") or str(a_ele).endswith("date"):
                        time_q_gold+=1
                        break
            if time_q_gold>0:
                have_time_sent_cnt_gold+=1
            if time_q_pred>0:
                have_time_sent_cnt_pred+=1
            for a in tuples_gold:
            # for a in tuples_pred:
                matched=0
                head = " ".join(g.tokens[a[0]:a[1]])
                tail = " ".join(g.tokens[a[2]:a[3]])
                relation = a[6]
                qualifier = a[7]
                time = " ".join(g.tokens[a[4]:a[5]])
                a_str = "'"+head + "', '" + relation + "', '" + tail + "', '" + qualifier + "', '" + time+"'"
                for b in tuples_pred:
                # for b in tuples_gold:
                    # print(g.tokens,a)
                    # my own modify
                    head = " ".join(g.tokens[b[0]:b[1]])
                    tail = " ".join(g.tokens[b[2]:b[3]])
                    relation = b[6]
                    qualifier = b[7]
                    time = " ".join(g.tokens[b[4]:b[5]])
                    b_str = "'"+head + "', '" + relation + "', '" + tail + "', '" + qualifier + "', '" + time+"'"
                    if a_str==b_str:
                    # if a_str_no_space==b_str_no_space:
                        matched=1
                        # print(a_str)
                        # print(" ".join(g.tokens) + "\t" + "[" + a_str + "]")
                        num_correct += 1
                        if a[-1].endswith("time") or a[-1].endswith("date"):
                            time_q_pred -= 1
                            time_q_gold -= 1
                        # tuples_pred_copy.remove(a)
                        # tuples_gold_copy.remove(b)
                        # tuples_matched.append(a)
                        break
                    # if a == b:
                    #     num_correct += 1
                    #     if a[-1].endswith("time") or a[-1].endswith("date"):
                    #         time_q_pred-=1
                    #         time_q_gold-=1
                    #     tuples_pred_copy.remove(a)
                    #     tuples_gold_copy.remove(b)
                    #     tuples_matched.append(a)
                    #     break
                    # else:
                    #     print(a,b)
                #recall negative
                #precision negative
                #if matched==0:
                    #print(" ".join(g.tokens) + "\t" + "[" + a_str + "]")

            if time_q_gold!=0 or time_q_pred!=0:
                f.write("%d\t%d\t%s\t%s\t[" %(time_q_gold,time_q_pred,g.text,p.text))
                for a in tuples_gold_copy:
                    s_value=" ".join([g.tokens[i] for i in range (a[0],a[1])])
                    o_value=" ".join([g.tokens[i] for i in range (a[2],a[3])])
                    q_value=" ".join([g.tokens[i] for i in range (a[4],a[5])])
                    f.write("(%s, %s, %s, %s, %s), " %(s_value,o_value,q_value,a[6],a[7]))
                f.write("]\t[")
                for a in tuples_pred_copy:
                    s_value=" ".join([g.tokens[i] for i in range (a[0],a[1])])
                    o_value=" ".join([g.tokens[i] for i in range (a[2],a[3])])
                    q_value=" ".join([g.tokens[i] for i in range (a[4],a[5])])
                    f.write("(%s, %s, %s, %s, %s), " %(s_value,o_value,q_value,a[6],a[7]))
                f.write("]\t[")
                for a in tuples_matched:
                    s_value=" ".join([g.tokens[i] for i in range (a[0],a[1])])
                    o_value=" ".join([g.tokens[i] for i in range (a[2],a[3])])
                    q_value=" ".join([g.tokens[i] for i in range (a[4],a[5])])
                    f.write("(%s, %s, %s, %s, %s), " %(s_value,o_value,q_value,a[6],a[7]))
                f.write("]\n")
        f.close()
        print("gold have time qualifier %d" %have_time_sent_cnt_gold)
        print("pred have time qualifier %d" %have_time_sent_cnt_pred)
        precision = safe_divide(num_correct, num_pred)
        recall = safe_divide(num_correct, num_gold)
        f1 = safe_divide(2 * precision * recall, precision + recall)

        return dict(
            num_correct=num_correct,
            num_pred=num_pred,
            num_gold=num_gold,
            precision=precision,
            recall=recall,
            f1=f1,
        )


class EntityScorer(StrictScorer):
    name: str = "entity"

    def make_sent_tuples(self, s: Sentence) -> List[Tuple[int, int, str]]:
        tuples = [(e.span[0], e.span[1], e.label) for e in s.entities]
        return sorted(set(tuples))


class QuintupletScorer(StrictScorer):
    name: str = "quintuplet"

    def make_sent_tuples(
        self, s: Sentence
    ) -> List[Tuple[int, int, int, int, int, int, str, str]]:
        tuples = []
        for r in s.relations:
            for q in r.qualifiers:
                t = (
                    r.head[0],
                    r.head[1],
                    r.tail[0],
                    r.tail[1],
                    q.span[0],
                    q.span[1],
                    r.label,
                    q.label,
                )
                tuples.append(t)
        return tuples


def score_preds(path_pred: str, path_gold: str) -> dict:
    preds = Data.load(path_pred).sents
    sents = Data.load(path_gold).sents
    results = {}
    # for scorer in [EntityScorer(), StrictScorer(), QuintupletScorer()]:
    for scorer in [QuintupletScorer()]:
        results[scorer.name] = scorer.run(preds, sents)
    print(json.dumps(results, indent=2))
    return results