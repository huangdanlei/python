import string
positive = open("positive.txt","r").read()
positive_d = positive.split("\n")

positive_dict = dict(s.split(",") for s in positive_d)
print positive_dict
negative = open("negative.txt","r").read()
negative_d = negative.split("\n")
negative_dict = dict(s.split(",") for s in negative_d)

text_e = open("example.txt","r").read()
text_l = text_e.split("\n")
i = 0
while i < len(text_l):
    text = str(text_l[i])
    def sentiment_score(positive_dict,negative_dict,text):
    	text = text.lower().translate(None, string.punctuation)
    	s = 0;
    	for word in text.split(" "):
    		if word in positive_dict.keys(): 
    			s = s + float(positive_dict[word])
    		if word in negative_dict.keys():
    			s = s + float(negative_dict[word])
    	if "very good" in text:
    			s = s + 2
    	if "not good" in text:
    			s = s - 1
    	return float(s) / len(text.split(" "))
    print sentiment_score(positive_dict,negative_dict,text)
    i += 1

    

