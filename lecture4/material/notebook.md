# Learning

## **Machine Learning**
Supervised learning -> given a data set of input-output pairs, learn a function to map inputs to outputs.

The tasks within supervised learning:
- Classification -> supervised learning task of learning a function mapping an input point to a discrete category. In other words, it categorizes the input into a category.
In the case of predicting the weather, we might for example have some historical data:

| Date      | Humidity  | Pressure | Rain  |
|:---------:|:---------:|:--------:|:-----:|
| January1  | 93%       | 999.7    | True  |
| January2  | 49%       | 1015.5   | False |
| January3  | 79%       | 1031.1   | False |
| January4  | 65%       | 984.9    | True  |
| January5  | 90%       | 975.2    | True  |

For example, based on the table above, we could infer:
```py
f(humidity, pressure) = Rain/No Rain

# and if we pass in a few data points form the table above
f(93, 999.7) == Rain
f(49, 1015.5) == No Rain
f(79, 1031.1) == No Rain
```
function f outputs a category based on the inputs

Then, we have a hypothesis function `h`, which takes the same parameters, but it instead estimates what function `f` does
```python
h(humidity, pressure)
```

## **Nearest-Neighbor classification**
- Judging the category of an input based on the nearest data point to it.

For example:

<img src="assets/nearestNeighbor.png" width="600"/>

- If we are to judge the category of the white data point, based on the `nearest-neighbor classification` algorithm, it would be classified as blue.

- However, things get trickier when:

<img src="assets/NN Problem.png" width="600"/>

- If we apply the nearest neighbor algorithm, the white data point would be classified as red, but, if we look at the bigger picture, it would seem that the white dot sort of belongs to the blue side.

- This is when we should rather use **``k-nearest-neighbor classification``**, , which chooses the most common class out of k neighbors (`k` is the number of neighbors we want to look at)

## **Perceptron Learning**
- It works by trying to draw a separator, or a decision boundary between different types of observations.
- The new data point is going to be classified based on the decision boundary
- It uses a technique called **linear regression**

<img src="assets/decisionboundary.png" width="600" />

We need a hypotheses function to calculate and define the line:

```python
x₁ = Humidity
x₂ = Pressure


1 if w₀ + w₁x₁ + w₂x₂ ≥ 0 # where w is some weight 
0 otherwise
```

The weights and values are represented by vectors:
- Weight vector **w**: (w₀, w₁, w₂ ...)
- Input Vector **x**: (1, x₁, x₂ ...)

The vectors have the same length.

This calculation: ``w₀ + w₁x₁ + w₂x₂``, is the **dot product** of the two vectors `w` and `x`.

Programmatically:
```py
w · x = sum([w[i] * x[i] for i in range(len(x))])
```

It can also be represented as:
<code>
    h<sub>w</sub>(x) = 1 if w · x >= 0
                       else 0 
</code>

### Perceptron Learning Rule
Given data point (x, y), update each weight according to:

<code>
w<sub>i</sub> = w<sub>i</sub> + a(y - h<sub>w</sub>(x)) * x<sub>i</sub>
</code>

Which can be interpreted as:

<code>
w<sub>i</sub> = w<sub>i</sub> + a(actual value - estimate) * x<sub>i</sub>
</code>

- If we correctly predict the category of the data point, then this expression: <code>a(actual value - estimate)</code> is going to be zero. Thus the entire right hand side of the expression would be zero, so the value of <code>w<sub>i</sub></code> would not change. This is to adjust the weight such that our prediction gets closer and closer to the actual value, for example, if this expression: <code>a(actual value - estimate)</code> is a negative value, meaning our estimate is greater than the actual value, we will have to update the weight by this negative value(decreasing the weight), and vice versa with positive differences.

- In this equation, this value: <code>a()</code>, alpha, is the learning rate, it decides how much the algorithm is going to update the weight.

- The result of this process is a threshold function that switches from 0 to 1 once the estimated value crosses some threshold, and such threshold is called **hard threshold**

<img src="assets/hardthreshold.png" width="600" />

- One way to go around this is use **logistic regression**(previously we were using linear regression), which gives us the ability to classify data points using what's called a **soft threshold**

<img src="assets/softthreshold.png" width="600" />

In this case, we are not getting only 0 and 1 anymore, but instead we get the a real number(a nonlossy version of floating point numbers, infinite precision) representing the probability of some event.

## Support Vector Machines

- The basic idea is that there are actually a lot of lines we can draw to separate the observations, for instance:

<img src="assets/supportvector.png" width="700" />

- However, the first two boundaries are problematic although they successfully separate the two groups of observations. Say, we are to analyze a new data point on the second picture for example, if that it is somewhere near the decision boundary but on the blue side, the result would be in accurate sicne the blue area covers so much more space than the red area.

- Support Vector Machines are designed to try to find the **maximum margin separator**, a boundary that maximizes the distance between any of the data points. This also works in higher dimensions, where instead of looking for a line of decision boundary, it finds the **hyperplane** that separates one set of data from another. This becomes handy when the decision boundary we are looking for is non-linear, something like:

<img src="assets/circleboundary.png" width="700" />

## **Regression**
- Regression is a supervised learning task of learning a function mapping an input point to a continuous value.

For example we might have a set of data as follows:

| advertising | sales |
| ----------- | ----- |
| 1200        | 5800  |
| 2800        | 13400 |
| 1800        | 8400  |

and the goal is to learn a function a function