import os
import sys
import pdb

src_folder, style = sys.argv[1:]

"""
https://gist.github.com/ksimonyan/fd8800eeb36e276cd6f9#note

mkdir data_val
tar xf ILSVRC2012_img_val.tar -C data_val

mkdir /tmp/ILSVRC2012_img_val/
tar -xf ~/Downloads/ILSVRC2012_img_val.tar -C /tmp/ILSVRC2012_img_val/
python label_as_filename.py /tmp/ILSVRC2012_img_val  caffe 

mkdir /tmp/ILSVRC2012_img_val/
tar -xf /mnt/nfs/seedcake/imagenet-data/ILSVRC2012_img_val.tar -C /tmp/ILSVRC2012_img_val/
python label_as_filename.py /tmp/ILSVRC2012_img_val  caffe 
"""

ground_truth_file = {'official': "ILSVRC2014_clsloc_validation_ground_truth.txt", 
                     'caffe': "caffe_clsloc_validation_ground_truth.txt"}

if style == 'official':
    get_class_id_func = lambda x: int(x)-1
elif style == 'caffe':
    get_class_id_func = lambda x: int(x.split()[1])

labels_text = open(ground_truth_file[style]).readlines()
labels = map(get_class_id_func, labels_text)

tgt_folder = "ILSVRC2012_img_val_labeled_%s" % style
tgt_folder = os.path.join(os.path.dirname(src_folder), tgt_folder)
if not os.path.isdir(tgt_folder):
    os.makedirs(tgt_folder)

for i,lab in zip(range(1, 50001),list(labels)):

    src_fname = "ILSVRC2012_val_%08d.JPEG" % i
    tgt_fname = "%d.%d.JPEG" % (lab, i)
    src_path = os.path.abspath(os.path.join(src_folder, src_fname))
    tgt_path = os.path.join(tgt_folder, tgt_fname)

    # Check if the target file already exists
    if not os.path.exists(tgt_path):
        os.symlink(src_path, tgt_path)
    else:
        # If the file exists, print a message. Alternatively, you can handle it differently.
        print(f"Target file already exists, skipping: {tgt_fname}")