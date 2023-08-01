import ROOT as r
import numpy as np
import sys

if __name__ == '__main__':
    
    file_path = sys.argv[1]
    simu_num = sys.argv[2]

    histFile = r.TFile.Open(file_path, "READ") #"sensors16.root"
    cam_list = histFile.GetListOfKeys()
    inner_ph = np.empty(0)
    
    for cam in cam_list:
        inner_ph_tmp = np.empty(0)
        if cam.GetName() != 'commit_hash':
            
            tree = histFile.Get(cam.GetName())
            print(tree)
            for entry in tree:
                #print(entry.innerPhotons)
                inner_ph_tmp = np.append(inner_ph_tmp, entry.innerPhotons)

        inner_ph = np.append(inner_ph, inner_ph_tmp)
    #np.save('/storage/gpfs_data/neutrino/SAND-LAr/SAND-LAr-OPTICALSIM-PROD/GRAIN/blindcam/inner_ph'+str(simu_num)+'.npy', inner_ph)
    #np.save('/inner_ph'+str(simu_num)+'.npy', inner_ph)
    