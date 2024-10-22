DATA_DIR="data/"

TEST_DATA_FILENAME=DATA_DIR+"t10k-images.idx3-ubyte"
TEST_LABELS_FILENAME=DATA_DIR+"t10k-labels.idx1-ubyte"
TRAINING_DATA_FILENAME=DATA_DIR+"train-images.idx3-ubyte"
TRAINING_LABELS_FILENAME=DATA_DIR+"train-labels.idx1-ubyte"


def read_images(filename,n_max_images=0):
    images=[]
    with open(filename,"rb") as f:
        _=f.read(4) #ignore the magic number
        n_images=toInt(f.read(4))
        n_rows=toInt(f.read(4))
        n_cols=toInt(f.read(4))
        
        if(n_max_images>0 and n_max_images<n_images):
            n_images=n_max_images
        
        for image in range(n_images):
            image=[]
            for row in range(n_rows):
                row=[]
                for _ in range(n_cols):
                    pixel=f.read(1)
                    row.append(pixel)
                image.append(row)
            images.append(image)
    return images            


def read_labels(filename,n_max_labels=0):
    labels=[]
    with open(filename,"rb") as f:
        _=f.read(4) #ignore the magic number
        n_labels=toInt(f.read(4))
        
        if(n_max_labels>0 and n_max_labels<n_labels):
            n_labels=n_max_labels
        
        for label in range(n_labels):
            label=f.read(1)
            labels.append(label)
    return labels     


def flatten_list(l):
    return [pixel for sublist in l for pixel in sublist]



# Converting 2D list/image to 1D list
def extract_features(X):
    return [flatten_list(sample) for sample in X]

def toInt(x):
    if(type(x) is int):
        return x
    else:
        return int.from_bytes(x)

def black_or_white(x):
    int_a=toInt(x)
    if(int_a>127):
        int_a=255
    else:
        int_a=0
    return int_a
def extreme_dist(x1,x2):
    return sum([(black_or_white(a)-black_or_white(b))**2 for a,b in zip(x1,x2)])**0.5


# Getting distance between two samples
def dist(x1,x2):
    return sum([(toInt(a)-toInt(b))**2 for a,b in zip(x1,x2)])**0.5

def get_distances_for_test_sample(X_train,test_sample):
    return [dist(train_sample,test_sample) for train_sample in X_train]


def most_common_element(l):
    return max(set(l),key=l.count)


def knn(X_test,X_train=read_images(TRAINING_DATA_FILENAME,60000),Y_train=read_labels(TRAINING_LABELS_FILENAME,60000),K=15):
    
    Y_Predicted=[]

    X_train=extract_features(X_train)
    X_test=extract_features(X_test)
    
    for test_sample in X_test:
        distances=get_distances_for_test_sample(X_train,test_sample)
        sorted_distaces_indices=[pair[0] for pair in sorted(enumerate(distances),key=lambda x:x[1])]
        
        nearest_neighbours=sorted_distaces_indices[:K]
        Y_nearest_neighbours_bytes=[Y_train[i] for i in nearest_neighbours]
        Y_nearest_neighbours_int=[toInt(y) for y in Y_nearest_neighbours_bytes]
        neighbour_predicted=most_common_element(Y_nearest_neighbours_int)
        Y_Predicted.append(neighbour_predicted)
    return Y_Predicted
    

def print_results(Y_test,Y_predicted):
    map=zip(Y_test,Y_predicted)
    for i,(y_t,y_p) in enumerate(map):
        print(f"Test Sample {i}: Actual:{toInt(y_t)} Predicted:{y_p}")

def accuracy(Y_test,Y_predicted):
    return sum([toInt(y_t)==y_p for y_t,y_p in zip(Y_test,Y_predicted)])/len(Y_test)


def main():
    
    n_train=1000
    n_test=100
    
    X_train=read_images(TRAINING_DATA_FILENAME,n_train)
    Y_train=read_labels(TRAINING_LABELS_FILENAME,n_train)
    
    X_test=read_images(TEST_DATA_FILENAME,n_test)
    Y_test=read_labels(TEST_LABELS_FILENAME,n_test)
    
    
    Y_predicted=knn(X_test,X_train,Y_train)
    
    
    print(accuracy(Y_test,Y_predicted))
    
    print(f'Tested for {len(Y_test)} samples')

if __name__ == '__main__':
    main()