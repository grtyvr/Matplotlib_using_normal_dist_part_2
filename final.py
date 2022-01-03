import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

import numpy as np
from scipy.stats import norm

# Create an array of points to use as the x-coordinates for plotting the normal distribution
x_min = norm.ppf(0.00005) # we will plot 99.99 % of the normal curve.
x_max = norm.ppf(0.99995)
x = np.linspace(x_min, x_max, 201)

plt.style.use('seaborn-whitegrid')

# paramaters for the normal distribution
mu = 2
sigma = 3

# how to translate between different scales on the x-axis'
def toZscore(x):
    return ((x - mu) / sigma)

def fromZscore(x):
    return ((sigma * x) + mu)

# get a reference to a frozen version of the normal function with the loc and scale paramaters set.
n = norm(loc=mu, scale=sigma)

# Rebuild the array of points to use as the x-coordinates for plotting the normal distribution
x_min = n.ppf(0.000005) # we will plot 99.999 % of the normal curve.
x_max = n.ppf(0.999995)
x = np.linspace(x_min, x_max, 201)

# create a figure and an axes
fig, ax = plt.subplots()
fig.set_figheight(6)
fig.set_figwidth(8)

# Create an Axes object that shares an x axis with the ax Axes that we just created above.
ax2 = ax.twinx()

# format that axis as a percentage.
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

# the second curve we want to plot, the CDF.
ax2.plot(x,
         n.cdf(x),
         label='Cumulative Distribution\n Function norm.cdf(x, loc={}, scale={})'.format(mu, sigma),
         lw=2,
         color='green'
        )

# plot our normal function.
ax.plot(x,
        n.pdf(x),
        label='Normal Distribution\n norm.pdf(x, loc={}, scale={})'.format(mu, sigma)
       )

# add our points of interest
ax.plot(fromZscore(-1.96),
        n.pdf(fromZscore(-1.96)),
        color='red',
        marker='o',
        alpha=0.5
       )
ax.plot(fromZscore(1.96),
        n.pdf(fromZscore(1.96)),
        color='red',
        marker='o',
        alpha=0.5
       )
# add vertical lines
ax.vlines(x=[fromZscore(-1.96), fromZscore(1.96)],
          ymin=[0, 0],
          ymax=[n.pdf(fromZscore(-1.96)), n.pdf(fromZscore(1.96))],
          color='red',
          alpha=0.5
         )

# add axis labels, title and legend
ax.set_xlabel('X')
ax.set_ylabel('Probability')
ax.set_title('The Normal (Gaussian) Distribution')

# customize our legend
fig.legend(
    fontsize='small',
    loc='upper left',
    framealpha=0.5,
    bbox_to_anchor=(0.15, 0.85) # note that here the coordinates are relative the the whole figure
)

# add some text.  By default the xy are in the axes coordinates
# but that can be changed with transformations
ax.text(-3.3*sigma, 
        n.pdf(fromZscore(-1.96)),
        '$(-1.96\sigma, {0:.2})$'.format(n.pdf(fromZscore(-1.96)))
       )
ax.text(2.1 * sigma + mu,
        n.pdf(1.96*sigma + mu),
        '$(1.96\sigma, {0:.2})$'.format(n.pdf(fromZscore(1.96)))
       )

# add fill below the normal curve
# create an array of x-values to plot against
x2=np.linspace(x_min, n.ppf(0.025))
ax.fill_between(x2, n.pdf(x2), alpha=0.75, facecolor='lightblue')

# add annotation.  By default the xy are in the axes coordinates
# but that can be changed with transformations
text_string ='This area is equal to\nthe value of the CDF at\n'
text_string += 'the right boundary.\nIn this case the right\nboundary is at $-1.96\sigma$\n'
text_string += 'where $\sigma$ = {} and the\n area is $2.50\%$ of the\n area under the curve.'.format(sigma)
ax.annotate(
    text_string,
    xy=(-2.1*sigma + mu, n.pdf(fromZscore(-1.96))/3),
    xytext=(2*sigma + mu,0.05),
    arrowprops=dict(arrowstyle='->'))

# add a horizontal line from the CDF to the right axis and a point at the intersection
ax2.hlines(y=n.cdf(fromZscore(-1.96)),
           xmin=-1.96*sigma + mu,
           xmax=x_max,
           color='green',
           alpha=0.5
          )
# add our dot
ax2.plot(fromZscore(-1.96), n.cdf(fromZscore(-1.96)), marker='o', color='green', alpha=0.4)

# add text to highlight the value of the CDF at -0.96
ax2.text(x_max,0.04, '$2.5\%$'.format(n.cdf(fromZscore(-1.96))))

# adjust the transparency and color of the grids for each axex object
ax.grid(visible=True, color='blue', alpha=.2)
ax2.grid(visible=True, color='green', alpha=0.2)

# add a vertical dashed line at the mean, -sigma and sigma.
ax.vlines(x=mu, ymin=0, ymax=n.pdf(mu), linestyle='dotted')
ax.vlines(x=[mu-sigma, mu+sigma], ymin=0, ymax=n.pdf(mu+sigma), linestyle='dotted')
ax.text(mu+0.02, 
        n.pdf(mu)/12,
        '$\mu$ = {}'.format(mu)
       )
ax.text(mu+sigma+0.02, 
        n.pdf(mu)/12,
        '$\mu + \sigma$'
       )
ax.text(mu-sigma+0.02, 
        n.pdf(mu)/12,
        '$\mu - \sigma$'
       )

# add an additional x-axis
# shift the original axes object up
fig.subplots_adjust(bottom=0.2)
ax3 = ax.secondary_xaxis(-0.08, functions=(toZscore, fromZscore))
ax3.set_xlabel('Standard Deviations')
ax3.xaxis.set_label_coords(-.11,-0.1)
ax3.set_xticks([x for x in range(-4,6)], minor=True)
ax3.tick_params(length = 10, which='major', direction='in')
ax3.tick_params(length= 10, which='minor', direction='inout')
# add tics to our primary x axis
ax.tick_params(length = 10, which='major', direction='in')
ax.tick_params(length= 5, which='minor', direction='inout')
ax.set_xticks([x for x in range(-10,16)], minor=True)

# move our initial x-axis label off the the left.
ax.xaxis.set_label_coords(-0.02, -0.025)


#plt.show()
plt.savefig('figure_3.png', bbox_inches='tight')
