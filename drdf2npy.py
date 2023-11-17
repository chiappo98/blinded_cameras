#
# Copyright 2020-2022 N. Tosi, V. Pia <nicolo.tosi@bo.infn.it>
#
# This program is free software:
# you can redistribute it and/or modify it under the terms of the GNU
# Lesser General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#

import drdf
import uuid
import numpy as np
import sys

if __name__ == '__main__':
  
  file_path = sys.argv[1]
  simu_num = sys.argv[2]
  
  testfile = drdf.DRDF()
  testfile.read(file_path)
  
  data_from_cameras = np.empty(0)
  for run, rundata in testfile.runs.items():
    #print('Run', run, 'with', len(rundata), 'events')
    #print(' with geometry', rundata.georef)
    for event, eventdata in rundata.items():
      #print('Event', event, 'with', len(eventdata), 'images')
      for src, image in eventdata.items():
        #print('Image from source', src, 'with size', image.pixels[:,:,0])
        data_from_cameras = np.append(data_from_cameras, image.pixels[:,:,1])

  # data_from_cameras.reshape(-1, 76, 1024)
  
  print(data_from_cameras.shape)
  np.save('blind_cameras_dataset/simulation_'+str(simu_num)+'.npy', data_from_cameras)
