## DMHC HOST Probe

 Device Mesh for Health Check
 
 DMHC is a mesh of devices, each one with a Heart rate, Oxygen saturation SpO2 and Temperature, (HOST) probe to capture values.
 
 ![Imagen](https://hackster.imgix.net/uploads/attachments/1351356/img_4461_bwFKbqEmXt.jpg?auto=compress%2Cformat&w=740&h=555&fit=max)
 
 The probe using AWS IoT EduKit and some units sensores.
 
 ![Imagen](https://hackster.imgix.net/uploads/attachments/1351986/dmhc_block_diagram_UNn0r63bXc.png?auto=compress%2Cformat&w=1280&h=960&fit=max)

 
 [Can see video demo here](https://www.youtube.com/watch?v=ma2zLZVV3kU)
 
 
### Gettting Started

The project description could be found at 
 https://www.hackster.io/jose-cruz/device-mesh-for-health-control-f12740
 
 
 
### Files and folders description

```dmhcV2.m5f```
- The main program build using [UIFlow v1.8.4](https://shop.m5stack.com/pages/uiflow)

```dmhcV2.py```
- Micropython source code for main program 

```setDeviceId.m5f``` 
- UIFlow program for set a device_id in AWS IoT Edukit EEprom memory

```setDeviceId.py``` 
- Micropython source code for setDeviceId.m5f

```/images folder``` 
- Have all png images files resources. 
- Need to be upload to AWS IoT Edukit using [M5Burner](https://shop.m5stack.com/pages/download) 

```/wav folder```
- Have all wav sound files resources. 
- Need to be upload too to AWS IoT EduKit

```/mp3 folder``` 
- Have source mp3 sound files created using [Amazon Polly](https://aws.amazon.com/polly/?nc1=h_ls). 
- They were converted to wav files using [Online Converter](https://www.online-convert.com/). 
- Need to be upload too to AWS IoT EduKit

```/lcad/DMHC_Host_Probe_Base.ldr``` 
- [Cad lego](http://www.melkert.net/LDCad) file, with all step instructions for base construction 

```/lcad/DMHC_Host_Probe_Base.pdf``` 
- All lego base construction instructions in pdf format

```/lambda_functions/dmhc_TimeStamp.js``` 
- Lambda function in Node.Js used to create in json message received a timestamp field server_time before put it in AWS IoT Analytics data store

```/lambda_functions/dmhc_ResetDevice.js``` 
- Lambda function in Node.Js used to reset device and send Slack and SMS notification to AWS SNS topic

