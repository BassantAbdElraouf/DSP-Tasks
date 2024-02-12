def ConvTest(Your_indices,Your_samples): 
    """
    Test inputs
    InputIndicesSignal1 =[-2, -1, 0, 1]
    InputSamplesSignal1 = [1, 2, 1, 1 ]
    
    InputIndicesSignal2=[0, 1, 2, 3, 4, 5 ]
    InputSamplesSignal2 = [ 1, -1, 0, 0, 1, 1 ]
    """
    
    expected_indices=[-2, -1, 0, 1, 2, 3, 4, 5, 6]
    expected_samples = [1, 1, -1, 0, 0, 3, 3, 2, 1 ]
    #print(type(expected_indices))
    #print(type(expected_samples))
    
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Conv Test case failed, your signal have different length from the expected one")
        #print("len(expected_samples)",len(expected_samples))
        #print("len(Your_samples)", len(Your_samples))
        #print("len(expected_indices)", len(expected_indices))
        #print("len(Your_indices)", len(Your_indices))
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Conv Test case failed, your signal have different indicies from the expected one")
            print("Your_indices", Your_indices)
            print("expected_indices", expected_indices)
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Conv Test case failed, your signal have different values from the expected one") 
            return
    print("Conv Test case passed successfully")