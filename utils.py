import xml.etree.ElementTree as ET
import numpy as np
from skimage.draw import polygon
import matplotlib.pyplot as plt

def load_roi_from_xml(file_xml, imshape):
    """
    Load an OsiriX XML region as a binary numpy array.
    
    Parameters:
    file_xml : str
        Path to the XML file of the annotation.
    imshape : tuple
        The shape of the 3D volume as a tuple (width, height, slices).
    
    Returns:
    numpy.ndarray
        A numpy array where positions in the ROI are assigned a value of 1.
    """
    tree = ET.parse(file_xml)
    root = tree.getroot()
    rois = root.find('.//array')
    
    volume = np.zeros(imshape, dtype=np.int32)
    
    for roi_dict in rois.findall('dict'):
        slice_index = -1
        points = []
        items = list(roi_dict)
        for i in range(len(items)):
            if items[i].tag == 'key':
                if items[i].text == "Slice":
                    slice_index = int(items[i + 1].text) - 1
                elif items[i].text == "ROIPoints":
                    points = items[i + 1].findall('string')
        
        if slice_index < 0 or slice_index >= imshape[2] or not points:
            continue
        
        x, y = [], []
        for point in points:
            coords = point.text.strip('{}').split(', ')
            x.append(float(coords[0]))
            y.append(float(coords[1]))
        
        rr, cc = polygon(y, x)
        volume[rr, cc, slice_index] = 1
    
    return volume

def plot_roi_slices(roi_array):
    """
    Plot the ROI arrays for each slice that contains an ROI using matplotlib.
    
    Parameters:
    roi_array : numpy.ndarray
        The 3D numpy array containing the ROI data.
    """
    slices = roi_array.shape[2]
    count = np.sum(roi_array, axis=(0, 1))
    
    for i in range(slices):
        if count[i] > 0:
            plt.imshow(roi_array[:, :, i], cmap='gray')
            plt.axis('off')
            plt.show()

def save_binary_mask(roi_array, slice_index, filepath):
    """
    Save a single ROI slice as an image file without any borders or padding.
    
    Parameters:
    roi_array : numpy.ndarray
        The 3D numpy array containing the ROI data.
    slice_index : int
        The index of the slice to save (0-based index).
    filepath : str
        The path where the image file will be saved.
    """
    img = roi_array[:, :, slice_index]
    plt.imsave(filepath, img, cmap='gray')

# Example usage:
# xml_file_path = 'path/to/your/roi.xml'  # Provide your XML file path
# imshape = (320, 320, 45)  # Replace with your image shape
# roi_array = load_roi_from_xml(xml_file_path, imshape)
# plot_roi_slices(roi_array)
# save_binary_mask(roi_array, slice_index=0, filepath='path/to/save/roi_slice.png')  # Save first non-empty slice

