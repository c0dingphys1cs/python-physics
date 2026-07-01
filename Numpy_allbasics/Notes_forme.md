```python
import numpy as np
import matplotlib.pyplot as plt
```

##arrays
#creates an array from a python list
```python
a1= np.array([2,4,6,8])
```
#creates an array of 5 zeros

```python
a2 = np.zeros(5)
```
#creates an array of 5 ones

```python
a3 = np.ones(5)
```
#creates 10 random floats from a standard normal (mean=0, std=1) distribution 
```python
a4 = np.random.randn(10)
```
#creates 10 random floats uniformly distribution between 0 and 1
```python
a5 = np.random.random(10)
```
#creates 50 evenly spaced values between 0 and 10 (inclusive)
```python
a6 = np.linspace(0,10,50)
```
#creates values from 0 to 10 (exclusive) with a step of 0.2

```python
a7= np.arange(0,10,0.1)
```

#Can we define a range in a4
#not directly- randn always draws from the standard normal distribution.
#in random we can shift and scale the output to get any distribution

```python
mean = 50
std = 10
a8 = mean + std*np.random.randn(10)
```

#if we want random numbers within a fixed min/max range
```python
a9 = np.random.uniform(5,15,10)
```

#only if we want to specify mean and std directly 
```python
a10 = np.random.normal(50,10,10)
```
_____
# array operations 
```python
a1*0.3
3*a1>10
1/a4 + a4
```

#very useful for plotting 
```python
plt.plot(a6, a6**2)
```
#to save and download graph make sure to save then show and then download it.
#plt.show()_ this will displays the graph and then closes it.

```python
plt.savefig("graph.jpg",dpi=300,bbox_inches="tight")
plt.show()


from google.colab import drive
files.download("graph.png")
```
```python
plt.hist(a8)
plt.show()
```
```python
def f(x):
    return x**2 * np.sin(x) / np.exp(x)
plt.plot(a7, f(a7))    

plt.savefig("graph.png",dpi=300,bbox_inches="tight")
plt.show()

```


