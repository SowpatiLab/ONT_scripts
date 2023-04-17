import os
import argparse
from fast5_research import Fast5
import sys

parser = argparse.ArgumentParser(description ='Add Sample ID metadata to fast5 file')

parser.add_argument('--fast5', help='Path to fast5 Dir',type=str, required=True)
parser.add_argument('--sampleID', help='Sample ID ', type=str, required=True)

args = parser.parse_args()


fast5_dir=args.fast5
sampleID=args.sampleID

os.chdir(fast5_dir)
for f in os.listdir():
    filename, file_ext = os.path.splitext(f)
    if file_ext == '.fast5':
        with Fast5(filename+file_ext) as fh:
            tracking_id = fh.tracking_id
            tracking_id["sample_id"] = sampleID   # Add sample_id to the tracking ID atrribute
            context_tags = fh.context_tags
            channel_id = fh.channel_meta
            
        # Print updated tracking_id with sample_id information
        print('tracking_id {}.'.format(tracking_id))

        # Repack fast5 by appending updated tracking id
        with Fast5.New(filename+file_ext, 'a', tracking_id=tracking_id,context_tags=context_tags,channel_id=channel_id) as h:
            h.repack()

