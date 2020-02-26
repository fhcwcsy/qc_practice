# How to Use Python Script to Run Qiskit Instead of Jupyter Notebook

Hao-Chien Wang

In this file, I share some tips to avoid errors while running qiskit in a `*.py`
file. My environment is Ubuntu 19.10 running Anaconda, but I believe this can
be done on other OS as well. My scripts can be found in this [repo](https://github.com/fhcwcsy/quantum_computing_practice).
If you still encounter problems after following this,
feel free to tell me the error messages and I'll try to help.

1. Copy your API token from your [IBM-Q Experience account page](https://quantum-computing.ibm.com/account).

2. Run

```{python}
qiskit.IBMQ.save_account('your_token')
```
either in a interactive python shell or put it in the beginning of your code.
This only need to be done once. Your API token will be saved in your computer.

3. In your python script (`*.py` file), whenever you want to connect to the server,
you need to use `qikit.IBMQ.load_account()` before that.

### A few other things to be noticed

- In the textbook, commands that start with `%` are for jupyter notebooks. You
can simply ignore those commands. 

- Functions like `qk.visualization.plot_histogram()` or `qc.draw(output='mpl')`
returns PLT images. You can use `plt_images.show()` to show it (but the program
will pause) or use `plt_images.savefig('some/path/filename.svg')` to save it
locally (you can use other image extensions as well).

