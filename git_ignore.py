import os
for root, dirs, files in os.walk(os.getcwd()):
 for file in files:
  name = str(root+'/'+file)
  if os.path.isfile(name):
   if os.stat(name).st_size > 30000000:
    f = open('/mnt/d/software/analysis_SOP/.gitignore','a')
    f.write(str(name.split('/mnt/d/software/analysis_SOP/')[1]+'\n'))
    f.close()
