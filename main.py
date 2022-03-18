import matplotlib.pyplot as plt
import cvb
import cv2

print("共發現"+str(len(cvb.DeviceFactory.discover_from_root(cvb.DiscoverFlags.IgnoreVins)))+"個裝置")

for discover_cam in cvb.DeviceFactory.discover_from_root(cvb.DiscoverFlags.IgnoreVins):
    
    try:
        device = cvb.DeviceFactory.open(discover_cam.access_token)
        print(str({discover_cam})+" 已連接")
        
        device_node_map = device.node_maps["Device"]
        exposure_node = device_node_map["ExposureTime"]
        exposure_node.value = 50000 
        # print(exposure_node.value)
        
        print("Vendor:  " + device_node_map["DeviceVendorName"].value)
        print("Model:   " + device_node_map["DeviceModelName"].value)
        print("Version: " + device_node_map["DeviceVersion"].value)
        print("Exposure: " + str(exposure_node.value))
        
    except :
        print(str({discover_cam})+" 無法連接")


# device = cvb.DeviceFactory.open(cvb.DeviceFactory.discover_from_root(cvb.DiscoverFlags.IgnoreVins)[1].access_token)

stream = device.stream
stream.start()
image, status = stream.wait() 
while status == cvb.WaitStatus.Ok:
                image, status = stream.wait() 
                # image, status = wait_for_newest(device.stream)
                # create numpy array from cvb image (without copying data)
                matrix = cvb.as_array(image)   
                
                cv2.namedWindow('image',cv2.WINDOW_AUTOSIZE)
                # cv2.resizeWindow("image", 1200, 600)
                resimg = cv2.resize(matrix,(1224,1024),interpolation=cv2.INTER_CUBIC)
                cv2.imshow('image',resimg)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    #exit()
                    break
stream.abort()
