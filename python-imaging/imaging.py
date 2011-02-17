# Image generation via Python Image Library
# -----------------------------------------
# Let's say we want to plot the Bank of England's historical interest rates
# as a graph.

# Load the [Bank of England historical interest rates
# ](https://spreadsheets.google.com/ccc?key=0AonYZs4MzlZbcGhOdG0zTG1EWkVQTjBYWm9pWHVRWkE)
import urllib
url = 'https://spreadsheets.google.com/pub?\
key=0AonYZs4MzlZbcGhOdG0zTG1EWkVQTjBYWm9pWHVRWkE&\
output=csv&\
range=B2:B3798'
data = urllib.urlopen(url).read()
data = [float(x) for x in data.split('\n')]

# Load the Python Image Library
import Image

# Configure the output path
import os.path
outpath = '../../talk-docs/python-imaging'

# Create a new RGB image of width 316 px (for 316 years of data)
# with color #E0E0E0
img = Image.new('RGB', (316, 220), (224, 224, 224))

# Save the image as a PNG. The extension determines the file type.
img.save(os.path.join(outpath, 'image-0.png'))

# Here's the result:
#
# ![Result](image-0.png)

# Now let' draw axes.

# Import the ImageDraw library that lets us draw on images
import ImageDraw
draw = ImageDraw.Draw(img)

# Draw a line every 50 pixels. We'll use y = 0 - 200 to plot 0 - 20% rates.
#
# draw.line takes ((x1,y1), (x2,y2)) as a parameter. By default, it draws
# a white line.
draw.line( ((0, 50), (img.size[0],  50)) )
draw.line( ((0,100), (img.size[0], 100)) )
draw.line( ((0,150), (img.size[0], 150)) )
draw.line( ((0,200), (img.size[0], 200)) )
img.save(os.path.join(outpath, 'image-1.png'))

# Here's the result:
#
# ![Result](image-1.png)

# Now let's draw the actual graph.
# draw.line takes a fill= parameter where you can specify the colour.
for (i, rate) in enumerate(data[::12]):
    draw.line(((i, 200), (i, 200-rate*10)), fill=(108,108,108))
img.save(os.path.join(outpath, 'image-2.png'))

# Here's the result:
#
# ![Result](image-2.png)

# Now we'll text labels for the years
import ImageFont
font = ImageFont.truetype("C:/SYSROOT/Fonts/arial.ttf", 10)
for (i, rate) in enumerate(data[::12]):
    year = 1694 + i
    if not year % 50:
        draw.text((i - 12, 200), str(year), font=font, fill=(0,0,0))
img.save(os.path.join(outpath, 'image-3.png'))

# ![Result](image-3.png)

# Image processing via Python Image Library
# -----------------------------------------
# PIL lets you manipulate the images as well. This is best shown via demos.
img = Image.open('sample.jpg')
img.save(os.path.join(outpath, 'sample.png'))
# ![Result](sample.png)

# Resize it
img = img.resize((200,150))
img.save(os.path.join(outpath, 'small.png'))
# ![Result](small.png)

# Brighten and saturate the image
import ImageEnhance
ImageEnhance.Brightness(img).enhance(2.0).save(os.path.join(outpath, 'bright.png'))
ImageEnhance.Color(img).enhance(2.0).save(os.path.join(outpath, 'color.png'))
# ![Result](bright.png)
# ![Result](color.png)

# For more samples, see
# [ngimage](http://ngimage.co.uk/dynamic/doc?image=spin-01.png&size)

# Emboss it, or trace contours
import ImageFilter
img.filter(ImageFilter.EMBOSS).save(os.path.join(outpath, 'emboss.png'))
img.filter(ImageFilter.CONTOUR).save(os.path.join(outpath, 'contour.png'))
# ![Result](emboss.png)
# ![Result](contour.png)


# Image generation via SVG
# ------------------------
# Another option is to use SVG to render the file.
# This makes it look better on print.
#
# Some sample reports created this way are at
# [Report Bee](http://blog.reportbee.com/visualising-student-performance) and
# [KLP](blog.klp.org.in/2011/01/visualizing-student-performance.html).

# We'll use tornado templates to render the file
from tornado import template

# Create a basic template that'll draw a grey box
svg = '''<svg width="316" height="220" xmlns="http://www.w3.org/2000/svg">
<rect x="0" y="0" width="316" height="220" style="fill:#e0e0e0"/>'''

# Add the axes
svg += '''
<line x1="0" x2="316" y1="50" y2="50" stroke-width="1" stroke="#fff"/>
<line x1="0" x2="316" y1="100" y2="100" stroke-width="1" stroke="#fff"/>
<line x1="0" x2="316" y1="150" y2="150" stroke-width="1" stroke="#fff"/>
<line x1="0" x2="316" y1="200" y2="200" stroke-width="1" stroke="#fff"/>'''

# Add the graph
svg += '''
{% for (i, rate) in enumerate(data[::12]) %}
 <rect x="{{ i }}" width="1" y="{{ 200 - rate*10 }}" height="{{ rate*10 }}"
  fill="#6c6c6c" stroke-width="0.1" stroke="#fff" />
{% end %}'''

# Add the labels
svg += '''
<g style="font-family:Arial;font-size:10px">
{% for (i, rate) in enumerate(data[::12]) %}
  {% set year = 1694 + i %}
  {% if not year % 50 %}
    <text x="{{ i-12 }}" y="200" style="dominant-baseline:hanging">
      {{ year }}
    </text>
  {% end %}
{% end %}
</g></svg>'''

# Generate the template and write the data
open(os.path.join(outpath, 'graph.svg'), 'w').write(template.Template(svg).generate(data=data))

# Here's the result:
#
# <embed src="graph.svg" width="316" height="220"></embed>
