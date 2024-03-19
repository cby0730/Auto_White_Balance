import cv2
import math
import argparse
import numpy as np
import matplotlib.pyplot as plt

color = {"A" : [0.44757, 0.40745], "B" : [0.34842, 0.35161], "C" : [0.31006, 0.31616], "D65" : [0.31271, 0.32902], "D93" : [0.28315, 0.29711], "E" : [0.33333, 0.33333]}

def to_A_color(image, temperature): 
    
    if temperature in list(color.keys()) :
        cie_y = 250
        cie_x = cie_y * color[temperature][0] / color[temperature][1]
        cie_z = cie_y * ( 1 - color[temperature][0] - color[temperature][1] ) / color[temperature][1]
        temperature_color = np.array([cie_x, cie_y, cie_z])
    else :
        return None, False
    
    white = np.array([255, 255, 255])
    if np.all(np.max(image, axis = (0, 1)) == white ) :

        image = cv2.cvtColor(image, cv2.COLOR_BGR2XYZ)
        
        max_xyz = np.max(image, axis = (0, 1)) # find max xyz
        K_xyz = temperature_color / max_xyz  # von Kries
        image = image * K_xyz # apply the addjustment to entire image
        
        balanced_image = np.clip(image, 0, 255).astype(np.uint8)

    else :
        image = cv2.cvtColor(image, cv2.COLOR_BGR2XYZ)

        num_max = int(0.05 * (image.shape[0] * image.shape[1])) # get top 5% of white spot
        top_xyz = np.sort(image.reshape(-1, 3), axis=0)[::-1][0:num_max] # sort
        top_mean_xyz = np.mean(top_xyz, axis=0) 
        K_xyz = temperature_color / top_mean_xyz  # von Kries
        image = image * K_xyz # apply the addjustment to entire image
        
        balanced_image = np.clip(image, 0, 255).astype(np.uint8)


    return cv2.cvtColor(balanced_image, cv2.COLOR_XYZ2BGR), True # convert back to BGR

def parse_args():
    parse = argparse.ArgumentParser(description='white balance') 
    parse.add_argument('-p', '--path', type=str, help='image path', required=True)
    parse.add_argument('-t', '--temperature', type=str, help='image color temperature', default = "A", required=True)
    args = parse.parse_args()  
    return args

if __name__ == '__main__' :
    args = parse_args()
    # 讀取圖像
    input_image = cv2.imread(args.path)
    WB_image, flag = to_A_color(input_image, args.temperature)
    cv2.imwrite("out/WB_image.jpg", WB_image)

    if flag :
        _, axes = plt.subplots(1, 2, figsize=(15, 8))
            
        axes[0].imshow(cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB))
        axes[0].set_title('Original Image')
        axes[0].axis('off')

        axes[1].imshow(cv2.cvtColor(WB_image, cv2.COLOR_BGR2RGB))
        axes[1].set_title('Auto White Balance')
        axes[1].axis('off')

        plt.tight_layout()
        plt.savefig('output.jpg')
        plt.show()

    else :
        print(f"There is no {args.temperature}, please try again")
