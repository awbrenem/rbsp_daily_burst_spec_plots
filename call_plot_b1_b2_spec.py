#! /usr/bin/env python
#Call as: unix> python3 call_plot_b1_b2_spec.py


#####!/opt/local/bin/python2.7

#--Download B1/B2 cdf file
#--Split them up into manageable chunks using split_cdf.py
#--Read these in one at a time, plot their spectra, then delete that file
#   to save space


import os
import datetime
import subprocess
import re
from bs4 import BeautifulSoup
import requests
import sys
sys.path.append('/Users/aaronbreneman/Desktop/code/Aaron/github.umn.edu/online_file_query/')
from Find_available_files_online import Find_available_files_online
import numpy as np

 
sc = 'a'
type = 'mscb1'
bt = '1'
#d0 = datetime.datetime(2014, 5, 9)  #earlier date
#d1 = datetime.datetime(2014, 5, 20)  #more recent date
d0 = datetime.datetime(2012, 9, 5)  #earlier date
d1 = datetime.datetime(2012, 9, 6)  #more recent date

#remote path
url = 'http://themis.ssl.berkeley.edu/data/rbsp/rbsp'+sc+'/l1/'+type+'/'
#local path
lp = '/Users/aaronbreneman/Desktop/code/Aaron/github.umn.edu/rbsp_split_b1_cdf/'

delta = d1 - d0
ndays = delta.days
d0.strftime("%Y-%m-%d")

dtmp = d0

#type of online file
ext = 'cdf'


filesonline = Find_available_files_online()


mydir = os.getcwd() #Main folder for program
#folder with Josh's split_cdf.py program
newdir = "/Users/aaronbreneman/Desktop/code/Aaron/github.umn.edu/rbsp_split_b1_cdf/"


#Initial clean out of the files in the out folder.
#If we don't do this Josh's code split_cdf.py won't work.
os.chdir(newdir)
os.system("rm -f out/*.cdf")
os.chdir(mydir)



for day in range(ndays):

    print("********")
    print(dtmp)
    print("********")

    yr = dtmp.strftime("%Y")
    mn = dtmp.strftime("%m")
    dy = dtmp.strftime("%d")
    date = yr + '-' + mn + '-' + dy

    filesavail = filesonline.listFD(url+yr+'/', ext)

    #Find which online file corresponds to requested file.
    #Need to do this because file version is unknown.
    m = " "
    finalfile = list()
    version = list()
    #foundfile = list()
    for y in range(0, len(filesavail)):
        tst = re.search("rbsp[ab]{1}_l1_"+type+"_"+yr+mn+dy+"_v[0-9]{2}.cdf", filesavail[y])
        if tst:
            tmp = filesavail[y]
            finalfile.append(tmp)
            version.append(finalfile[y][-6:-4])



    #find the latest version of file if there is more than one
    index_max = np.argmax(version)
    finalfile = finalfile[index_max]


    #If there is an online file the proceed
    if finalfile:

        #extract filename from full path
        rf = finalfile[-31:]


        #download the file
        str1 = "wget "
        str2 = "-O " + lp + rf + " "
        str3 = url + yr + "/" + rf
        os.system(str1+str2+str3)


        #Run this from the split_cdf folder cd /Users/aaronbreneman/Desktop/code/Aaron/github.umn.edu/rbsp_split_b1_cdf/
        #file = "rbspa_l1_mscb1_20140509_v02.cdf"  ;Returned value
        os.chdir(newdir) # change the current working directory
        os.system("./split_cdf.py " + rf)

        exit_code = subprocess.call(['/Applications/exelis/idl84/bin/idl', '-e',
                                     'plot_b1_b2_spec', '-args',
                                     '%s' % sc, '%s' % type, '%s' % date])


        #Delete the files in the out folder or else Josh's code split_cdf.py won't work.
        os.system("rm -f out/*.cdf")
        os.chdir(mydir)


        dtmp += datetime.timedelta(days=1)
