#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 16:02:10 2018

@author: BallBlueMeercat
"""

from pylab import figure, scatter
import corner
import emcee
import matplotlib.pyplot as pl
import scipy.optimize as op
import numpy as np
import time

import timer
import msim
#import lnlike
import lnprob

# emcee parameters:
ndim, nwalkers = 3, 200
nsteps = 100000
burnin = 30000

def stats(gamma_true, m_true, de_true, zpicks, mag, noise, sigma):
    """
    Takes in:
            gamma_true = interaction constant;
            m_true = e_m(t)/ec(t0) at t=t0;
            de_true = e_de(t)/ec(t0) at t=t0;
            zpicks = list of z to match the interpolated dlmpc to;
            mag = list of n apparent magnitudes mag for zpicks redshits;
            noise = np.ndarray of unique Gaussian noise values for mag;
            sigma = standard deviation used to generate Gaussian noise.
    Returns:
    """
#    print('-stats has been called')
    # Finding a "good" place to start using alternative method to emcee.

#    print('gamma_true',gamma_true)
#    print('m_true',m_true)
#    print('de_true',de_true)
    
    print('Finding a "good" place to start')
    nll = lambda *args: -lnprob.lnprob(*args)  # type of nll is: <class 'function'>
    result = op.minimize(nll, [gamma_true, m_true, de_true],
                         args=(zpicks, mag, noise))
    gamma_ml, m_ml, de_ml = result["x"]
    print('%s, %s, %s = result["X"]'%(gamma_ml,m_ml,de_ml))
        
    # Initializing walkers in a Gaussian ball around the max likelihood.
    # Number in front of the np.random.rand(ndim) is stepsize
    pos = [result["x"] + 1*np.random.randn(ndim) for i in range(nwalkers)]    
    print('pos = ',pos)    
    
    # Sampler setup
    timee0 = time.time()    # starting emcee timer
    print('_____ sampler start')
    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob.lnprob, args=(zpicks, mag, noise))
    sampler.run_mcmc(pos, nsteps)
    print('_____ sampler end')
    timee1=time.time()      # stopping emcee timer
    
    print('_____ stats corner plot')
    
    # Corner plot (walkers' walk + histogram).
    samples = sampler.chain[:, burnin:, :].reshape((-1, ndim))
    fig = corner.corner(samples, labels=["$\gamma$", "$m$", "$de$"], 
                        truths=[gamma_true, m_true, de_true])
    pl.show()
    fig.savefig('zz_nsteps'+str(nsteps)+str(time.strftime("%c"))+
                'nwalkers'+str(nwalkers)+'.png')
    
    # Marginalised distribution (histogram) plot.
    pl.hist(sampler.flatchain[:,0], 100)
    pl.show()
    
    # Chains.    
    figure()
    pl.title('flatChains with gamma_true in blue')
    pl.plot(sampler.flatchain[:,0].T, '-', color='k', alpha=0.3)
    pl.axhline(gamma_true, color='blue')
    pl.show

    figure()
    pl.title('flatChains with m_true in red')
    pl.plot(sampler.flatchain[:,1].T, '-', color='k', alpha=0.3)
    pl.axhline(m_true, color='red')
    pl.show
    
    figure()
    pl.title('flatChains with de_true in green')
    pl.plot(sampler.flatchain[:,2].T, '-', color='k', alpha=0.3)
    pl.axhline(de_true, color='green')
    pl.show
    
#    fig, axes = pl.subplots(3, figsize=(10, 7), sharex=True)
#    samples = sampler.get_chain()
#    labels = ['gamma', 'm', 'de']
#    for i in range(ndim):
#        ax = axes[i]
#        ax.plot(samples[:, :, i], "k", alpha=0.3)
#        ax.set_xlim(0, len(samples))
#        ax.set_ylabel(labels[i])
#        ax.yaxis.set_label_coords(-0.1, 0.5)
#
#    axes[-1].set_xlabel("step number");
    
    slnprob = sampler.flatlnprobability
    gamma = sampler.flatchain[:,0]
    m = sampler.flatchain[:,1]
    de = sampler.flatchain[:,2]

    print('_____ magbest calculation')
    # Simulating magnitude using best parameters found by emcee.
    bi = np.argmax(sampler.flatlnprobability)   # index with highest post prob                                       
    gammabest = sampler.flatchain[bi,0]         # parameters with the highest 
    mbest = sampler.flatchain[bi,1]             # posterior probability
    debest = sampler.flatchain[bi,2]
    

    # Results getting printed:
    print('best index is =',str(bi))
    print('gammabest is =',str(gammabest))
    print('mbest is =',str(mbest))
    print('debest is =',str(debest))
  
    # Mean acceptance fraction. In general, acceptance fraction has an entry 
    # for each walker so, in this case, it is a 50-dimensional vector.
    print('Mean acceptance fraction:', np.mean(sampler.acceptance_fraction))
    print('Number of steps:', str(nsteps))
    print('Number of walkers:', str(nwalkers))
    
    if not (-0.1 < gammabest < 0.1 and 0.299 < mbest < 0.301 and 0.699 < debest < 0.701):
        print('')
        print('parameters are outside of prior when they get to magbest')
        print('')
    # Plot of mag simulted using best emcee parameters.
    magbest = msim.msim(gammabest, mbest, debest, zpicks)

    twosigma = sigma * 2    # errorbars
    
    # Plot of magnitudes simulated using "true" parameters, overlayed with
    # magnitudes simulated using emcee best parameters.
    figure()
    pl.title('True parameters mag and best emcee parameters mag')
    pl.errorbar(zpicks, mag, yerr=twosigma, fmt='o', alpha=0.3)
    best_fit = scatter(zpicks, magbest, lw='3', c='r')
    pl.legend([best_fit], ['Mag simulated with best emcee parameters'])
    pl.show()
    
    timer.timer('sampler', timee0, timee1)

    return gamma, m, de, slnprob
#except Exception as e:
#        logging.error('Caught exception:',str(e))
#        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))