#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 13:52:36 2018

@author: BallBlueMeercat
"""

import numpy as np
from datasim import magn

def lnlike(theta, data, sigma, firstderivs_key, names):
    '''
    Takes in:
        theta = numpy.ndarray, guessed values for parameters;
        data = dictionary, {'mag':mag, 'zpicks':zpicks};
        sigma = int/float, error on data;
        firstderivs_key = string, model being tested;
        params = list of dictionaries {string:value} of names and
        current guessed values of parameters being emcee fitted:
            [{'matter':float} = e_m(t)/ec(t0) at t=t0;
            {'Mcorr':float} = corrected absolute mag M;
            {'gamma':float} = interaction term;
            {'zeta':float} = interaction term;
            ... {'parameter':value})].
    Returns:
        float, likelihood for firstderivs_key model with theta parameters.
    '''
    mag = data['mag']
    model = magn(names, theta, data, firstderivs_key) # mag, but with theta params
    var = sigma**2
    likelihood = -0.5*np.sum((mag-model)**2 /var +0.5*np.log(2*np.pi*var))
    return likelihood

def lnprior(th, key):
    '''
    Takes in:
        th = numpy.ndarray, guessed values for parameters;

    Returns:
        0.0 if all conditions on theta values are met;
        -np.inf if theta values are outside of prior.
    '''
    Mcorr_min, Mcorr_max = -20, -18


    if Mcorr_min < th[0] < Mcorr_max:
        if (0 < th[1] < 1 or th[1] == 1): # matter

            if key == 'waterfall':
                # radiation, a_ombar, b_ombar, c_ombar
                if 0 < th[2] < 1 and 0 < th[3] < 1:
                    if 0 < th[4] < 1 and 0 < th[5] < 1:
                        l = 1
                        # v_in, w_in, x_in, y_in, z_in
                        if abs(th[6]) < l and abs(th[7]) < l and abs(th[8]) < l:
                            if abs(th[9]) < l and abs(th[10]) < l:
                                return 0.0

            elif key == 'exotic':
                # radiation
                if 0 < th[2] < 1:
                    # gamma, zeta
                    if -2 < th[3] < 0.1 and -1.5 < abs(th[4]) < 3.5:
                        return 0.0

            elif key == 'late_intxde':
                if -2 < th[2] < 0.1: # interaction terms
                    return 0.0

            elif key == 'heaviside_late_int':
                if -1.45 < th[2] < 0.1: # interaction terms
                    return 0.0

            elif key == 'late_int':
                if -15 < th[2] < 0.1: # interaction terms
                    return 0.0

            elif key == 'expgamma':
                if -0.1 < th[2] < 1.5: # interaction terms
                    return 0.0

            elif key == 'txgamma':
                if -0.5 < th[2] < 0.1: # interaction terms
                    return 0.0

            elif key == 'zxgamma':
                if -10 < th[2] < 0.1: # interaction terms
                    return 0.0

            elif key == 'zxxgamma':
                if -0.1 < th[2] < 12: # interaction terms
                    return 0.0

            elif key == 'gammaxxz':
                if -1 < th[2] < 1: # interaction terms
                    return 0.0

            elif key == 'rdecay':
                if -2 < th[2] < 0.1: # interaction terms
                    return 0.0

            elif key == 'interacting':
                if -1.5 < th[2] < 0.1: # interaction terms
                    return 0.0

            elif key == 'LCDM':
                return 0.0

            else:
                if abs(th[4]) < 10: # interaction terms
                    return 0.0

    return -np.inf

def lnprob(theta, data, sigma, firstderivs_key, names):

    lp = lnprior(theta, firstderivs_key)
    if not np.isfinite(lp):
        return -np.inf

    return lp + lnlike(theta, data, sigma, firstderivs_key, names)