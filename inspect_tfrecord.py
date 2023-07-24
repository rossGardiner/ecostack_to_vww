import tensorflow.compat.v1 as tf
from google.protobuf.json_format import MessageToJson 
import json

for example in tf.python_io.tf_record_iterator("vww_tfrecords/val.record-00000-of-00010"):
    #print(tf.train.Example.FromString(example))
    eg = tf.train.Example.FromString(example)
    jsonMessage = MessageToJson(tf.train.Example.FromString(example))
    
    json_data = json.loads(jsonMessage)
    print(list(json_data['features']['feature']['image/class/label']['int64List']['value']))
    break
