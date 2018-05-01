#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 21:45:40 2018

@author: BallBlueMeercat
"""
from pylab import figure, plot, xlabel, ylabel, title, show
import matplotlib.pyplot as pl


import paramfinder

# Model parameteres:  
gamma_true = 0.0       # Interaction term, rate at which DE decays into matter.
m_true = 0.3           # (= e_m(t)/e_crit(t0) at t=t0).
de_true = 1 - m_true   # (de = e_de(t)/e_crit(t0) at t=t0).

# Number of datapoints to be simulated.
npoints = 1000

nsteps = 10000

# Statistical parameteres:
mu = 0          # mean
sigma = 0.1     # standard deviation

def repeatrun():
    i = 0
    while i < 1:
        print('_____________________ run number',i)
        gammabest, mbest, debest = paramfinder.paramfinder(npoints, nsteps, gamma_true, m_true, sigma, mu)
        i += 1
    
    return

#repeatrun()


def nevaluator():
    
    gamma = []
    m = []
    numpoints = []
    
    npoints = 0
    run = 0
    while npoints < 30000:
        print('_____________________ run number',run)
        npoints += 1000
        gammabest, mbest, debest = paramfinder.paramfinder(npoints, nsteps, gamma_true, m_true, sigma, mu)
        gamma.append(gammabest)
        m.append(mbest)
        numpoints.append(npoints)
        run += 1

    figure()
    xlabel('number of datapoints used')
    ylabel('parameter value')
    pl.axhline(gamma_true, color='blue')
    plot(numpoints, gamma, '.')
    title('gamma found vs dataset size')
    show()
    
    figure()
    xlabel('number of datapoints used')
    ylabel('parameter value')
    pl.axhline(m_true, color='red')
    plot(numpoints, m, '.')
    title('m found vs dataset size')
    show()
    
    return gamma, m, numpoints

#nevaluator()


def stepevaluator():
    
    gamma = []
    m = []
    steps = []
    
    nsteps = 0
    run = 0
    while nsteps < 100000:
        run += 1
        print('_____________________ run number',run)
        nsteps += 10000
        gammabest, mbest, debest = paramfinder.paramfinder(npoints, nsteps, gamma_true, m_true, sigma, mu)
        gamma.append(gammabest)
        m.append(mbest)
        steps.append(nsteps)
    
    figure()
    xlabel('emcee steps')
    ylabel('parameter value')
    pl.axhline(gamma_true, color='blue')
    plot(steps, gamma, '.')
    title('gamma found vs steps taken')
    show()
    
    figure()
    xlabel('emcee steps')
    ylabel('parameter value')
    pl.axhline(m_true, color='red')
    plot(steps, m, '.')
    title('m found vs steps taken')
    show()
    
    return gamma, m, steps

stepevaluator()


def errevaluator():
    
    gamma = []
    m = []
    error = []
    
    sigma = 0.005
    run = 0
    while sigma < 0.1:
        run += 1
        print('_____________________ run number',run)
        sigma += 0.003
        gammabest, mbest, debest = paramfinder.paramfinder(npoints, nsteps, gamma_true, m_true, sigma, mu)
        gamma.append(gammabest)
        m.append(mbest)
        error.append(sigma)
    
    figure()
    xlabel('sigma')
    ylabel('parameter value')
    pl.axhline(gamma_true, color='blue')
    plot(error, gamma, '.')
    title('gamma found vs s.d. of noise added')
    show()
    
    figure()
    xlabel('sigma')
    ylabel('parameter value')
    pl.axhline(m_true, color='red')
    plot(error, m, '.')
    title('m found vs s.d. of noise added')
    show()
    
    return gamma, m, error

#errevaluator()