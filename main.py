import pandas as pd
import itertools
import json


def is_sublist(list1, list2):  # return true if list 2 is sublist of list1
    return all(item in list1 for item in list2)


def filter_item_support(item_support_count, threshold):
    filtered_dict = {k: {k1: v1 for k1, v1 in v.items() if v1 >= threshold} for k, v in item_support_count.items()}
    return filtered_dict


def get_item_combinations(items_set, number_of_items_in_list):  # gets different combinations of elements in a list
    return itertools.combinations(items_set, number_of_items_in_list)


def get_item_list(trans_dic, combination_list, number_of_items_in_list, min_sup_count, item_support_count):  # recursion?  # item_set changes in 2 item list (to be the new output of the 1 item list)
    if number_of_items_in_list > 3:  # base case
        return item_support_count

    item_support_count[number_of_items_in_list] = {}
    # get the different combinations of elements (that has > min support count)
    combinations = get_item_combinations(combination_list, number_of_items_in_list)
    # loop through all the combinations (maybe 1 item) see how many it occurs throughout the {trans_dic}
    for item in combinations:
        item_support_count[number_of_items_in_list][item] = 0
        # then get all the support count
        for transaction in trans_dic.values():
            if is_sublist(transaction, item):
                item_support_count[number_of_items_in_list][item] = item_support_count[number_of_items_in_list][
                                                                        item] + 1
    # removes items that is below the min sup count
    item_support_count = filter_item_support(item_support_count, min_sup_count)
    return get_item_list(trans_dic, combination_list, number_of_items_in_list + 1, min_sup_count, item_support_count)


def convert_dict_keys_to_str(input_dict):
    if isinstance(input_dict, dict):
        new_dict = {}
        for key, value in input_dict.items():
            if isinstance(key, tuple):
                new_key = str(key)
            else:
                new_key = str(key)
            new_dict[new_key] = convert_dict_keys_to_str(value)
        return new_dict
    elif isinstance(input_dict, list):
        return [convert_dict_keys_to_str(element) for element in input_dict]
    else:
        return input_dict


def select_item_sets(item_sets):  # select item sets
    if item_sets[3]:
        return item_sets[3]
    elif item_sets[2]:
        return item_sets[2]
    else:
        return item_sets[1]


def calc_support_confidence(rules, transactions, min_confidence):
    """
    parameters: all the association rules and the transaction tables
    algorithm: loop through the association rules check the cache if exists (take the support count value) if not
                compute it.
    """
    output = []
    count_cache = {}
    # ( (x) , (y,z)  )       it means x->y,z  association rule
    for rule in rules:
        merged_tuple = tuple(sorted(tuple(itertools.chain.from_iterable(rule))))
        antecedent = tuple(sorted(tuple(rule[0])))

        if merged_tuple not in count_cache:
            count_cache[merged_tuple] = 0
            for transaction in transactions.values():
                if is_sublist(transaction, merged_tuple):
                    count_cache[merged_tuple] += 1

        if antecedent not in count_cache:
            count_cache[antecedent] = 0
            for transaction in transactions.values():
                if is_sublist(transaction, rule[0]):
                    count_cache[antecedent] += 1

        confidence = count_cache[merged_tuple] / count_cache[antecedent]
        confidence_type = "weak"
        if confidence >= min_confidence:
            confidence_type = "strong"
        rule_confidence = ", ".join(antecedent) + " -> " + ", ".join(rule[1]) + \
                          " confidence = " + str(confidence*100) + "%--->" + confidence_type
        output.append(rule_confidence)

    return output


def generate_association_rules(items):  # for association rules for items
    # Generate all possible combinations of the items
    item_combinations = []
    for i in range(1, len(items)):
        item_combinations += list(itertools.combinations(items, i))

    # Generate association rules
    association_rules = []
    for combination in item_combinations:
        remaining_items = tuple(set(items) - set(combination))
        association_rules.append((combination, remaining_items))
    return association_rules


def apriori():
    df = pd.read_excel('CoffeeShopTransactions.xlsx', usecols=lambda column: column not in ['Date', 'Time'])

    trans_dict = {}  # hold the transactions with relationships aka all data in memory
    item_set = set()  # holds all the unique elements
    size_of_transaction = len(df)
    min_supp = float(input("Enter the minimum support: "))  # support has to be a value between 0~1 float
    min_supp_count = float(min_supp) * size_of_transaction

    min_confidence = float(input("Enter the minimum confidence : "))

    for index, row in df.iterrows():  # Build the transaction dictionary
        transaction_id = row['Transaction Number']
        Item_1 = row['Item 1'].lower().replace(" ", "")  # Normalize the data
        Item_2 = row['Item 2'].lower().replace(" ", "")
        Item_3 = row['Item 3'].lower().replace(" ", "")

        item_set.add(Item_1)
        item_set.add(Item_2)
        item_set.add(Item_3)

        trans_dict[transaction_id] = list({Item_1, Item_2, Item_3})

    items = get_item_list(trans_dict, item_set, 1, min_supp_count, {})  # generates all frequent item lists
    selected_items = select_item_sets(items)  # generate association rules then calculate confidence

    frequent_item_list = convert_dict_keys_to_str(items)
    print("Frequent item lists: ")
    print(json.dumps(frequent_item_list, indent=4))

    for item in selected_items:
        rules = generate_association_rules(item)
        for string in calc_support_confidence(rules, trans_dict, min_confidence):
            print(string)
        print()


apriori()

# print(generate_association_rules(('coffee', 'tea', 'juice')))
# calc_support_confidence((('tea',), ('coffe', 'juice')),"test")
