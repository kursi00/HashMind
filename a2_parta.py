#    Main Author(s): Ahmed kursi
#    Main Reviewer(s): 

class HashTable:
    """
    A hash table that stores key-value pairs and resolves collisions using separate chaining.
    It supports insertion, modification, removal, search, and resizing of the table when the load factor exceeds a threshold
    """

    def __init__(self, cap=32):
        """
        Initializes the hash table with a given initial capacity.
        
        Args:
            cap (int): The initial number of slots in the table. Defaults to 32.
        
        This constructor sets up the internal table with a specified capacity and initializes the size to 0.
        """
        self._capacity = cap
        self.size = 0
        self.table = [None] * self._capacity

    def insert(self, key, value):
        """
        Inserts a new key-value pair into the table. If the key already exists, the pair is not added.
        
        Args:
            key (Any): The key to be inserted into the table.
            value (Any): The value associated with the key.
        
        Returns:
            bool: True if the key-value pair was successfully inserted, False if the key already exists.
        
        If the number of stored elements exceeds 70% of the table's capacity, the table will be resized.
        """
        index = hash(key) % self._capacity
        if self.table[index] is not None:
            for item in self.table[index]:
                if item[0] == key:
                    return False
            self.table[index].append((key, value))
        else:
            self.table[index] = [(key, value)]
        self.size += 1

        if self.size / self._capacity > 0.7:
            self._resize()
        return True

    def modify(self, key, value):
        """
        Modifies the value associated with an existing key in the table.
        
        Args:
            key (Any): The key whose value is to be modified.
            value (Any): The new value to associate with the key.
        
        Returns:
            bool: True if the key was found and modified, False if the key was not found.
        
        This function allows the modification of an existing key-value pair.
        """
        index = hash(key) % self._capacity
        if self.table[index] is not None:
            for i, item in enumerate(self.table[index]):
                if item[0] == key:
                    self.table[index][i] = (key, value)
                    return True
        return False

    def remove(self, key):
        """
        Removes a key-value pair from the table.
        
        Args:
            key (Any): The key to be removed.
        
        Returns:
            bool: True if the key-value pair was successfully removed, False if the key was not found.
        
        This function removes a key-value pair and adjusts the table accordingly.
        """
        index = hash(key) % self._capacity
        if self.table[index] is not None:
            for i, item in enumerate(self.table[index]):
                if item[0] == key:
                    self.table[index].pop(i)
                    if len(self.table[index]) == 0:
                        self.table[index] = None
                    self.size -= 1
                    return True
        return False

    def search(self, key):
        """
        Searches for a key in the table and returns its associated value.
        
        Args:
            key (Any): The key to search for.
        
        Returns:
            Any: The value associated with the key if found, None if the key is not found.
        
        This function allows retrieval of the value for a specific key in the table.
        """
        index = hash(key) % self._capacity
        if self.table[index] is not None:
            for item in self.table[index]:
                if item[0] == key:
                    return item[1]
        return None

    def capacity(self):
        """
        Returns the current capacity of the table (the number of available slots).
        
        Returns:
            int: The current capacity of the table.
        
        This function gives the number of available slots in the table, which is equal to the number of buckets in the hash table.
        """
        return self._capacity

    def __len__(self):
        """
        Returns the number of elements currently stored in the hash table.
        
        Returns:
            int: The current number of elements in the table.
        
        This function returns how many key-value pairs are stored in the hash table.
        """
        return self.size

    def _resize(self):
        """
        Resizes the table by doubling its capacity and rehashing all stored elements.
        
        This function is automatically called when the table's load factor exceeds 0.7.
        """
        old_table = self.table
        self._capacity *= 2
        self.table = [None] * self._capacity
        self.size = 0

        for chain in old_table:
            if chain is not None:
                for key, value in chain:
                    self.insert(key, value)


