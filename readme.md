# Ecostack to VWW

Some utils to convert the ecostack pollinator detection dataset (available here: https://vision.eng.au.dk/ecostack/) from YOLO annotation format into MSCOCO, visualwakewords (vww, see: https://arxiv.org/abs/1906.05721 and https://blog.tensorflow.org/2019/10/visual-wake-words-with-tensorflow-lite_30.html). A TFRecord conversion is also required to train using repo accessible here: https://github.com/rossGardiner/visual-wake-words 

Files `dataset_utils.py` and `download_and_convert_visualwakewords_lib.py` are copied from tf_slim library. See: https://github.com/tensorflow/models/blob/master/research/slim/README.md


# Download Ecostack dataset 

```console 
wget https://vision.eng.au.dk/?download=/data/EcoStack/insects/train1201.zip
wget https://vision.eng.au.dk/?download=/data/EcoStack/insects/val1201.zip
wget https://vision.eng.au.dk/?download=/data/EcoStack/insects/test1201.zip
unzip *.zip 
```

Should leave three directories: `train1201/`, `test1201/`, `val1201/`. You may need to rename stuff

# VirtualEnv

```
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
NB: not a lean `requirements.txt` 

# Annotations: YOLO -> MSCOCO
Check the script args:
```
python3 labels_convert_yolo_mscoco.py --help

usage: labels_convert_yolo_mscoco.py [-h] [-b BINARY] [-p PREFIX] [-a ANNOTATION_DIR]

optional arguments:
  -h, --help            show this help message and exit
  -b BINARY, --binary BINARY
                        binary classes or not, 1 or 0 (yes or no)
  -p PREFIX, --prefix PREFIX
                        prefix, train, test or val
  -a ANNOTATION_DIR, --annotation_dir ANNOTATION_DIR
                        annotation directory
```
```
python3 labels_convert_yolo_mscoco.py -p train
python3 labels_convert_yolo_mscoco.py -p val
python3 labels_convert_yolo_mscoco.py -p test
```

# Annotations: MSCOCO -> VWW
```
python3 labels_convert_mscoco_vww.py -p train
python3 labels_convert_mscoco_vww.py -p val
python3 labels_convert_mscoco_vww.py -p test
```
# Annotations: VWW -> TFRecord
```
python3 labels_convert_vww_tfrecord.py -p train
python3 labels_convert_vww_tfrecord.py -p val -s 10
python3 labels_convert_vww_tfrecord.py -p test
```

# Check: Tfrecord
Play around with `inspect_tfrecord.py` to check the contents of a resultant tfrecord file