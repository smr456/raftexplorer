from exploreRaft import exploreRaft
from get_EO_analysis_results import get_EO_analysis_results
from get_EO_analysis_files import get_EO_analysis_files
import os
import glob
from astropy.io import fits
import argparse

## Command line arguments
parser = argparse.ArgumentParser(
        description='Plot full focal plane EO test result to output file')

    ##   The following are 'convenience options' which could also be specified in the filter string
parser.add_argument('-r', '--run', default=None, help="(raft run number (default=%(default)s)")
args = parser.parse_args()
run=args.run
#run = 10517
g = get_EO_analysis_results()
raft_list, data = g.get_tests(run=run, site_type='Raft')
res = g.get_results(test_type="total_noise", data=data, device=raft_list)
print(raft_list)
#print(res)
nl = g.get_results(test_type="nonlinearity",data=data, device=raft_list)

eR = exploreRaft()
ccd_list = eR.raftContents(run=run, raftName=raft_list)
#print(ccd_list)

gf = get_EO_analysis_files()
files_list = gf.get_files(run=str(run), testName='qe_raft_analysis', FType="fits",
                            matchstr='QE')

#print(files_list)
import pickle
pfile=str('RaftRun'+run+'.p')
f=open(pfile,'wb')
pickle.dump(raft_list,f)
pickle.dump(res,f)
pickle.dump(ccd_list,f)
pickle.dump(files_list,f)
pickle.dump(nl,f)
f.close()
for key in files_list:
#    print(files_list[key],'\n \n')
    print('found'+ str(files_list[key][0])+' /u/ek/qefiles/ritz','\n')
    os.system('cp '+ str(files_list[key][0])+' /u/ek/ritz/qefiles/')    
    #hdulist=fits.open(files_list[key][0])
