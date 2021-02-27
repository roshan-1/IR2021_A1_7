from preprocess import *
from build_index import *
import pickle


def query_and(list1, list2):
    p1 = list1.head
    p2 = list2.head
    resultant = linked_list()
    count = 0
    while p1 is not None and p2 is not None:
        if p1.doc_id == p2.doc_id:
            count += 1
            resultant.append(p1.doc_id, p1.freq)
            p1 = p1.next
            p2 = p2.next
        
        elif p1.doc_id > p2.doc_id:
            count+= 1
            p2 = p2.next
        
        else:
            count+= 1
            p1 = p1.next
        
    return resultant, count



def query_or(list1, list2):
    p1 = list1.head
    p2 = list2.head
    resultant = linked_list()
    count = 0
    while p1 is not None and p2 is not None:
        if p1.doc_id == p2.doc_id:
            count += 1
            resultant.append(p1.doc_id, p1.freq)
            p1 = p1.next
            p2 = p2.next
        
        elif p1.doc_id > p2.doc_id:
            resultant.append(p2.doc_id, p2.freq)
            count+= 1
            p2 = p2.next
        
        else:
            resultant.append(p1.doc_id, p1.freq)
            count+= 1
            p1 = p1.next
        
    while p1 is not None:
        resultant.append(p1.doc_id, p1.freq)
        p1 = p1.next

    while p2 is not None:
        resultant.append(p2.doc_id, p2.freq)
        p2 = p2.next

    return resultant, count

def subtract(list1, list2):
    p1 = list1.head
    p2 = list2.head
    resultant = linked_list()
    count = 0
    while p1 is not None and p2 is not None:
        if p1.doc_id == p2.doc_id:
            count += 1
            p1 = p1.next
            p2 = p2.next
        
        elif p1.doc_id > p2.doc_id:
            new_node = node(p2.doc_id, p2.freq)
            if(resultant.head is None):
                resultant.head = resultant.tail = new_node
            else:
                resultant.tail.next = new_node
                tail = new_node
            count+= 1
            p2 = p2.next
        
        elif p2.doc_id > p1.doc_id:
            resultant.append(p1.doc_id, p1.freq)
            count+= 1
            p1 = p1.next

    while p1 is not None:
        resultant.append(p1.doc_id, p1.freq)
        count+= 1
        p1 = p1.next
    
    return resultant, count
        

def query_andnot(list1,list2):
    list3, count1 = query_and(list1, list2)
    resultant, count2 = subtract(list1, list3)
    return resultant, count1+count2


def query_ornot(list1, list2):
    list3, count1 = query_andnot(list2, list1)
    resultant, count2 = subtract(universal_list, list3)
    return resultant, count1+count2


if __name__ == "__main__":
    file1 = open('tokens.pkl','rb')
    tokens = pickle.load(file1)
    file2 = open('token_freq.pkl','rb')
    tokens_freq = pickle.load(file2)        
    file3 = open('file_info.pkl','rb')
    file_info = pickle.load(file3)     
    universal_list = linked_list()    
    inverted_index = {}     
    for word in tokens:
        inverted_index[word] = linked_list() 
    inverted_index, universal_list = buildIndex('stories/*',inverted_index,universal_list)
    query = input('Enter the Query')
    processed_query = process_query(query)
    print(type(processed_query))
    process_word = processed_query.split()
    query_op = input('Enter the Operations')
    query_op = query_op.replace('[','')
    query_op = query_op.replace(']','')
    query_op = query_op.split(',')
    print(query_op)
    print(type(query_op[0]))
    total = []
    i=0
    for word in process_word:
        if word in tokens:
            total.append(inverted_index[word])
        print(type(total[i]))

    final_count = 0
    for i in range(len(process_word)-1):
        word1 = total[0]
        print(type(word1))
        word2 = total[1]
        print(query_op[i])
        print(type(query_op[i]))
        if query_op[i] == 'OR':
            word3,count1 = query_or(word1,word2)
        elif query_op[i] == 'AND':
            word3,count1 = query_and(word1,word2)
        elif query_op[i] == 'OR NOT':
            word3,count1 = query_ornot(word1,word2)
        elif query_op[i] == 'AND NOT':
            word3,count1 = query_andnot(word1,word2)
        final_count += count1
        total.remove(word1)
        total.remove(word2)
        total.insert(0,word3)
    print(total[0].len)
    print(final_count)