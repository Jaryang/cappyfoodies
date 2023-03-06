import json
import string
import os
import re
import nltk
from nltk.corpus import stopwords
# Note: relevant modules from nltk need to be pre-installed by the code 
# as follows:
# ---------------------------------------------------------------------
# import nltk
# import ssl
# try:
    # _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
    # pass
# else:
    # ssl._create_default_https_context = _create_unverified_https_context

# nltk.download("stopwords")
# nltk.download("punkt")
# ---------------------------------------------------------------------


def read_review_json(address, hint = -1):
    """
    Convert json data into Python dict
    
    Inputs: 
        address(str): address of the file
        hint(int): specify how many bites would be read(-1 means "read all")
    Outputs: a dict of reviews of the restaurants
    """
    
    with open(address) as f:
        dta_json = f.readlines(hint)
    
    return json.loads(dta_json[0])


def gene_text_dict(res_info):
    """
    Generate a dict containing comments for each restaurant
    
    Inputs:
        res_info: a list of dictionaries containing user information
    Outputs:
        res_text_dict: a dict of user comment
    """
    
    res_text_dict = {}

    for idx, user in enumerate(res_info):
        user_comment = user["text"]
        name = "user{}".format(idx + 1)
        res_text_dict[name] = user_comment
    
    return res_text_dict


def tokenize(text):
    """
    Tokenize the text
    """
    
    tokens = nltk.word_tokenize(text)
    punctuations = string.punctuation
    stop_words = set(stopwords.words("english"))
    extra_stop_words = set(["'s", "...", "'ve", "n't", "'t", "'d","'ll",
                           "'re", "...."])
    stop_words.update(extra_stop_words)
    new_tokens = []
    
    for token in tokens:
        if (token not in punctuations) and (token.lower() not in stop_words)            and (re.match(r"\d+", token) == None):
                new_tokens.append(token.lower())
    
    return new_tokens


def review_cleaner(review_dta):
    """
    Clean the review data
    
    Inputs:
        review_dta: a dict of review of the restaurants
    Outputs:
        new_dta: cleaned new data
    """
    
    new_dta = dict()
    
    for restaurant, res_info in review_dta.items():
        # Add text into dict
        res_dict = dict()
        res_dict["information"] = gene_text_dict(res_info)
        
        # Tokenize the text 
        tokens_lst = []
        for user, text in res_dict["information"].items():
            tokens_lst.extend(tokenize(text))
        res_dict["tokens"] = tokens_lst
        
        new_dta[restaurant] = res_dict
        
    return new_dta


def export_to_json(review_dta, filename):
    """
    Export the cleaned review data as json format
    
    Input:
        review_dta: a dictionary containing the cleaned review data
        filename(str): filename of the output json file
    """
    address = 'yelp_dataset/cleaned_data'
    os.makedirs(address, exist_ok=True)
    file_path = address + "/" + filename
    
    with open(file_path, "w") as f:
        json.dump(review_dta, f)
        

if __name__ == "__main__":
    
    address = "yelp_dataset/uncleaned_yelp_reviews_new.json"
    review_dta = read_review_json(address)
    cleaned_new_dta = review_cleaner(review_dta)
    filename = "cleaned_review.json"
    export_to_json(cleaned_new_dta, filename)





