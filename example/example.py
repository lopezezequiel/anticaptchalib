from anticaptchalib import *

#Solving captcha1
captcha = Image.open('01.png')
fn = lambda color: 0 if color == 80 else 1
print solve_captcha(captcha, fn, 'patterns01')

#Solving captcha2
captcha = Image.open('02.png')
fn = lambda color: 0 if color == (255,255,255) else 1
print solve_captcha(captcha, fn, 'patterns02')

#Solving captcha3
captcha = Image.open('03.png')
fn = lambda color: 0 if color not in [(230,200,230), (245,245,245)]  else 1
print solve_captcha(captcha, fn, 'patterns03')

#Generating patterns
generate_patterns('samples03', 'patterns04', fn)
