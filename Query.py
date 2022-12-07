import time
# from plyer import accelerometer
import numpy as np
def data_query():
    x,y,z=[],[],[]
    while len(x)!=13:
        temp=get_acceleration()
        x.append(temp[0])
        y.append(temp[1])
        z.append(temp[2])
        time.sleep(0.05)

    data_list=[np.array(x),np.array(y),np.array(z)]
    data=np.transpose(data_list, (1, 2, 0))
    return data

def get_acceleration():
    val = accelerometer.acceleration[:3]
    return val

def pred(data_test,model):
    model.allocate_tensors()

    # Get input and output tensors.
    input_details = model.get_input_details()
    output_details = model.get_output_details()

    model.set_tensor(input_details[0]['index'], np.expand_dims(data_test[0], axis=0))

    model.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    output_data = model.get_tensor(output_details[0]['index'])
    print(output_data)
    arg = np.argmax(output_data)
    if arg == 0:
        MP='Running'
    if arg == 1:
        MP = 'Sitting'
    if arg == 2:
        MP = 'Walking'
    return MP

def pred2(data_test,model):
    #When Importing the tensorflow package

    output_data=model.predict(data_test)

    arg = np.argmax(output_data)
    if arg == 0:
        MP='Sitting'
    if arg == 1:
        MP = 'Walking'
    if arg == 2:
        MP = 'Running'
    return MP