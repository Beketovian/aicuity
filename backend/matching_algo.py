
def perform_matching(ids_and_scores):
    matching_scores = [(elem[1] * (2/3) * (1 - elem[2]), elem[0]) for elem in ids_and_scores]
    matching_scores = sorted(matching_scores)
    result_dict = {matching_scores[i][1]:i for i in range(len(matching_scores))}
    return result_dict