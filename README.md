# Horos/OsiriX Python Tools

<img src="./images/logo.webp" alt="logo of repository">
<center> <small>Logo created by chatGPT</small> </center>  

</br>

Need to automate the conversion of ROIs to binary masks? _There's a script for that!_  
Lacking a Mac but still need to visualize those ROIs? No worries, _there's a script for that too!_



how to use xml2mask.py

in bash:
```bash
python xml2mask.py -dicom /path/to/dicom.dcm -xml /path/to/roi.xml -o /path/to/output/mask.nii
```

If you want to call this script from a larger Python script, you could import the xml_to_mask function directly and use it like this:

```python
from xml2mask import xml_to_mask

xml_to_mask('/path/to/dicom.dcm', '/path/to/roi.xml', '/path/to/output/mask.nii')
```