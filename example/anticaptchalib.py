import os
from PIL import Image


def get_images(directory):

    def images():
        for f in os.listdir(directory):
            yield Image.open(os.path.join(directory, f))

    return images()


def binarize(image, fn):

    new_image = Image.new('1', image.size)
    for xy in get_iterator(image):
        new_image.putpixel(xy, fn(image.getpixel(xy)))
    return new_image
    

def get_segments(image):
    image = image.copy()
    segments = []

    for xy in get_iterator(image):
        if image.getpixel(xy) == 0:
            new_segment = get_segment(image, xy)
            segments.append(new_segment)
    return segments


def get_pixel(image, xy):
    try:
        return image.getpixel(xy)
    except:
        return 1


def get_segment(image, xy, segment=None):
    x, y = xy
    
    if segment is None:
        segment = Image.new('1', image.size, 'white')

    image.putpixel(xy, 1)
    segment.putpixel(xy, 0)
        

    adjacent = [(x, y-1), (x+1, y-1), (x-1, y), 
    (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)]

    for a in adjacent:
        if get_pixel(image, a) == 0:
            get_segment(image, a, segment)

    return segment


def get_iterator(image):
    def iterator():
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                yield (x, y)
    
    return iterator()

def get_limits(image):
    min_x, min_y = image.size
    max_x, max_y = 0, 0
    
    for x, y in get_iterator(image):
        if image.getpixel((x, y)) == 0:
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
                    
    return (min_x, min_y, max_x+1, max_y+1)
    

def trim(image):
    cropped = image.crop(get_limits(image))
    cropped.load()
    return cropped


def get_weight(image):
    weight = 0
    for xy in get_iterator(image):
        if image.getpixel(xy) == 0:
            weight += 1
    return weight
    

def invert(image):
    image = image.copy()
    for xy in get_iterator(image):
        color = 0 if image.getpixel(xy) == 1 else 1
        image.putpixel(xy, color)
    return image


def get_patterns(samples, fn):
    def patterns():
        for sample in samples:
            for s in get_segments(binarize(sample, fn)):
                yield trim(s)
                
    return patterns()
                

def find_image(image, directory):
    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        i = Image.open(path)
        if i.tostring() == image.tostring():
            return f
    return None


def generate_patterns(samples_directory, patterns_directory, fn):
    samples = get_images(samples_directory)
    c = 0
    for p in get_patterns(samples, fn):
        if not find_image(p, patterns_directory):
            path = os.path.join(patterns_directory, '%s.png' % c)
            c += 1
            p.save(path, 'PNG')
            

def sort_segments(segments):
    
    def position_compare(s1, s2):
        return  get_limits(s1)[0] - get_limits(s2)[0]
    
    sorted(segments, cmp=position_compare)


def solve_captcha(image, fn, patterns_directory):
    image = binarize(image, fn)
    segments = get_segments(image)
    sort_segments(segments)

    segments = [trim(s) for s in segments]

    response = ''

    for s in segments:
        name = find_image(s, patterns_directory)
        if name is None:
            return None
        else:
            response += os.path.splitext(name)[0]
    
    return response
