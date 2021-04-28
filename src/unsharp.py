import argparse
import os
from wand.image import Image

parser = argparse.ArgumentParser()
parser.add_argument("image_file", help="The image to unsharp")
parser.add_argument("-r", "--radius", help="Unsharp radius", type=int, default=10)
parser.add_argument("-s", "--sigma", help="Unsharp sigma", type=int, default=4)
parser.add_argument("-a", "--amount", help="Unsharp amount", type=int, default=1)
parser.add_argument("-t", "--threshold", help="Unsharp threshold", type=int, default=0)
args = parser.parse_args()

if os.path.isfile(args.image_file) == False:
    raise RuntimeError("File '%s' doesn't exists" %args.image_file)

with Image(filename=args.image_file) as img:
    img.unsharp_mask(radius=args.radius, sigma=args.sigma, amount=args.amount, threshold=args.threshold)
    source_parent_path=os.path.abspath(os.path.join(args.image_file, os.pardir))
    source_file_name_split = os.path.splitext(os.path.basename(args.image_file))
    destination_file_name = source_file_name_split[0] + "_unsharp.png"
    destination_file_path = os.path.join(source_parent_path, destination_file_name)
    img.save(filename=destination_file_path)