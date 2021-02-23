from preprocess import *
import pickle

class node:
    def __init__(self,doc_id,freq=0):
        self.doc_id = doc_id
        self.freq = freq
        self.next = None

class linked_list:
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail
        self.len = 0

def display(list,file_info):
    temp = list.head
    print(list.len)
    while(temp is not None):
        print(temp.doc_id,temp.freq,file_info[temp.doc_id])
        temp = temp.next

def buildIndex(path,inverted_index):
    doc_id = 1
    for file in glob.glob(path): 
        fpath = file
        fname = file.split("\\")[1]        
        fname = fname.split(".")[0]                                           
        if os.path.isdir(file):                        
            if fname == "SRE":                
                for file1 in glob.glob(file+'/*'):                                                      
                    fname1 = file1.split("\\")[2]        
                    fname1 = fname1.split(".")[0]                    
                    if fname1 == "" or fname1=="index":
                        continue
                    else:
                        print(doc_id,fname1)                        
                        file = open(file1,"r",encoding='unicode_escape')        
                        doc = file.read() #reading contents of doc        
                        doc = delete_spec_chars(str(doc)) #deleting special characters
                        doc = re.sub(r'\d+','',doc) #deleting numbers
                        tokens = word_tokenize(doc) #extracting tokens
                        tokens_without_stopwords = [word.lower() for word in tokens if word not in stop_words and len(word) > 1] #Removing stopwords                                                           
                        tokens_final = lematize(tokens_without_stopwords)                        
                        uq_dict = find_unique(tokens_final)
                        for word in uq_dict.keys():
                            new_node = node(doc_id,uq_dict[word])
                            if inverted_index[word].head is None:
                                inverted_index[word].head = inverted_index[word].tail = new_node
                            else:
                                inverted_index[word].tail.next = new_node
                                tail = new_node
                            inverted_index[word].len = inverted_index[word].len + 1
                        doc_id += 1                        
            else:
                continue   
        else:                                          
            if fname == "index":
                continue
            print(doc_id,fname)
            file = open(file,"r",encoding='unicode_escape')        
            doc = file.read() #reading contents of doc        
            doc = delete_spec_chars(str(doc)) #deleting special characters
            doc = re.sub(r'\d+','',doc) #deleting numbers
            tokens = word_tokenize(doc) #extracting tokens
            tokens_without_stopwords = [word.lower() for word in tokens if word not in stop_words and len(word) > 1] #Removing stopwords                    
            tokens_final = lematize(tokens_without_stopwords)                        
            uq_dict = find_unique(tokens_final)
            for word in uq_dict.keys():
                new_node = node(doc_id,uq_dict[word])
                if inverted_index[word].head is None:
                    inverted_index[word].head = inverted_index[word].tail = new_node
                else:
                    inverted_index[word].tail.next = new_node
                    tail = new_node
                inverted_index[word].len = inverted_index[word].len + 1
            doc_id += 1
    return inverted_index

if __name__ == "__main__":
    # unique_words,unique_words_dict,file_info = process('stories/*') 
    # print(len(unique_words),len(unique_words_dict),len(file_info))
    # f = open('tokens.pkl','wb')
    # pickle.dump(unique_words,f)
    # f.close()
    # f1 = open('token_freq.pkl','wb')
    # pickle.dump(unique_words_dict,f1)
    # f1.close()   
    # f2 = open('file_info.pkl','wb')
    # pickle.dump(file_info,f2)
    # f2.close()       
    file1 = open('tokens.pkl','rb')
    tokens = pickle.load(file1)
    file2 = open('token_freq.pkl','rb')
    tokens_freq = pickle.load(file2)        
    file3 = open('file_info.pkl','rb')
    file_info = pickle.load(file3) 
    inverted_index = {}     
    for word in tokens:
        inverted_index[word] = linked_list()  
    inverted_index = buildIndex('stories/*',inverted_index)          
    for word in inverted_index.keys():
        print(word)
        display(inverted_index[word],file_info)
        break


