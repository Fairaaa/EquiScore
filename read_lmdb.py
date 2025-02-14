import lmdb
import pickle

def read_lmdb(lmdb_path):
    env = lmdb.open(
        lmdb_path,
        subdir=False,
        readonly=True,
        lock=False,
        readahead=False,
        meminit=False,
        max_readers=256,
    )  
    data_l = {}
    out_list = []
    with env.begin() as txn:
        for key, value in txn.cursor():
            data = pickle.loads(value)
            out_list.append(data)
    env.close()
    return out_list

if __name__ == "__main__":
    lmdb_path = "/home/liyifei/workspace/EquiScore/pocket.lmdb"
    print(read_lmdb(lmdb_path))