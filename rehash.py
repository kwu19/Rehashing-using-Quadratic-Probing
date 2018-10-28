#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 17:20:23 2018

@author: kefei
"""

class HashTable:
    def __init__(self, size):
        self.size = size
        self.slots = [None] * self.size
        self.data = [None] * self.size

    def put(self, key, data):
        stop = False
        
        if data is None:
            raise ValuError("None cannot be stored in this HashTable")
            
        hashvalue = self.hashfunction(key)
        print(hashvalue)
        oldhash = hashvalue
        i = 1
        
        if self.slots[hashvalue] == None:
            self.data[hashvalue] = data
            self.slots[hashvalue] = key
        else:
            if self.slots[hashvalue] == key:
                self.data[hashvalue] = data  # update/replace
            else:  # collision circumstance
                while not stop:
                    print("old hash is %d" %hashvalue)
                    oldhash = hashvalue + (i**2)
                    print(oldhash)
                    nextslot = self.rehash(oldhash)
                    if (self.slots[nextslot] == None):
                        self.slots[nextslot] = key  # updating or new data insertion
                        self.data[nextslot] = data
                        stop = True
                    else:
                        i += 1

                    # We only get here if the while loop ends, meaning we have space
                    # to add a value, or update an existing one
                    #self.slots[nextslot] = key  # updating or new data insertion
                    #self.data[nextslot] = data
  
    def get(self, key):
        startslot = self.hashfunction(key)
        data = None
        stop = False
        found = False
        position = startslot
        
        while (self.slots[position] != None and
               not found and
               not stop):
            
            if self.slots[position] == key:  # We've found it
                found = True
                data = self.data[position]
            else:
                position = self.rehash(position)
                if position == startslot:  # key is not in the dictionary/hashtable/map
                    stop = True
                    
        return data

    def hash(self, astring):
        _sum = 0
        for i, c in enumerate(astring, start=1):
            _sum = _sum + ord(c)*i    
        return _sum%self.size

    def hashfunction(self, key):
        if isinstance(key, int):
            h = self.hash(str(key))
        elif isinstance(key, str):
            h = self.hash(key)
        else:
            raise NotImplementedError("This data type isn't available for keys")

        return h  # Key must be an int
    
    def __getitem__(self, key):
        if not (isinstance(key, str) or isinstance(key, int)):
            raise TypeError("Key must be a string or int")
            
        val = self.get(key)
        
        if not val:  # it's None
            raise KeyError
        
        return val
        
    def __setitem__(self, key, value):
        if not (isinstance(key, str) or isinstance(key, int)):
            raise TypeError("Key must be a string or int")
            
        self.put(key, value)
        
    def __len__(self):
        counter = 0
        
        for key in self.slots:
            if key != None:
                counter += 1
                
        return counter
    
    def __contains__(self, key):
        return True if self.get(key) is not None else False
    
    def __str__(self):
        d_str = "{"
        for k, v in zip(self.slots, self.data):
            if k is not None:
                d_str += f"{repr(k)}:{repr(v)}, "
        d_str = d_str[:-2] + "}"
        return d_str
    
    def __repr__(self):
        return self.__str__()
    
    
    
    def rehash(self, oldhash):
        """Rehashing using quadratic probing
        
        Take parameter old hash and if collision happens return new hash"""
        #return (oldhash + 1) % self.size
        newhash = oldhash % self.size  # calculate new hash
        print("new hash is %d" %newhash)  
        print(self.slots[newhash])
                
        return newhash
   
# Test
h = HashTable(12)
h.put('apple', "MacBook Pro")
h.put('google', "Pixel")
h.put('microsoft', "Surface Book Pro")
h.slots

#As we can see here, when we want to put key "microsoft" and data "Surface Book Pro", 
#a collision occurs. At position 10, we've already have "apple" at that position. 
#So by rehashing we searched for a new position 11 and check if it is empty or not. 
#And we see None in that position, so we put "microsoft" in position 11.

h.put('dell', "lemon")
h.put('pencil', "cake")
h.put('act', "actor")
h.put('class', "professor")
h.put('baidu', "wifi")
h.slots

#Right now, we add a lot of keys into the hash. Now we can see, 
#for "baidu" we have the old position in 8, but by searching we found that
# we met a collision, since "google" is in position 8 right now. Then by rehashing, 
# we find new position 9, but still, there is "class" in position 9. 
#Again we find a new position 0, at last, there is no key in that position, 
# so we put "baidu" in that position.