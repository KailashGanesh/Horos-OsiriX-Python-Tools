import argparse
import pydicom
import numpy as np
from utils import load_xml_to_numpy, save_binary_mask_image

def xml_to_mask(dicom_path, xml_path, output_path):
    # Load DICOM file to get image shape
    dicom_image = pydicom.dcmread(dicom_path)
    image_shape = (dicom_image.Rows, dicom_image.Columns, len(dicom_image.pixel_array))

    # Load ROI from XML and convert to binary mask numpy array
    roi_array = load_xml_to_numpy(xml_path, image_shape)

    # Save binary mask to output path
    first_non_empty_slice_index = next((i for i, sum_val in enumerate(np.sum(roi_array, axis=(0, 1))) if sum_val > 0), None)
    if first_non_empty_slice_index is not None:
        save_binary_mask_image(roi_array, first_non_empty_slice_index, output_path)
        print(f"Binary mask saved to {output_path}")
    else:
        print("No ROI found in the XML file.")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Convert XML ROI annotations to a binary mask given a DICOM image.')
    parser.add_argument('-dicom', required=True, help='Path to the DICOM file.')
    parser.add_argument('-xml', required=True, help='Path to the ROI XML file.')
    parser.add_argument('-o', '--output', required=True, help='Path to save the output binary mask file.')
    return parser.parse_args()

def run_script():
    args = parse_arguments()
    xml_to_mask(args.dicom, args.xml, args.output)

if __name__ == "__main__":
    run_script()
