#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import re
import unicodedata
import nltk
from nltk.corpus import stopwords
ADDITIONAL_STOPWORDS = ['sc','www','ieee','aaai','conference','workshop','demonstration','demonstrations','acl','emnlp','cvpr','conference','nips','acm','ieee','kdd','1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']
science_stopwords = ['paper','papers','author','propose','result','results','show','experiments','present','novel','approach','include','included','proceeding','proceedings','contained','contains','high level','rights','right','reserved','ieee',
                    'method','datset','corpus','copyright','sae','time','average','experimental','experiments','experiment','copyright','sae','datasets','performance','training','test','state','art','_','machine learning','deep learning','abstract','authors','topics','discussed','given','discussed','discuss','proof']
import matplotlib.pyplot as plt


# In[5]:


from sklearn.feature_extraction.text import TfidfTransformer 
from sklearn.feature_extraction.text import CountVectorizer
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text


# In[6]:


other_stopwords = ["a","a's","able","about","above","according","accordingly","across","actually","after","afterwards","again","against","ain't","all","allow","allows","almost","alone","along","already","also","although","always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","aren't","around","as","aside","ask","asking","associated","at","available","away","awfully","b","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","c","c'mon","c's","came","can","can't","cannot","cant","cause","causes","certain","certainly","changes","clearly","co","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldn't","course","currently","d","definitely","described","despite","did","didn't","different","do","does","doesn't","doing","don't","done","down","downwards","during","e","each","edu","eg","eight","either","else","elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","f","far","few","fifth","first","five","followed","following","follows","for","former","formerly","forth","four","from","further","furthermore","g","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","h","had","hadn't","happens","hardly","has","hasn't","have","haven't","having","he","he's","hello","help","hence","her","here","here's","hereafter","hereby","herein","hereupon","hers","herself","hi","him","himself","his","hither","hopefully","how","howbeit","however","i","i'd","i'll","i'm","i've","ie","if","ignored","immediate","in","inasmuch","inc","indeed","indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isn't","it","it'd","it'll","it's","its","itself","j","just","k","keep","keeps","kept","know","known","knows","l","last","lately","later","latter","latterly","least","less","lest","let","let's","like","liked","likely","little","look","looking","looks","ltd","m","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more","moreover","most","mostly","much","must","my","myself","n","name","namely","nd","near","nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine","no","nobody","non","none","noone","nor","normally","not","nothing","novel","now","nowhere","o","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","own","p","particular","particularly","per","perhaps","placed","please","plus","possible","presumably","probably","provides","q","que","quite","qv","r","rather","rd","re","really","reasonably","regarding","regardless","regards","relatively","respectively","right","s","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","she","should","shouldn't","since","six","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","t","t's","take","taken","tell","tends","th","than","thank","thanks","thanx","that","that's","thats","the","their","theirs","them","themselves","then","thence","there","there's","thereafter","thereby","therefore","therein","theres","thereupon","these","they","they'd","they'll","they're","they've","think","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","together","too","took","toward","towards","tried","tries","truly","try","trying","twice","two","u","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","uucp","v","value","various","very","via","viz","vs","w","want","wants","was","wasn't","way","we","we'd","we'll","we're","we've","welcome","well","went","were","weren't","what","what's","whatever","when","whence","whenever","where","where's","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","while","whither","who","who's","whoever","whole","whom","whose","why","will","willing","wish","with","within","without","won't","wonder","would","would","wouldn't","x","y","yes","yet","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","z","zero"]
science_stopwords = ADDITIONAL_STOPWORDS+science_stopwords+other_stopwords


# In[7]:


my_stop_words = text.ENGLISH_STOP_WORDS.union(science_stopwords)


# ## User defined functions

# In[8]:


def basic_clean(text):
    """
      A simple function to clean up the data. All the words that
      are not designated as a stop word is then lemmatized after
      encoding and basic regex parsing are performed.
    """
    wnl = nltk.stem.WordNetLemmatizer()
    porter_stemmer=PorterStemmer()
    stopwords =list(my_stop_words)
#     print(stopwords)
    text = (unicodedata.normalize('NFKD', text)
    .encode('ascii', 'ignore')
    .decode('utf-8', 'ignore')
    .lower())
     # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)
    words = re.sub(r'[^\w\s]', '', text).split()
    final_words = [wnl.lemmatize(word) for word in words if word not in stopwords]
#     final_words=[porter_stemmer.stem(word=word) for word in final_words]
    text =' '.join(final_words)
    return text


# In[9]:


def my_tokenizer(text):
    # create a space between special characters 
    print("tokenize",text)
    text=re.sub("(\\W)"," \\1 ",text)

    # split based on whitespace
    return re.split("\\s+",text)


# In[10]:


from nltk.stem import PorterStemmer

# init stemmer
porter_stemmer=PorterStemmer()

def my_cool_preprocessor(text):
    
    text=text.lower() 
    text=re.sub("\\W"," ",text) # remove special chars
#     text=re.sub("\\s+(in|the|all|for|and|on)\\s+"," _connector_ ",text) # normalize certain words
    
    # stem words
    words=re.split("\\s+",text)
    stemmed_words=[porter_stemmer.stem(word=word) for word in words]
    return ' '.join(stemmed_words)


# In[11]:


def reg_clean_nos(essay):
    nonPunctEssay = re.sub("[^a-zA-Z\\s+,.]", " ", essay)
    nonPunctEssay = re.sub("[^a-zA-Z]", " ", nonPunctEssay)
    return nonPunctEssay
def reg_remove_puntuation(each_essay):
    each_essay = unicodedata.normalize('NFKD', each_essay).encode('ascii','ignore')
    each_essay = each_essay.decode('utf-8')
    each_essay= each_essay.replace("’", "'")
    each_essay= each_essay.replace("…", " ")
    each_essay= each_essay.replace(".", " ")
    
    each_essay = re.sub('\[*?\]\"\'', '', each_essay)
    each_essay = re.sub("[,?\[\]\{\}\(\):;<>\\\/\-_]", " ", each_essay)
    nonPunctEssay = re.sub("[,?\[\]\{\}\(\)\":;<>]", " ", each_essay)
    each_essay=each_essay.replace("@", " at ")
    each_essay=each_essay.replace("#", " hash ")
    each_essay=each_essay.replace("$", " dollar ")
    each_essay=each_essay.replace("%", " percent ")
    each_essay=each_essay.replace("'l ", "l ")
    nonPunctEssay = re.sub("[,?\[\]\{\}\(\)\"\':;<>\\\/\-_]", "", each_essay)
    
    return nonPunctEssay


# ## Data Import

# In[12]:


cols =['Authors','Title','Source_Title','Year','Link','Cited','Abstract','AuthorKey','Eng_Controlled','Eng_Unctrolled','Eng_MainHeading','Scival_topic','Scival_Score']


# In[13]:


cvpr = pd.read_csv('../Data/Paper_Details/PaperDetails_Gr2021_CVPR.csv',header=None)
nips =pd.read_csv('../Data/Paper_Details/PaperDetails_Gr2021_NIPS.csv',header=None)
kdd =pd.read_csv('../Data/Paper_Details/PaperDetails_Gr2021_KDD.csv',header=None)
acm =pd.read_csv('../Data/Paper_Details/PaperDetails_Gr2021_ACM.csv',header=None)
ieee =pd.read_csv('../Data/Paper_Details/PaperDetails_Gr2021_IEEE.csv',header=None)
ind =pd.read_csv('../Data/Paper_Details/PaperDetails_Gr2021_IND.csv',header=None)
nlp1 =pd.read_csv('../Data/Paper_Details/PaperDetails_Gr2021_NLP1.csv',header=None)
nlp2 =pd.read_csv('../Data/Paper_Details/PaperDetails_Gr2021_NLP2.csv',header=None)
nlp3 =pd.read_csv('../Data/Paper_Details/PaperDetails_Gr2021_NLP3.csv',header=None)
cs7 = pd.read_csv('../Data/Paper_Details/PaperDetails_Gr2021_CS_1to7.csv',header=None)

# In[14]:


cvpr.columns =cols
nips.columns =cols
kdd.columns =cols
acm.columns =cols
ieee.columns =cols
ind.columns =cols
nlp1.columns =cols
nlp2.columns =cols
nlp3.columns =cols
cs7.columns = cols


# In[15]:


final_df = pd.DataFrame()
for df in [cvpr,nips,kdd,acm,ieee,ind,nlp1,nlp2,nlp3,cs7]:
    final_df = final_df.append(df)
final_df.reset_index(drop=True,inplace=True)
final_df.fillna('', inplace=True)


# In[32]:


start_year = 2018
end_year = 2021


# In[17]:


conf_include = pd.read_csv('../Data/Paper_Details/Results/conf_title_count.csv')
accept = list(set(conf_include[conf_include['Accept']=='Y']['Source_Title']))

accept2 =list(set(cs7['Source_Title']))

accept3 = accept + accept2

# In[18]:


final_df = final_df[final_df['Source_Title'].isin(accept3)]
final_df.reset_index(drop=True,inplace=True)
final_df.shape



working_cols = ['Abstract','AuthorKey','Eng_Controlled','Eng_Unctrolled','Eng_MainHeading','Scival_topic']


# In[22]:


text_filter = {"Title":{'cols':['Title'],'name':'title'},
               "Abstract":{'cols':['Abstract'],'name':'abstract'},
                "Title + Abstract (TA)":{'cols':['Title','Abstract'],'name':'ta'},
                "TA + Author Keywords (TAA)":{'cols':['Title','Abstract','AuthorKey'],'name':'taa'},
                "TAA + Scopus Keywords":{'cols':['Title','Abstract','AuthorKey','Eng_Controlled','Eng_Unctrolled','Eng_MainHeading'],'name':'taask'},
                "Author Keywords+Scopus Keywords":{'cols':['AuthorKey','Eng_Controlled','Eng_Unctrolled','Eng_MainHeading'],'name':'aksk'}}


# In[68]:


for key,value in text_filter.items():
    print(value)


# ##  COunt Vectorizer

# In[33]:



bigram_num = 50
year_gaps = [1]
ngrams = {'uni':(1,1),'bigram':(2,2),'trigram':(3,3)}

for year_gap in year_gaps:
    names = []
    year =start_year
    while( year<end_year):
        first = year
        last = year+year_gap
        if last>=end_year:
            last = end_year
        str_ = str(first)+'-'+str(last)
        names.append(str_)
        year = last
    print("year range",names)
    for txt,ngramR in ngrams.items():
        
        print(year_gap,ngramR)
       
        
       
        for key,value in text_filter.items():
            working_cls = value['cols']
            text_type = value['name']
            print(working_cls,text_type)
            year = start_year
            df_list = []
            print("length of df",len(df_list))
            for yr_str in names:
                first,last = yr_str.split('-')
                working_df = final_df[(final_df['Year']>=int(first))&(final_df['Year']<int(last))]
                working_df['text'] =''

                for col in working_cls:
                    working_df['text'] = working_df['text'] +" "+ working_df[col]
                working_df['text'] = working_df['text'].apply(lambda x:reg_remove_puntuation(x))
                working_df['text'] = working_df['text'].apply(lambda x:basic_clean(x))
                docs=working_df['text'].tolist()
                docs = [i for i in docs if i!=' ']
                cv = CountVectorizer(ngram_range=ngramR,stop_words=list(my_stop_words),max_features=2000)#,tokenizer=my_tokenizer,preprocessor=basic_clean)
                count_vector=cv.fit_transform(docs)
            #     word_set = basic_clean(''.join(str(working_df['text'].tolist())))
            #     print('initial_wordset',word_set[:20])
                feature_array = np.array(cv.get_feature_names())
                cv_sorting = np.argsort(count_vector.toarray()).flatten()[::-1]
                print(first,last)
                n = bigram_num
                top_n = feature_array[cv_sorting][:n]
        #             print(top_n)
                x = {k: v for k, v in cv.vocabulary_.items() if k in top_n}
                xdf =pd.DataFrame(x.items())
                xdf.sort_values(by=[1],ascending=False)
                df_list.append(xdf)
                year = last
            writer=pd.ExcelWriter(r"../Data/Paper_Details/Results/"+txt+"_"+text_type+"_CountVec_gap_"+str(year_gap)+".xlsx")
            _ = [A.to_excel(writer,sheet_name="{0}".format(names[i])) for i, A in enumerate(df_list)]
            print("file_write completed...")
            writer.save()
 
