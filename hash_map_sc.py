# Name: Olivia Chen
# Course: CS261 - Data Structures
# Description: Implements a HashMap using the method
# Separate Chaining with a linked list

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates a key/value pair in the hash map. If the given key already
        exists, the associated value is replaced with the new value
        If the key does not exist, a new key/value pair is added
        If the load factor is greater than or equal to 1, the table's
        size will be doubled
        """

        # if load factor >= 1: resize_table(self._capacity*2)
        if self.table_load() >= 1:
            self.resize_table(self._capacity*2)

        # compute an index
        hash = self._hash_function(key)
        index = hash % self._capacity       # the bucket index

        bucket = self._buckets.get_at_index(index)      # the linked list bucket

        for node in bucket:
            if node.key == key:             # key already exists, update value
                node.value = value
                return

        bucket.insert(key, value)
        self._size+=1

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table. All existing key/value
        pairs will be moved to the new table by rehashing the links
        If new_capacity is less than 1, this does nothing
        If new_capacity is 1+, check if it is prime. If not, it is changed
        to the next highest prime number using the methods _is_prime()
        and _next_prime()
        """
        if new_capacity < 1:
            return

        # if not prime, go to next prime number
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)
        self._capacity = new_capacity

        # rehash the links
        old_table = self._buckets
        self._buckets = DynamicArray()
        self._size = 0

        # build the new hash table -> sized based on new capacity
        for index in range(self._capacity):
            self._buckets.append(LinkedList())

        for index in range(old_table.length()):
            bucket = old_table[index]           # get the bucket
            for item in bucket:
                self.put(item.key, item.value)


    def table_load(self) -> float:
        """
        Returns the current hash table's load factor
        """

        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        empty = 0
        for index in range(self._capacity):
            bucket = self._buckets[index]       # get the linked list
            if bucket._size == 0:    # check if bucket is empty
                empty +=1

        return empty


    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key
        If the key is not in the hash map, returns None
        """
        value = None

        # compute the hash to get the bucket
        hash = self._hash_function(key) % self._capacity
        bucket = self._buckets[hash]

        for val in bucket:
            if key == val.key:
                return val.value

        return value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key exists in the hash map, otherwise
        returns False. If the hash map is empty, returns False
        """
        if self._size == 0:
            return False

        # get hash/index and bucket(ll)
        hash = self._hash_function(key) % self._capacity
        bucket = self._buckets[hash]

        # iterate through bucket to find matching key
        for node in bucket:
            if node.key == key:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes a given key and its associated value from the hash map
        If the key does not exist in the hash map, does nothing
        (no exception raised)
        """
        hash = self._hash_function(key) % self._capacity
        bucket = self._buckets[hash]

        # key doesn't exist, do nothing
        if bucket.length() == 0:
            return

        # iterate through LL bucket
        for node in bucket:
            if node.key == key:
                bucket.remove(node.key)
                self._size -=1


    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a
        key/value pair stored in the hash map
        """
        key_val = DynamicArray()

        # iterate through hash map to get the bucket
        for index in range(self._capacity):
            bucket = self._buckets[index]

            # iterate through the bucket (LL)
            for node in bucket:
                key_val.append((node.key, node.value))

        return key_val

    def clear(self) -> None:
        """
        Clears the hash table contents without changing the underlying
        capacity
        """
        # sets an empty linked list to each bucket
        for index in range(self._capacity):
            self._buckets[index] = LinkedList()

        # re-initialize size
        self._size = 0



def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Receives an unsorted dynamic array and returns a tuple containing
    a new dynamic array comprised of the mode(s) of the unsorted array
    and the frequency of its occurrence
    O(N) runtime complexity
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    mode_da = DynamicArray()        # return array

    # if array is empty
    if da.length() == 0:
        return mode_da, 0

    # put input array into a hashmap in order to "sort" values
    for index in range(da.length()):
        if map.table_load() >= 1:
            map.resize_table(map._capacity * 2)

        # get hash and its bucket/index
        hash = map._hash_function(da[index]) % map.get_capacity()
        bucket = map._buckets[hash]
        node_len = 0

        # "put" in hash map
        if bucket.length() == 0:
            bucket.insert(da[index], 1)
            map._size+=1
        elif bucket.length() >=1:
            # this for loop will only ever execute >n times per outer loop
            for node in bucket:
                node_len +=1
                if node.key == da[index]:
                    node.value +=1
                    node_len = 0
                # reached end of ll, can add new node
                elif node.key != da[index] and bucket.length() == node_len:
                    node_len = 0
                    bucket.insert(da[index], 1)



    current_mode = 0
    # Go back through hash map to find mode
    for index in range(map._capacity):
        bucket = map._buckets[index]

        # this loop should only ever execute >n times
        for node in bucket:
            if node is not None and mode_da.length() == 0:      # first bucket only to initialize mode
                mode_da.append(node.key)
                current_mode = node.value
            elif node.value == current_mode:        # multiple modes
                mode_da.append(node.key)
            elif node.value > current_mode:         # new mode found
                mode_da = DynamicArray()
                mode_da.append(node.key)
                current_mode = node.value

    return mode_da, current_mode



# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print('\nPDF - put example 1')
    print('-------------------')
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print('\nPDF - put example 2')
    print('-------------------')
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print('\nPDF - resize example 1')
    print('----------------------')
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print('\nPDF - resize example 2')
    print('----------------------')
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print('\nPDF - table_load example 1')
    print('--------------------------')
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print('\nPDF - table_load example 2')
    print('--------------------------')
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print('\nPDF - empty_buckets example 1')
    print('-----------------------------')
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print('\nPDF - empty_buckets example 2')
    print('-----------------------------')
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print('\nPDF - get example 1')
    print('-------------------')
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print('\nPDF - get example 2')
    print('-------------------')
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print('\nPDF - contains_key example 1')
    print('----------------------------')
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print('\nPDF - contains_key example 2')
    print('----------------------------')
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print('\nPDF - remove example 1')
    print('----------------------')
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print('\nPDF - get_keys_and_values example 1')
    print('------------------------')
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print('\nPDF - clear example 1')
    print('---------------------')
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print('\nPDF - clear example 2')
    print('---------------------')
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print('\nPDF - find_mode example 1')
    print('-----------------------------')
    da = DynamicArray(['apple', 'apple', 'grape', 'melon', 'peach'])
    mode, frequency = find_mode(da)
    print(f'Input: {da}\nMode : {mode}, Frequency: {frequency}')

    print('\nPDF - find_mode example 2')
    print('-----------------------------')
    test_cases = (
        ['219', '219', '219', '326', '913', '651', '-319', '602', '292', '-13', '-13', '-13', '-290', '-292'],
        ['Arch', 'Manjaro', 'Manjaro', 'Mint', 'Mint', 'Mint', 'Ubuntu', 'Ubuntu', 'Ubuntu'],
        ['one', 'two', 'three', 'four', 'five'],
        ['2', '4', '2', '6', '8', '4', '1', '3', '4', '5', '7', '3', '3', '2']
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f'Input: {da}\nMode : {mode}, Frequency: {frequency}\n')
