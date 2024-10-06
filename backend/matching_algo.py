import random

def perform_matching(ids_and_scores):
    #matching_scores = [(elem[1] * (2/3) * (1 - elem[2]), elem[0]) for elem in ids_and_scores]
    matching_scores = []
    for vid_id, text_score, static_score, transcript in ids_and_scores:
        curr_score = text_score
        if static_score:
            curr_score *= 0.66
        matching_scores.append((curr_score, vid_id, transcript))
        print(vid_id, text_score, static_score, curr_score)
        
    matching_scores = sorted(matching_scores)[::-1]
    result_dict = dict()
    for i in range(len(matching_scores)):
        if len(matching_scores[i][2]) > 0:
            curr_transcript = random.sample(matching_scores[i][2], 1)
        else:
            curr_transcript = {}
        result_dict.update({matching_scores[i][1]:[i, curr_transcript]})
    return result_dict