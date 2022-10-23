import os
import glob
import shutil
import zipfile
import tempfile


ensemble_results = []
for zip_file in glob.glob('/work/ws/nemo/fr_rk250-autopytorch_thesis-0/**/tmp.zip', recursive=True):
    zf = zipfile.ZipFile(zip_file)
    with tempfile.TemporaryDirectory() as tempdir:
        zf.extractall(tempdir)
        if os.path.exists(glob.glob(os.path.join(tempdir, "*.log")[0])):
            os.remove(os.path.join(tempdir, glob.glob(os.path.join(tempdir, "*.log")[0])))

        shutil.make_archive(os.path.join(os.path.dirname(zip_file), 'tmp_reduced'), 'zip', tempdir)
    os.remove(zip_file)
