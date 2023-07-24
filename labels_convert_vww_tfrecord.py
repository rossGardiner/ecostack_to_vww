import download_and_convert_visualwakewords_lib
import argparse
import os 

argParser = argparse.ArgumentParser()
argParser.add_argument("-p", "--prefix", help="prefix, train, test or val", default="train")
argParser.add_argument("-a", "--annotation_dir", help="annotation directory", default="annotations/")
argParser.add_argument("-s", "--shards", type=int, help="nr of shards for the tfrecord files, reccomend 100 for train and 10 for val", default=100)
argParser.add_argument("-t", "--tfrecord_dir", help="output dir for tfrecord format files", default="vww_tfrecords")
args = argParser.parse_args()

def make_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)
        print(f"Created directory at {os.path.abspath(d)}")

make_dir(args.annotation_dir)
make_dir(args.tfrecord_dir)

vww_filename = f"{args.annotation_dir}/vww_{args.prefix}1201_insect_mscoco.json"
tfrecord_filename = f"{args.prefix}.record"
imgdir = f"{args.prefix}1201"
shardnr = args.shards

download_and_convert_visualwakewords_lib.create_tf_record_for_visualwakewords_dataset(vww_filename, imgdir, f"{args.tfrecord_dir}/{tfrecord_filename}", shardnr)