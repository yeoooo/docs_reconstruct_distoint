from skimage.metrics import structural_similarity
from PIL import Image
import cv2
import numpy as np
import glob


# np.set_printoptions(threshold=784,linewidth=np.inf) 

class DisjointSet:
    
    def __init__(self, n): 
        self.data = list(range(n))
        self.size = n 
        self.bottom = list(range(n))
        
    def find(self, index):#반환은 이전의 point의 내용과 같다
        return self.data[index], self.bottom[self.data[index]] 
    
    def union(self, x, y):
        x, _ = self.find(x)
        y, k = self.find(y) 
        if x == y: return #같은 경우는 필요없음 -> 종료 
    
        for i in range(self.size): 
            if self.find(i)[0] == y: 
                self.data[i] = x
        self.bottom[x] = k

# def getShreds(path):
#     # Gather the extracted shreds from a directory and store their edge info

#     shreds = []
#     for file in glob.glob(path):
#         cv2.COLOR_BGR2GRAY
#         image = cv2.imread(file) // 128
#         height, width = image.shape[0:2]
#         # Set Edge pixel widths
#         leftEdge = image[0:height, 0:1] // 128   
#         rightEdge = image[0:height, width - 1:width] // 128
#         info = {'image': image, 'left': leftEdge, 'right': rightEdge}
#         shreds.append(info)
#     return shreds

def h_getShreds(path):
    cnt = 0
    shreds = []
    tmp = []
    for file in glob.glob(path):
        image = cv2.imread(file)
        image = (image // 128)*255
        height, width = image.shape[0:2]
        topEdge = image[0:1,0:width]
        botEdge = image[height - 1:height, 0:width]
        info = {'image' : image, 'top' : topEdge, 'bottom':botEdge}
        
        shreds.append(info)
    
    return shreds
def h_getShreds(path):
    cnt = 0
    shreds = []
    for file in glob.glob(path):
        image = cv2.imread(file)
        height, width = image.shape[0:2]
        topEdge = image[0:1,0:width]
        botEdge = image[height - 1:height, 0:width]
        info = {'image' : image, 'top' : topEdge, 'bottom':botEdge}
        shreds.append(info)
    
    return shreds

def mse(imageA, imageB):
	# The 'Mean Squared Error' between the two images is the sum of the squared 
    # difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
    # Return the MSE
	return err

def calcSimilarity(left, right, test1, test2):
    left = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
    right = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)
    m = mse(left, right)
    return m

def combine(leftImage, rightImage):
    # Combine two shreds
    return np.concatenate((rightImage, leftImage), axis=1)

def h_combine(topImage, botImage):
    return np.concatenate((botImage,topImage),axis=0)

def getSimilarityScores(shreds):
    # Gather the similarity scores for shred comparisons
    similarity = []
    cnt = 0
    # Compare the left side of a shred with the right side of every other shred
    for index1, i in enumerate(shreds):
#         final = cv2.cvtColor(shreds[index1]['image'],cv2.COLOR_BGR2RGB)
#         cv2.imwrite(f"/home/aiffel-dj16/Desktop/Document-Reconstructor-master/testImages/index/process{index1}.png".format(index1),final)

        for index2, j in enumerate(shreds):
            # If comparing the same shred, continue
            if i is j:
                continue
            m = calcSimilarity(i['top'], j['bottom'], i['image'], j['image'])
            
            similarity.append({m: (index1, index2)})
    return similarity

def h_getSimilarityScores(shreds):
    # Gather the similarity scores for shred comparisons
    similarity = []
    # Compare the left side of a shred with the right side of every other shred
    for index1, i in enumerate(shreds):
        for index2, j in enumerate(shreds):
            # If comparing the same shred, continue
            if i is j:
                continue
            m = calcSimilarity(i['top'], j['bottom'], i['image'], j['image'])#이미지 1의 상단 엣지와 이미지 2의 하단 엣지 비교
            
            similarity.append({m: (index1, index2)})
    return similarity

def h_unShred(shreds, similarity):
    cnt=0
    merged = DisjointSet(len(shreds))
    finalIndex = ""
    

    #merged와 b_merged에 이미 판단한 조각에 대해 재판단 하지 않도록
    #끝의 index를 반환함으로써 아래에 붙일 수 있도록
    for j in sorted(similarity, key=lambda d: list(d.keys())):
    #simikarity = {sim : (patch1, patch2)}
       
#         if len(merged) == len(shreds) - 1:#선택된 조각이 마지막 조각이면
#             break

        for tup in j:
            # if tup == 0:
            #     continue 
#             if tup > 10000:
#                 break
            
            t = j[tup][0]#28
            b = j[tup][1]#42
            
            
            
            top_t, top_b = merged.find(t)# merged patch의 위, 아래
            bott_t, bott_b = merged.find(b) # b_merged patch의 위, 아래 
            
            if top_t == bott_t:
                continue
            
            if  top_b != t or b != bott_t:
                continue
#             else:
#                 print("t = {} \nb = {}".format(merged.find(t),merged.find(b)))
#                 print("top_t = ",top_t)
#                 print("top_b = ",top_b)
#                 print("bott_t = ",bott_t)
#                 print("bott_b = ",bott_b)
            print(f'top :{t}, bottom:{b}')
            print("top_t = ",top_t,"top_b = ",top_b)
            print("bott_t = ",bott_t,"bott_b = ",bott_b)
            
#             if top_t == bott_t or (top_b != t and bott_b != b):
#                 break
            
            print("-----------------------------------------")
            print(f"Mean Squared Error: {tup}")
            print("-----------------------------------------")
            
            
            shreds[top_t]['image'] = h_combine(shreds[top_t]['image'], shreds[bott_t]['image']) 
            merged.union(t,b)
            # print(merged.size)
            


            final = cv2.cvtColor(shreds[top_t]['image'],cv2.COLOR_BGR2RGB)
            cv2.imwrite(f"/Users/kyeong/Document-Reconstructor-master/process/process{cnt}.png".format(cnt),final)
            cnt += 1

            finalIndex = top_t
            
            
#             print(merged.find(0))
#             print(merged.find(b)[0])
            break

    return finalIndex

def min_zone(unshredded):  #제일 작은 공백 찾기 
                            #인자는 img
    width, height = unshredded.size

    unshredded = np.array(unshredded)
    unshredded = (unshredded//128)*255#보험용
    
    zone = np.array([[255 for j in range(3)] for i in range(width)])
    cnt = 0
    cnt_arr = []
    for i, line in enumerate(unshredded):
        if zone.all() == line.all():#공백 감지
            cnt += 1
        else:
            cnt_arr.append(cnt)
            cnt = 0
    cnt_arr = sorted(list(set(cnt_arr)))
    return cnt_arr

def clustering(unshredded, output_path):
    
    unshredded = cv2.imread(unshredded_path)

    image = Image.fromarray(unshredded)
    unshredded = (unshredded//128)*255#보험용

    width, height = image.size

    zone_height = min_zone(image)
    
    selector = 0
    sp = 0
    cnt = 0
    ep = 0
    
    hard_zone_height = 6
    #자간고려

    zone = np.array([[[255 for j in range(3)] for i in range(width)] for k in range(hard_zone_height)])
    zone = zone.astype("uint8")

    for i in range(0,(height//hard_zone_height)+1):
        
        if zone.all() == unshredded[i * hard_zone_height : (hard_zone_height * i) + hard_zone_height+1].all():#탐색한 부분이 공백인 경우
            print(selector)
            ep += hard_zone_height
            

            if selector == 0 or selector == 1:#이전 상태와 같은 경우


                selector = 1 
                continue


            elif selector != 1:
                
                selector = 1

        else:#탐색한부분이 글자인 경우
            ep += hard_zone_height
            print(selector)
            if selector == 0 or selector == 2: #이전 상태와 같은 경우
                

                selector = 2
                continue

            elif selector != 2:#상태가 다른 경우
                
                selector = 2

        if ep == sp:
            continue


        region = image.crop((0,sp,width,ep))            
        region.save(f"{output_path + str(cnt)}.png")
        print(sp, ep)

        cnt += 1
        sp = ep


if __name__ == '__main__':

    # path = "/Users/kyeong/dev/python3/Document-Reconstructor-master/asset/*"
    # shreds = h_getShreds(path)
    # similarity = getSimilarityScores(shreds)

    # finalIndex = h_unShred(shreds, similarity)
    # final = cv2.cvtColor(shreds[finalIndex]['image'], cv2.COLOR_BGR2RGB)
    # cv2.imwrite(f"/Users/kyeong/dev/python3/Document-Reconstructor-master/result/recontructed_h.png", final)
    
    # unshredded_path는 이전에 unshredding에 대한 결과가 있는 경로여야 합니다.
    unshredded_path = "/Users/kyeong/dev/python3/Document-Reconstructor-master/result/recontructed_h.png"
    output_path = "/Users/kyeong/dev/python3/Document-Reconstructor-master/result/clustered/"
    
    clustering(unshredded_path, output_path)

