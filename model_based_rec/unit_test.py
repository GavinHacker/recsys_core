import pickle as pkl
import subprocess
import tempfile
import os
import common.config as cfg
import common.common as common

v_from_pkl = None
with open('/Users/gavin/python_machinelearn/recsys/data/dict2vec', 'rb') as f:
  v_from_pkl = pkl.load(f)

predict_x = v_from_pkl.transform({'美国':1, '日本1':1})
print(predict_x[predict_x != 0])


def run(cmd):

    conn = common.get_connection()
    base_dir = cfg.get_config_property('dir_base_url', conn)
    temp_dir = base_dir + os.sep + 'tmp' + os.sep
    out_temp = tempfile.SpooledTemporaryFile(max_size=10 * 1000 * 1000)
    final_temp_dir = temp_dir + os.sep
    try:
        fileno = out_temp.fileno()
        p = subprocess.Popen(cmd, shell=False, cwd=final_temp_dir, stdout=fileno,
                             stderr=fileno, universal_newlines=True)
        p.wait()
        out_temp.seek(0)
        print(out_temp.read().decode('utf8', 'replace'))
    except Exception as e:
        raise RuntimeError('run error: %s' % str(e))
    finally:
        if out_temp:
            out_temp.close()


cmd = cfg.get_config_property('lib_fm_path', common.get_connection())
run(cmd)