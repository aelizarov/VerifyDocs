#!/usr/bin/env python
# coding: utf-8

# In[4]:


from verifydocs import *
from flask import Flask,jsonify,request


# In[13]:


app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def hello_world():
    url = request.args.get('url')
    npi = request.args.get('npi')
    dob = request.args.get('dob')
    mode = request.args.get('mode')
    if mode:
    	url_mode = bool(int(mode))
    else:
    	url_mode = True
    validity = validate(url,npi,dob,url_mode)
    return jsonify(validity)


# In[14]:


if __name__ == '__main__':
    app.run()


# In[ ]:




