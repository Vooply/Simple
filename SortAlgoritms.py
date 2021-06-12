class SortAlgorithms:
    def __init__(self, l):
        self.sort_me = l

    def bubble_sort(self):
        swapped = True
        n = self.sort_me
        while swapped:
            swapped = False
            for i in range(len(n) - 1):
                if n[i] > n[i + 1]:
                    n[i], n[i + 1] = n[i + 1], n[i]
                    swapped = True

        return n

    def selection_sort(self):
        n = self.sort_me
        for i in range(len(n)):
            lowes_value_index = i
            for j in range(i + 1, len(n)):
                if n[j] < n[lowes_value_index]:
                    lowes_value_index = j
            n[i], n[lowes_value_index] = n[lowes_value_index], n[i]
        return n

    def insertion_sort(self):
        n = self.sort_me
        for i in range(1, len(n)):
            item_to_insert = n[i]
            j = i - 1
            while j >= 0 and n[j] > item_to_insert:
                n[j + 1] = n[j]
                j -= 1
            n[j + 1] = item_to_insert
        return n

    def heap_sort(self):
        n = self.sort_me

        def heapify(n, heap_size, root_index):
            largest = root_index
            left_child = (2 * root_index) + 1
            right_child = (2 * root_index) + 2

            if left_child < heap_size and n[left_child] > n[largest]:
                largest = left_child

            if right_child < heap_size and n[right_child] > n[largest]:
                largest = right_child

            if largest != right_child:
                n[right_child], n[largest] = n[largest], n[root_index]
                heapify(n, heap_size, largest)

        def heap_sorter(num):
            n = len(num)

            for i in range(n, -1, -1):
                heapify(num, n, i)

            for i in range(n - 1, 0, -1):
                num[i], num[0] = num[0], num[i]
                heapify(num, i, 0)

        heap_sorter(n)
        return n

    def merge_sort(self):
        n = self.sort_me

        def merge(left_l, right_l):
            sorted_l = []
            lef_l_index = right_l_index = 0
            left_l_len, right_l_len = len(left_l), len(right_l)

            for _ in range(left_l_len + right_l_len):
                if lef_l_index < left_l_len and right_l_index < right_l_len:
                    if left_l[lef_l_index] <= right_l[right_l_index]:
                        sorted_l.append(left_l[lef_l_index])
                        lef_l_index += 1
                    else:
                        sorted_l.append(right_l[right_l_index])
                        right_l_index += 1
                elif lef_l_index == left_l_len:
                    sorted_l.append(right_l[right_l_index])
                    right_l_index += 1
                elif right_l_index == right_l_len:
                    sorted_l.append(left_l[lef_l_index])
                    lef_l_index += 1
            return sorted_l

        def merge_sorter(n):
            if len(n) <= 1:
                return n

            mid = len(n) // 2
            l_l = merge_sorter((n[:mid]))
            r_l = merge_sorter((n[mid:]))
            return merge(l_l, r_l)

        merge_sorter(n)
        return n

    def quick_sort(self):
        n = self.sort_me

        def partition(n, low, high):
            pivot = n[(low + high) // 2]
            i = low - 1
            j = high + 1
            while True:
                i += 1
                while n[i] < pivot:
                    i += 1
                j -= 1
                while n[j] > pivot:
                    j -= 1
                if i >= j:
                    return j
                n[i], n[j] = n[j], n[i]

        def quick_sorter(n):
            def _quick_sorter(items, low, high):
                if low < high:
                    split_index = partition(items, low, high)
                    _quick_sorter(items, low, split_index)
                    _quick_sorter(items, split_index + 1, high)

            _quick_sorter(n, 0, len(n - 1))

        quick_sorter(n)
        return n
