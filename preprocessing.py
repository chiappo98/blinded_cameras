import sys
import numpy as np
from matplotlib import pyplot as plt 
from matplotlib.backends.backend_pdf import PdfPages

if __name__ == '__main__':
    
  sim_num = 0
  data_path = '/storage/gpfs_data/neutrino/SAND-LAr/SAND-LAr-OPTICALSIM-PROD/GRAIN/blindcam/data'
  
  with open(data_path+'/simulation.npy', 'rb') as f:    #'+str(sim_num)+'
    data_in = np.load(f)
  with open(data_path+'/inner_ph.npy', 'rb') as g:      #'+str(sim_num)+'
    inner_ph_in = np.load(g)
  
  ###### parameters #################
  drdf_threshold = 10
  root_threshold = 10
  evn_element = 50
  cam_element = 0
  ###################################
  
  ###### fixed parameters ###########
  n_cam_in_grain = 54
  cam_side_length = 31
  ###################################
  
  
  
  ##### process data from response.drdf #####
  
  print('\n' + '############## process data from response.drdf ##############')
  
  data = data_in.reshape(-1, n_cam_in_grain, cam_side_length**2)    #data_in.reshape(-1, 76, 1024)
  print('data shape :',data.shape, '=', data_in.shape)
  # fill a list of list : for each event, blinded cameras are stored
  overthr_evn = np.unique( np.where( data > drdf_threshold )[0] )
  overthr_data = np.empty((2,1))
  for evn in overthr_evn:
    tmp = np.array([ [evn], [np.unique( np.where( data[evn] > drdf_threshold )[0] )] ], dtype=object)
    overthr_data = np.hstack((overthr_data, tmp))
  overthr_data = overthr_data[:2,1:]
  evn_num = overthr_data[0][evn_element]
  cam_num = overthr_data[1][evn_element][cam_element]
  print('over threshold data :', overthr_data.shape[1])
  
  print('\n')
  
  
  ##### process data from root file #####
  
  print('\n' + '################ process data from root file ################') 
  
  inner_ph = inner_ph_in.reshape(n_cam_in_grain, -1)    #inner_ph_in.reshape(76,-1)  
  print('inner photons shape :',inner_ph.shape)
  
  overthr_inner_evn = np.unique( np.where( inner_ph > root_threshold )[1] )
  overthr_cam = np.empty((2,1))
  for inn_evn in overthr_inner_evn:
    tmp = np.array([ [inn_evn], [np.unique( np.where( inner_ph.T[inn_evn] > root_threshold ) )] ], dtype=object)
    overthr_cam = np.hstack((overthr_cam, tmp))
  overthr_cam = overthr_cam[:2,1:]
  print('over threshold cam :', overthr_cam.shape[1])
  
  print('\n')
  
  ##### plot cameras with inner photons over threshold #####
  
  write_pdf = False
  if write_pdf :
    pdf = PdfPages('./blinded.pdf')
    for evn in overthr_inner_evn:
      idx = np.where(overthr_cam[0] == evn)
      for cam in overthr_cam[1][idx][0]:
        fig = plt.figure()
        matrix = plt.pcolormesh(data[evn][cam].reshape(cam_side_length,cam_side_length))
        plt.colorbar(matrix)
        #plt.title('cam-'+str(num))
        pdf.savefig(fig)
        plt.close()
    pdf.close()
  
  
  ##### to delete in the future #####
  
  plot = False
  if plot:
    #data_num = np.where(data == np.max(data[evn_num][cam_num]))[0][0]
    fig, ax = plt.subplots(1,2)
    ax[0].hist(data[evn_num][cam_num],100)
    ax[0].set_yscale('log')
    
    cam = ax[1].pcolormesh(data[evn_num][cam_num].reshape(cam_side_length,cam_side_length))
    plt.colorbar(cam)
    
    fig.set_figwidth(15)
    plt.savefig('./test.png')#data_path+'/test.png')
