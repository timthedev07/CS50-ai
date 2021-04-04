# Neural Networks

- Neurons are connected to and receive electrical signals from other neuton
- Neurons process input signals and can ba activated

### Artificial neural network
Mathematical model for learning inspired by biological neural networks
- Model mathematical function from inputs to outputs based on the structure and parameters of the network.
- Allows for learning the network's parameters based on data.
- The idea of neurons are represented as **nodes** in a graph, where they can connect to each other by an **edge**.

In this equation:

```python
h(x1, x2) = w0 + w1x1 + w2x2
```

The w0 can be considered to be multiplied by one, but it's also reasonable to call it a **bias**.

## Activation functions
An activation function that determines when it is that this output becomes active, changes to another classification.
 
- Step function - a binary classification which gives 0 before a certain threshold is reached and 1 after the threshold is reached. 

    `g(x) = 1 if x >= 0; else 0`

    <img src="assets/step.png" width="700" />

- Logistic function - where rather than giving a certain value(0 or 1), there is some probability, and the result might be a real number. 

    `g(x) = (e^x)/(e^x + 1)`

    <img src="assets/logistic.png" width="700" />

- Rectified linear unit(ReLU) - it works by taking the maximum between the input and 0. So if it's positive, it remains unchanged, but if it's negative, it goes ahead and levels out at 0.

    <img src="assets/relu.png" width="700" />

## **Neural Network Structure**
The idea of hypothesis functions can be represented as follows:
<img src="assets/nnstructure.png" width="700" />

The two nodes on the left are inputs, x1 and x2, and they are both connected to the output(node on the right), via the edge between the nodes, which in this case is defined as the weight. Finally a bias `w0` is going to be passed in to a activation function, which then gets a result.

For example, the picture below is the truth table for the OR operator:

<img src="assets/truthTable.png" width="100" />
They are connected to the output unit by an edge with a weight of 1. The output unit then uses function g(-1 + 1x₁ + 1x₂) with a threshold of 0 to output either 0 or 1 (false or true).

This can be represented using a neural network. x₁ and x₂ are the inputs, they are connected to the result node by an edge with a weight of 1(that means they are going to be multiplied by the weight, which is 1). The output node then uses adds a bias, which in this case is -1 to the activation function to calculate the final result.

Of course we could have more than two inputs there. We might have something like this:

<img src="assets/multiple.png" width="400"/>

Thus we get the formula for computing the output is:

<img src="assets/formula.png" width="300"/>


