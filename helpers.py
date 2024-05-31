def generate_conditional_pattern_base(tree, prefix):
    conditional_pattern_base = {}
    for item, node in tree.items():
        new_prefix = prefix.copy()
        new_prefix.append(item)
        support = node['count']

        # Tambahkan ke conditional pattern base
        conditional_pattern_base[tuple(new_prefix)] = support

        # Rekursif untuk anak-anak node
        conditional_pattern_base.update(
            generate_conditional_pattern_base(node['children'], new_prefix))
    return conditional_pattern_base

def build_conditional_fp_tree(conditional_pattern_base):
    conditional_fp_tree = {}
    for pattern, support in conditional_pattern_base.items():
        current_node = conditional_fp_tree
        for item in pattern:
            if item not in current_node:
                current_node[item] = {'count': support,
                                      'parent': None, 'children': {}}
            else:
                current_node[item]['count'] += support
            if 'parent' in current_node[item]:
                current_node[item]['parent'] = current_node
            current_node = current_node[item]['children']
    return conditional_fp_tree

def generate_frequent_patterns(tree, min_support, prefix, frequent_patterns):
    for item, node in tree.items():
        new_prefix = prefix.copy()
        new_prefix.append(item)
        support = node['count']

        # Tambahkan ke frequent patterns jika support mencukupi
        if support >= min_support:
            frequent_patterns[tuple(new_prefix)] = support

        # Rekursif untuk anak-anak node
        generate_frequent_patterns(
            node['children'], min_support, new_prefix, frequent_patterns)

# Fungsi untuk menghasilkan Frequent 2-itemsets
def generate_frequent_2_itemsets(tree, min_support, frequent_2_itemsets):
    # Iterasi melalui setiap item pada Conditional FP-tree
    for item, node in tree.items():
        support_item = node['count']
        # Cek apakah item tersebut memenuhi syarat support
        if support_item >= min_support:
            # Jika memenuhi, iterasi lagi untuk mencari item yang memiliki support cukup
            for child_item, child_node in node['children'].items():
                support_2_itemset = child_node['count']
                # Cek apakah pasangan item memenuhi syarat support
                if support_2_itemset >= min_support:
                    # Tambahkan ke frequent 2-itemsets
                    frequent_2_itemsets[(item, child_item)] = support_2_itemset
def calculate_lift(itemset, support_AB, support_A, support_B):
    return support_AB / (support_A * support_B)

# Fungsi untuk mengevaluasi kualitas aturan asosiasi
def evaluate_association_rules(association_rules, frequent_patterns):
    evaluation_results = {}
    for itemset, support_AB in association_rules.items():
        item_A, item_B = itemset
        support_A = frequent_patterns.get((item_A,), 0)
        support_B = frequent_patterns.get((item_B,), 0)
        confidence = support_AB / support_A
        lift = calculate_lift(itemset, support_AB, support_A, support_B)
        evaluation_results[itemset] = {'support_AB': support_AB, 'support_A': support_A,
                                       'support_B': support_B, 'confidence': confidence, 'lift': lift}
    return evaluation_results
def get_item_names(df, group_name):
    return df[df["item group"] == group_name]["item name"].unique().tolist()
