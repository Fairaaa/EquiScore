import pickle
from collections import OrderedDict
import random
import glob
import numpy as np
import os
random.seed(0)
from collections import defaultdict,Counter

'''
only add pose < 2A  , which pdb id in training 
add challenge decoys to active samples
'''

def filter_targets(file_paths,targets):
    filtered_keys = []
    for name in file_paths:
        if name.split('/')[-1].split('_')[0] in targets:
            filtered_keys.append(name)
    return filtered_keys
def get_part_data(data_dir,names,fast_num = 5,active_names = None):
    # data_name = []
    pro_decoy_pro = defaultdict(list)
    for i in names:
        pro = i.split('_')[0]
        if active_names is None:
            pro_decoy_pro[pro].append(i)
        else:
            if pro in active_names:
                pro_decoy_pro[pro].append(i)

    pro_decoy_pro_5 = defaultdict(list)
    for key in pro_decoy_pro.keys():
        if len(pro_decoy_pro[key]) <= fast_num:
            # print(key)

            pro_decoy_pro_5[key] = pro_decoy_pro[key]
        else:
            pro_decoy_pro_5[key] =pro_decoy_pro[key][:fast_num]
    pro_decoy_pro_5 = sum(pro_decoy_pro_5.values(),[])
    print('mean of actives : decoys in cross_decoys',np.mean(list(dict(Counter([i.split('_')[2] for i in pro_decoy_pro_5])).values())))
    return [data_dir + name for name in pro_decoy_pro_5]
def get_part_data_screen_pose(data_dir,names,fast_num = 5,active_names = None):
    # data_name = []
    pro_decoy_pro = defaultdict(list)
    for i in names:
        pro = i.split('_active')[0]
        if active_names is None:
            pro_decoy_pro[pro].append(i)
        else:
            # flag = pro.split('_')[0] + '_' + pro.split('_')[1]
            if pro in active_names:
                pro_decoy_pro[pro].append(i)

    pro_decoy_pro_5 = defaultdict(list)
    # print(' pro_decoy_pro_5',len( pro_decoy_pro_5))
    for key in pro_decoy_pro.keys():
        if len(pro_decoy_pro[key]) <= fast_num:
            # print(key)

            pro_decoy_pro_5[key] = pro_decoy_pro[key]
        else:
            pro_decoy_pro_5[key] =pro_decoy_pro[key][:fast_num]
    pro_decoy_pro_5 = sum(pro_decoy_pro_5.values(),[])
    print('mean of actives : decoys in cross_decoys',np.mean(list(dict(Counter([i.split('_')[2] for i in pro_decoy_pro_5])).values())))
    # print('all decoy ',len(pro_decoy_pro_5)/len(active_names))
    return [data_dir + name for name in pro_decoy_pro_5]
def get_part_data_screen(data_dir,names,fast_num = 5,active_names = None):
    # data_name = []
    pro_decoy_pro = defaultdict(list)
    for i in names:
        pro = i.split('-')[0]
        if active_names is None:
            pro_decoy_pro[pro].append(i)
        else:
            if pro in active_names:
                pro_decoy_pro[pro].append(i)

    pro_decoy_pro_5 = defaultdict(list)
    # print(' pro_decoy_pro_5',len( pro_decoy_pro_5))
    for key in pro_decoy_pro.keys():
        if len(pro_decoy_pro[key]) <= fast_num:
            # print(key)

            pro_decoy_pro_5[key] = pro_decoy_pro[key]
        else:
            pro_decoy_pro_5[key] =pro_decoy_pro[key][:fast_num]
    pro_decoy_pro_5 = sum(pro_decoy_pro_5.values(),[])
    print('mean of actives : decoys in cross_decoys',np.mean(list(dict(Counter([i.split('_')[2].split('-')[1] for i in pro_decoy_pro_5])).values())))
    # print('all decoy ',len(pro_decoy_pro_5)/len(active_names))
    return [data_dir + name for name in pro_decoy_pro_5]
#------------------------------------------------------
# 先获取了pdbbind 的数据

# valid_keys = glob.glob('/home/caoduanhua/score_function/data/pdb_screen/active_pocket/*')
valid_keys =glob.glob('/home/caoduanhua/score_function/data/D-PDBbind_PDBscreen/PDB_bind_active_pocket/*')
# valid_keys +=glob.glob('/home/caoduanhua/score_function/data/general_refineset/generalset_active_pocket_without_h/*')
active_pros = set([v.split('/')[-1].split('_')[0] for v in valid_keys])

print('pdb actives pros :',len(active_pros))
cross_decoys= os.listdir('/home/caoduanhua/score_function/data/D-PDBbind_PDBscreen/PDB_bind_cross_decoy_pocket/')

cross_decoys_pros = set([v.split('/')[-1].split('_')[0] for v in cross_decoys])
print('cross_decoys_pros :',len(cross_decoys_pros))
cross_decoys_dir = '/home/caoduanhua/score_function/data/D-PDBbind_PDBscreen/PDB_bind_cross_decoy_pocket/'

valid_keys += get_part_data(cross_decoys_dir,cross_decoys,fast_num=10,active_names = active_pros)

print(' pdbbind len of decoys: ',len(cross_decoys))
#----------------------------------------------------------------
############# add pose enhanced samples ###############

cross_decoys_dir_pose = '/home/caoduanhua/score_function/data/general_refineset/pdbbind-data_arguement_active_2a_3_pocket-4/'
poses = os.listdir('/home/caoduanhua/score_function/data/general_refineset/pdbbind-data_arguement_active_2a_3_pocket-4/')
valid_keys_poses = get_part_data(cross_decoys_dir_pose,poses,fast_num=100,active_names = active_pros)
print('pose enhanced samples: ',len(valid_keys_poses))
print('screen pose pros: ',len(set([i.split('/')[-1].split('_')[0] for i in valid_keys_poses])))
valid_keys += valid_keys_poses
print('all valid keys in pdbbind ',len(valid_keys))

############################## add challenge decoys ##############################

# valid_keys_decoys = glob.glob('/home/caoduanhua/score_function/data/general_refineset/pdbbind-shape_decoy_align_pocket-5/*')
# print('all challedge decoys : ',len(valid_keys_decoys))
# valid_keys_decoys  = [i for i in valid_keys_decoys if i.split('/')[-1].split('_')[0] in active_pros]
# print('last challedge decoys : ',len(valid_keys_decoys))
# valid_keys += valid_keys_decoys
print(' pdbbind len of shape decoys + active + crossdecoy  + pose enhanced : ',len(valid_keys))

######################################################################################
# 先获取了pdbbind 的数据


###########################################################################################################################
import pickle
with open('/home/caoduanhua/score_function/data/pdb_screen/score_bins_name_file/pdbscreen_active_5_2.pkl','rb') as f:
    data_names = pickle.load(f)
data_names = [i.split('.')[0].replace('_active','') for i in data_names]

valid_keys_screen = glob.glob('/home/caoduanhua/score_function/data/D-PDBbind_PDBscreen/PDB_screen_active_-5_pocket/*')
# 过滤

valid_keys_screen = [ i for i in valid_keys_screen if i.split('/')[-1].replace('_active_0','') in data_names]
active_pros_screen = set([v.split('/')[-1].replace('_active_0','') for v in valid_keys_screen])

print('pdb screen actives pros :',len(active_pros_screen))
cross_decoys_screen= os.listdir('/home/caoduanhua/score_function/data/D-PDBbind_PDBscreen/PDB_screen_cross_decoy_pocket/')

cross_decoys_pros_screen = set([v.split('-')[0] for v in cross_decoys_screen])

print('cross_decoys_pros :',len(cross_decoys_pros_screen))
cross_decoys_dir_screen = '/home/caoduanhua/score_function/data/D-PDBbind_PDBscreen/PDB_screen_cross_decoy_pocket/'

valid_keys_screen += get_part_data_screen(cross_decoys_dir_screen,cross_decoys_screen,fast_num=10,active_names = active_pros_screen)

print(' pdd screen len of decoys: ',len(cross_decoys_screen))
#-------------------------------------------------------------------------------
cross_decoys_dir_screen_pose = '/home/caoduanhua/score_function/data/pdb_screen/pdb_sceen_active_2a_4_pocket/'
screen_poses = os.listdir('/home/caoduanhua/score_function/data/pdb_screen/pdb_sceen_active_2a_4_pocket/')
active_pros_screen = [i.split('_')[0] + '_' +  i.split('_')[2] for i in active_pros_screen]
valid_screen_poses = get_part_data_screen_pose(cross_decoys_dir_screen_pose,screen_poses,fast_num=100,active_names =active_pros_screen)

print('pose enhanced screen samples: ',len(valid_screen_poses))
print('screen pose pros: ',len(set([i.split('/')[-1].split('_')[0] for i in valid_screen_poses])))
valid_keys_screen += valid_screen_poses
print('all valid keys in pdbbind ',len(valid_keys_screen))

# ########################################################### challenge decoys ##################
# valid_keys_screen_shape = glob.glob('/home/caoduanhua/score_function/data/pdb_screen/screen_shape_pocket/*')
# print(' all pdb screen len of shape decoys : ',len(valid_keys_screen_shape))
# # remove sp score > -5
# data_names = [i.split('_')[0] + '_' +  i.split('_')[2] for i in data_names]
# valid_keys_screen_shape = [i for i in valid_keys_screen_shape if i.split('/')[-1].split('_align')[0] in data_names]
# print(' pdb screen len of shape decoys  remove sp score>-5: ',len(valid_keys_screen_shape))
# valid_keys_screen_shape = [i for i in valid_keys_screen_shape if i.split('/')[-1].split('_align')[0] in active_pros_screen]

# print(' last pdb screen len of shape decoys : ',len(valid_keys_screen_shape))
# valid_keys_screen += valid_keys_screen_shape
print(' pdb screen len of shape decoys + active + crossdecoy + pose enhanced: ',len(valid_keys_screen))

print('removeing duplicated target from training data ..........')
#------------------------------------------------------
valid_keys = valid_keys_screen + valid_keys
print('valid_keys_screen + valid_keys',len(valid_keys))


with open('/home/caoduanhua/score_function/data/uniport_analysis/duplicated_with_independent_pdb_ids_from_uniport_id/all_dulicatedpdb_ids.pkl','rb') as f:
    duplicated_targets = pickle.load(f)
    print('duplicated tragets: ',len(duplicated_targets))
dude_gene =  set(OrderedDict.fromkeys([v.split('/')[-1].split('_')[0] for v in valid_keys]))
print('len of the before remove duplicated target: ',len(dude_gene))
dude_gene = dude_gene - duplicated_targets
print('len of the after remove duplicated target: ',len(dude_gene))
print('remove done!')
#-----------------------------------------------------------------------

train_keys = [k for k in valid_keys if k.split('/')[-1].split('_')[0] in dude_gene]    
test_keys = [k for k in valid_keys if k.split('/')[-1].split('_')[0] in duplicated_targets]   
print ('Num train keys: ', len(train_keys))
print ('Num test keys: ', len(test_keys))

################## uniport hierarchy sample pipeline test ##############################
# 直接得到对应的pdb id

with open('/home/caoduanhua/score_function/data/uniport_analysis/hierarchy_uniport_sets_list/eight_class_remove_duplicated.pkl','rb') as f:
    eight_class_remove_duplicated = pickle.load(f)
with open('/home/caoduanhua/score_function/data/uniport_analysis/hierarchy_uniport_sets_list/uniport_to_pdb_dict.pkl','rb') as f:
    uniport_to_pdb_dict = pickle.load(f)
def select_uniport_for_val(eight_class_remove_duplicated,uniport_to_pdb_dict,rate = 0.12,seed = 42):
    np.random.seed(seed)
    val_uniport_ids = []
    val_uniport_pdb_ids =[]
    for uniport_set in eight_class_remove_duplicated:
        uniport_set = list(uniport_set)
        size = int(rate*len(uniport_set))
        val_uniport_ids.extend(np.random.choice(uniport_set,size = size))
    for uniport_id in val_uniport_ids:

        val_uniport_pdb_ids.extend(uniport_to_pdb_dict[uniport_id])
    return val_uniport_ids,val_uniport_pdb_ids

val_uniport_ids,val_uniport_pdb_ids = select_uniport_for_val(eight_class_remove_duplicated,uniport_to_pdb_dict,seed = 42)
val_keys = [k for k in train_keys if k.split('/')[-1].split('_')[0]  in val_uniport_pdb_ids ]
train_keys = [k for k in train_keys if k.split('/')[-1].split('_')[0] not in val_uniport_pdb_ids ]

print ('Num train keys: ', len(train_keys))
print ('Num val keys: ', len(val_keys))
print ('Num test keys: ', len(test_keys))
print('train/val = ',len(train_keys)/len(val_keys))
print('NUm uniport ids',len(val_uniport_ids))
with open('train_keys.pkl', 'wb') as f:
    pickle.dump(train_keys, f)
with open('test_keys.pkl', 'wb') as f:
    pickle.dump(test_keys, f)
with open('val_keys.pkl', 'wb') as f:
    pickle.dump(val_keys, f)