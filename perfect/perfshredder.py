from PIL import Image
import random
import os
import glob


#https://instagram-engineering.com/instagram-engineering-challenge-the-unshredder-7ef3f7323ab1
def shredImage(sequence, outputPath, demoPath,image,shred_width, shred_height,width,height):
    # Create jumbled shred fiiles
    shredded = Image.new('RGBA', image.size)
    for i, shred_index in enumerate(sequence):
        # Calculate the dimensions of each shred and it's shuffled order
        shred_x1, shred_y1 = shred_width * shred_index, 0 #1~3 까지 잘랐으면 3~5, 5~7 단위로 자르기
        shred_x2, shred_y2 = shred_x1 + shred_width, height

        # Crop the shred region and save it
        region = image.crop((shred_x1, shred_y1, shred_x2, shred_y2))
        region.save(f"{outputPath + str(i)}.png")
        shredded.paste(region, (shred_width * i, 0))
        shredded.save(demoPath)

def h_shredImage(sequence, outputPath, demoPath,image,shred_width,shred_height,width,height):#수직 절단 
    shredded = Image.new('RGBA', image.size)
    for i, shred_index in enumerate(sequence):
        shred_x1, shred_y1 = 0, shred_height * shred_index
        shred_x2, shred_y2 = width, shred_height + shred_y1

        region = image.crop((shred_x1, shred_y1, shred_x2, shred_y2))
        region.save(f"{outputPath + str(i)}.png")
        shredded.paste(region, (0,shred_height * i))
        shredded.save(demoPath)

def do_shred(method ,SHREDS, path, output_path, demo_path):
    

    # Open the image
    image = Image.open(path)
    shredded = Image.new('RGBA', image.size)

    # Gather the width, height
    width, height = image.size

    # Shred width must not be lower than 14px
    shred_width = width // SHREDS
    if shred_width < 14:
        shred_width = 14
        SHREDS = width // 14
    
    shred_height = height // SHREDS
    if shred_height < 14:
        shred_width = 14
        SHREDS = height //14

    # Shuffle a list of a range between 0 and the shred value given
    sequence = list(range(0, SHREDS))
    # random.shuffle(sequence)

    if method == "H":
        h_shredImage(sequence, output_path, demo_path,image,shred_width,shred_height,width,height)
    elif method == "V":
        shredImage(sequence, output_path, demo_path,image,shred_width,shred_height,width,height)

def h_shredder_for_perfShred(sequence, outputPath, demoPath,image,shred_width,shred_height,width,height,j):#수직 절단 
    shredded = Image.new('RGBA', image.size)
    i = 0
    for i, shred_index in enumerate(sequence):
        file_index = shred_index
        shred_index = shred_index % 20
        
        
        shred_x1, shred_y1 = 0, shred_height * shred_index
        shred_x2, shred_y2 = width, shred_height + shred_y1

        region = image.crop((shred_x1, shred_y1, shred_x2, shred_y2))
        region.save(f"{outputPath + str(file_index)}.png")
        # shredded.save(demoPath+"perfDemo{}.png")
        # shredded.save(demoPath,f"perfDemo{j}.png")
        # shredded.save(f"{demo_path + str(i)}.png")
        # "{outputPath + str(i)}.png"
        shredded.paste(region, (0,shred_height * i))
        
        shredded.save(f"{demo_path + 'perfect_shredded_'+str(j)}.png")
    

def do_perfShred(SHREDS, path, output_path, demo_path):
    file_list = os.listdir(path) 
    j = 0
    print(file_list)
    for i in file_list:
        if i == '.DS_Store':
            continue
        image = Image.open(path+i)
        width, height = image.size
        
        # Shred width must not be lower than 14px
        shred_width = width // SHREDS
#         if shred_width < 14:
#             shred_width = 14
#             SHREDS = width // 14
        
        shred_height = height // SHREDS
        if shred_height < 14:
            shred_width = 14
            SHREDS = height //14

        sequence = list(range(j*20, (j+1)*20))
        print(sequence)
        random.shuffle(sequence)
        h_shredder_for_perfShred(sequence, output_path, demo_path, image, shred_width, shred_height, width, height,j)
        j += 1
    
if __name__ == "__main__":
    path = "/Users/kyeong/dev/python3/Document-Reconstructor-master/testImages/shredThis.png"
    outputPath = "/Users/kyeong/dev/python3/Document-Reconstructor-master/asset/"
    demoPath = "/Users/kyeong/dev/python3/Document-Reconstructor-master/demos/notPerf_Demo.png"

    # do_shred('H'orizontal/'V'ertical, Shreds, source_imge, output_path, demo_output_path)
    do_shred("H", 10, path, outputPath, demoPath)


    # path = outputPath
    # outputPath = "/Users/kyeong/dev/python3/Document-Reconstructor-master/perfect_asset/"
    # demo_path = "/Users/kyeong/dev/python3/Document-Reconstructor-master/demos/"
    # do_perfShred(20, path, outputPath, demo_path)

