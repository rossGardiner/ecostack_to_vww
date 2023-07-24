import download_and_convert_visualwakewords_lib
import argparse 
import os

argParser = argparse.ArgumentParser()
argParser.add_argument("-p", "--prefix", help="prefix, train, test or val", default="train")
argParser.add_argument("-a", "--annotation_dir", help="annotation directory", default="annotations/")
argParser.add_argument("-t", "--threshold", type=float, help="threshold, percent of image to annotate as positive (switching from detection to classification dataset", default=0.001)
args = argParser.parse_args()

def make_annotations_dir(d:str =f"{args.annotation_dir}"):
    if not os.path.exists(d):
        os.makedirs(d)
        print(f"Created directory at {os.path.abspath(d)}")

make_annotations_dir()
mscoco_file = f"{args.annotation_dir}/{args.prefix}1201_insect_mscoco.json"
threshold = args.threshold

download_and_convert_visualwakewords_lib.create_labels_file("insect", "labels.txt")

vww_filename = args.annotation_dir + "/vww_" + mscoco_file.split("/")[-1]

download_and_convert_visualwakewords_lib.create_visual_wakeword_annotations(mscoco_file, vww_filename, threshold, "insect")