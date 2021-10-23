import xml.etree.ElementTree as ET
from xml.dom import minidom
from tqdm import tqdm
import os
from glob import glob
import shutil


def format_vehicle_xml_object_xml(output_file,path_image,folder_name, id_object, class_name, xmin, ymin, xmax, ymax):
    """
    This function paste data to the pascal voc annotations
    """
    template_xml_file= ET.parse(output_file)
    root = template_xml_file.getroot()
    path=root.find('path')
    filename=root.find('filename')
    folder=root.find('folder') 
    
    data = ET.Element('object')
    
    name = ET.SubElement(data, 'name')
    pose = ET.SubElement(data, 'pose')
    truncated = ET.SubElement(data, 'truncated')
    difficult = ET.SubElement(data, 'difficult')
    bndbox = ET.SubElement(data, 'bndbox')

    bndbox_elem1 = ET.SubElement(bndbox, 'xmin')
    bndbox_elem2 = ET.SubElement(bndbox, 'ymin')
    bndbox_elem3 = ET.SubElement(bndbox, 'xmax')
    bndbox_elem4 = ET.SubElement(bndbox, 'ymax')
    
    path.text=path_image 
    filename.text=path_image.split('/')[-1]
    folder.text=folder_name
    data.set('id',id_object )    
    name.text = class_name
    pose.text = 'Unspecified'
    truncated.text = '0'
    difficult.text = '0'

    bndbox_elem1.text = str(xmin)
    bndbox_elem2.text = str(ymin)
    bndbox_elem3.text = str(xmax)
    bndbox_elem4.text = str(ymax)

    
    root.append(data)
    vehicle_xml = ET.tostring(root)
    
    with open(output_file, "wb") as f:
        f.write(vehicle_xml)
        
#Initialize Paths
ROOT_PATH=os.getcwd()

#Images Paths
TRAIN_PATH = ROOT_PATH + '/Insight-MVT_Annotation_Train/'
TEST_PATH = ROOT_PATH + '/Insight-MVT_Annotation_Test/'

#Original Annotations Paths
TRAIN_ANNOT_PATH = ROOT_PATH + '/DETRAC-Train-Annotations-XML/'
TEST_ANNOT_PATH = ROOT_PATH + '/DETRAC-Test-Annotations-XML/'

#Destionation Paths (To save PASCAL VOC annotations)
SAVE_TRAIN_PATH=ROOT_PATH + '/train_annotations_voc_format/'
SAVE_TEST_PATH=ROOT_PATH + '/test_annotations_voc_format/'

PATHS= [TRAIN_PATH, TEST_PATH]
ANNOT_PATHS= [TRAIN_ANNOT_PATH, TEST_ANNOT_PATH]
SAVE_PATHS=[SAVE_TRAIN_PATH, SAVE_TEST_PATH]

SUBSET_NAMES=['TRAIN SUBSET', 'TEST SUBSET']

template_file=ROOT_PATH+'/template.xml'

for P in range(0, len(PATHS)):
    print('Transform |{}| annotations to PASCAL VOC Format'.format(SUBSET_NAMES[P]))
    os.chdir(PATHS[P])
    folders= os.listdir()
    for folder in tqdm(folders):
        os.makedirs(SAVE_PATHS[P]+folder, exist_ok=True)

        os.chdir(PATHS[P]+folder) 
        images= sorted(glob('*'))
        
        xml_file= ET.parse(ANNOT_PATHS[P]+folder+'.xml')
        root = xml_file.getroot()
        frames= root.findall("frame")

        for F in range(0, len(frames)):
            targets= frames[F].find('target_list').findall('target')
            output_file_name= SAVE_PATHS[P]+folder+'/'+frames[F].attrib['num']+'.xml'
            shutil.copyfile(template_file, output_file_name)
            for target in targets:
                #retrieve some data
                id=target.attrib['id']
                
                box=target.find('box')
                attribute = target.find('attribute')

                x_min=round(float(box.attrib['left']))
                y_min=round(float(box.attrib['top']))
                x_max=round(float(box.attrib['width'])) + x_min
                y_max=round(float(box.attrib['height'])) + y_min

                name=attribute.attrib['vehicle_type']

                path_img= TRAIN_PATH+folder+'/'+frames[F].attrib['num']+'.jpg'
                
                format_vehicle_xml_object_xml(output_file_name, path_img,folder, id, name, x_min, y_min, x_max, y_max)
            
            
            xml_file= ET.parse(output_file_name)
            xml_data = xml_file.getroot()
            
            pretty_xml_file = minidom.parseString(ET.tostring(xml_data)).toprettyxml(indent="   ")
            with open(output_file_name, "w") as f:
                f.write(pretty_xml_file)      

