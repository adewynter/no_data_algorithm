from sklearn.metrics import f1_score, accuracy_score
from collections import Counter


def print_metrics(labels, successes, test_set, suff, flips=None, return_instead=False):
    """ 
    If flips is None it will only print acc, f1, succ.
    successes must be a summable array
    test_set must be of the form [(x, label)]
    labels must be of the form [label]
    """
    Y = [int(p[-1]) for p in test_set]
    _good_labels = [int(g) for g in labels]
    acc = round(accuracy_score(Y, _good_labels), 3)
    f1 = round(f1_score(Y, _good_labels)*100., 3)
    succ = round(sum(successes)*100/len(test_set), 3)
    if flips is not None:
        flips = [int(g[0]) for g in flips]
        flips = round(sum(flips)*100/len(test_set), 3)
        if not return_instead:
            print(f"{suff}-phenomenon test score: {acc} | Successes: {succ} | F1: {f1} | Flips: {flips}")
        else:
            return acc, f1, succ, flips
    else:
        if not return_instead:
            print(f"{suff}-phenomenon test score: {acc} | Successes: {succ} | F1: {f1}")
        else:
            return acc, f1, succ
        

def get_majority_vote(raw_scores):
    """
    Get majority vote for an array
    """
    scores = raw_scores
    _z = Counter(scores)
    z = _z.most_common()
    if len(z) > 1:
        if z[0][-1] == z[1][-1]:
            return int((z[0][0] + z[1][0])/2)
    return z[0][0]


def count(x):
    # I find this easier to use than counter
    ones, zeros = 0, 0
    for a in x:
        if a == 1: ones += 1
        if a == 0: zeros += 1
    return {1: round(ones*100/len(x), 2), 
            0: round(zeros*100/len(x), 2),
            "other": round((len(x) - ones - zeros)*100/len(x), 2)}
