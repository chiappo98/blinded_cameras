import ROOT as r
import numpy as np
import sys

if __name__ == '__main__':
    
    file_path = sys.argv[1]
    simu_num = sys.argv[2]

    histFile = r.TFile.Open("sensors16.root", "READ")
    cam_list = histFile.GetListOfKeys()
    
    for cam in cam_list:
        if cam.GetName() != 'commit_hash':
            
            tree = histFile.Get(cam.GetName())
            
            for entry in tree:
                print(entry.innerPhotons)
                #append to numpy

    #save numpy