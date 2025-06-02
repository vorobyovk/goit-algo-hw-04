def merge_two_lists(list1, list2):
    merged = []
    i, j = 0, 0
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            merged.append(list1[i])
            i += 1
        else:
            merged.append(list2[j])
            j += 1    
    merged.extend(list1[i:])
    merged.extend(list2[j:])
    return merged

def merge_k_lists(lists):    
    if not lists:
        return []
    if len(lists) == 1:
        return lists[0]
    
    while len(lists) > 1:
        merged_iteration = []
        # Зливаємо списки попарно
        for i in range(0, len(lists), 2):
            list1 = lists[i]
            if (i + 1) < len(lists):
                list2 = lists[i+1]
                merged_iteration.append(merge_two_lists(list1, list2))
            else:
                merged_iteration.append(list1)
        lists = merged_iteration
        
    return lists[0]

# Приклад використання:
lists1 = [[1, 4, 5], [1, 3, 4], [2, 6]]
merged_list1 = merge_k_lists(lists1)
print(f"Списки для злиття: {lists1}")
print(f"Відсортований список: {merged_list1}") 

lists2 = [[], [1, 2, 3], [], [0, 5]]
merged_list2 = merge_k_lists(lists2)
print(f"\nСписки для злиття: {lists2}")
print(f"Відсортований список: {merged_list2}") 

lists3 = [[10, 20], [15, 25], [5, 30], [1, 12]]
merged_list3 = merge_k_lists(lists3)
print(f"\nСписки для злиття: {lists3}")
print(f"Відсортований список: {merged_list3}") 

lists4 = [[1,2,3]]
merged_list4 = merge_k_lists(lists4)
print(f"\nСписки для злиття: {lists4}")
print(f"Відсортований список: {merged_list4}") 

lists5 = []
merged_list5 = merge_k_lists(lists5)
print(f"\nСписки для злиття: {lists5}")
print(f"Відсортований список: {merged_list5}") 