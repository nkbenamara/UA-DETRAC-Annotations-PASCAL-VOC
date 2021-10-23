# UA-DETRAC-Annotations-PASCAL-VOC
The python script provided in this repository allows:
- Convert UA-DETRAC XML Annotations to PASCAL VOC XML annotations.
- Generate an annotation for each frame in a separate file, instead of a single annotation per sequence.

(From) Original XML Annotations (UA-DETRAC):

         <target id="1">
            <box left="592.75" top="378.8" width="160.05" height="162.2"/>
            <attribute orientation="18.488" speed="6.859" trajectory_length="5" truncation_ratio="0.1" vehicle_type="car"/>
         </target>
         <target id="2">
            <box left="557.65" top="120.98" width="47.2" height="43.06"/>
            <attribute orientation="19.398" speed="1.5055" trajectory_length="72" truncation_ratio="0" vehicle_type="car"/>
         </target>
         

(To) Converted XML Annotations (UA-DETRAC in PASCAL VOC Format: 

   <object id="1">
      <name>car</name>
      <pose>Unspecified</pose>
      <truncated>0</truncated>
      <difficult>0</difficult>
      <bndbox>
         <xmin>593</xmin>
         <ymin>379</ymin>
         <xmax>753</xmax>
         <ymax>541</ymax>
      </bndbox>
   </object>
   <object id="2">
      <name>car</name>
      <pose>Unspecified</pose>
      <truncated>0</truncated>
      <difficult>0</difficult>
      <bndbox>
         <xmin>558</xmin>
         <ymin>121</ymin>
         <xmax>605</xmax>
         <ymax>164</ymax>
      </bndbox>
   </object>
   
