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

import msim
import lnlike
import lnprob

# emcee parameters:
ndim, nwalkers = 3, 6
nsteps = 1000
burnin = 200

def stats(gamma_true, m_true, de_true, n, zpicks, mag, noise, sigma):
    """
    Takes in:
            gamma_true = interaction constant;
            m_true = e_m(t)/ec(t0) at t=t0;
            de_true = e_de(t)/ec(t0) at t=t0;
            n = dimensionless number of data points to be generated;
            zpicks = list of z to match the interpolated dlmpc to;
            mag = list of n apparent magnitudes mag for zpicks redshits;
            noise = ;
            sigma = sigma.
    Returns:
    """
#    print('-stats has been called')
    # Finding a "good" place to start using alternative method to emcee.
    nll = lambda *args: -lnlike.lnlike(*args)  # type of nll is: <class 'function'>
    result = op.minimize(nll, [gamma_true, m_true, de_true],
                         args=(n, zpicks, mag, noise))
    gamma_ml, m_ml, de_ml = result["x"]    
    
    # Initializing walkers in a Gaussian ball around the max likelihood. 
    pos = [result["x"] + 1*np.random.randn(ndim) for i in range(nwalkers)]    
        
    
    # Sampler setup
    times0 = time.time()    # starting emcee timer
    
    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob.lnprob, args=(n, zpicks, mag, sigma))
    sampler.run_mcmc(pos, nsteps)
    
    times1=time.time()      # stopping emcee timer
    times=times1 - times0   # time to run emcee
    timesmin = round((times / 60),1)    # minutes
    timessec = round((times % 60),1)    # seconds
    
    
    # Corner plot (walkers' walk + histogram).
    samples = sampler.chain[:, burnin:, :].reshape((-1, ndim))
    fig = corner.corner(samples, labels=["$\gamma$", "$m$", "$de$"], 
                        truths=[gamma_true, m_true, de_true])
    fig.savefig('nsteps'+str(nsteps)+str(time.strftime("%c"))+
                'nwalkers'+str(nwalkers)+'.png')
    
    
    # Marginalised distribution (histogram) plot.
    pl.hist(sampler.flatchain[:,0], 100)
    pl.show()

    
    # Simulating magnitude using best parameters found by emcee.
    bi = np.argmax(sampler.lnprobability)   # index with highest post prob                                       
    gammabest = sampler.flatchain[bi,0]      # parameters with the highest 
    mbest = sampler.flatchain[bi,1]         # posterior probability
    debest = sampler.flatchain[bi,2]
    
    magbest = msim.msim(gammabest, mbest, debest, n, zpicks)

    twosigma = sigma * 2
    
    # Plot of magnitudes simulated using "true" parameters, overlayed with
    # magnitudes simulated using emcee best parameters.
    figure()
    pl.title('True parameters mag and best emcee parameters mag')
    pl.errorbar(zpicks, mag, yerr=twosigma, fmt='o', alpha=0.3)
    best_fit = scatter(zpicks, magbest, lw='3', c='r')
    pl.legend([best_fit], ['Mag simulated with best emcee parameters'])
    pl.show()
    
    
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
    print('Sampler time:',str(int(timesmin))+'min'
          ,str(int(timessec))+'s')
    
    return
#except Exception as e:
#        logging.error('Caught exception:',str(e))
#        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))