# -- coding: utf-8 --
import numpy as np;
import matplotlib.pyplot as plot;
from scipy.stats import norm;
from scipy.stats import multivariate_normal
import math 

def task1(mu1, sigma1, mu2, sigma2):
    fig, ax = plot.subplots(1);
    x = np.linspace(-10, 15, 100);
    
    var1 = math.sqrt(sigma1)
    var2 = math.sqrt(sigma2)

    pdf_res_f1 = norm.pdf(x, mu1, var1);
    pdf_res_f2 = norm.pdf(x, mu2, var2);
    ax.plot(x, pdf_res_f1,lw=3, alpha=1.0);
    ax.plot(x, pdf_res_f2,lw=3, alpha=1.0);
    
 
task1(0, 1.5, 3, 4) # a)   
task1(-4, 2, 3, 1.5) # b)
task1(2, 2, 2, 1) # c)

def task1secPart(MM1, SM1, MM2, SM2):
    
    bx = plot.axes(projection = '3d')
    
    xLine = np.linspace(-10,10,100);
    yLine = np.linspace(-10,10,100);
    
    x,y = np.meshgrid(xLine,yLine);
    pos = np.empty(x.shape + (2,))
    pos[:, :, 0] = x
    pos[:, :, 1] = y
    xarray = []
    for i in range(len(MM1)):
        xarray.append(multivariate_normal(SM1[i], MM1[i]));

    for i in range(len(xarray)):
        bx.plot_surface(x, y, xarray[i].pdf(pos) ,rstride=1, cstride=1, cmap='plasma')

    
task1secPart([3,2], [[1.5,0], [0,1.5]], [8,5], [[3,0],[0,3]]) #d)
task1secPart([3,2], [[1,0], [0,3]], [8,5], [[2,0],[0,1]]) #e)
task1secPart([3,2], [[1,0.6],[0.6, 3]], [8,5], [[2,-0.6], [-0.6, 1]]) #f)

def task2(sigma): 
    
    cx = plot.subplots(1, 1);
    mu = [0,0];
    
    s = np.random.multivariate_normal(mu, sigma, 600);
    s = np.transpose(s);

    cx[1].scatter(s[0], s[1], 2);
    plot.xlim(-10,10)
    plot.ylim(-10,10)
    
    
task2([[2,0], [0,2]])
task2([[0.1,0], [0,0.1]])
task2([[1, -0.7], [-0.7, 2.5]])
task2([[0.2, 0], [0,2]])
task2([[2,0], [0,0.2]])
task2([[2.5, 0.7], [0.7, 1]])
    
def g2d(x,sigma,ni,w):
    res =-0.5* np.matmul(np.transpose(x-ni),np.matmul(np.linalg.inv(sigma),x-ni));
    res = res - 0.5 * np.log(np.linalg.det(sigma)) + np.log(w);
    return res;
    
def classify2d (x,ni1, sigma1,w1,ni2,sigma2,w2):
    if(g2d(x,sigma1,ni1,w1)>g2d(x,sigma2,ni2,w2)):
        return 1;
    else:
        return 2;
    
def zad3gen(ni, sigma, ni1, sigma1,row,probs):

    fig, ax = plot.subplots(1, 1);

    s = np.random.multivariate_normal(ni, sigma, 300);
    s1 = np.random.multivariate_normal(ni1, sigma1, 300);
    s = np.transpose(s);
    s1 = np.transpose(s1);
    ax.scatter(s[0],s[1],2,'red');
    ax.scatter(s1[0],s1[1],2);
    s = np.transpose(s);
    s1 = np.transpose(s1);

    i=0;
    for prob in probs:
        fig, ax = plot.subplots(1, 1);

        firstclass =[];
        secondclass =[];
        error1=0;
        error2=0;
        for i in range (0,len(s)):
            if(classify2d(s[i],ni,sigma,prob, ni1,sigma1,1-prob) == 1):
                firstclass.append(s[i]);
            else:
                secondclass.append(s[i]);
                error1+= 1;
        for i in range (0,len(s)):
            if(classify2d(s1[i],ni,sigma,prob, ni1,sigma1,1-prob) == 1):
                firstclass.append(s1[i]);
                error2+=1; 
            else:
                secondclass.append(s1[i]);


        firstclass = np.transpose(firstclass);
        secondclass = np.transpose(secondclass);
        ax.scatter(firstclass[0],firstclass[1],2,'red');
        ax.scatter(secondclass[0],secondclass[1],2);
        print (error1, error2,prob);
        

ni1 = [3,2];
ni2 = [8,5];
probs = [1/2,1/3,1/4,1/5,2/3,3/4,4/5];
sigma1s =[ [[1.5,0],[0,1.5]],[[1,0],[3,2]],[[1,0.6],[0.6,3]]];
sigma2s = [[[3,0],[0,3]],[[2,0],[0,1]],[[2,-0.6],[-0.6,1]]];
row = 0;
for row in range(0,3):
    sigma1= sigma1s[row];
    sigma2 = sigma2s[row];
    prob=0.5;
    zad3gen(ni1, sigma1 , ni2 , sigma2,row,probs);
   
    
#s = np.random.normal(2, 5, 100);   
#print(s);
    
    
    
    
    
    
    
    
    