import numpy as np
import sys
from pathlib import Path
from scipy.stats import entropy
from matplotlib import pyplot as plt

pbooster = None

"""
============================ CLASSES ========================================
Class User is used for defining users. Users are described with attribute topic-frequency.
Class PBooster represents anonymization model. Model is defined by attributes epsilon and lambda.
"""

class User:
    def __init__(self, topic_frequency, name):
        self.topic_frequency = topic_frequency
        self.name = name

class PBooster:
    def __init__(self, lambda_param, epsilon):
        self.epsilon = epsilon
        self.lambda_param = lambda_param


"""
============================= ALGORITHM FUNCTIONS ===========================
"""

def historySize(topic_frequency):
    """ Function takes 1 argument - dictionary topic_frequency, and calculates size of browsing history."""
    history_size = 0
    for topic in topic_frequency:
        history_size += topic_frequency[topic]

    return history_size


def calculateTopicProbability(topic_frequency):
    """ Function takes 1 argument - dictionary topic_frequency, and calculates probability of each topic.
        Result is stored in dictionary and returned."""
    topic_probability = dict()
    history_size = historySize(topic_frequency)

    for topic in topic_frequency:
        topic_probability[topic] = float(topic_frequency[topic] / history_size)

    return topic_probability


def calculatePrivacy(topic_frequency):
    """ Used for calculating privacy. Function takes 1 argument - dictionary topic_frequency.
        Function returns float value that represents level of achieved privacy."""
    probability = calculateTopicProbability(topic_frequency)
    prob_list = []

    for prob in probability:
        prob_list.append(probability[prob])
    privacy = entropy(prob_list, base=10)

    return privacy


def calculateUtilityLoss(topic_frequency, topic_frequency_new):
    """ Used for calculating utility loss. Function takes 2 arguments - dictionaries topic_frequency and topic_frequency_new.
        Function returns float value that represents loss of utility."""
    probability_start = calculateTopicProbability(topic_frequency)
    probability_new = calculateTopicProbability(topic_frequency_new)
    values_start = np.array(list(probability_start.values()))
    values_new = np.array(list(probability_new.values()))

    cos_sim = (np.dot(values_start, values_new))/(np.linalg.norm(values_start)*np.linalg.norm(values_new))
    utility_loss = 0.5 * (1 - cos_sim)

    return utility_loss


def calculateFunctionG(topic_frequency, to_be_added):
    """ Used for calculating optimization function G. Function takes 2 arguments - dictionaries topic_frequency and to_be_added.
        Function returns float value that represents result of G."""
    topic_frequency_new = dict()
    for topic in topic_frequency:
        topic_frequency_new[topic] = topic_frequency[topic] + to_be_added[topic]

    privacy = calculatePrivacy(topic_frequency_new)
    utility_loss = calculateUtilityLoss(topic_frequency, topic_frequency_new)
    G_function = (pbooster.lambda_param * privacy) - utility_loss

    return G_function

def topicSelection(user):
    """ Function represents greedy LS algorithm with goal of maximizing non-monotone non-negative submodular function.
        Algorithm is based on adding and subtracting elements from ground set to_be_added until no improvement in G can be done.
        Function takes 1 argument - object of class User that defines user who's browsing history is being anonymized.
        Function returns dictionary to_be_added that represents result of optimization algorithm."""
    n = len(user.topic_frequency)
    bound_check = float(1 + (pbooster.epsilon/n**2))

    to_be_added = dict()
    topic_freq_new = dict()

    for topic in user.topic_frequency:
        to_be_added[topic] = 0
        topic_freq_new[topic] = user.topic_frequency[topic]

    val = 0
    restart = False
    while True:

        """ Adding elements """
        for topic in to_be_added:
            modified = to_be_added.copy()
            modified[topic] += 1
            G_modified = calculateFunctionG(user.topic_frequency, modified)

            if G_modified > bound_check*val:
                to_be_added = modified.copy()
                val = G_modified
                restart = True
                break

        if restart:
            restart = False
            continue

        """ Subtracting elements """
        for topic in to_be_added:
            modified = to_be_added.copy()
            if modified[topic] - 1 < 0:
                continue
            modified[topic] -= 1
            G_modified = calculateFunctionG(user.topic_frequency, modified)

            if G_modified > bound_check*val:
                to_be_added = modified.copy()
                val = G_modified
                restart = True
                break
        if restart:
            restart = False
            continue

        return to_be_added


"""
======================== READING DATA ===================================
Function for reading artificially created data located in separate file.
"""

def readData(file):
    with open(file, encoding="utf8") as fp:
        users = []
        for line in fp:
            line = line.strip('\n')
            if line.startswith('#'):
                continue
            elif line.startswith('Lambda'):
                lambda_params = ((line.split(': '))[1]).split(', ')
            elif line.startswith('Epsilon'):
                epsilon = float((line.split(': '))[1])
            elif line.startswith('User'):
                freq_dict = dict()
                line = line.split(': ')
                topics = line[1].split(', ')
                for topic in topics:
                    key_value = topic.split(' ')
                    freq_dict[key_value[0]] = int(key_value[1])
                target = User(freq_dict, line[0])
                users.append(target)

    return lambda_params, epsilon, users


"""
================================ MAIN =====================================
"""

def main():
    global pbooster
    userData = Path(sys.argv[1])

    lambda_params, epsilon, users = readData(userData)

    """Finding optimal privacy and utility loss for user with browsing history size = 50 and different values of lambda."""
    target = None
    privacyAxis, utilityAxis = [], []
    for U in users:
        if U.name == 'User50':
            target = U

    for param in lambda_params:
        pbooster = PBooster(float(param), epsilon)
        a = topicSelection(target)

        c_new = dict()
        for topic in target.topic_frequency:
            c_new[topic] = target.topic_frequency[topic] + a[topic]

        privacyValue = calculatePrivacy(c_new)
        privacyAxis.append(privacyValue)
        utilityLossValue = calculateUtilityLoss(target.topic_frequency, c_new)
        utilityAxis.append(1-utilityLossValue)

        print("Lambda: ", param)
        print("Privacy: ", privacyValue)
        print("Utility: ", 1 - utilityLossValue)
        print("===================================")

    """Plots graph that shows affect of lambda parameter on utility for user with browsing history size = 50."""
    plt.plot(lambda_params, utilityAxis, 'o')
    plt.xlabel('Lambda')
    plt.ylabel('Korisnost')
    plt.show()

    """Plots graph that shows effect of lambda parameter on privacy for user with browsing history size = 50.."""
    plt.plot(lambda_params, privacyAxis, 'o')
    plt.xlabel('Lambda')
    plt.ylabel('Privatnost')
    plt.show()

    """Finding optimal privacy and utility loss for users with browsing history size = 25 and lambda = 10."""
    param = 0
    privacyAxis, utilityAxis, users25 = [], [], []
    for L in lambda_params:
        if L == '10':
            param = L
    for U in users:
        if U.name == 'User25':
            users25.append(U)

    for target in users25:
        pbooster = PBooster(float(param), epsilon)
        a = topicSelection(target)

        c_new = dict()
        for topic in target.topic_frequency:
            c_new[topic] = target.topic_frequency[topic] + a[topic]

        privacyValue = calculatePrivacy(c_new)
        privacyAxis.append(privacyValue)
        utilityLossValue = calculateUtilityLoss(target.topic_frequency, c_new)
        utilityAxis.append(1-utilityLossValue)

        print("User: ", target.name)
        print("Privacy: ", privacyValue)
        print("Utility: ", 1-utilityLossValue)
        print("===================================")

    """Plots graph that shows privacy and utility for users with  browsing history size = 25 and lambda = 10."""
    plt.plot(utilityAxis, privacyAxis, 'o')
    plt.xlabel('Korisnost')
    plt.ylabel('Privatnost')
    plt.show()

if __name__ == '__main__':
    main()
