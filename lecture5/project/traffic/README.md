# My experience constructing the neural network for this assignment - Tim

My solution is clearly not optimal, but I got a sense of what's bad practice and what not to do during my experimentation. I tried many other values for the number of nodes in the hidden layer, but 128 is by far the best one I have tested out.

In conclusion, values that are either too large or too small would not be ideal, in addition, if there are too many hidden layers regardless of their number of nodes or activation functions, the accuracy is going to decrease.

Result of running the code above:
$ python traffic.py gtsrb
```
Finish loading data
2021-04-07 08:07:05.945509: I tensorflow/compiler/mlir/mlir_graph_optimization_pass.cc:176] None of the MLIR Optimization Passes are enabled (registered 2)
Epoch 1/10
500/500 [==============================] - 11s 20ms/step - loss: 5.1483 - accuracy: 0.1711 
Epoch 2/10
500/500 [==============================] - 10s 20ms/step - loss: 1.5350 - accuracy: 0.5378
Epoch 3/10
500/500 [==============================] - 10s 20ms/step - loss: 0.9598 - accuracy: 0.7042
Epoch 4/10
500/500 [==============================] - 10s 19ms/step - loss: 0.7082 - accuracy: 0.7887
Epoch 5/10
500/500 [==============================] - 10s 19ms/step - loss: 0.5257 - accuracy: 0.8473
Epoch 6/10
500/500 [==============================] - 10s 19ms/step - loss: 0.5213 - accuracy: 0.8527
Epoch 7/10
500/500 [==============================] - 10s 19ms/step - loss: 0.4686 - accuracy: 0.8675
Epoch 8/10
500/500 [==============================] - 10s 19ms/step - loss: 0.3459 - accuracy: 0.9009
Epoch 9/10
500/500 [==============================] - 10s 19ms/step - loss: 0.3381 - accuracy: 0.9064
Epoch 10/10
500/500 [==============================] - 10s 19ms/step - loss: 0.3024 - accuracy: 0.9150
333/333 - 2s - loss: 0.1607 - accuracy: 0.9570
```